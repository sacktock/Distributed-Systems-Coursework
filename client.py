import socket
import sys
import json

def server_request(server_name, port, raw_json):
    # create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)

    #cConnect the socket to the port where the server is listening
    server_address = (server_name, port)
    print('connecting to {} port {}'.format(*server_address))
    try:
        sock.connect(server_address)
    except socket.timeout:
        # server timeout
        sock.close()
        print('server timeout ... ')
        print('exiting ... ')
        sys.exit()
        return b''
    except ConnectionRefusedError:
        # server is unavailable
        sock.close()
        print('server is unavailable ... ')
        print('exiting ... ')
        sys.exit()
        return b''
    
    response = b''
    
    try:
        # send message
        message = str.encode(raw_json)
        print('sending {!r}'.format(message))
        sock.sendall(message)

        # look for the response
        while True:
            data = sock.recv(1024)
            print('received {!r}'.format(data))
            # construct the server response
            if data:
                response += data
            else:
                print('no more data from', server_address)
                break
            
    finally:
        # close the connection
        print('closing socket')
        sock.close()
        # return the server response
        return response
    
def home_page_display(user_code):
    print('------------------------')
    print('========================')
    print('------------------------')
    print()
    print('WELCOME TO "JUST HUNGRY"')
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
        sys.exit()

def menu_page_display(user_code):
    print('--------')
    print()
    print('OUR MENU')
    print()
    print('--------')
    print('--------')
    print() # make read request to the distributed system and await response - only as an extension for now
    print('A. CHICKEN WINGS - PRICE 10.95')
    print('B. FISH FINGERS - PRICE 11.85')
    print()
    print('--------')
    print('--------')
    print()
    print('PRESS {ITEM LETTER} + {ENTER} TO START AN ORDER')
    print('1. PRESS 1 + {ENTER} TO RETURN TO THE HOME PAGE')
    print('2. PRESS 2 + {ENTER} TO EXIT')

    resp = input()
    while resp not in ['1','2', 'A', 'B']:
        resp = input('Invalid Choice ... try again ... \n')

    if resp == 'A':
        make_order_page_display(user_code,'CHICKEN WINGS', '10.95')
    elif resp == 'B':
        make_order_page_display(user_code,'FISH FINGERS', '11.85')
    elif resp == '1':
        home_page_display(user_code)
    else:
        sys.exit()

def order_page_display(user_code):
    print('-----------')
    print()
    print('YOUR ORDERS')
    print()
    print('-----------')
    print()
    print('-----------')
    print('-----------')
    print() # make read request to the distributed system and await response
    print('ORDER AT 11:59 AM 14/02/2020 - CHICKEN WINGS - ORDER STATUS: DELIVERED')
    print()
    print('-----------')
    print('-----------')
    print()
    print('user: '+ user_code)
    print()
    print('1. PRESS 1 + {ENTER} TO RETURN TO THE HOME PAGE')
    print('2. PRESS 2 + {ENTER} TO EXIT')

    resp = input()
    while resp not in ['1','2']:
        resp = input('Invalid Choice ... try again ... \n')
        
    if resp == '1':
        home_page_display(user_code)
    else:
        sys.exit()

def make_order_page_display(user_code,item, price):
    print('---------------------')
    print()
    print('ORDERING - '+item)
    print()
    print('---------------------')
    print()
    print('PRICE - '+price)
    print()
    print('All we need is your postcode ... ')
    print()
    post_code = input('please enter your postcode below ... \n')
    while not post_code: # make postcode api request to the distributed system and await response
        post_code = input('please enter a valid postcode ... try again ... \n')

    print()
    print('please confirm your order ...')
    print()
    print('ORDERING - '+item+ '; TO '+post_code+ '; TOTAL PRICE - '+price)
    print('PLEASE CONFIRM (Y/n)')
    resp = input()
    while resp not in ['Y', 'n']:
        resp = input('Invalid choice ... try again (Y/n) ...\n')

    if resp == 'Y':
        # make write request to the distributed system and await response
        print('ORDER CONFIRMED')
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
        home_page_display(user_code)
    elif resp == '2':
        order_page_display(user_code)
    else:
        sys.exit()

# enter some arbitrary user code     
print()
print('---------')
print('login ...')
print('---------')
print()
user_code = input('please enter your unique "user code"\n')
while not user_code:
    user_code = input('your "user code" must be non empty ... try again ...\n')
print()

home_page_display(user_code)

# remote function calls: make_order(user_code, item, price, delivery_address),
# get_orders(user_code), get_delivery_address(post_code)
# optional // get_menu()
