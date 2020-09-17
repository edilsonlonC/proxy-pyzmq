#!/home/edilson/anaconda3/bin/python3.8
import zmq
import sys
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
port = sys.argv[1]
socket.bind(f"tcp://*:{port}")

def upload(request):
    filename = request.get('filename')
    bytes_to_save = request.get('bytes')
    with open(f"files/{filename}", 'wb') as f:
        f.write(bytes_to_save)
    socket.send_multipart([json.dumps({'file_saved': True}).encode('utf-8')])

        
socket.send_multipart([b'uploading'])

def decide_commands(request):
    command = request.get('command')
    if command == 'upload':
        upload(request)
    return
  
    command = args[0]
def main():
    print(f"server is running on port : {port}")
    while True:
        request = socket.recv_multipart()
        print(request)
        files = json.loads(request[0])
        if len(request) > 1:
            files['bytes'] = request[1]
        decide_commands(files)


if __name__ == '__main__':
    
    main()
    