import select, socket, sys, queue, os
import socket
from os import listdir
from os.path import isfile, join

def sendthis(s, msg, recipient):
    # MESSAGE LOGGING: uncomment for debugging
    # print "\n------sending------"
    # print msg
    # print "-------------------\n"

    s.sendto(msg, (recipient, 1998))

def recvresp(s):

    # Only wait 10 seconds for a response
    s.settimeout(10.0)
    try:
        response,addr = s.recvfrom(1024)
    except socket.timeout:
        print ("socket timed out :(")
        response = false
    
    # Log messages to console
    lst = response.split("\n")
    if lst.pop(0)=="message":
        print ("-------MESSAGE FROM SERVER-------")
        print ("\n".join(lst))
        print ("---------------------------------")

    # MESSAGE LOGGING: uncomment to log all recieved messages
    # print "\n-----recieved------"
    # print response 
    # print "-------------------\n"

    return response

def collectFiles():
    # Look through MyDrawer Folder for files, add them to an array
    files = [f for f in listdir("MyDrawer/") if isfile(join("MyDrawer/", f))]

    # Build a string out of the array
    fileString = ""
    for f in files:
        fileString += "\n" + f

    return fileString

def sendFile(s, filename, recipient):
    # send 1024 bytes at a time
    buf = 1024

    # open the file for binary read
    f = open("MyDrawer/"+filename, "rb")

    # read buffer size and send until entire file sent.
    fileData = f.read(buf)
    while fileData:
        s.sendto(fileData, (recipient[0],1998))
        fileData = f.read(buf)
    f.close

def recvFile(s, filename):
    # Recieve 1024 bytes at a time
    buf = 1024

    # Open the file for binary write
    f = open("MyDrawer/"+filename, "wb")

    # Wait 5 seconds for first response.
    s.settimeout(5.0)
    recv = False
    data = ""
    try:
        # Recieve 1024 bytes at a time and write to file until complete
        while True:
            data,addr = s.recvfrom(buf)
            f.write(data)
            recv = True
    except socket.timeout:
        print ("socket timed out.")
    
    # Print message if file was received
    if data:
        print ("File recieved! your file is now located in your drawer.")
        print ("To share it with others, run the 'u' command and update files. ")

    f.close
    return recv

# Set up the socket
HOST= ''
PORT = 8888           # The same port as used by the server and other clients
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP uses Datagram, but not stream
s.bind((HOST, PORT))

# Get server address
print ("\nWelcome!")
server_addr = raw_input("\n     Where is your filing cabinet (IP addr)? ")

# Register user with server
print ("Ok, registering you with "+server_addr+"\n")
msg = "iam\n" + raw_input("     Who are you? ")
sendthis(s, msg, server_addr)
recvresp(s)

# Collect files
print ("\nIn your local filesystem, you have a folder called MyDrawer.")
print ("\nAll files in your drawer will be shared with the cabinet directory.\n")
filestring = collectFiles()
print ("your files:\n", filestring)

# Send file names to server
raw_input("\nwhen you're ready to share, press enter...")
sendthis(s, "ihave" + filestring, server_addr)
recvresp(s)

while True:
    print ("\nAvailiable options:")
    print ("     l (list): check the cabinet directory for a list of availiable files.")
    print ("     s (search): check for a certain file in the cabinet.")
    print ("     g (grab): get a file from a drawer.")
    print ("     u (update): update your drawer, sharing any new files with the cabinet.")
    print ("     o (open): open your drawer, allowing people to get files from you.")
    print ("     q (quit): exit the program.")

    command = raw_input("\n     >")
    print

    if (command=="o"): # OPEN COMMAND: waits for another user to request a file
        print ("your drawer is now open for other clients to get your files!")
        print ("type 'c' and press enter to close your drawer." )
        
        inputs = [s, sys.stdin]
        
        # Allow for input from stdin and the socket, so user can close
        while inputs:
            if (command =="c"): break
            # Separate inputs
            readable, writable, exceptional = select.select(inputs, inputs, inputs)
            for i in readable:
                if i is s:
                    # Wait for a request
                    response, addr = s.recvfrom(1024)
                    # Got a request, record the filename
                    fn = response.split("\n")[1]
                    # Send the file.
                    sendFile(s, fn, addr)
                elif i is sys.stdin:
                    # Check for close command
                    command = raw_input()
                    if (command == "c"):
                        print ("closing drawer...")
                        break
            for ex in exceptional: # Error handling
                print ('something bad happened.')
                break 
    elif (command == "l"): # LIST COMMAND: ask server to list files
        sendthis(s, "list", server_addr)
        recvresp(s)

    elif (command == "s"): # SEARCH COMMAND: ask server to search for a certain file
        msg = "doyouhave\n" + raw_input("what filename do you want to check for? ")
        sendthis(s, msg, server_addr)
        recvresp(s)

    elif (command == "g"): # GRAB COMMAND: ask server for file location, then try to get file
        fileiwant = raw_input("what filename do you want to get? ")
        msg = "whereis\n" + fileiwant
        sendthis(s, msg, server_addr)
        
        ips = recvresp(s).split("\n")

        # I got an IP list
        if (ips.pop(0) == "filelocations"):
            # Loop thru IPs in list, requesting the file. 
            # If request timed out, try next IP, otherwise all good.
            for ip in ips:
                msg = "giveme\n"+fileiwant
                sendthis(s,msg,ip)
                if recvFile(s, fileiwant):
                    break

    elif (command == "u"): # UPDATE COMMAND: update this user's shared files
        print ("\nAll files in your drawer will be shared with the cabinet directory.\n")

        filestring = collectFiles()
        print ("your files:\n", filestring)

        raw_input("\nwhen you're ready to share, press enter...")
        sendthis(s, "ihave\n" + filestring, server_addr)
        recvresp(s)

    elif (command == "q"):
        sendthis(s, "goodbye", server_addr)
        print ("\ngoodbye!\n")
        s.close
        sys.exit(0)

s.close()
