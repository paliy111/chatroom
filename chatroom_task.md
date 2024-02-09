# Implement a Chatroom

The task for next week is simple: implement a chatroom!
Use the echo server as a starting point.
Here is the protocol:

We will use [JSON](https://docs.python.org/3/library/json.html) to encode data that is sent between the client and the server.
JSON is a way to turn python `dict` structures into strings that can be encoded into `bytes` and sent over a socket.

## Handshake

The client start by connecting and sending a `hello` message, the server responds with a `welcome` message.


    client > server: {"code": "hello", "name": "YOUR NAME HERE"}
    server > client: {"code": "welcome"}

This is the intial handshake. 

## Messaging

During messaging there are several message types.

A `who` message will get you the names of all connected users.

    client > server: {"code": "who"}
    server > client: {"code": "users", "users": ["list", "of", "names", "here"]}

A `text` message will send your text to one of these users

    client > server: {"code": "outgoing", "to": "YOUR FRIEND'S NAME HERE", "content": "MESSAGE CONTENT HERE"}

This will cause the server to relay the message to the other user:

    server > other_client: {"code": "incoming", "from": "SENDER'S USER NAME HERE", "content": "MESSAGE CONTENT HERE"}

An `outgoing_broadcast` message will spam everyone:

    client > server: {"code": "outgoing_broadcast", "content": "SPAM CONTENT HERE"}
    server > all (except sender): {"code": "incoming_broadcast", "from": "SENDER'S NAME", "content": "SPAM CONTENT HERE"}

## Quitting

A client what wants to disconnect should first send the `quit` message

    client > server: {"code": "quit"}

## Error Handling

* The server should not crash when clients disconnect without sending `quit` first.
* The server should not crash if client sends something which is invalid data, e.g.
not a JSON string.

## Client Script

Writing a Server always comes with writing a Client.
The Client program should work like this

    $ python client.py server_ip server_port my_nickname
    connecting to server at {server_ip}, {server_port)
    current users:
    {list of users, one per line}

    enter your message>

This will send a message to another user:

    user|your text here

This will broadcast

    *|your spam here

This will send a `who` message

    who

*NOTE* this means that `*` is an illegal username.

If you are smart, you will implement a Pythonic Client class,
and connect it to the keyboard later.

## Tests

If you are serious, you will write some tests - at least an e2e test to efficiently 
test that your code works.

## Tips

You might find [`dataclass`](https://docs.python.org/3/library/dataclasses.html) useful.

## Bonus Problem

How do we solve the case where two users try to connect using the same name?
