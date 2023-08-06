import requests
import websocket
import json
import threading
import time

def send_message(token,channel_id,message):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    data = {
        "content": f"{message}"
    }
    header = {
        "authorization": f"{token}"
    }
    r = requests.post(url,headers=header,data=data)
    print(r.text)

def join_server(token,server_id):
    url = f"https://discord.com/api/v9/invites/{server_id}"
    header = {
        "authorization": f"{token}"
    }
    r = requests.post(url,headers=header)
    print(r.text)

def delete_message(token,channel_id,message_id):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}"
    header = {
        "authorization": f"{token}"
    }
    r = requests.delete(url,headers=header)
    print(r.text)

def edit_message(token,channel_id,message_id,message_content):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}"
    header = {
        "authorization": f"{token}"
    }
    data = {
        "content":f"{message_content}"
    }
    r = requests.patch(url, headers=header,data=data)
    print(r.text)

def typing(token,channel_id):
    url = f"https://discord.com/api/v9/channels/{channel_id}/typing"
    header = {
        "authorization": f"{token}"
    }
    r = requests.post(url,headers=header)
    print(r.text)
    print(f"Typing on {channel_id} id's channel")

def version():
    print("© Copyright by Emrovsky in 2021 v8")

def create_role_name_new_role(token,guild_id):
    url = f"https://discord.com/api/v9/guilds/{guild_id}/roles"
    header = {
        "authorization": f"{token}"
    }
    data = {
        "name":"new role"
    }
    r = requests.post(url,data=data,headers=header)
    print(r.text)

def logging_message(token):
    def send_json_request(ws, request):
        ws.send(json.dumps(request))

    def recieve_json_response(ws):
        response = ws.recv()
        if response:
            return json.loads(response)

    def heartbeat(interval, ws):
        print('Listening has started')
        while True:
            time.sleep(interval)
            heartbeatJSON = {
                "op": 1,
                "d": "null"
            }
            send_json_request(ws, heartbeatJSON)

    ws = websocket.WebSocket()
    ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
    event = recieve_json_response(ws)

    heartbeat_interval = event['d']['heartbeat_interval'] / 1000
    threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

    token = token
    payload = {
        'op': 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "windows",
                "$browser": "chrome",
                "$device": 'pc'
            }
        }
    }
    send_json_request(ws, payload)

    while True:
        event = recieve_json_response(ws)

        try:
            print(f"{event['d']['author']['username']}: {event['d']['content']}")

            op_code = event['op']
            if op_code == 11:
                print('heartbeat received')
        except:
            pass

def send_friend_request(token,user_id):
    headers = {'Authorization': token}
    r = requests.put(f"https://discordapp.com/api/v9/users/@me/relationships/{user_id}", headers=headers,json={'content-type:': "application/json"})
    print("Friend request has been send!")

def last_dms(token):
    url = "https://discord.com/api/v9/users/@me/channels"

    header = {
        "authorization": token
    }

    r = requests.get(url, headers=header)
    print(r.text)

def read_all_user_note(token):
    url = "https://discord.com/api/v9/users/@me/notes"

    header = {
        "authorization": token
    }

    r = requests.get(url, headers=header)
    print(r.text)

def public_servers(token,how_much_server):
    if int(how_much_server) > (48):
        print("ERROR : MAXIMUM NUMBER OF SERVERS IS 48 PER PAGE")
        exit()
    url = f"https://discord.com/api/v9/discoverable-guilds?offset=0&limit={how_much_server}"
    header = {
        "authorization": token
    }
    r = requests.get(url, headers=header)
    data = json.loads(r.text)
    guild = data["guilds"]
    a = 0
    while True:
        aga = guild[a]
        name = guild[a]["name"]
        desc = guild[a]["description"]
        inv = guild[a]["vanity_url_code"]
        print(name)
        print(desc)
        print("discord.gg/" + inv)
        print("------------------------------------------------------")
        a += 1
        if str(a) == how_much_server:
            break


def check_token(token):
    url = "https://discord.com/api/v9/discoverable-guilds?offset=0&limit=10"
    header = {
        "authorization": token
    }
    r = requests.get(url,headers=header)
    if r.text == '{"message": "You need to verify your account in order to perform this action.", "code": 40002}':
        print("Your account was suspended")
    if r.text != '{"message": "You need to verify your account in order to perform this action.", "code": 40002}':
        print("Your account was working")
def wawe_to(token,channel_id):
    url = f"https://discord.com/api/v9/channels/{channel_id}/greet"

    header = {
        "authorization": token
    }
    data = {"sticker_ids": ["749054660769218631"]}
    r = requests.post(url, headers=header, data=data)
    print(r.text)
def remove_friend(token):
    headers = {'Authorization': token}
    requests.delete(f"https://discordapp.com/api/v9/users/@me/relationships/874622121580560415", headers=headers,json={'content-type:': "application/json"})
    print("Removed from friend list")

def kick_user(token,guild_id,member_id):
    header = {'Authorization': token}
    r = requests.delete(f"https://discord.com/api/v9/guilds/{guild_id}/members/{member_id}",headers=header)
    print("The user was kicked in this server")

def ban_user(token,guild_id,member_id):
    header = {'Authorization': token}
    r = requests.put(f"https://discord.com/api/v9/guilds/{guild_id}/bans/{member_id}",headers=header)
    print("The user was banned in this server")


def audit_logs(token,guild_id):
    url = f"https://discord.com/api/v9/guilds/{guild_id}/audit-logs?limit=50"

    header = {
        "authorization": token,
        "content-type": "application/json"
    }

    r = requests.get(url, headers=header)
    print(r.text)

def gift_code(gift_code):
    url = "https://discord.com/api/v9/entitlements/gift-codes/"+gift_code
    r = requests.get(url)
    print(r.text)

def avatar(token,user_id):
    url = f"https://discord.com/api/v9/users/{user_id}/profile"

    header = {
        "authorization": token
    }
    r = requests.get(url, headers=header)
    sa = json.loads(r.text)
    data = sa["user"]
    nick = data["username"]
    discri = data["discriminator"]
    av = data["avatar"]
    print("User : " + nick + "#" + discri)
    avatar_def = f"https://cdn.discordapp.com/avatars/{user_id}/{av}.webp?size=256"
    print("Avatar : " + avatar_def)
    bio = data["bio"]
    print("Biography : " + bio)
    mut_guild = sa["mutual_guilds"][0]["id"]
    print("Mutual guild id's : " + mut_guild)