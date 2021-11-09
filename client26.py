"""EX 2.6 client implementation
   Author:
   Date:
"""

import socket
import protocol
import sys

SAVED_PHOTO_LOCATION = sys.argv[0][:-sys.argv[0][::-1].find(r'/')]+"/clienttmp.jpg"
def handle_server_response(mu_socket,cmd):
    data = cmd
    ans,params = protocol.get_msg(mu_socket)
    if ans :
        if cmd == "DELETE" :
            print (params)
        if cmd == "COPY":
            print(params)
        if cmd=="DIR":
            print(params)
        if cmd=="EXECUTE":
            print(params)
        if cmd == "TAKE SCREENSHOT":
            if params :
                print("screenshot scussefuly taken via server ")
            else :
                print("error in screenshot - need fix!!! ")
        if cmd=="SAVE_PHOTO":
            if params.isdigit():
                photo = open(SAVED_PHOTO_LOCATION, 'wb')
                recvice = mu_socket.recv(int(params))
                photo.write(recvice)
                photo.close()
            else :
                print("server is not working with our protocol - it need to send the screenshot mem size ")
    else :
        print ("the command could execute please check the server side ")


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))
    while True:
        user_input = input("Enter command\n")
        # Check if user entered a valid command as defined in protocol
        valid_cmd = protocol.check_cmd(user_input)
        if valid_cmd:
            # If the command is valid:
            # 1. Add length field ("RAND" -> "04RAND")

            my_socket.send(protocol.create_msg(user_input).encode())
            # 2. Send it to the server
            if user_input == 'EXIT':
                break
            # 3. If command is EXIT, break from while loop
            respone = protocol.get_msg(my_socket)

            # 4. Get server's response
            if respone[0]:
                print(respone[1])

            # 5. If server's response is valid, print it

            else:
                print("Response not valid\n")
        else:
            print("Not a valid command")

    print("Closing\n")
    # Close socket


if __name__ == "__main__":
    main()
