# Import module
import socket			
import pickle
import logging

# Configure the logging
logging.basicConfig(filename='lab.log', format='%(asctime)s - %(message)s', level=logging.INFO)


def send_msg(s, msg):
    data = pickle.dumps(msg)
    s.send(data)


# Create a socket object
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
except socket.error as err:
    print("socket creation failed with error %s" %(err))

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345			

logging.info(f'server starting on port {port}')

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
host = socket.gethostname()
s.bind((host, port))		
print ("socket binded to %s" %(port))

# put the socket into listening mode
s.listen(5)	
print ("socket is listening")		

# Establish connection with client.
c, addr = s.accept()	
print ('Got connection from', addr )

list = []

# a forever loop until we interrupt it or
# an error occurs
while True:
    msg = ""

    recvd_data = c.recv(4096)
    data = pickle.loads(recvd_data)

    if(data[0] == "LIST"):
        logging.info(f'REQUEST {data[0]} received')
        list.clear()
        msg = "List is clean"
    elif(data[0] == "SEARCH"):
        logging.info(f'REQUEST {data[0]} {data[1]} received')
        if(data[1] in list):
            msg = "Item {} exist".format(data[1])
        else:
            msg = "Item {} doesnt exist".format(data[1])
    elif(data[0] == "DELETE"):
        logging.info(f'REQUEST {data[0]} {data[1]} received')
        if(data[1] in list):
            list.remove(data[1])
            msg = "Item {} is removed".format(data[1])
        else:
            msg = "Item {} does not exist".format(data[1])
    elif(data[0] == "ADD"):
        logging.info(f'REQUEST {data[0]} {data[1]} received')   
        list.append(data[1])
        msg = "Item {} is added to the list".format(data[1])
    elif(data[0] == "QUIT"):
        logging.info(f'REQUEST {data[0]} received')  
        msg = "Program terminated"
        send_msg(c, msg)
        logging.info(f'RESPONSE {msg} sent')
        c.close     # Close the connection with the client

        break       # Breaking once connection closed

    send_msg(c, msg)    
    logging.info(f'RESPONSE {msg} sent')

    print("list: ", list)
    
print("Connection end")