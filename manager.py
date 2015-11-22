__author__ = 'michele'

import requests
import json
from crypto import AESCipher
import sys
import hashlib

slack_token_ciphred = 'OpFOMmWwXimjfckCzwGuES/xpZpp9UAASuHlCaXFqAlf/Vd2Nwu1AzqUNSnvGdHht2Q15TVDEW12NdnORhsatzvSZFdvHUIFv3b5+gO/iPg='
    # 'xoxp-14631819508-14631819700-15093267796-44ec2395f4'

base_url = 'https://slack.com/api/'

method_auth_test = 'auth.test'
method_channel_list = 'channels.list'
method_groups_list = 'groups.list'
method_im_list = 'im.list'
method_chat_delete = 'chat.delete'

slack_token = ''

def _token():
    return '?token=' + slack_token


def get_base_info():
    response = requests.get(base_url + method_auth_test + '?token=' + slack_token)
    return json.loads(response.content)


def get_channel_list(exclude_archieved=False):
    if exclude_archieved:
        exclude_archieved_param = '&exclude_archieved=1'
    else:
        exclude_archieved_param = '&exclude_archieved=0'
    response = requests.get(base_url + method_channel_list + _token() + exclude_archieved_param)

    return json.loads(response.content).get('channels')


def get_groups_list(exclude_archieved=False):
    if exclude_archieved:
        exclude_archieved_param = '&exclude_archieved=1'
    else:
        exclude_archieved_param = '&exclude_archieved=0'
    response = requests.get(base_url + method_groups_list + _token() + exclude_archieved_param)

    return json.loads(response.content).get('groups')


def get_im_list():
    response = requests.get(base_url + method_im_list + _token())
    return json.loads(response.content).get('ims')


def delete_message(ts, channel):
    ts_argument = '&ts=' + ts
    channel_argument = '&channel=' + channel
    response = requests.get(base_url + method_chat_delete + _token() + ts_argument + channel_argument)


def _get_history(chat_type, channel, lastest=None, oldest=None, count=100, include_unreads=True):
    channel_arg = '&channel=' + channel
    lastest_arg = ('&lastest=' + lastest) if lastest else ''
    oldest_arg = ('&oldtest=' + oldest) if oldest else ''
    count_arg = '&count=' + str(count)
    include_unreads_arg = '&unreads=1' if include_unreads else ''

    response = requests.get(base_url + chat_type + '.history' + _token() + channel_arg + lastest_arg + oldest_arg +
                            count_arg + include_unreads_arg)

    response_dict = json.loads(response.content)
    return response_dict.get('messages'), response_dict.get('has_more')


def delete_all_channel_messages(channel_type, channel):
    delete_all = lambda x: delete_message(x.get('ts'), channel)

    messages, has_more = _get_history(channel_type, channel)

    map(delete_all, messages)
    while has_more:
        messages, has_more = _get_history(channel_type, channel)
        map(delete_all, messages)


if __name__ == "__main__":

    key = hashlib.md5(sys.argv[1]).hexdigest()

    slack_token = AESCipher(key).decrypt(slack_token_ciphred)

    base_info = get_base_info()

    channels_list = get_channel_list()
    groups_list = get_groups_list()
    ims_list = get_im_list()

    first_channel_id = channels_list[0].get('id')

    history, has_more = _get_history('channels', first_channel_id, count=10)

    print base_info