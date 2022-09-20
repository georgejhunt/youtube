#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Short -- picks videoIds fri youtube URLs 

infile = 'mathszone.csv'
with open(infile,'r') as fp:
    for line in fp.readlines():
        start =line.find('watch?v=')
        if start != -1:
            line = (line[start+8:])
            end = line.find('&list')
            print(line[:end])
