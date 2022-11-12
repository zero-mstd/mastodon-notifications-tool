#!/usr/bin/env python

import json
import itertools

file = 'notifications.json'

with open(file, 'r') as old_file:
    old_data = json.load(old_file)
    old_noti = old_data['notifications_list']
    old_pair = old_data['url_content_pair']

old_noti.sort(key = lambda x: int(x[0]), reverse = True)
new_noti = list(k for k,_ in itertools.groupby(old_noti))

new_data = {
    'notifications_list': new_noti,
    'url_content_pair': old_pair
    }

with open (file, 'w') as new_file:
    json.dump(new_data, new_file, ensure_ascii=False, indent=2)
