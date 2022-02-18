#############################################################################
# Program:
#    PythonWebServer, Computer Networks

# Author:
#    Brandon Jarrell
# Summary:
#    This program acts as a WebServer. Returns HTML files, txt files and images.
#     works in the cwd of where the file is located. currently does not work with
#     multiple client, but that would be easy to implement if required. This is a
#     good start for a local webserver for say a raspberry pi or ePortfolio
##############################################################################

#############################################################################
#
# Changes made to my code for the Python Web Server Take-2:
#   -made it so that the content type actually was returned and useful
#   -the little icons in the icon folder were not being used correctly
#    because I accidientally messed up the file path in my operation
#
#############################################################################
from socket import *
import sys
import os
os.system('cls')

def openFile(requestedFile):
   with open(requestedFile, "rb") as x: #open the file
      content = x.read()
   return content


# Return proper content type
def contentType(filepath):
   fileName, typeOfFile = os.path.splitext(filepath)
   contentType = ''
   if(typeOfFile == ".txt"):
      contentType = "Content-Type: text/plain\r\n"
   elif(typeOfFile == ".jpg"):
      contentType = "Content-Type: image/jpeg\r\n"
   elif(typeOfFile == ".gif"):
      contentType = "Content-Type: image/gif\r\n"
   elif(typeOfFile == ".html"):
      contentType = "Content-Type: text/html\r\n"
   return contentType

def parseRequest(request):
   requestType = '' #holder for the request
   requestItem = '' #holder for the item requested
   typeDone = False
   for x in request:   
      if not typeDone: #add all characters up to get type
         if x == ' ':  #and stop at space
            typeDone = True
            continue
         requestType += x
         continue
         #do it again to get the item being asked for
      if x == ' ': #and stop at the space
         break
      requestItem += x
   return requestType, requestItem


# Server Connection Setup
serverPort = int(sys.argv[1]) if len(sys.argv) == 2 else 6789
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
os.system('cls')
print ("Server is running on port " , str(serverPort))



try:
   # Main Server Loop
   
   while 1:
      #establish the connection
      webClientConnection, Client1 = serverSocket.accept()
      message = webClientConnection.recv(1028).decode()
      #parse the request into its components
      requestType, requestItem = parseRequest(message)
      header = contentType(requestItem)

      #if its a GET (always will be in this case)
      if requestType == 'GET':
         file_to_open = '' 
         if requestItem == '/': #if the user does not define what they want
            file_to_open = 'bufbomb.html' #direct them to the "homepage" (Simple HTML)
         elif requestItem[0] == '/':
            file_to_open = requestItem[1:]
            
         # try to open the file  Content-type: "
         OK_Header = "HTTP/1.0 200 OK\r\nConnection: close\r\n"
         FNF_Header = "HTTP/1.0 404 Not Found\r\n"
         try:
            file_to_send = openFile(file_to_open)#open the file
            webClientConnection.send((OK_Header + header + "\r\n").encode('ascii'))#send the header
         except:
             webClientConnection.send(FNF_Header.encode('ascii'))
             print("failed attempt")
             webClientConnection.close()
             continue
         
         #send the actual desired content
         webClientConnection.send(file_to_send)
         webClientConnection.close()
         print("Content sent, connection closed")

      # Things to be done include:
      #  -accept a connection 
      #  -read the request (if an empty request ignore it)
      #  -parse token from the request string
      #  -make sure the file exists
      #     -all files are to be relative to the directory 
      #      in which the web server was started
      #  -create and send the status line
      #  -create and send the "Content-type:" header
      #  -What goes between the header lines and the requested file?
      #  -send the file or 404 message
      #     -open a file in binary like ... = open(filepath, "rb")
      #  -don't forget to close the connection socket


except KeyboardInterrupt:
   print ("\nClosing Server")
   serverSocket.close()
   quit()


