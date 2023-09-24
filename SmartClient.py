#!/usr/bin/env python3

# CSC361 A1 - Brendon Waters - V00963713
# SmartClient.py

import sys
import socket
import re
import ssl

# This is for checking HTTPS from tutorials
# context = ssl.create_default_context()
# conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname="www.google.ca")

def main():
    URL = sys.argv[1].strip()
    print("URL Entered: " + URL)
    match = parseURL(URL)
    if match.group(2) is not None and not '':
        PROTOCOL = match.group(2).upper()
    else:
        PROTOCOL = 'HTTP'
    HOST = match.group(3)
    print("Hostname obtained: " + HOST)
    print("Protocol: " + PROTOCOL)
    if match.group(5) !='':
        PORT = int(match.group(5))
    else:
        if PROTOCOL == 'HTTP':
            PORT = int(80)
        else:
            PORT = int(443)
    print("Port: " + str(PORT))
    if match.group(4) != '':
        ENDPOINT = match.group(5)
    else:
        ENDPOINT = '/'
    print("Endpoint: " + str(ENDPOINT)) 
    data = sendRequest(PROTOCOL, HOST, PORT, ENDPOINT)
    print("Received: ", repr(data))
    print("-----Response Header-----")
    for key,value in data.items():
        print(key + ': '+ value)

def sendRequest(PROTOCOL, HOST, PORT, ENDPOINT):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'GET ' + bytes(ENDPOINT, 'utf-8') + b' ' + bytes(PROTOCOL,'utf-8') + b'/1.1\r\nHost: ' + bytes(HOST, 'utf-8') + b'\r\nConnection: Keep-Alive\r\nAccept: text/html\r\n\r\n')
        data = parseResp(s.recv(1024))
        print(data.get('HTTP/1.1'))
        print(data.get('HTTP/1.0'))
        # if (data.get('HTTP/1.1') == '302 Moved Temporarily' or '301 Moved Permanently'):
            # print('moved 1.1')
            # parseURL(data.get('HTTP/1.1'))
            # ENDPOINT = data.get()
        while not (data.get('HTTP/1.0') == '302 Moved Temporarily' or '301 Moved Permanently'):
            print('moved 1.0')
            match = parseURL(data.get('Location'))
            sendRequest(PROTOCOL, HOST, PORT, ENDPOINT = match.group(3))
    return data

def parseResp(data):
    list = data.decode().split('\r\n')
    # print(list)
    d = dict(re.split(r'[\s|:]', each, 1) for each in list if each !='')
    d = {k.lstrip():v.lstrip() for (k, v) in d.items()}
    return d

def parseURL(input):
    pattern = re.compile(r'((https|http)://)?([a-zA-Z.]+):?(/[\w]+)(\d*)', re.IGNORECASE)
    return pattern.match(input)

if __name__ == '__main__':
    main()