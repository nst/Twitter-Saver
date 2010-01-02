#!/usr/bin/python

# Nicolas Seriot
# 2010-01-01
# http://github.com/nst/Twitter-Saver

import sys
import urllib2
import json

def user_readable_statuses_count(username):
    theurl = 'http://twitter.com/users/show.json?screen_name=%s' % username
    try:
        lines = urllib2.urlopen(theurl).readlines()
    except Exception, e:
        print e
    
    d = json.loads(''.join(lines))
    
    if d['protected']:
        return 0
    
    return int(d['statuses_count'])

def user_timeline_statuses(username, page=1):
    theurl = 'http://twitter.com/statuses/user_timeline/%s.json?count=200&page=%d' % (username, page)
    try:
        lines = urllib2.urlopen(theurl).readlines()
    except Exception, e:
        print e
        return []
        
    return json.loads(''.join(lines))

def print_statuses(username):
    count = user_readable_statuses_count(username)
    div, mod = divmod(count, 200)
    pages = div + (1 if mod else 0)

    for page in range(1, pages+1):
        for d in user_timeline_statuses(username, page):
            print unicode("%(id)s\t%(created_at)s\t%(text)s" % d).encode('utf-8')

if len(sys.argv) != 2:
    print "USAGE: %s <username>" % sys.argv[0]
    sys.exit(1)

print_statuses(sys.argv[1])
