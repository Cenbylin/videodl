#!/usr/local/bin/python
# encoding: utf-8
'''
@author: Cenbylin
'''
import json
if __name__ == '__main__':
    str = '[{"a":1},{"b":2}]'
    print type(json.loads(str)[0])
