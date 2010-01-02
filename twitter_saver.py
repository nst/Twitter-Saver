#!/usr/bin/python

# Nicolas Seriot
# 2010-01-01
# http://github.com/nst/Twitter-Saver

import sys
import urllib2
import json

def install_authentication_handler(url, login, password):
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, url, login, password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)

def user_statuses_count(username):
    theurl = 'http://twitter.com/users/show.json?screen_name=%s' % username
    try:
        lines = urllib2.urlopen(theurl).readlines()
    except Exception, e:
        print e
        return 0
    
    return int(json.loads(''.join(lines))['statuses_count'])

def user_timeline_statuses(username, page=1):
    theurl = 'http://twitter.com/statuses/user_timeline/%s.json?count=200&page=%d' % (username, page)
    try:
        lines = urllib2.urlopen(theurl).readlines()
    except Exception, e:
        print e
        return []
        
    return json.loads(''.join(lines))

def print_statuses(username):
    count = user_statuses_count(username)
    div, mod = divmod(count, 200)
    pages = div + (1 if mod else 0)

    for page in range(1, pages+1):
        statuses = user_timeline_statuses(username, page)
        if not statuses:
            break
        for d in statuses:
            print unicode("%(id)s\t%(created_at)s\t%(text)s" % d).encode('utf-8')

if len(sys.argv) not in [2, 4]:
    print "USAGE: %s <username> [<login> <password>]" % sys.argv[0]
    sys.exit(1)

username = sys.argv[1]
login = sys.argv[2] if len(sys.argv) == 4 else None
password = sys.argv[3] if len(sys.argv) == 4 else None

if login and password:
    install_authentication_handler('http://twitter.com/statuses', login, password)

print_statuses(username)
