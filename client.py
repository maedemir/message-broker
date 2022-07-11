import socket
import sys

buffer_size = 1024
encoding = 'ascii'


def receive_data(conn):
    conn.settimeout(10.0)
    while True:
        message_length = int(conn.recv(buffer_size).decode(encoding))
        msg = conn.recv(message_length)
        if not msg:  # server has no msg
            continue
        msg = msg.decode(encoding)
        print("from server-->", msg)
        message = msg
        conn.settimeout(None)
        split_msg = message.split()
        if split_msg[0] == "subAck:":
            print("Subscribing on ", split_msg[1:])
        elif msg == "pubAck":
            print("Message published successfully")
            sys.exit()
        elif msg == "topic not found":
            sys.exit()
        elif split_msg[0] == 'Pong':
            sys.exit()
        elif split_msg[0] == 'Ping':
            pong(conn)


def send_data(connection, message):
    message = message.encode(encoding)
    message_length = len(message)
    message_length = str(message_length).encode(encoding)  # length of ascii message should also be encoded
    message_length += b' ' * (buffer_size - len(message_length))  # we put 1024 - message length space so that client
    # can encode more easily
    connection.send(message_length)  # first we send length of message
    connection.send(message)  # then the massage itself

def subscribe(conn, message):  # here message is the list of all topics that are from argv
    if len(message) == 0:
        print("Topic can't be empty! try again...")
        sys.exit()
    msg = "Subscribe"
    for m in message:   # we create original request as an string
        # for example : subscribe t1 t2 t2
        msg += " " + m
    send_data(conn, msg)


def publish(conn, message):
    msg = "Publish "
    if len(message) <= 1:   # 2 arguments are needed for publishing
        print("you must specify topic and massage for publishing!")
        sys.exit()
    msg += message[0] + " "
    message = message[1:]
    for m in message:
        msg += " " + m
    send_data(conn, msg)


def ping(client):
    send_data(client, "Ping")


def pong(client):
    send_data(client, "Pong")


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("please enter a correct format of input!")
        sys.exit()
    host = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    if sys.argv[3] == "Subscribe":
        subscribe(s, sys.argv[4:])
    elif sys.argv[3] == "Publish":
        publish(s, sys.argv[4:])
    elif sys.argv[3] == "Ping":
        ping(s)
    elif sys.argv[3] == "Pong":
        pong(s)
    else:
        print("The command you entered is not supported!")
        sys.exit()
    while True:
        try:
            receive_data(s)
        except socket.error:
            print("timeout")
