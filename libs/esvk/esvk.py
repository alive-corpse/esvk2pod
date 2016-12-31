#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple wrapper around vk.com api for getting items from open walls by Evgeniy Shumilov <evgeniy.shumilov@gmail.com>
Requirements: requests, json
"""

import json
import urllib2
from httplib import HTTPConnection
import requests


class esVKWall:
    user = ''
    __pwd = ''
    token = ''
    authurl = 'https://oauth.vk.com/authorize?client_id=%s&scope=%s&display=mobile&v=5.3&response_type=token'
    scopes = 'audio'

    def __init__(self, api='5.60', uagent='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
                 appid='', appsecret=''):
        self.api = api
        self.baseurl = 'https://api.vk.com/method/'
        self.uagent = uagent
        self.headers = headers = {'User-Agent': uagent}
        if appid and appsecret:
            self.appid = appid
            self.appsecret = appsecret

    def auth(self, uname, passwd):
        """
        Authentication method for vkontakte
        :param uname: Email or phone number of user
        :param passwd: password for authorisation
        :return: session token
        """
        import re
        if uname and passwd:
            s = requests.session()
        r = self.getContent(self.authurl % (self.appid, self.scopes))
        authurl = re.findall('action="(.*?)"', r.content.replace('\n', ''))[0]
        fields = re.findall('<input .*?name="(.*?)".*?value="(.*?)"', r.content.replace('\n', ''))
        payload = {}
        for f in fields:
            payload[f[0]] = f[1]
        payload['email'] = uname
        payload['pass'] = passwd
        r = s.post(authurl, payload)
        if r.url.find('access_token') == -1:
            authurl = re.findall('action="(.*?)"', r.content.replace('\n', ''))
        self.r2 = r = s.post(authurl)
        self.res = res = re.findall('access_token=(.*?)&expires_in=([0-9]*)&user_id=([0-9]*)', r.url)[0]
        self.token = res[0]
        self.expires = res[1]
        self.user_id = res[2]
        self.v = vkontakte.API(api_id=self.appid, api_secret=self.appsecret, token=self.token)
        return self.token
        else:
        sys.exit("Username and email should not be empty")

    def login(self):
        """
        Login procedure
        :return: session token
        """
        import sys, getpass
        sys.stdout.write('E-mail or phone number: ')
        self.user = sys.stdin.readline().replace('\n', '')
        self.__pwd = getpass.getpass('Password: ')
        return self.auth(self.user, self.__pwd)

    def getContent(self, url, headers=None):
        if url:
            if headers:
                if 'User-Agent' not in headers.keys():
                    headers['User-Agent'] = self.headers['User-Agent']
            else:
                headers = self.headers
            return urllib2.urlopen(urllib2.Request(url, None, headers)).read()

    def getHeaders(self, url, headers=None):
        if url:
            if headers:
                if 'User-Agent' not in headers.keys():
                    headers['User-Agent'] = self.headers['User-Agent']
            else:
                headers = self.headers
            request = urllib2.Request(url=url, headers=headers)
            request.get_method = lambda: 'HEAD'
            response = urllib2.urlopen(request).info()
            return response

    def getGroup(self, gname):
        if gname:
            resp = self.getContent(self.baseurl + 'groups.getById?v=' + self.api +
                                '&fields=description&group_ids=' + gname)
            return json.loads(resp)['response'][0]

    def getWall(self, gname, count=20, offset=0):
        if gname:
            group = self.getGroup(gname)
            gid = group['id']
            return json.loads(self.getContent(self.baseurl + 'wall.get?v=' + self.api + '&owner_id=-' + str(gid) +
                                              '&count=' + str(count) + '&offset=' + str(offset)))

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

    # def getAudio(self, audioid, ownerid, token):
    #     if audioid and ownerid and token:
    #         raw = self.s.get(self.baseurl + 'audio.getById?v=' + self.api + '&audios=' + str(audioid) + '_'
    #                          + str(ownerid))
    #         link = json.loads(raw.text)
    #         print link
