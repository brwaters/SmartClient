#!/usr/bin/env python3

# CSC361 A1 - Brendon Waters - V00963713
# SmartClient.py

import sys
import socket
import re
import ssl

# This is for checking HTTPS from tutorials
# context = ssl.create_default_context()
# context.set_alpn_protocols(['http/1.1','h2'])
# conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname="www.google.ca")
# conn.connect(("www.google.ca", 443))
# conn.sendall(b'GET / HTTP/1.1\r\nHost: www.gooogle.ca\r\n\r\n')
# list =  conn.selected_alpn_protocol()
# if list and'h2' in list:
#     print('HTTP2 supported')
# else:
#     print("HTTP2 not supported")

def main():
    URL = sys.argv[1].strip()
    # print("URL Entered: " + URL)
    match = parseURL(URL)
    PROTOCOL, HOST, ENDPOINT, PORT = assignRequestParameters(match)
    data = sendRequest(PROTOCOL, HOST, ENDPOINT, PORT)
    print("-----Response Header-----")
    if data:
        for key,value in data.items():
            print(key + ': '+ value)

def sendRequest(PROTOCOL, HOST, ENDPOINT, PORT):
    if not (PROTOCOL or HOST or ENDPOINT or PORT):
        return None
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'GET ' + bytes(ENDPOINT, 'utf-8') + b' ' + bytes(PROTOCOL,'utf-8') + b'/1.1\r\nHost: ' + bytes(HOST, 'utf-8') + b'\r\nConnection: Keep-Alive\r\nAccept: text/html\r\n\r\n')
        # response = b""
        # while True:
        #     data = s.recv(1024)
        #     if not data:
        #         break
        #     response += data
        # data = parseResp(response)
        data = parseResp(s.recv(1024 * 4))
        # print(data)
        # print("Received: ", repr(data))
        # print(data.get('HTTP/1.1'))
        # print(data.get('HTTP/1.0'))
        if (data.get('HTTP/1.1') == ('302 Moved Temporarily' or '301 Moved Permanently')):
            # print('moved 1.1')
            # print(data.get('Location'))
            match = parseURL(data.get('Location'))
            PROTOCOL, HOST, ENDPOINT, PORT = assignRequestParameters(match)
            # print(ENDPOINT)
            data = sendRequest(PROTOCOL, HOST, ENDPOINT, PORT)
            
        if (data.get('HTTP/1.0') == ('302 Moved Temporarily' or '301 Moved Permanently')):
            # print('moved 1.0')
            # print(data.get('Location'))
            match = parseURL(data.get('Location'))
            PROTOCOL, HOST, ENDPOINT, PORT = assignRequestParameters(match)
            # print(ENDPOINT)
            data = sendRequest(PROTOCOL, HOST, ENDPOINT, PORT)
        else:
            # data = parseResp(s.recv(1024 * 4))
            return data

def parseResp(data):
    list = data.decode().split('\r\n')
    # print(list)
    d = dict(re.split(r'[\s|:]', each, 1) for each in list if each !='')
    d = {k.lstrip():v.lstrip() for (k, v) in d.items()}
    return d

def parseURL(input):
    pattern = re.compile(r'((https|http)://)?([a-zA-Z.]+)([/\w]*.?[\w]*):?(\d*)', re.IGNORECASE)
    return pattern.match(input)

def assignRequestParameters(match):
    if match.group(2) is not None and not '':
        PROTOCOL = match.group(2).upper()
    else:
        PROTOCOL = 'HTTP'
    HOST = match.group(3)
    # print("Hostname obtained: " + HOST)
    # print("Protocol: " + PROTOCOL)
    if match.group(4) != '':
        ENDPOINT = match.group(4)
    else:
        ENDPOINT = '/'
    if match.group(5) !='':
        PORT = int(match.group(5))
    else:
        if PROTOCOL == 'HTTPS':
            PORT = int(443)
        else:
            PORT = int(80)
    # print("Port: " + str(PORT))
    # print("Endpoint: " + str(ENDPOINT))
    print("-----Request Header-----")
    print("GET " + PROTOCOL.lower() + "://" + HOST + ENDPOINT + ' ' + PROTOCOL + "/1.1")
    print("Host: " + HOST)
    print("Connection: Keep-Alive")
    print("-----Request End-----")
    return PROTOCOL, HOST, ENDPOINT, PORT

if __name__ == '__main__':
    main()