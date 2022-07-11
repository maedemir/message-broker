import socket
import threading
import time
host = '127.0.0.1'
port = 1373
encoding = 'ascii'
buffer_size = 1024
publications = {}


def handler(connection, address):
    isConnected = True
    while isConnected:
        try:
            message_length = int(connection.recv(buffer_size).decode(encoding))
            message = connection.recv(message_length)   # reading massage from buffer
            if not message:     # no data to receive
                continue
            message = message.decode(encoding)
            print("new massage from clients: {}".format(message))
            if message == "disconnect":
                isConnected = False
            else:
                tempMessage = message.split()  # default separator is any whitespace
                command = message.split()[0]
                if command == "Subscribe":
                    subscribe_client(connection, tempMessage[1:])  # list of all topics one tend to subscribe
                elif command == "Publish":
                    print(tempMessage[1:])
                    publish_client(connection, tempMessage[1:])
                elif command == "Ping":
                    pong(connection)
                elif command == "Pong":
                    print("pong message from:", address)
                #time.sleep(10)
                #send_data(connection, 'Ping')
        except:
            remove_client(connection)
            print('client {} disconnected '.format(address))
            break
    connection.close()


def remove_client(connection):
    for p in publications:
        if connection in publications[p]:
            publications[p].remove(connection)
    connection.close()


def send_data(connection, message):
    message = message.encode(encoding)
    message_length = len(message)
    message_length = str(message_length).encode(encoding)  # length of ascii message should also be encoded
    message_length += b' ' * (buffer_size - len(message_length))  # we put 1024 - message length space so that client
    # can encode more easily
    connection.send(message_length)  # first we send length of message
    connection.send(message)  # then the massage itself


def subscribe_client(connection, message):
    for m in message:
        if m in publications.keys():
            if connection not in publications[m]:
                publications[m].append(connection)
        else:
            publications[m] = [connection]
    ack = "subAck:"     # sending sub ack to client
    for topic in publications.keys():
        if connection in publications[topic]:
            ack += " " + topic
    try:
        send_data(connection, ack)
    except:
        print("could not send subAck")


def publish_client(connection, message):    # format of  massage is ['topic1', 'massage']
    topic = message[0]
    text = message[1:]
    newMessage = topic + ":"
    for t in text:
        newMessage += t + " "
    if topic not in publications.keys():
        send_data(connection, "topic not found")
    else:
        send_data(connection, "pubAck")
        for client in publications[topic]:
            try:
                send_data(client, newMessage)
            except:     # client has closed its connection
                remove_client(client)


def ping(connection):
    send_data(connection, "Ping")


def pong(connection):
    send_data(connection, "Pong")


if __name__ == "__main__":
    HOST_INFORMATION = (host, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(HOST_INFORMATION)
    print("Server is listening on port {} ...".format(port))
    s.listen()
    while True:
        conn, address = s.accept()
        t = threading.Thread(target=handler, args=(conn, address)).start()
        print("New client with address = {} has connected".format(address))
