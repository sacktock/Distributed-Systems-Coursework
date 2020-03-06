import socket
import sys
import Pyro4
import json
import requests
from datetime import datetime

# back end server namespaces
# the first namespace in the list 'replica.server1' is the primary server
server_namespaces = ['replica.server1', 'replica.server2', 'replica.server3']

# make sure the following command line is running in a seperate terminal shell
# python -m Pyro4.naming

####################################################
# Request handler class
####################################################

@Pyro4.expose
class RequestHandler(object):

    def get_menu(self):
        print('processing a get_menu request ... ')
        response = '' # construct the json repsonse
        for namespace in server_namespaces: # for each back end server
            print('trying', namespace)
            try:
                request_handler = Pyro4.Proxy("PYRONAME:"+namespace)    
                response = request_handler.get_menu()
                if response['valid'] == 1: # if the request is successful break
                    break
                else:
                    continue # try the next server
            except: # no response from the back end server
                response = ''
                continue

        if response:
            print('sending response back ... ')
            return response # forward the response from the back end server to the client
        else:
            print('sending error back ... ') # send error back if none of the back end servers responded
            return json.loads('{ "request" : "get_menu", "valid" : 0, "error" : "server side error occured" }')

    def make_order(self, user_code, item, price, post_code):
        print('processing a make_order request ... ')
        response = '' # construct the json repsonse
        for namespace in server_namespaces: # for each back end server
            print('trying', namespace)
            try:
                request_handler = Pyro4.Proxy("PYRONAME:"+namespace)    
                response = request_handler.make_order(user_code, item, price, str(datetime.now()), post_code, True)
                if response['valid'] == 1: # if the request is successful break
                    break
                else:
                    continue # try the next server
            except: # no response from the back end server
                response = ''
                continue

        if response:
            print('sending response back ... ')
            return response # forward the response from the back end server to the client
        else:
            print('sending error back ... ') # send error back if none of the back end servers responded
            return json.loads('{ "request" : "make_order", "valid" : 0, "error" : "server side error occured" }')

    def get_orders(self, user_code):
        print('processing a get_orders request ... ')
        response = '' # construct the json response
        for namespace in server_namespaces: # for each back end server
            print('trying', namespace)
            try:
                request_handler = Pyro4.Proxy("PYRONAME:"+namespace)    
                response = request_handler.get_orders(user_code)
                if response['valid'] == 1: # if the request is successful break
                    break
                else:
                    continue # try the next server
            except: # no response from the back end server
                response = ''
                continue

        if response:
            print('sending response back ... ')
            return response # forward the response from the back end server to the client
        else:
            print('sending error back ... ') # send error back if none of the back end servers responded
            return json.loads('{ "request" : "get_orders", "valid" : 0, "error" : "server side error occured" }')

    def get_motd(self):
        print('processing a get_motd request ... ')
        response = '' # construct the json response
        for namespace in server_namespaces: # for each back end server
            print('trying', namespace)
            try:
                request_handler = Pyro4.Proxy("PYRONAME:"+namespace)    
                response = request_handler.get_motd()
                if response['valid'] == 1: # if the request is successful break
                    break
                else:
                    continue # try the next server
            except: # no response from the back end server
                response = ''
                continue

        if response:
            print('sending response back ... ')
            return response # forward the response from the back end server to the client
        else:
            print('sending error back ... ') # send error back if none of the back end servers responded
            return json.loads('{ "request" : "get_motd", "valid" : 0, "error" : "server side error occured" }')

    def is_valid_postcode(self, post_code):
        print('processing a is_valid_postcode request ... ')
        try:
            print('making web service request ... ')
            response = requests.get('https://api.postcodes.io/postcodes/'+post_code).json() # make request to the web service api
            if response['status'] == 200: # if request is successful
                print('sending response back ... ')
                return json.loads('{ "request" : "is_valid_postcode", "valid" : 1 }') # return json response to the client
            else:
                print('sending error back ... ') # if request is unsuccessful return error response to the client
                return json.loads('{ "request" : "is_valid_postcode", "valid" : 0, "error" : "'+response['error']+'" }')
        except:
            print('sending error back ... ') # if the api did not respond
            return json.loads('{ "request" : "is_valid_postcode", "valid" : 0, "error" : "could not access webservice" }')

####################################################
# Main code
####################################################

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(RequestHandler)   # register the greeting maker as a Pyro object
ns.register("just.hungry", uri)   # register the object with a name in the name server

print("front-end-server ready ...")
daemon.requestLoop()     
