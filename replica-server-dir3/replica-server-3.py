import socket
import sys
import Pyro4
import json
import pandas as pd
import csv
import os
from _thread import *
import threading

server_namespaces = ['replica.server1', 'replica.server2']

# python -m Pyro4.naming

@Pyro4.expose
class RequestHandler(object):

    def get_menu(self):
        print('processing a get_menu request ... ')
        
        response = '{ "request" : "get_menu", "valid" : 1, "menu" : [ '
        try:
            menu = pd.read_csv(os.path.join('menu.csv'))
        except:
            print('sending error back ...')
            return json.loads('{ "request" : "get_menu", "valid" : 0, "error" : "missing menu.csv file"')
        for index, row in menu.iterrows():
            response += ('{ "item" : "'+row['item']+'", "price" : '+str(row['price'])+'}, ')

        response = response[:-2]+' ] }'
        print('sending response back ...')
        return json.loads(response)

    def make_order(self, user_code, item, price, date_time, post_code, propagate_bit):
        print('processing a make_order request ... ')
        try:
            f = open(os.path.join('orders.csv'), 'a')
            f.write(user_code+','+item+','+str(price)+','+date_time+','+post_code+',CONFIRMED\n')
            f.close()
        except:
            print('sending error back ...')
            return json.loads('{ "request" : "make_order", "valid" : 0, "error" : "failed to write to the orders.csv file"}')
        print('sending response back ...')
        if propagate_bit:
            start_new_thread(self.update_orders, (user_code, item, price, date_time, post_code))
        return json.loads('{ "request" : "make_order", "valid" : 1}')

    def get_orders(self, user_code):
        print('processing a get_orders request ... ')

        response = '{ "request" : "get_orders", "valid" : 1, "orders" : [ '
        try:
            orders = pd.read_csv(os.path.join('orders.csv'))
        except:
            print('sending error back ...')
            return json.loads('{ "request" : "get_orders", "valid" : 0, "error" : "missing orders.csv file"')
        flag = False
        for index, row in orders.iterrows():
            if row['user_code'] == user_code:
                flag = True
                response += ('{"item" : "'+row['item'] + '", "price" : '+str(row['price'])+ ', "time_stamp" : "'
                             +row['time_stamp']+'", "post_code" : "'+row['post_code']+'", "status" : "'+row['status']+'" }, ')

        if flag:
            response = response[:-2]+' ] }'
        else:
            response += '] }'
        print('sending response back ...') 
        return json.loads(response)

    def get_motd(self):
        print('processing a get_motd request ... ')
        try:
            f = open(os.path.join('motd.txt'), 'r')
            motd = f.read()
            f.close()
        except:
            print('sending error back ...')
            return json.loads('{ "request" : "get_motd", "valid" : 0, "error" : "could not open motd.txt file" }')
        print('sending response back ...') 
        return json.loads('{ "request" : "get_motd", "valid" : 1, "motd" : "'+motd+'" }')

    def update_orders(self, user_code, item, price, date_time, post_code):
        print('updating orders ... ')
        for namespace in server_namespaces:
            print('trying', namespace)
            for _ in range(3):
                try:
                    request_handler = Pyro4.Proxy("PYRONAME:"+namespace)    
                    response = request_handler.make_order(user_code, item, price, date_time, post_code, False)
                    if response['valid'] == 1:
                        print('make_order request successfully propogated to '+namespace+' ... ')
                        break
                    else:
                        print('failed to propogate make_order request to '+namespace+' ... ')
                        continue
                except:
                    print('failed to propogate make_order request to '+namespace+' ... ')
                    continue
        print('update_orders method completed ... ')

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(RequestHandler)   # register the greeting maker as a Pyro object
ns.register("replica.server3", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()
