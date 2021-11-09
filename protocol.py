"""EX 2.6 protocol implementation
   Author: IDAN DORON HAI MAMAN 214926941
   Date:10/26/2021

 __o__       o__ __o            o         o        o          o
   |        <|     v\          <|>       <|>      <|\        /|>
  / \       / \     <\         < >       < >      / \\o    o// \
  \o/       \o/       \o        |         |       \o/ v\  /v \o/
   |         |         |>       o__/_ _\__o        |   <\/>   |
  < >       / \       //        |         |       / \        / \
   |        \o/      /         <o>       <o>      \o/        \o/
   o         |      o           |         |        |          |
 __|>_      / \  __/>          / \       / \      / \        / \



"""


LENGTH_FIELD_SIZE = 4
PORT = 8820

def checkforpath (path):
    return path != " " and type(path) == type(str) and r'/' in path
def check_cmd(data):
    """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""
    data = str(data)
    if "DELETE" in data:
        return checkforpath(data, "DELETE")
    if "COPY" in data:
        check = data.split(' ')
        return  len(check) == 3 and check[0] == "COPY" and checkforpath(check[1]) and checkforpath(check[2])
    if "DIR" in data:
        return checkforpath(data, "DIR")
    if "EXECUTE" in data:
        return checkforpath(data, "EXECUTE")
    if "TAKE SCREENSHOT" in data:
        if "TAKE SCREENSHOT" in data:
            return True
        return False
    if "SEND_PHOTO" in data:
        if "SEND_PHOTO" in data:
            return True
        return False




def create_msg(data):
    """Create a valid protocol message, with length field"""
    return str(len(data)).zfill(LENGTH_FIELD_SIZE) + data


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """

    size = my_socket.recv(LENGTH_FIELD_SIZE).decode()

    if size.isdigit():
        msg = my_socket.recv(int(size)).decode('ascii')
        return True, msg
    else:
        return False, "Error"



