#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Microservice for making podcast rss feed from vk.com audiogroup's walls
"""

import sys
import base64
from libs.esvk.esvk import esVKWall
from libs.esrss.esrss import esRss
import libs.server.bottle as bottle
import libs.server.wsgiserver as wsgiserver

route = bottle.route
response = bottle.response

if len(sys.argv) >= 3:
    port = int(sys.argv[1])
    host = sys.argv[2]
elif len(sys.argv) == 2:
    port = int(sys.argv[1])
    host = 'localhost'
else:
    port = 8080
    host = 'localhost'

audiopostfix = 'vk2podaudio'
localaudiourl = 'http://%s:%s/%s' % (host, str(port), audiopostfix)

vw = esVKWall()

def wall2Pod(gname, localaudiourl=localaudiourl, count=20, offset=0):
    if gname:
        group = vw.getGroup(gname)
        if group['is_closed'] == 0:
            photo = vw.getBiggestPhoto(group)
            if photo:
                rss = esRss(title=group['name'], link='http://vk.com/' + gname, description=group['description'], image_url=photo)
            else:
                rss = esRss(title=group['name'], link='http://vk.com/' + gname, description=group['description'])
            items = vw.getWall(gname, count, offset)['response']
            if items.has_key('items'):
                items = items['items']
            for i in items:
                if type(i) == dict:
                    if i.has_key('text'):
                        description = i['text']
                    if i.has_key('attachments'):
                        for a in i['attachments']:
                            for c in a.keys():
                                if c == 'photo':
                                    description = vw.getBiggestPhoto(a[c], True) + '<br>' + description
                            for c in a.keys():
                                if c == 'audio':
                                    if i.has_key('from_id'):
                                        link = 'https://vk.com/wall' + str(i['from_id']) + '_' + str(i['id'])
                                    elif i.has_key('owner_id'):
                                        link = 'https://vk.com/wall' + str(i['owner_id']) + '_' + str(['id'])
                                    else:
                                        link = ''
                                    rss.addItem(title=a[c]['artist'] + ' - ' + a[c]['title'], description=description,
                                                link=link, enclosure_url=localaudiourl + '/' +
                                                base64.b16encode(a[c]['url'].split('?')[0]) + '.mp3',
                                                enclosure_length=str(a[c]['duration']), enclosure_type='audio/mpeg')
            return rss.Feed()
        else:
            print "ERROR: Group is closed"
            return ''

@route('/')
def root():
    return 'Hello!'

@route('/vk2pod/<query>')
@route('/vk2pod/<query>/<count>')
@route('/vk2pod/<query>/<count>/<offset>')
def vk2podq(query='', count=10, offset=0):
    if query:
        response.headers['Content-Type'] = 'xml/application'
        return wall2Pod(query, localaudiourl=localaudiourl, count=count, offset=offset)
    else:
        response.headers['Content-Type'] = 'text/plain'
        return 'Empty request'

@route('/' + audiopostfix + '/<query>')
def audioStream(query=''):
    if query:
        url = base64.b16decode(query[:-4])
        response.headers['Content-Type'] = 'audio/mpeg'
        return vw.s.get(url, stream=True).raw
    else:
        response.headers['Content-Type'] = 'text/plain'
        return 'Empty request'

print 'Server will started on host %s and port %s' % (host, port)

wsgiapp = bottle.default_app()
httpd = wsgiserver.Server(wsgiapp, listen=host, port=port)
httpd.listen = host
httpd.port = port
httpd.serve_forever()