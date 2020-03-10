# Distributed Systems summative 2019-20
This project is built in python 3.6.3 and uses Pyro4 for client to server and server to server communications.  
This project consists of 5 python scripts client.py, front-end-server.py, replica-server-1.py, replica-server-2.py, replica-server-3.py.  
To successfully run this project and test its functionality follow the following steps in order:  
- **note:** first ensure the following python modules are installed on your machine / on the version of python you are running: sys, json, Pyro4, requests, datetime, pandas, os, threading and _thread.
- You will likely need to install Pyro4 on mira using **pip3 install Pyro4**.
- Open a terminal shell and run the command **python -m Pyro4.naming**, or **python3 -m Pyro4.naming** if using linux / mira.
- Open a terminal shell and navigate to this directory and launch the front end server using the command **python front-end-server.py**, or **python3 front-end-server.py** if using linux / mira.
- Open a terminal shell and navigate to ./replica-server-dir1 and launch the primary server using the command **python replica-server-1.py**, or **python3 replica-server-1.py** if using linux / mira.
- Open a terminal shell and navigate to ./replica-server-dir2 and launch the first back up server using the command **python replica-server-2.py**, or **python3 replica-server-2.py** if using linux / mira.
- Open a terminal shell and navigate to ./replica-server-dir3 and launch the second back up server using the command **python replica-server-3.py**, or **python3 replica-server-3.py** if using linux / mira.
- Finally open the last terminal shell and navigate to this directory and run the client script using the command **python client.py**, or **python3 client.py** if using linux / mira.
- **ALTERNATIVELY:** **(THIS SHOULD WORK ON MIRA)** run the python script **startup.py**, with **python3 startup.py** to start up all programs on xterm terminals.
- **note:** if non of the above approaches work try running each of the scripts from the python IDLE (you still need to run **python -m Pyro4.naming** from a terminal shell).

# The client
When you launch the client script you will be prompted to enter a 'unique user code', this is not an authentication system, so just enter some arbitrary code.  
When you make a food order your user code will be attached to it, and when you view you orders the system will only respond with orders made by the user code that is active in the client.  
This helps to seperate food orders made by different users, if you restart the client enter the same user code to view the orders you have made previously.  
The rest of the client program is very intuitive so follow the instructions and prompts given to you on the screen.  
**note:** when the client starts up it makes a get_motd() request to the system, to check that it is up and running.  

# The servers
The servers print to the console, each time they begin processing a request, each time they finish processing a request and each time they try to connect to another back-end server.  
The console messages are again very intuitive so you can easily understand what is going on behind the scenes.

# System design
To view the system design open the **DataFlowDiagram.pdf** file.  
The client can make the following requests to the front-end-server:
- get_menu() - retreives the menu in json format from the system.
- get_orders(user_code) - retreives all the orders made under the current user.
- get_motd() - retreives the message of the day from the system.
- make_order(user_code, item, price, post_code) - writes an order to the system and expects a success / failure response.
- is_valid_postcode(post_code) - sends a post code to the system for validation.

The front-end-server handles the following requests like so:
- get_menu() - forwards the request to the primary server (replica-server-1).
- get_orders(user_code) - forwards the request to the primary server.
- get_motd() - forwards the request to the primary server.
- make_order(user_code, item, price, date_time, post_code, propagate_bit) - sets the propagate bit to **True**, creates a timestamp and forwards the request to the primary server.
- is_valid_postcode() - makes the following webservice api request: GET api.postcodes.io/postcodes/:post_code.

the replica-servers
- get_menu() - reads the local menu.csv and constructs and returns a json response.
- get_orders(user_code) - reads and queries the local orders.csv and constructs and returns a json response.
- get_motd() - reads the local motd.txt file and constructs and returns a json response.
- make_order(user_code, item, price, date_time, post_code, propagate_bit) - writes the order to orders.csv and propagates the result to the back-up servers (on a different thread) if the propagate_bit is set to **True**.

**note:** all messages are constructed through json (so you must have json installed in python).  

# Passive replication
This system mimics passive replication by having one primary server (replica-server-1) and two back up servers (replica-server-2, replica-server-3).  
The front end server attempts to connect to the primary and if a connection is established it breaks out the loop and forwards the request.  
If the primary server is not available it loops through the rest of the servers and breaks when it finds one that is available.  
As a result we implement passive replication and fulfil the following transparency requirements: 
- Location: the client connects to the front end server at (just.hungry), and doesn't know where the back end servers are located.
- Relocation: if the front end server switches the primary server and starts using different resources, the client doesn't know because this information is hidden from it. (to test this maybe delete some of the primary servers local resources / files)
- Replication: the client has no idea if there are multiple back end servers and duplicated data because it only connects to the front end server, and any information about which back end server processed the clients request is hidden.
- Failure: if a back end server fails to respond or process the clients request this information is hidden from the client and the front end server tries another replica. (to test this try turning off the primary server)

# Webservice
The postcode checker that is used in the project can be found at the link: https://postcodes.io/  
The front-end-server directly makes the api request: https://api.postcodes.io/postcodes/:postcode  
- A valid request / response looks like: https://api.postcodes.io/postcodes/DH1%1JN -> { "status" : 200 "result" : { ... } }
- An invalid request / response looks like: https://api.postcodes.io/postcodes/notapostcode -> { "status" : 404 "error" : "Invalid Postcode" }

**note:** the front-end-server makes the webservice api calls instead of the replicas because the webservice is treated as a seperate component.

# Data integrity
If one of the back-end servers goes down you may get inconsistent results when making get_orders() requests after restarting that server.  
If this is the case make sure that all the orders.csv files are all identical before you restart the system.

**note:** if you get inconsistent results when making get_menu() or get_motd() requests, make sure all the menu.csv files are identical and all the motd.txt files are indentical (this should always be the case).
