# message-broker
A message broker is a server that distributes messages received from clients. Of course, these brokers can do a lot more!
There are two important operations in the server, one is Publish and the other is Subscribe
In the Subscribe operation, the client requests to listen to a specific topic. In Publish client publishes a message
on a specific topic. Finally, broker delivers messages into the hands of all those listening on that thread
In this section, all communication between the server and the client is implemented in TCP format.

<img width="592" alt="image" src="https://user-images.githubusercontent.com/72692826/178341898-7c8ee8e5-56fb-4fdf-b8e3-c7af7da50783.png">

## Commands

1) Client to server
- Publish: This command sends a message from the client side to the server under a specific title. Messages are ASCII strings and
its length is arbitrary.
- Subscribe: This command informs the server that this client is requesting to receive messages from the given title.
- Ping: This command is sent from the client side to ensure connection. Note that server response would be a sigle pong message.

2) Server to client
- Message: This command sends a message from the server side to the client if the client has subscribed for that subject(note
that this command includes message and title). Messages are ASCII strings of arbitrary length.
- SubAck: This command is sent from the server side to confirm that the subscription operation has been successful
- PubAck: This command is sent from the server side to confirm that the Publish operation is successful.
- Pong: This command is sent from the server side in response to the Ping message from client

## Persian project description

[message-broker.pdf](https://github.com/maedemir/message-broker/files/9087055/message-broker.pdf)
