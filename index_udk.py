#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 12:21:02 2019

@author: dan
"""
from utilites import load, dump
from rutermextract import TermExtractor as TE
from sys import stderr

to_del = set()
udk = load('udk.json')

for code, value in [ (k, udk[k]['text']) for k in udk.keys() ]:
    if value:
        terms = [ t.normalized for t in TE()(value)]
        data = udk[code]
        data.update({'terms':terms})
        udk.update({code:data})
        print(code, terms, file = stderr)
    else:
        to_del |= {code}

for code in to_del:
    udk.pop(code)
    
dump(udk, 'indexed.udk.json')
