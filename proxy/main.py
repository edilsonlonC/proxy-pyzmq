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
    print(db.users)
    socket.send_multipart([b'prueba'])

def upload(request):
    hash_parts = request.get('parts_hash')
    choose_server(hash_parts)

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
    