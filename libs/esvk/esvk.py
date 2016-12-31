#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple wrapper around vk.com api for getting items from open walls by Evgeniy Shumilov <evgeniy.shumilov@gmail.com>
Requirements: requests, json
"""

import os
import re
import sys
import json
import requests


class esVKWall:

    def __init__(self, api='5.60', uagent='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'):
        self.s = requests.Session()
        self.s.headers['User-Agent'] = uagent
        self.api = api
        self.baseurl = 'https://api.vk.com/method/'
        self.uname = ''
        self.passwd = ''
        cpath = os.path.join(os.curdir, 'esvk.conf')
        if os.path.isfile(cpath):
            with open(cpath) as f:
                for l in f.readlines():
                    k = l.split('=')[0].replace('"', '').strip()
                    if k == 'uname':
                        self.uname = '='.join(l.split('=')[1:]).replace('"', '').replace("'", '').strip()
                    if k == 'passwd':
                        self.__pwd = '='.join(l.split('=')[1:]).replace('"', '').replace("'", '').strip()

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
            gid = group['id']
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
            if obj.has_key('sizes'):
                for s in obj['sizes']:
                    psize = s['height'] * s['width']
                    if photosize <= psize:
                        photo = s['src']
                        photosize = psize
            else:
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

    def getAudio(self, owner_id, audio_id):
        """
        Method to get audio urls from vk
        :param audio: array of strings or string like as 'ownerid_id'
        :return: dict of records like 'ownerid_id': 'audiourl'
        """
        if owner_id and audio_id and self.uname and self.__pwd:
            r = self.s.get('https://m.vk.com/')
            authurl = re.findall('form method="post" action="(.*)"', r.content)[0]
            data = {'email': self.uname, 'pass': self.__pwd}
            r = self.s.post(authurl, data)
            if r.content.find('<span class="mm_label">') != -1:
                data = {'act': 'reload_audio', 'al': 1, 'ids': '%s_%s' % (str(owner_id), str(audio_id))}
                r = self.s.post('https://vk.com/al_audio.php', data)
                res = r.content[r.content.find('https:'):r.content.find('?')].replace('\\/', '/')
                return res
            else:
                return ''
        else:
            return ''
