# Import socket module
import socket
import pickle

def send_data(s, userinput):
    data = pickle.dumps(userinput)
    s.send(data)

def recvd_msg(s):
    recvd_msg = s.recv(4096)
    return pickle.loads(recvd_msg)

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 12345

# connect to the server on local computer
s.connect(('127.0.0.1', port))

while True:
    print("\nAvailiable options:")
    print("     LIST: create new list.")
    print("     SEARCH: search for a item in the list.")
    print("     DELETE: delete an item from the list.")
    print("     ADD: add an item to the list")
    print("     QUIT: exit the program.")

    userinput = []
    userinput = input("\n>").split()
    print("\n")

    if(len(userinput) == 0):
        print("Enter QUIT to exit or Enter command")
    elif(len(userinput) == 1):
        if(userinput[0] == "LIST"):
            print("Missing list name: LIST")
            print("usage: l <name>")
        elif(userinput[0] == "SEARCH"):
            print("Missing element: SEARCH")
            print("usage: s <item>")
        elif(userinput[0] == "DELETE"):
            print("Missing element: DELETE")
            print("usage: d <item>")
        elif(userinput[0] == "ADD"):
            print("Missing element: ADD")
            print("usage: a <item>")
        elif(userinput[0] == "QUIT"):
            send_data(s, userinput)
            print(recvd_msg(s))
            break
        else:
            print("Invalid command: ", userinput[0])
            print("Valid commands are: \nLIST \nSEARCH \nDELETE \nADD \nQUIT")
    elif(len(userinput) == 2):
        if(userinput[0] == "LIST"):
            send_data(s, userinput)
            print("New list: ", userinput[1])
            print(recvd_msg(s))
        elif(userinput[0] == "SEARCH"):
            send_data(s, userinput)
            print("Searching item: ", userinput[1])
            print(recvd_msg(s))
        elif(userinput[0] == "DELETE"):
            send_data(s, userinput)
            print("deleting item: ", userinput[1])
            print(recvd_msg(s))
        elif(userinput[0] == "ADD"):
            send_data(s, userinput)
            print("Adding item: ", userinput[1])
            print(recvd_msg(s))
        elif(userinput[0] == "QUIT"):
            print("adding item: ", userinput[1])
            print(recvd_msg(s))
        else:
            print("Invalid command: ", userinput[0])
            print("Valid commands are: \nLIST \nSEARCH \nDELETE \nADD \nQUIT")
    else:
        print("Too many inputs: ")
        print("Valid commands with correct inputs are: \nLIST <name>\nSEARCH <item>\nDELETE <item>\nADD <item>\nQUIT")

# close the connection
s.close()
