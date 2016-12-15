#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from lxml import etree


class esRss:
    '''
    RSS generator class by Evgeniy Shumilov <evgeniy.shumilov@gmail.com>
    '''
    def __init__(self, title, link='', description='', language='ru', copyright='', image_url='', image_title='',
                 image_link='', managingEditor='', lastBuildDate='', encoding='UTF-8'):
        self.rss = etree.Element('rss')
        self.rss.set('version', '2.0')
        self.channel = etree.Element('channel')
        etree.SubElement(self.channel, 'title').text = title
        if link:
            etree.SubElement(self.channel, 'link').text = link
        else:
            self.__err__('Feed should contain link')
        if description:
            etree.SubElement(self.channel, 'description').text = description
        else:
            self.__err__('Feed should contain description')
        if image_url:
            img = etree.Element('image')
            etree.SubElement(img, 'url').text = image_url
            if image_title:
                etree.SubElement(img, 'title').text = image_title
            if image_link:
                etree.SubElement(img, 'link').text = image_link
            self.channel.append(img)
        if language:
            etree.SubElement(self.channel, 'language').text = language
        if copyright:
            etree.SubElement(self.channel, 'copyright').text = copyright
        if managingEditor:
            etree.SubElement(self.channel, 'managingEditor').text = managingEditor
        if lastBuildDate:
            etree.SubElement(self.channel, 'lastBuildDate').text = lastBuildDate
        if encoding:
            self.prefix = '<?xml version="1.0" encoding="' + encoding + '" ?>'
        else:
            self.prefix = '<?xml version="1.0"?>'
        self.items = []

    def __err__(self, message='', code=0):
        if message:
            sys.stderr.write(message + '\n')
        if code:
            sys.exit(code)

    def __paramItem__(self, title, source, params={}):
        if title:
            item = etree.Element(title)
            if source:
                item.text = source
            for p in params.keys():
                if params[p]:
                    item.set(p, params[p])
            return item
        else:
            self.__err__('Parametred item should contain at least title')
            return None

    def addItem(self, title='', description='', link='', author='', category='', category_domain='', comments='',
                enclosure_url='', enclosure_length='', enclosure_type='', guid='', guid_isPermaLink='',
                pubDate='', source_url='', source_src=''):
        item = etree.Element('item')
        if title and description:
            if title:
                etree.SubElement(item, 'title').text = title
            if description:
                etree.SubElement(item, 'description').text = description
            if link:
                etree.SubElement(item, 'link').text = link
            if author:
                etree.SubElement(item, 'author').text = author
            if comments:
                etree.SubElement(item, 'comments').text = comments
            if pubDate:
                etree.SubElement(item, 'pubDate').text = pubDate
            if enclosure_url:
                enc = self.__paramItem__('enclosure', '', {'url': enclosure_url, 'length': enclosure_length,
                                         'type': enclosure_type})
                if enc != None:
                    item.append(enc)
            if category:
                cat = self.__paramItem__('category', category, {'domain': category_domain})
                if cat != None:
                    item.append(cat)
            if guid:
                gid = self.__paramItem__('guid', guid, {'isPermaLink': guid_isPermaLink})
                if gid != None:
                    item.append(gid)
            if source_url:
                src = self.__paramItem__('source', source_src, {'url': source_url})
                if src != None:
                    item.append(src)
            self.items.append(item)
        else:
            self.__err__('Item should contain title or description')

    def Feed(self):
        if self.items:
            for i in self.items:
                self.channel.append(i)
            self.rss.append(self.channel)
        return self.prefix + '\n' + etree.tostring(self.rss, pretty_print=True)

