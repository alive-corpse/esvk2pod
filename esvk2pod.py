#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
from libs.esvk.esvk import esVKWall
from libs.esrss.esrss import esRss

def wall2Pod(gname, localurl, count=20, offset=0):
    vw = esVKWall(localurl)
    if gname:
        group = vw.getGroup(gname)
        if group['is_closed'] == 0:
            photo = vw.getBiggestPhoto(group)
            if photo:
                rss = esRss(title=group['name'], link='http://vk.com/' + gname, description=group['description'], image_url=photo)
            else:
                rss = esRss(title=group['name'], link='http://vk.com/' + gname, description=group['description'])
            items = vw.getWall(gname, count, offset)['response']
            for i in items:
                if type(i) != int:
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
                                                link=link, enclosure_url=localurl + '/' + base64.b16encode(a[c]['url'].split('?')[0])
                                                + '.mp3', enclosure_length=str(a[c]['duration']), enclosure_type='audio/mpeg')
            return rss.Feed()
        else:
            print "ERROR: Group is closed"
            return ''

#wall2Pod('metal_world', 3, 5)
print wall2Pod('free_audiobooks', 'http://shumiloff.ru/vk2rss', 5, 2)