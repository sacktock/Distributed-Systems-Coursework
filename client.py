import socket
import sys
import json
import Pyro4

def make_get_menu_request():
    print()
    print('fetching menu ... ')
    try:
        request_handler = Pyro4.Proxy("PYRONAME:just.hungry")    
        return request_handler.get_menu() 
    except:
        return ''

def make_get_orders_request(user_code):
    print()
    print('fetching orders ... ')
    try:
        request_handler = Pyro4.Proxy("PYRONAME:just.hungry")    
        return request_handler.get_orders(user_code) 
    except:
        return ''

def make_order_request(user_code ,item, price, post_code):
    print()
    print('processing order ... ')
    try:
        request_handler = Pyro4.Proxy("PYRONAME:just.hungry")    
        return request_handler.make_order(user_code ,item, price, post_code) 
    except:
        return ''

def make_get_motd_request():
    print()
    print('accessing server ... ')
    try:
        request_handler = Pyro4.Proxy("PYRONAME:just.hungry")    
        return request_handler.get_motd() 
    except:
        return ''

def make_is_valid_postcode_request(post_code):
    print()
    print('processing post code ... ')
    try:
        request_handler = Pyro4.Proxy("PYRONAME:just.hungry")    
        return request_handler.is_valid_postcode(post_code) 
    except:
        return ''
    
def home_page_display(user_code):
    print('------------------------')
    print('========================')
    print('------------------------')
    print()
    print('"JUST HUNGRY"')
    print('motd: '+motd)
    print()
    print('------------------------')
    print('========================')
    print('------------------------')
    print()
    print('user: '+ user_code)
    print()
    print('1. PRESS 1 + {ENTER} TO VIEW THE MENU')
    print('2. PRESS 2 + {ENTER} TO VIEW YOUR ORDERS')
    print('3. PRESS 3 + {ENTER} TO EXIT')

    resp = input()

    while resp not in ['1','2','3']:
        resp = input('Invalid Choice ... try again ... \n')

    if resp == '1':
        menu_page_display(user_code)
    elif resp == '2':
        order_page_display(user_code)
    else:
        quit()

def menu_page_display(user_code):
    while True:
        response = make_get_menu_request()
        if response:
        # parse json response
            try:
                if response['valid'] == 1:
                    lst = ['A', 'B', 'C', 'E', 'D', 'F', 'G']
                    menu_items = response['menu']
                    print('--------')
                    print()
                    print('OUR MENU')
                    print()
                    print('--------')
                    print('--------')
                    print()
                    for i in range(0, len(menu_items)):
                        print(lst[i]+'. ' + menu_items[i]['item'], ' Price: '+str(menu_items[i]['price']))
                    print()
                    print('--------')
                    print('--------')
                    print()
                    print('PRESS {ITEM LETTER} + {ENTER} TO START AN ORDER')
                    print('1. PRESS 1 + {ENTER} TO RETURN TO THE HOME PAGE')
                    print('2. PRESS 2 + {ENTER} TO EXIT')

                    resp = input()
                    while resp not in (['1','2'] + lst):
                        resp = input('Invalid Choice ... try again ... \n')

                    if resp in lst:
                        index = lst.index(resp)
                        make_order_page_display(user_code,menu_items[index]['item'], menu_items[index]['price'])
                        return
                    elif resp == '1':
                        return
                    else:
                        quit()
                elif response['valid'] == 0:
                    # server side error
                    print(response['error']+' ... ')
                    retry =input('Try again : [Y/n] \n')
                    if retry == 'Y':
                        continue
                    else:
                        print('returning to the home page ...')
                        return
            except:
                # server responded with unexpected json
                print('server responded badly with no valid bit ... ')
                retry =input('Try again : [Y/n] \n')
                if retry == 'Y':
                    continue
                else:
                    print('returning to the home page ...')
                    return
        else:
            # server didn't respond with anything
            print('nothing received from the server ... ')
            retry =input('Try again : [Y/n] \n')
            if retry == 'Y':
                continue
            else:
                print('returning to the home page ...')
                return
    
def order_page_display(user_code):
    while True:
        response = make_get_orders_request(user_code)
        if response:
        # parse json response
            try:
                if response['valid'] == 1:
                    orders = response['orders']
                    print('-----------')
                    print()
                    print('YOUR ORDERS')
                    print()
                    print('-----------')
                    print()
                    print('-----------')
                    print('-----------')
                    print() 
                    if orders == []:
                        print('NO RECENT ORDERS')
                    for order in orders:
                        print('ORDER AT '+order['time_stamp']+' TO '+order['post_code']+' - '+order['item']+', Price: '+str(order['price']))
                    print()
                    print('-----------')
                    print('-----------')
                    print()
                    print('user: '+ user_code)
                    print()
                    print('1. PRESS 1 + {ENTER} TO RETURN TO THE HOME PAGE')
                    print('2. PRESS 2 + {ENTER} TO REFRESH THIS PAGE')
                    print('3. PRESS 3 + {ENTER} TO EXIT')

                    resp = input()
                    while resp not in ['1','2','3']:
                        resp = input('Invalid Choice ... try again ... \n')
        
                    if resp == '1':
                        return
                    elif resp == '2':
                        continue
                    else:
                        quit()
                elif response['valid'] == 0:
                    # server side error
                    print(response['error']+' ... ')
                    retry =input('Try again : [Y/n] \n')
                    if retry == 'Y':
                        continue
                    else:
                        print('returning to the home page ...')
                        return
            except:
                # server responded with unexpected json
                print('server responded badly with no valid bit ... ')
                retry =input('Try again : [Y/n] \n')
                if retry == 'Y':
                    continue
                else:
                    print('returning to the home page ...')
                    return
        else:
            # server didn't respond with anything
            print('nothing received from the server ... ')
            retry =input('Try again : [Y/n] \n')
            if retry == 'Y':
                continue
            else:
                print('returning to the home page ...')
                return

