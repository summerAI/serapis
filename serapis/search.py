#!/usr/bin/env python
# coding=utf-8
"""
Search module
"""
from __future__ import unicode_literals
from __future__ import absolute_import

__author__ = "Manuel Ebert"
__copyright__ = "Copyright 2015, summer.ai"
__date__ = "2015-11-20"
__email__ = "manuel@summer.ai"

import requests
from dateutil.parser import parse as parse_date
from .config import config  # Make sure to use absolute imports here


def search_diffbot_cache(word):
    response = requests.get('http://api.diffbot.com/v3/search', params={
        'token': config.credentials['diffbot'],
        'query': requests.utils.quote('"{}"'.format(word)),
        'col': 'GLOBAL-INDEX'
    }).json()
    if not response.get('objects'):
        if response.get('error'):
            print("Response Error '{}' (code: {})".format(response['error'], response['errorCode']))
        else:
            print("NO RESULTS")
    results = []
    for object in response.get('objects', []):
        if object.get('text'):
            result = {
                "title": object.get('title'),
                "url": object.get('pageUrl'),
                "author": object.get('author'),
                "date": parse_date(object.get('date', '')).isoformat(),
                "doc": object.get('text')
            }
            results.append(result)
    return results


def search_duckduckgo(term):
    result = []
    try:
        req = requests.get('http://api.duckduckgo.com/?q={}&format=json'.format(term)).json()
    except:
        return result
    if req['AbstractSource'] not in config.duckduckgo_sources:
        return result
    if req.get('Abstract'):
        result.append({
            'title': req['Heading'],
            'url': req['AbstractURL'],
            'author': None,
            'date': None,
            'source': req['AbstractSource'],
            'doc': req['Abstract']
        })
    if req.get('Definition'):
        result.append({
            'title': req['Heading'],
            'url': req['DefinitionURL'],
            'source': req['DefinitionSource'],
            'author': None,
            'date': None,
            'doc': req['Definition']
        })
    return result
