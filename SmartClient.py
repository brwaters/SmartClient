#!/usr/bin/env python3

# CSC361 A1 - Brendon Waters - V00963713
# SmartClient.py

import sys
import socket
import re

def main():
    URL = sys.argv[1].strip()
    print(URL)
    match = parseURL(URL)
    HOST = match.group(0)
    print(HOST)
    PORT = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'GET / HTTP/1.1\r\nHost: ' + bytes(HOST, 'utf-8') + b'\r\nAccept: text/html\r\n\r\n')
        data = s.recv(1024)
    print('Received', repr(data))

def parseURL(input):  
    pattern = re.compile(r"[A-Za-z0-9]+.*([A-Za-z0-9]+(\.[A-Za-z0-9]+)+)", re.IGNORECASE)
    return pattern.match(input)

if __name__ == "__main__":
    main()