def make_order_page_display(user_code,item, price):
    print('---------------------')
    print()
    print('ORDERING - '+item)
    print()
    print('---------------------')
    print()
    print('PRICE - '+str(price))
    print()
    print('All we need is your postcode ... ')
    print()
    post_code = input('please enter your postcode below ... \n')
    address = ''
    while True:
        response = make_is_valid_postcode_request(post_code)
        if response:
            try:    
                if response['valid'] == 1:
                    print('address found at this post code ... ')
                    print(response['address']+' '+ post_code)
                    confirm = input('Is this your address? [Y/n]\n')
                    while confirm not in ['Y','n']:
                        confirm = input('Invalid Choice ... try again ... \n')
                    if confirm == 'Y':
                        address = response['address']
                        break
                    else:
                        retry =input('Try again : [Y/n] \n')
                        if retry == 'Y':
                            continue
                        else:
                            print('ORDER SUCCESSFULLY CANCELLED')
                            print('returning to the home page ...')
                            return
                        
                elif response['valid'] == 0:
                    # server side error
                    print(response['error']+' ... ')
                    retry =input('Try again : [Y/n] \n')
                    if retry == 'Y':
                        if response['error'] == 'Not a valid post code':
                            post_code = input('please enter a valid post code ... \n')
                        continue
                    else:
                        print('ORDER SUCCESSFULLY CANCELLED')
                        print('returning to the home page ...')
                        return
            except:
                # server responded with unexpected json
                print('server responded badly ... ')
                retry =input('Try again : [Y/n] \n')
                if retry == 'Y':
                    continue
                else:
                    print('ORDER SUCCESSFULLY CANCELLED')
                    print('returning to the home page ...')
                    return
        else:
            # server didn't respond with anything
            print('nothing received from the server ... ')
            retry =input('Try again : [Y/n] \n')
            if retry == 'Y':
                continue
            else:
                print('ORDER SUCCESSFULLY CANCELLED')
                print('returning to the home page ...')
                return

    print()
    print('please confirm your order ...')
    print()
    print('ORDERING - '+item+ '; TO '+address +' '+post_code+ '; TOTAL PRICE - '+str(price))
    print('PLEASE CONFIRM (Y/n)')
    resp = input()
    while resp not in ['Y', 'n']:
        resp = input('Invalid choice ... try again (Y/n) ...\n')

    if resp == 'Y':
        while True:
        # make server request
            response = make_order_request(user_code ,item, price, post_code)
            if response:
                try:
                    if response['valid'] == 1:
                        print('ORDER CONFIRMED')
                        break
                        
                    elif response['valid'] == 0:
                        # server side error
                        print(response['error']+' ... ')
                        retry =input('Try again : [Y/n] \n')
                        if retry == 'Y':
                            continue
                        else:
                            print('ORDER SUCCESSFULLY CANCELLED')
                            print('returning to the home page ...')
                            return
                except:
                    # server responded with unexpected json
                    print('server responded badly ... ')
                    retry =input('Try again : [Y/n] \n')
                    if retry == 'Y':
                        continue
                    else:
                        print('ORDER SUCCESSFULLY CANCELLED')
                        print('returning to the home page ...')
                        return
            else:
                # server didn't respond with anything
                print('nothing received from the server ... ')
                retry =input('Try again : [Y/n] \n')
                if retry == 'Y':
                    continue
                else:
                    print('ORDER SUCCESSFULLY CANCELLED')
                    print('returning to the home page ...')
                    return
    else:
        print('ORDER SUCCESSFULLY CANCELLED')

    print()
    print('1. PRESS 1 + {ENTER} TO RETURN TO THE HOME PAGE')
    print('2. PRESS 2 + {ENTER} TO VIEW YOUR ORDERS')
    print('3. PRESS 3 + {ENTER} TO EXIT')

    resp = input()
    while resp not in ['1','2','3']:
        resp = input('Invalid choice ... try again ...\n')
        
    if resp == '1':
        return
    elif resp == '2':
        order_page_display(user_code)
        return
    else:
        quit()
    
# enter some arbitrary user code     
print()
print('---------')
print('login ...')
print('---------')
print()
user_code = input('please enter your unique "user code"\n')
while not user_code:
    user_code = input('your "user code" must be non empty ... try again ...\n')

# check the front-end-server is running by making a get motd request
while True:
    # make server request
    response = make_get_motd_request()
    if response:
        try:
            if response['valid'] == 1:
                motd = response['motd']
                while True:
                    home_page_display(user_code)
                break
            elif response['valid'] == 0:
                # server side error
                print(response['error']+' ... ')
                retry =input('Try again : [Y/n] \n')
                if retry == 'Y':
                    continue
                else:
                    print('exiting ...')
                    quit()
        except:
            # server responded with unexpected json
            print('server responded badly ... ')
            retry =input('Try again : [Y/n] \n')
            if retry == 'Y':
                continue
            else:
                print('exiting ...')
                quit()
    else:
        # server didn't respond with anything
        print('nothing received from the server ... ')
        retry =input('Try again : [Y/n] \n')
        if retry == 'Y':
            continue
        else:
            print('exiting ...')
            quit()
