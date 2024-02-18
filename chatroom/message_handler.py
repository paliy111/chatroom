def find_key_for_value(d, value):
    keys_for_value = [key for key, val in d.items() if val == value]
    return keys_for_value[0]

def _handle_hello(message, sender, usernames: dict, messages: dict):
    usernames[message["name"]] = sender
    response = {"code": "welcome"}
    messages[sender] = []
    messages[sender].append(response)

def _handle_who(_, sender, usernames: dict, messages: dict):
    response = {"code": "users", "users": list(usernames.keys())}
    messages[sender].append(response)

def _handle_outgoing(message, sender, usernames: dict, messages: dict):
    if message["to"] in usernames.keys():
        response = {"code": "incoming", "from": find_key_for_value(usernames, sender), "content": message["content"]}
        messages[usernames[message["to"]]].append(response)

def _handle_broadcast(message, sender, usernames: dict, messages: dict):
    senders_name = find_key_for_value(usernames, sender)
    for name, user in usernames.items():
        if senders_name == name:
            continue
        response = {"code": "incoming_broadcast", "from": senders_name,
                    "content": message["content"]}
        messages[user].append(response)

def _handle_quit(_, sender, usernames: dict, messages: dict):
    del usernames[find_key_for_value(usernames, sender)]
    if sender in messages:
        del messages[sender]
    sender.close()

def message_decoder(message, sender, usernames: dict, messages: dict):
    code = message["code"]
    handlers = {
        "hello": _handle_hello,
        "who": _handle_who,
        "outgoing": _handle_outgoing,
        "outgoing_broadcast": _handle_broadcast,
        "quit": _handle_quit,
    }
    handler = handlers[code]
    handler(message, sender, usernames, messages)
