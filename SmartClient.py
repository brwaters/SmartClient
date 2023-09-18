#!/usr/bin/env python3

# CSC361 A1 - Brendon Waters - V00963713
# SmartClient.py

import sys
import socket
import re

def main():
    URL = sys.argv[1].strip()
    print("URL Entered: " + URL)
    match = parseURL(URL)
    if match.group(2) != '':
        PROTOCOL = 'HTTP'
    else:
        PROTOCOL = match.group(2).upper()
    HOST = match.group(3)
    print("Host name obtained: " + HOST)
    print("Protocol: " + PROTOCOL)
    if match.group(4) !='':
        PORT = int(match.group(4))
    else:
        PORT = int(80)
    print("Port: " + str(PORT))
    data = sendRequest(PROTOCOL, HOST, PORT)
    # print("Received: ", repr(data))
    # data = parseResp(data)
    # print("Received: " + repr(data))
    print("-----Response Header-----")
    for key,value in data.items():
        print(key + ': '+ value)

def sendRequest(PROTOCOL, HOST, PORT):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'GET / ' + bytes(PROTOCOL,'utf-8') + b'/1.1\r\nHost: ' + bytes(HOST, 'utf-8') + b'\r\nConnection: Keep-Alive\r\nAccept: text/html\r\n\r\n')
        data = parseResp(s.recv(1024))
        # if 'HTTP/1.0' in data is '302 Moved Temporarily':    
    return data

def parseResp(data):
    list = data.decode().split('\r\n')
    # print(list)
    d = dict(re.split(r'[\s|:]', each, 1) for each in list if each !='')
    d = {k.lstrip():v.lstrip() for (k, v) in d.items()}
    return d

def parseURL(input):
    pattern = re.compile(r'((https|http)://)?(www.[\w]+.[\w]+):?(\d*)', re.IGNORECASE)
    return pattern.match(input)

if __name__ == '__main__':
    main()