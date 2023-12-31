#!/usr/bin/env python3

# CSC361 A1 - Brendon Waters - V00963713
# SmartClient.py

import sys
import socket
import re
import ssl


def main():
    try:
        URL = sys.argv[1].strip()
        # print('URL Entered: ' + URL)
        match = parseURL(URL)
        PROTOCOL, HOST, ENDPOINT, PORT = assignRequestParameters(match)
        data, supportHTTP2, passProtected = sendRequest(PROTOCOL, HOST, ENDPOINT, PORT)
        print('-----Response Header-----')
        if data:
            for key,value in data.items():
                print(key + ': '+ value)
        print('-----Response End-----')
        print('-----Report Start-----')
        print('website: ' + PROTOCOL.lower() + '://' + HOST)
        if supportHTTP2:
            print('HTTP2 supported')
        else:
            print('HTTP2 not supported')
        if passProtected:
            print('Password Protected')
        else:
            print('Not Password Protected')
        parseCookies(data, HOST)
        print('-----Report End-----')
    except Exception as e:
        print(e)

    

def sendRequest(PROTOCOL, HOST, ENDPOINT, PORT):
    context = ssl.create_default_context()
    context.set_alpn_protocols(['http/1.1', 'h2'])

    data = {}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if PROTOCOL == 'HTTPS':
            s = context.wrap_socket(s, server_hostname=HOST)
        s.connect((HOST, PORT))
        s.sendall(b'GET ' + bytes(ENDPOINT, 'utf-8') + b' HTTP/1.1\r\nHost: ' + bytes(HOST, 'utf-8') + b'\r\nConnection: close\r\nAccept: text/html\r\n\r\n')

        response = b''
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

        data = parseResp(response)
        if PROTOCOL == 'HTTPS':
            supportHTTP2 = s.selected_alpn_protocol() == 'h2'
        else:
            supportHTTP2 = False
        passProtected = data.get('HTTP/1.1') == '401 Unauthorized' and 'WWW-Authenticate' in data
        # Check for redirection
        if data.get('HTTP/1.1') in ('302 Moved Temporarily', '301 Moved Permanently'):
            location = data.get('Location')
            match = parseURL(location)
            PROTOCOL, HOST, ENDPOINT, PORT = assignRequestParameters(match)
            return sendRequest(PROTOCOL, HOST, ENDPOINT, PORT)

    return data, supportHTTP2, passProtected

def parseResp(data):
    data = data.decode(errors='ignore')
    header, _, body = data.partition('\r\n\r\n')
    list = header.split('\r\n')
    d = {}

    httpVer, _, status = list[0].partition(' ')
    d[httpVer] = status
    d2 = dict(re.split(r'[:]', each, 1) for each in list[1:] if each !='')
    d2 = {k.lstrip():v.lstrip() for (k, v) in d2.items()}
    d.update(d2)
    bodysize = 1000
    if len(body) > bodysize:
        body = body[:bodysize] + '\n...[Truncated]'
        print('-----Truncated Body Start-----')
        print(body + '\n')
        print('-----Truncated Body End-----')
    return d

def parseURL(input):
    pattern = re.compile(r'((https|http)://)?([a-zA-Z.-]+)([/\w]*.?[\w]*):?(\d*)', re.IGNORECASE)
    return pattern.match(input)

def assignRequestParameters(match):
    if match.group(2) is not None and not '':
        PROTOCOL = match.group(2).upper()
    else:
        PROTOCOL = 'HTTP'
    HOST = match.group(3)
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
    print('-----Request Header-----')
    print('GET ' + PROTOCOL.lower() + '://' + HOST + ENDPOINT + ' ' + PROTOCOL + '/1.1')
    print('Host: ' + HOST)
    print('Connection: close')
    print('-----Request End-----')
    return PROTOCOL, HOST, ENDPOINT, PORT

def parseCookies(data, HOST):
    cookies = [value for key, value in data.items() if key.lower() == 'set-cookie']

    if cookies:
        print('-----Cookies-----')
        for cookie in cookies:
            components = cookie.split(";")
            name, value = components[0].split("=", 1)
            print('cookie name: ' + name.strip() + ', domain name: ' + HOST)

            for comp in components[1:]:
                comp = comp.strip()
                if 'expires' in comp.lower():
                    expires = comp.split("=")[1].strip()
                    print('cookie name: ' + name.strip() + ', expires time: ' + expires + '; domain name: ' + HOST)
                elif 'domain' in comp.lower():
                    domain = comp.split("=")[1].strip()
                    print('cookie name: ' + name.strip() + ', domain name: ' + domain)
        print('-----Cookies End-----')


if __name__ == '__main__':
    main()