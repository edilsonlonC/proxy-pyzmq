from dotenv import load_dotenv
load_dotenv()
from database.database import database
import json


db = database()
import zmq
#!/home/edilson/anaconda3/bin/python3.8
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

def choose_server(hash_parts):
    number_servers = db.servers.count_documents({})
    servers = db.servers.find({},{'address':1,'port':1,'_id':0})
    server_itr = 0
    server_list = list()
    for h in hash_parts:
        if server_itr >= number_servers:
            server_itr = 0
        server_list.append(servers[server_itr])
        server_itr = server_itr + 1
    print(server_list)

    response = {
        'servers': server_list,
        'hash_parts': hash_parts
    }

    socket.send_multipart([json.dumps(response).encode('utf-8')])

def upload(request):
    hash_parts = request.get('hash_parts')
    choose_server(hash_parts)

def user_exist(username,password):
    user = db.users.find_one({'username':username,'password':password})
    return True if user else False

def register(files):
    username = files.get('username')
    password = files.get('password')
    print('')


def decide_command(request):
    command = request.get('command')
    if command == 'upload':
        upload(request)



def main():
    print('server is running on port 5556')
    while True:
        request = socket.recv_multipart()
        json_request = json.loads(request[0])
        decide_command(json_request)

if __name__ == '__main__':
    main()
    