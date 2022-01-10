#!/usr/bin/env python
import sys
import json
import requests
import re

############### You should change the following two lines first ###############
headers = {'Authorization': 'Bearer <your_access_token_here>'}
# (e.g.) headers = {'Authorization': 'Bearer AbcDEFg1HIJk2L3M4NopqRST5uvwx6yZAbCde7f8gHi'}
domain = '<your_domain_here>'
# (e.g.) domain = 'https://mastodon.social'
###############################################################################

save_frequence = 30
file_name = 'notifications.json'
url = domain + '/api/v1/notifications'
argv = ''
since_id = 0
new_list = []
if len(sys.argv) == 2:
    if sys.argv[1] == '--continue':
        argv = 'c'
    elif sys.argv[1] == '--update':
        argv = 'u'

def deal_with_data(data, i, t, a, u, s, c):
    if s in data['url_content_pair']:
        pass
    else:
        data['url_content_pair'][s] = c
    new_list.append([i, t, a, u, s])

def read_file():
    if argv != '':
        with open(file_name, 'r') as rf:
            data = json.load(rf)
            if argv == 'c':
                max_id = data['notifications_list'][-1][0]
                global url
                url = domain + '/api/v1/notifications?max_id=' + str(max_id)
            elif argv == 'u':
                global since_id
                since_id = data['notifications_list'][0][0]
    else:
        data = {
                'notifications_list':[],
                'url_content_pair':{}
                }
    return data

def write_file(data):
    with open(file_name, 'w') as rf:
        if argv == 'u':
            data['notifications_list'][0:0] = new_list
        else:
            data['notifications_list'].extend(new_list)
        json.dump(data, rf, ensure_ascii=False, indent=2)
    new_list.clear()
    print('    Write in.')

data = read_file()
p = 1    # page count
while 1:
    nr = requests.get(url, headers = headers)
    if nr.status_code == 429:
        reset = nr.headers['x-ratelimit-reset']
        print('You run out the rate limits, which will be reset at ' + reset)
        print('After that, you can run: python export.py --continue')
        break
    nj = nr.json()
    q = 0    # item count in this page
    for e in nj:
        i = e['id']
        if i <= since_id:
            p = 0    # used for break outsider
            break
        t = e['type']
        a = e['created_at']
        u = e['account']['acct']
        if t[:6] == 'follow':    # type follow or follow_request has no status
            s = '-'
            c = '-'
        else:
            s = e['status']['url']
            c = e['status']['content']
        deal_with_data(data, i, t, a, u, s, c)
        q = q + 1
    print('Page ' + str(p) + ', ' + str(q) + ' notifications.', end=" ")
    if ('Link' in nr.headers) and ('rel="next"' in nr.headers['Link']):
        if p == 0:
            print('Updated.')
            break
        next_url = re.match(r"\<(.*?)\>", nr.headers['Link']).groups()[0]
        url = next_url
        print('Next url: ' + url)
        if p % save_frequence == 0:
            write_file(data)
        p = p + 1
    else:
        print('Done.')
        break

write_file(data)

