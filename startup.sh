pip3 install Pyro4
xterm -e python3 -m Pyro4.naming &
xterm -e python3 ./front-end-server.py &
xterm -e python3 ./replica-server-1.py &
xterm -e python3 ./replica-server-2.py &
xterm -e python3 ./replica-server-3.py &
xterm -e python3 ./client.py &