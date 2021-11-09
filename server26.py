"""EX 2.6 server implementation
   Author:
   Date:
"""
import os.path
import socket
import protocol
import sys
import pyautogui
import subprocess
import shutil
import glob
SAVED_PHOTO_LOCATION = sys.argv[0][:-sys.argv[0][::-1].find(r'/')]+"/serverTmp.jpg"

def internal_check (data, code_name):
    check = data.split(' ')
    if len(check) ==2:
        if check[0] == code_name and os.path.exists(check[1]):
            return True
    return False
def check_cmd_server(data):
    """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""
    data = str(data)
    if "DELETE" in data:
        return internal_check(data, "DELETE")
    if "COPY" in data:
        check = data.split(' ')
        return  len(check) == 3 and check[0] == "COPY" and os.path.exists(check[1]) and os.path.exists(check[2])
    if "DIR" in data:
        return internal_check(data, "DIR")
    if "EXECUTE" in data:
        return internal_check(data, "EXECUTE")
    if "TAKE SCREENSHOT" in data:
        return True
    if "SEND_PHOTO" in data:
        return True
    return False

def check_client_request(cmd):
    return check_cmd_server(cmd), cmd.split(" ")[0], cmd.split[1:]
def handle_client_request(command, params):
    data = str(command)
    if "DELETE" in data:
        try:
            os.remove(params[0])
            return "OK"
        except:
            return "Error"
    if "COPY" in data:
        try:
            shutil.copy(params[0], params[1])
            return "OK"
        except :
            return "Error"
    if "DIR" in data:
        try :
            glob.glob(params[0]+"/*.*")
            return "OK"
        except :
            return "Error"
    if "EXECUTE" in data:
        try:
            subprocess.call(params[0])
            return "OK"
        except  :
            return "Error"
    if "TAKE SCREENSHOT" in data:
        try:
            image = pyautogui.screenshot()
            image.save(SAVED_PHOTO_LOCATION)
            return "OK"
        return "Error"
    if "SEND_PHOTO" in data:
        try:
            return os.path.getsize(SAVED_PHOTO_LOCATION)
        except :
            return "Error"


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)

        if valid_msg:
            print("valid massage: " + str(cmd))
            # 1. Print received message

            if protocol.check_cmd(str(cmd)):

                msg_v = protocol.create_msg(protocol.create_server_rsp(cmd))
                print(msg_v)
                client_socket.send(msg_v.encode())
            # 2. Check if the command is valid
            # 3. If valid command - create response
            else:
                response = "Wrong command"
                client_socket.send(response.encode())
                break
        else:
            response = "Wrong protocol"
            client_socket.send(response.encode())
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage
        if cmd == "EXIT":
            break

        # Handle EXIT command, no need to respond to the client

        # Send response to the client

    print("Closing\n")
    # Close sockets


if __name__ == "__main__":
    main()
