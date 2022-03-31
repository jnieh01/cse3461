# first of all import the socket library
import socket			
import pickle

def send_msg(s, msg):
    data = pickle.dumps(msg)
    s.send(data)


# next create a socket object
s = socket.socket()		
print ("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345			

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))		
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
        list.clear()
        msg = "List is clean"
    elif(data[0] == "SEARCH"):
        if(data[1] in list):
            msg = "Item {} exist".format(data[1])
        else:
            msg = "Item {} doesnt exist".format(data[1])
    elif(data[0] == "DELETE"):
        if(data[1] in list):
            list.remove(data[1])
            msg = "Item {} is removed".format(data[1])
        else:
            msg = "Item {} doesnt exist".format(data[1])
    elif(data[0] == "ADD"):
        list.append(data[1])
        msg = "Item {} is added to the list".format(data[1])
    elif(data[0] == "QUIT"):
        msg = "Exit the program"
        send_msg(c, msg)
        c.close     # Close the connection with the client
        break       # Breaking once connection closed

    send_msg(c, msg)    
    
    print ("data: ", data)
    print("list", list)
