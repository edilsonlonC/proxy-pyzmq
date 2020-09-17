#!/home/edilson/anaconda3/bin/python3.8

import zmq 
import json
import sys
from hashlib import sha256 , sha224

files = {}

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")

def upload(servers,parts_hash,filename):
    servers_json = json.loads(servers)
    servers_list = servers_json.get('servers')
    file = open(filename,'rb')
    for s in range(len(servers_list)):
        bytes_to_send = file.read(1)
        address = servers_list[s]['address']
        port = servers_list[s]['port']
        context_server = zmq.Context()
        socket_server = context_server.socket(zmq.REQ)
        socket_server.connect(f"tcp://{address}:{port}")
        print(parts_hash[s])
        socket_server.send_multipart([parts_hash[s],bytes_to_send,files.get('command').encode('utf-8')])
        response = socket_server.recv_multipart()
        print(response)
    print(len(servers_list), len(parts_hash))
    return

def get_hash(files):
    filename = files.get('filename')
    hash_list = list()
    with open(filename,'rb') as f:
        m = sha224()
        _bytes = f.read(1)
        m.update(_bytes)
        hash_list.append(m.digest())
        while _bytes:
            m = sha224()
            _bytes = f.read(1)
            m.update(_bytes)
            hash_list.append(m.digest())
    return hash_list




def get_servers_proxy (args):
    if len(args) < 3:
        print('arguments are misssed')
        return
    filename = args[1]
    files['filename'] = filename
    hash_parts = get_hash(files)
    try:
        file = open(f"{filename}",'rb')
        bytes_to_send = file.read()
        hash_parts.append(json.dumps(files).encode('utf-8'))
        socket.send_multipart(hash_parts)
        response = socket.recv_multipart()
        upload(response.pop(-1),response,filename)
    except FileNotFoundError:
        print(f"the file {filename} doesn't exist")
   


def decide_command():
    if len(sys.argv) <= 1:
        print('arguments are missing')
        return
    args = sys.argv[1:]
    command = args[0]
    print(command)
    files['command'] = command
    if command == 'upload':
        get_servers_proxy(args)
    else:
        socket.send_multipart([b'prueba'])
        response = socket.recv_multipart()

def main():
    decide_command()

if __name__ == '__main__':
    main()
    