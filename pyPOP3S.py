# -*- coding: utf-8 -*-

import email.parser
import getpass
import socket
import ssl
import poplib
import sys

def main():
    argv = sys.argv
    argc = len(argv)

    if argc < 3:
        print("Usage: python {0} <pop3s server> <port number | service name>".format(argv[0]))
        return

    hostname = argv[1]

    if argv[2].isnumeric():
        portnum = int(argv[2])
    else:
        portnum = socket.getservbyname(argv[2])

    if argc > 3:
        username = argv[3]
    else:
        username = input("username: ")

    if argc > 4:
        passwd = argv[4]
    else:
        passwd = getpass.getpass("Password: ")

    pop3s(hostname, portnum, username, passwd)

def pop3s(hostname, portnum, username, passwd):
    if portnum == 110:
        pop3 = poplib.POP3(hostname, port=portnum)
    elif portnum == 995:
        pop3 = poplib.POP3_SSL(hostname, port=portnum)
    else:
        print("Could not determine if it is \"POP3\" or \"POP3 over SSL/TLS\"")
        return

    if "+OK" not in str(pop3.getwelcome()):
        print("connect failed.")
        return

    print("connected to {0}:{1:d}".format(hostname, portnum))

    """
    send user.
    """
    try:
        res_user = pop3.user(username)
    except:
        print("command \"user\" failed.")
        return
    print(res_user.decode(encoding="ascii"))

    """
    send pass.
    """
    try:
        res_pass = pop3.pass_(passwd)
    except:
        print("command \"pass\" failed.")
        return
    print(res_pass.decode(encoding="ascii"))

    """
    get list.
    """
    try:
        res_list = pop3.list()
    except:
        print("command \"list\" failed.")
        return

    """
    get all mail subject.
    """
    headers = [pop3.top(i + 1, 0) for i in range(len(res_list[1]))]
    title = [get_date_and_subject(headers[i][1]) for i in range(len(res_list[1]))]
    
    print_date_and_subject(title)

    """
    print select menu
    """
    while True:
        print("select[{0:d}-{1:d}](0...list, -1 or char ...exit) : ".format(1, len(headers)), end="")
        workStr = input()

        if workStr == "":
            # do nothing to stay connect.
            pop3.noop()

        try:
            n = int(workStr)
        except:
            break

        if n < 0:
            break
        elif n == 0:
            # do nothing to stay connect.
            pop3.noop()

            # print subject list.
            print_date_and_subject(title)
        elif 1 <= n and n <= len(headers):
            # get message.
            content = pop3.retr(n)

            # print message.
            print(get_content(content[1]))

    """
    quit
    """
    try:
        pop3.quit()
    except:
        print("pop3.quit() error.")
        return
    print("quit.")

def get_date_and_subject(header):
    fp = email.parser.BytesFeedParser()
    [fp.feed(x + b'\r\n') for x in header]
    msg = fp.close()
    return (msg['Date'], str(email.header.make_header(email.header.decode_header(msg['subject']))))

def print_date_and_subject(title):
    for i in range(len(title)):
        print("{0:4d}: {1:40s} {2}".format(i + 1, title[i][0], title[i][1]))

def get_content(content):
    msg = email.message_from_bytes(b'\r\n'.join(content))
    charset = msg.get_content_charset()
    payload = msg.get_payload(decode=True)
    try:
        if payload:
            if charset:
                return payload.decode(charset)
            else:
                return payload.decode()
        else:
            # "payload not found."
            return msg._payload[-1]._payload
    except:
        # if it cannot be decoded.
        return msg._payload[-1]._payload

if __name__ == "__main__":
    main()
