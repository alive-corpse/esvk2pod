#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import base64
import requests

class esVKWall:
    def __init__(self, api='5.60', uagent='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'):
        self.s = requests.Session()
        self.s.headers['User-Agent'] = uagent
        self.api = api
        self.baseurl = 'https://api.vk.com/method/'

    def getGroup(self, gname):
        if gname:
            raw = self.s.get(self.baseurl + 'groups.getById?v=' + self.api + '&fields=description&group_ids=' + gname)
            group = json.loads(raw.text)
            return group['response'][0]
        else:
            return None

    def getWall(self, gname, count=20, offset=0):
        if gname:
            group = self.getGroup(gname)
            gid = group['gid']
            raw = self.s.get(self.baseurl + 'wall.get?v=' + self.api + '&owner_id=-' + str(gid) + '&count=' +
                             str(count) + '&offset=' + str(offset))
            wall = json.loads(raw.text)
            return wall
        else:
            return None

    def getBiggestPhoto(self, obj, wrap=False):
        if obj:
            photo = ''
            photosize = 0
            for p in obj.keys():
                if p.startswith('photo_') or p.startswith('src_'):
                    psize = p.split('_')[1]
                    if psize.endswith('small') or psize.endswith('medium') or psize.endswith('big'):
                        if psize == 'small':
                            psize = 1
                        elif psize == 'medium':
                            psize = 2
                        elif psize == 'big':
                            psize = 3
                        elif psize.startswith('x'):
                            psize = 3 + len(psize.replace('big', ''))
                        else:
                            psize = -1
                    else:
                        psize = int(psize)
                    if photosize < psize:
                        photo = obj[p]
                        photosize = psize
            if photo and wrap:
                return '<img src="%s">' % photo
            else:
                return photo
        else:
            return ''

    def getAudio(self, audioid, ownerid, token):
        if audioid and ownerid and token:
            raw = self.s.get(self.baseurl + 'audio.getById?v=' + self.api + '&audios=' + str(audioid) + '_'
                             + str(ownerid))
            link = json.loads(raw.text)
            print link
