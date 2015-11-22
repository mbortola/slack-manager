__author__ = 'michele'

import requests
import json

slack_token = 'xoxp-14631819508-14631819700-15093267796-44ec2395f4'

base_url ='https://slack.com/api/'


method_auth_test = 'auth.test'
method_channel_list='channels.list'
method_groups_list='groups.list'
method_im_list='im.list'

def _token():
    return '?token='+slack_token

def get_base_info():
    response=requests.get(base_url+method_auth_test+'?token='+slack_token)
    return json.loads(response.content)

def get_channel_list(exclude_archieved=False):
    if exclude_archieved:
        exclude_archieved_param='&exclude_archieved=1'
    else:
        exclude_archieved_param='&exclude_archieved=0'
    response = requests.get(base_url+method_channel_list+_token()+exclude_archieved_param)

    return json.loads(response.content).get('channels')

def get_groups_list(exclude_archieved=False):
    if exclude_archieved:
        exclude_archieved_param='&exclude_archieved=1'
    else:
        exclude_archieved_param='&exclude_archieved=0'
    response = requests.get(base_url+method_groups_list+_token()+exclude_archieved_param)

    return json.loads(response.content).get('groups')

def get_im_list():
    response = requests.get(base_url+method_im_list+_token())
    return json.loads(response.content).get('ims')

if __name__ == "__main__":
    base_info=get_base_info()

    channels_list= get_channel_list()
    groups_list = get_groups_list()
    ims_list = get_im_list()

    print base_info