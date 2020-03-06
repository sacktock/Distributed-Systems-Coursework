# Distributed Systems summative 2019-20
This project consists of 5 python scripts client.py, front-end-server.py, replica-server-1.py, replica-server-2.py, replica-server-3.py.
To successfully run this projet and test its functionality follow the follwoing steps in order:
- note: first ensure the following python modules are installed on your machine / on the version of python you are running: sys, json, Pyro4, requests, datetime, pandas, os and threading, _thread.
- Open a terminal shell and run the command **python -m Pyro4.naming**, or **python3 -m Pyro.naming** if using linux / mira.
- Open a terminal shell and navigate to this directory and launch the front end server using the command **python front-end-server.py**, or **python3 front-end-server.py** if using linux / mira.
- Open a terminal shell and navigate to ./replica-server-dir1 and launch the primary server using the command **python replica-server-1.py**, or **python3 replica-server-1.py** if using linux / mira.
- Open a terminal shell and navigate to ./replica-server-dir2 and launch the first back up server using the command **python replica-server-2.py**, or **python3 replica-server-2.py** if using linux / mira.
- Open a terminal shell and navigate to ./replica-server-dir3 and launch the second back up server using the command **python replica-server-3.py**, or **python3 replica-server-3.py** if using linux / mira.
- Finally open the last terminal shell and navigate to this directory and run the client script using the command **python client.py**, or **python3 client.py** if using linux / mira.


