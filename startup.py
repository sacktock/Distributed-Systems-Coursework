import os

os.system('bash -c python3 -m Pyro4.naming')
os.system('bash -c python3 front-end-server.py')
os.system('bash -c python3 replica-server-dir1/replica-server-1.py')
os.system('bash -c python3 replica-server-dir2/replica-server-2.py')
os.system('bash -c python3 replica-server-dir3/replica-server-3.py')
os.system('bash -c python3 client.py')
