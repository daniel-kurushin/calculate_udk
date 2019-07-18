#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:22:18 2019

@author: dan
"""
import re


from bs4 import BeautifulSoup as BS
from requests import get
from requests.models import MissingSchema
from utilites import dump

from sys import stderr

udk = {}
parsed = set([])

def parse_udk(url, udk, parsed):
    
    def get_base_url(url):
        try:
            fname = url.split('/')[-1]
            return re.sub(fname, '', url)
        except IndexError:
            return url
    
    try:
        assert url not in parsed, (0, 'URL is parsed')
        parsed |= {url}
        
        base = get_base_url(url)
        
        teacode = BS(get(url).content, "lxml")
        assert teacode.find('h1').string.count('404') == 0, (404, 'Page not foud')
        x = teacode.find('tr')
        
        while 1:
            try:
                x = x.nextSibling
            except AttributeError:
                print(url, teacode, file = stderr)
                break
            try:
                strings = "".join([ str(a) for a in x.contents])
                if strings.count('table') > 0:
                    break
            except AttributeError:
                pass
            
        table = x.find('table')
        
        for tr in table('tr'):
            try:
                proceed = 1
                code, value, _ = [ c for c in tr('td')]
                assert re.match('\d',code.string), (1, 'No code in cell')
                url = base + code.find('a')['href'].strip('.')
            except AssertionError:
                proceed = 0
            except TypeError:
                url = ''
            except ValueError:
                proceed = 0
            except Exception as e:
                print(tr, file = stderr)
                proceed = 0
                raise e
            if proceed:
                udk.update({code.string:{'url':url, 'text':value.string}})
                dump(udk, 'udk.json', quiet=1)
                parse_udk(url, udk, parsed)

    except (AssertionError, MissingSchema) as e:
        print(url, e, file = stderr)
        pass
    
if __name__ == '__main__':
    parse_udk('https://www.teacode.com/online/udc/', udk, parsed)
#    parse_udk('https://www.teacode.com/online/udc/57/576.53.html', udk, parsed)
