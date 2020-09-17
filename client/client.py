#!/home/edilson/anaconda3/bin/python3.8

import zmq 
import json
import sys
files = {}

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")

def upload (args):
    if len(args) < 3:
        print('arguments are misssed')
        return
    filename = args[1]
    files['filename'] = filename
    try:
        file = open(f"{filename}",'rb')
        bytes_to_send = file.read()
        socket.send_multipart([json.dumps(files).encode('utf-8'),bytes_to_send])
        response = socket.recv_multipart()
        print(response)
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
    files['hash_parts'] = 'parts_hash'
    if command == 'upload':
        upload(args)
    else:
        socket.send_multipart([b'prueba'])
        response = socket.recv_multipart()

def main():
    decide_command()

if __name__ == '__main__':
    main()
    