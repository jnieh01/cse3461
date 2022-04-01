# Import module
import socket
import pickle
import logging

def send_data(s, userinput):
    data = pickle.dumps(userinput)
    s.send(data)

def recvd_msg(s):
    recvd_msg = s.recv(4096)
    return pickle.loads(recvd_msg)

# Create a socket object
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
except socket.error as err:
    print("socket creation failed with error %s" %(err))

# Define the port on which you want to connect
port = 12345

# connect to the server on local computer
s.connect(('127.0.0.1', port))

# Command count
i = 0

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


while True:
    print("\nAvailiable command:")
    print("\tLIST: Clean the list")
    print("\tSEARCH: Search for a item in the list")
    print("\tDELETE: Delete an item from the list")
    print("\tADD: Add an item to the list")
    print("\tQUIT: Exit the program")

    userinput = []
    userinput = input('\ncommand[{}]> '.format(i)).split()

    if(len(userinput) == 0):
        print("Enter QUIT to exit or Enter command")
    elif(len(userinput) == 1):
        if(userinput[0] == "LIST"):
            send_data(s, userinput)
            print("Creating list...")
            print(recvd_msg(s))
        elif(userinput[0] == "SEARCH"):
            print("Missing element: SEARCH")
            print("usage: SEARCH <item>")
        elif(userinput[0] == "DELETE"):
            print("Missing element: DELETE")
            print("usage: DELETE <item>")
        elif(userinput[0] == "ADD"):
            print("Missing element: ADD")
            print("usage: ADD <item>")
        elif(userinput[0] == "QUIT"):
            send_data(s, userinput)
            print("Exiting...")
            print(recvd_msg(s))
            break
        else:
            print("Invalid command: ", userinput[0])
            print("Valid commands are: \nLIST \nSEARCH \nDELETE \nADD \nQUIT")
    elif(len(userinput) == 2):
        if(userinput[0] == "LIST"):
            print("Too many inputs: LIST")
            print("usage: LIST")
        elif(userinput[0] == "SEARCH"):
            send_data(s, userinput)
            print(f'Searching item {userinput[1]}... ')
            print(recvd_msg(s))
        elif(userinput[0] == "DELETE"):
            send_data(s, userinput)
            print(f'Deleting item {userinput[1]}...')
            print(recvd_msg(s))
        elif(userinput[0] == "ADD"):
            send_data(s, userinput)
            print(f'Adding item {userinput[1]}...')
            print(recvd_msg(s))
        elif(userinput[0] == "QUIT"):
            print("Too many inputs: QUIT")
            print("usage: QUIT")
        else:
            print("Invalid command: ", userinput[0])
            print("Valid commands are: \n\tLIST \n\tSEARCH \n\tDELETE \n\tADD \n\tQUIT")
    else:
        print("Too many inputs: ")
        print("Valid commands with correct inputs are: \nLIST \nSEARCH <item>\nDELETE <item>\nADD <item>\nQUIT")
    
    i += 1

# close the connection
s.close()
