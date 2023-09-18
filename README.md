Pass URL query to application through stdin like so:
`./SmartClient.py www.hostname.com` -  while in this dir
Accepted URL formats are:
`PROTOCOL://www.HOSTNAME.com:PORT` or `www.HOSTNAME.com:PORT` or `PROTOCOL://www.HOSTNAME.com` or `PROTOCOL://www.HOSTNAME.com`
If PROTOCOL not provided defaults to HTTP and if PORT not provided defaults to 80.
Additional arguments will be ignored.
You may need to update perm on file with:
`sudo u+x SmartClient.py` in order the run the file.