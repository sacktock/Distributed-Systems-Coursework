import sys
import Pyro4
import json
import pandas as pd
import os
from _thread import *
import threading

# back up server namespaces
server_namespaces = ['replica.server2', 'replica.server3']

# make sure the following command line is running in a seperate terminal shell
# python -m Pyro4.naming

####################################################
# Request handler class
####################################################

@Pyro4.expose
class RequestHandler(object):

    def get_menu(self):
        print('processing a get_menu request ... ')
        response = '{ "request" : "get_menu", "valid" : 1, "menu" : [ ' # create json response
        try:
            menu = pd.read_csv(os.path.join('menu.csv')) # read the menu.csv file into a dataframe object
        except:
            print('sending error back ...') # send error back if file can't be read
            return json.loads('{ "request" : "get_menu", "valid" : 0, "error" : "missing menu.csv file"')
        for index, row in menu.iterrows(): # iterate through the dataframe rows
            response += ('{ "item" : "'+row['item']+'", "price" : '+str(row['price'])+'}, ') # construct the json response

        response = response[:-2]+' ] }'
        print('sending response back ...')
        return json.loads(response) # return the json response

    def make_order(self, user_code, item, price, date_time, post_code, propagate_bit):
        print('processing a make_order request ... ')
        try:
            f = open(os.path.join('orders.csv'), 'a') # open the orders.csv file
            f.write(user_code+','+item+','+str(price)+','+date_time+','+post_code+',CONFIRMED\n') # append the order to the file
            f.close()
        except:
            print('sending error back ...') # send error back if the file can't be appended to
            return json.loads('{ "request" : "make_order", "valid" : 0, "error" : "failed to write to the orders.csv file"}')
        print('sending response back ...')
        if propagate_bit: # if propagate bit propagate the make order request to the back up servers
            start_new_thread(self.update_orders, (user_code, item, price, date_time, post_code)) # update orders in a new thread
        return json.loads('{ "request" : "make_order", "valid" : 1}') # return the json response

    def get_orders(self, user_code):
        print('processing a get_orders request ... ')
        response = '{ "request" : "get_orders", "valid" : 1, "orders" : [ ' # create json response
        try:
            orders = pd.read_csv(os.path.join('orders.csv')) # read the orders.csv file into a dataframe object
        except:
            print('sending error back ...') # send error back if file can't be read
            return json.loads('{ "request" : "get_orders", "valid" : 0, "error" : "missing orders.csv file"')
        flag = False # set flag to false, indicating if some orders exist for this user
        for index, row in orders.iterrows(): # iterate through the dataframe rows
            if row['user_code'] == user_code:
                flag = True # set flag to true
                response += ('{"item" : "'+row['item'] + '", "price" : '+str(row['price'])+ ', "time_stamp" : "' # construct the json response
                             +row['time_stamp']+'", "post_code" : "'+row['post_code']+'", "status" : "'+row['status']+'" }, ')
        if flag: # if flag remove ', ' from the end of the json response
            response = response[:-2]+' ] }'
        else:
            response += '] }'
        print('sending response back ...') 
        return json.loads(response) # return the json response

    def get_motd(self):
        print('processing a get_motd request ... ')
        try:
            f = open(os.path.join('motd.txt'), 'r') # open the motd.txt file
            motd = f.read()
            f.close()
        except:
            print('sending error back ...') # send error back if the file can't be read
            return json.loads('{ "request" : "get_motd", "valid" : 0, "error" : "could not open motd.txt file" }')
        print('sending response back ...') 
        return json.loads('{ "request" : "get_motd", "valid" : 1, "motd" : "'+motd+'" }') # return the json response

    def update_orders(self, user_code, item, price, date_time, post_code):
        print('updating orders ... ')
        for namespace in server_namespaces: # for each of the back up servers
            print('trying', namespace)
            for _ in range(3): # try to reach the back up server 3 times
                try:
                    request_handler = Pyro4.Proxy("PYRONAME:"+namespace)    
                    response = request_handler.make_order(user_code, item, price, date_time, post_code, False)
                    if response['valid'] == 1: # if the request to the back up server is successful
                        print('make_order request successfully propogated to '+namespace+' ... ')
                        break
                    else:
                        print('failed to propogate make_order request to '+namespace+' ... ')
                        continue
                except:
                    print('failed to propogate make_order request to '+namespace+' ... ')
                    continue
        print('update_orders method completed ... ')

####################################################
# Main code
####################################################

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(RequestHandler)   # register the request handler as a Pyro object
ns.register("replica.server1", uri)   # register the object with a name in the name server

print("replica-server-1 ready ... ")
daemon.requestLoop()
