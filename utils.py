#!/usr/bin/env python

from config import config
import smtplib

def sendAlertEmail(errors):
    username = config['gmail']['username']
    password = config['gmail']['password']
    msg = "Subject: [ALERT] %s\n\n%s\n\n%s" % (errors[0], "\n".join(errors), config['gmail']['site_url'])
    fromaddr = config['gmail']['from_address']
    toaddrs = config['gmail']['to_addresses']

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()