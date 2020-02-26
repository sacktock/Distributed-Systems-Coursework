import socket
import sys
import Pyro4

@Pyro4.expose
class RequestHandler(object):

    def get_menu(self):
        return '{ "request" : "get_menu", "valid" : 1, "menu" : [ {"item" : "CHICKEN WINGS", "price" : 11.85}, {"item" : "FISH FINGERS", "price" : 10.95} ] }'

    def make_order(self, user_code, item, price, post_code):
        return '{ "request" : "make_order", "valid" : 1}'

    def get_orders(self, user_code):
        return '{ "request" : "get_orders", "valid" : 1, "orders" : [ {"item" : "CHICKEN WINGS", "price" : 11.85, "time_stamp" : "11:59 AM 14/02/2020" } ] }'

    def get_motd(self):
        return '{ "request" : "get_motd", "valid" : 1, "motd" : "Weclome to Just Hungry UK!" }'

    def is_valid_postcode(self, post_code):
        return '{ "request" : "is_valid_postcode", "valid" : 1, "post_code" : "DH1 1JN", "address" : "1 Renny Street" }'
        

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(RequestHandler)   # register the greeting maker as a Pyro object
ns.register("just.hungry", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()     
