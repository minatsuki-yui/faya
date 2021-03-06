#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
import os
import random
import re
import main_lib.simple as lib
from core import db, enc, sock, sender
from core.Fconf import config

_registered_actions = {}

faya_db = db.name('faya_dict')
faya_db_b = db.name('faya_dict_b')


def action(name):
    def decorator(f):
        _registered_actions[name] = f
        return f

    return decorator


@action("faya")
def faya(data):
    if data == 'ver':
        ver = config.ver
        return f'版本为 {ver}'
    elif data == 'love':
        return 'Love~'
    elif not data:
        return ['在', '你好呀', '( ´▽｀)'][random.randint(0, 2)]


# learn


@action("learn")
def learn(data, nickname):
    faya_dict = faya_db.get()

    if nickname != 'master':
        return '目前只有wy有权限教我。'
    else:
        yltl = data.split(':', 1)
        if len(yltl) != 2:
            return 'wy你是蠢么'
        else:
            faya_dict[yltl[0]] = yltl[1]
            faya_db.set(faya_dict)
            return '学会了！(ง •̀_•́)ง '


@action("us")
def phon(data):
    return yd.get_phon(data, 'us')


@action("uk")
def phon(data):
    return yd.get_phon(data, 'uk')


@action("?")
def dummy(data):
    if data:
        return yd.get_ydword(data)


# @action("+")
# def phon(data):
#    json_add('words.json', round(datetime.timestamp(datetime.now())), [data, 0])
#    return f'已添加{data}'


@action("unlearn")
def popmark(data):
    faya_dict = faya_db.get()

    if data not in faya_dict:
        return '教过我了 你是蠢么'
    else:
        faya_dict.pop(data)
        faya_db.set(faya_dict)
        return '已忘记。'


# blur learn


@action("blearn")
def learn(data):
    faya_dict = faya_db_b.get()

    yltl = data.split(':', 1)
    if len(yltl) != 2:
        return 'wy你是蠢么'
    else:
        faya_dict[yltl[0]] = yltl[1]
        faya_db_b.set(faya_dict)
        return '学会了！(ง •̀_•́)ง '


@action("unblearn")
def popmark(data):
    blur = faya_db_b.get()

    if data not in blur:
        return 'wy你是蠢么'
    else:
        blur.pop(data)
        faya_db_b.set(blur)
        return '已忘记。'


# len


@action("len")
def show_len(data):
    return str(len(data))


# shijing


@action("poem")
def give_poem():
    poems = db.name('sj').get()
    poem = list(poems)[random.randint(0, len(poems) - 1)]
    return poem + '\n' + poems[poem].replace('。', '。\n').replace('？', '？\n').replace('！', '！\n').replace('；', '；\n')


@action("mzd")
def dummy():
    red = db.name('red').get()
    red.pop('now')
    red_key = list(red)[random.randint(0, len(red) - 1)]
    push = '毛泽东语录: \n\n' + red[red_key]['p']
    if red[red_key]['from']:
        push += '\n   -' + red[red_key]['from']

    return push


# dict


# calculator

@action("cal")
def cal(data):
    cal_reg = re.compile('[\.\+\-\*\(\)\d/]+')
    in_cal = re.findall(cal_reg, data)
    if in_cal:
        if in_cal[0] != data:
            return '输入不合法'
        else:
            try:
                return '计算结果为:' + str(eval(data))
            except SyntaxError:
                return '输入算式有误'


'''
@action("wiki")
def dummy(data):
    if data:
        # import subprocess
        wiki_key = data.replace(' ', '_')
        # s =  subprocess.Popen(f'sudo proxychains4 python3.6 __wiki.py {wiki_key}',stdout=subprocess.PIPE, close_fds=True)
        # stdoutdata, stderrdata = s.communicate()
        import la_eric
        return la_eric.get('?key=' + wiki_key)
 '''


@action("md5")
def dummy(data):
    if data:
        return enc.Cipher().get_md5(data)


# mark


@action("mark")
def mark(data, nickname):
    to_mark = data.split(' ', 1)

    marked = db.name(nickname)

    marked_dict = marked.get()

    if len(to_mark) == 2:
        if to_mark[0] != 'key':

            marked_dict[to_mark[0]] = to_mark[1]

            marked.set(marked_dict)

            return '记住了。' + to_mark[0] + ',' + to_mark[1]

        else:
            return 'key不能作为key'
    elif data == 'key':
        faya_reply = '目前全部key为:'
        for each_key in marked_dict:
            faya_reply += '\n' + each_key
        return faya_reply
    elif data in marked_dict:
        return marked_dict[data]
    else:
        return "格式不对╮(￣▽￣"")╭"


@action("popmark")
def popmark(data, nickname):
    marked = db.name(nickname)

    marked_dict = marked.get()

    if data in marked_dict:
        marked_dict.pop(data)
        marked.set(marked_dict)
        return '已去除。'
    else:
        return '你还没使用此key'


# roll


@action("roll")
def roll_someting(data, nickname):
    if (data == '吃啥') and (nickname == 'haru' or nickname == 'master'):
        rolled = db.name('r_mod').get()
        rolled = rolled[random.randint(0, len(rolled) - 1)]

        reply = '随机推荐：\n' + rolled['name']
        if 'average_cost' in rolled:
            reply += '\n' + rolled['average_cost']
        else:
            reply += '\n人均未知'

            reply += '\n地址：' + rolled['address']

        if 'distance' in rolled:
            reply += '\n距离宿舍约：' + rolled['distance'] + ' ' + rolled['duration']

        return reply
    else:

        return str(random.randint(0, 100))


'''
@action("addroll")
def add_roll(data, nickname):
    if nickname == 'haru' or nickname == 'wy':
        to_add_roll = data.split(' ', 2)

        with open('data/r_mod.json', 'r') as to_roll:
            to_roll_dict = json.loads(to_roll.read())

        if to_add_roll[0] not in to_roll_dict:

            tempo = {'name': to_add_roll[0]}
            id_iput = len(to_add_roll)

            if id_iput > 2:
                tempo['address'] = to_add_roll[2]
            else:
                tempo['address'] = '未知'

            if id_iput > 1:
                tempo['average_cost'] = to_add_roll[1]

            to_roll_dict.append(tempo)

            with open('data/r_mod.json', 'w') as outfile:
                json.dump(to_roll_dict, outfile, ensure_ascii=False)
                outfile.write('\n')
            return '已添加这家店。'
        else:
            return '这家店已在列表里'

@action("poproll")
def pop_roll(data, nickname):
    if nickname == 'haru' or nickname == 'wy':
        asked_key = data
        with open('data/r_mod.json', 'r') as to_roll:
            to_roll_dict = json.loads(to_roll.read())

        for each in to_roll_dict:
            if asked_key == each['name']:
                to_roll_dict.remove(each)
                with open('data/r_mod.json', 'w') as outfile:
                    json.dump(to_roll_dict, outfile, ensure_ascii=False)
                    outfile.write('\n')
                return '已去除这家店。'
            else:
                return '这家店不在列表里'
'''


# wx


@action("wx")
def dummy(data, nickname):
    print(nickname)
    if nickname == 'master':
        try_wx = data.split('.', 1)
        if len(try_wx) == 2:
            return sender.send_wx(try_wx[0], try_wx[1])
        else:
            return 'wx格式有误'
    elif nickname == 'haru':
        try_wx = data.split('.', 1)
        if len(try_wx) == 2:
            if try_wx[0] == 'tf':
                return sender.send_wx(try_wx[0], 'from haru: ' + try_wx[1])
            else:
                return '暂时不能发别人'
        else:
            return 'wx格式有误'


import sys


@action('qq')
def dummy(data, nickname):
    app = sys.argv[0].split('/')[-1][0:-3]
    if app == 'qq':
        return '。。你为什么要这么做'
    else:
        msg = f'from {nickname} {app}：{data}'
        os.system(f'qq send group test群 {msg}')
        return 'faya已转发至群'


@action('line')
def dummy(data, nickname):
    app = sys.argv[0].split('/')[-1][0:-3]
    if app == 'line':
        return '。。你为什么要这么做'
    else:
        msg = f'from {nickname} {app}：{data}'
        sock.send(msg, 'line')
        return 'faya已转发至line'


# ～
'''
@action("syn")
def syn(data, nickname):
    if nickname == 'wy':
        with open('syn.json', 'r', encoding='utf-8') as c:
            conf = json.loads(c.read())

        if data == 'qun':
            if conf['qun'] == True:
                return '向群的转发已经是打开中哦'
            else:
                conf['qun'] = True
                with open('faya_dict.json', 'w') as outfile:
                    json.dump(conf, outfile, ensure_ascii=False)
                    outfile.write('\n')
                return '打开了line转发至群的传送门'
        if data == 'line':
            if conf['line'] == True:
                return '向line的转发已经是打开中哦'
            else:
                conf['line'] = True
                with open('faya_dict.json', 'w') as outfile:
                    json.dump(conf, outfile, ensure_ascii=False)
                    outfile.write('\n')
                return '打开了群转发至line的传送门'
'''


@action("～")
def wxrp(data, nickname):
    from core import sender
    if nickname == 'master':
        with open('wx.txt', 'r') as last:
            lastest = last.read()
        return sender.send_wx(lastest, data)


@action("~?")
def dummy():
    with open('wx.txt', 'r') as last:
        lastest = last.read()
    return f'~ 对象为 {lastest}'


@action("unicodeDecode")
def dummy(data):
    s = data.encode('utf-8')
    return s.decode('unicode-escape')


@action("unicodeEncode")
def dummy(data):
    s = data.encode('unicode-escape')
    return s.decode('utf-8')


# bilibili
from main_lib.more import bilibili, yd


@action("list")
def get_bilibili(data):
    return bilibili.get_bilibili(data)


# bilibili


@action("follow")
def follow_bilibili(data):
    return bilibili.add_bilibili(data)


@action("update")
def up():
    msg = bilibili.get_pagelist()
    return msg


@action("xr")
def xr(data):
    from main_lib.more import currency
    return currency.exchange(data)


# mh
'''  
from main_lib.need_update import faya_mh


@action("alter")
def alter(data):
    return faya_mh.mh_alter(data)


@action("?mh")
def mh(data):
    mh_data = faya_mh.get_mh(data)

    if type(mh_data) == str:
        return mh_data
    else:
        return '\n\n'.join(mh_data).strip()
'''


@action("alias")
def alter(nickname, data):
    arg = data.split('=')
    if len(arg) != 2:
        return '输入有误'
    else:
        if arg[1] in _registered_actions:
            if arg[0] in _registered_actions:
                return '会覆盖原有命令的说。还是算了吧'

            a = db.name(nickname)
            b = a.get()
            b[arg[0] + '_alt'] = arg[1]
            a.set(b)

            return '知道了(~￣△￣)~'
        else:
            return f'faya没{arg[0]}命令'


def do_action(action_name, data, nickname, contact):
    parameter = {
        'data': data,
        'nickname': nickname,
        'contact': contact
    }

    f = _registered_actions[action_name]
    args = inspect.getfullargspec(f)[0]
    num = len(args)
    if num == 0:
        return f()
    elif num == 1 and parameter:
        return f(parameter[args[0]])
    elif num == 2 and parameter:
        return f(parameter[args[0]], parameter[args[1]])


def execute_simple_function(f, parameter):
    args = inspect.getfullargspec(f)[0]
    num = len(args)
    if num == 0:
        return f()
    elif num == 1 and parameter:
        return f(parameter[args[0]])
    elif num == 2 and parameter:
        return f(parameter[args[0]], parameter[args[1]])
    else:
        return f()



def simple_if(nickname, content):
    faya_reply = 0

    if (nickname == 'master') and (content == '1@3$5^7*9)'):
        faya_reply = '!2#4%6&8(0'

    if content.find('https://minatsuki-yui.github.io/') >= 0 and nickname == 'master':
        faya_reply = 'blog 更新了哦'

    if content.find("http") >= 0 and content.find("zhihu.com") >= 0:
        faya_reply = '少看知乎多读书。 '

        if nickname == 'xds':
            faya_reply += '受不了xds'

    if nickname == 'xds' and content.find("http") >= 0:

        ng_dict = ['nico', 'bilibili', 'youtube']

        for each in ng_dict:
            if each in content:
                faya_reply = '不吃安利 不看'

    # if xds jp

    xds_jp = re.compile('[ぁ-んァ-ヶ]+')  # [ぁ-んァ-ヶ亜-熙]+ partly [ぁ-龥]+ all
    is_jp = re.findall(xds_jp, content)

    if len(is_jp) and nickname == 'xds':
        if 'ゆい' not in is_jp[0]:
            faya_reply = 'xds日语真好'

    if ('欧拉' in content) or ('無駄' in content):
        if not content.replace('欧拉', '').replace('無駄', ''):
            ola_tmp = content.replace('欧拉', 'a')
            muda_tmp = ola_tmp.replace('無駄', '欧拉')
            return muda_tmp.replace('a', '無駄')

    if faya_reply:
        return faya_reply
    else:
        return 0


def scenario(nickname, content, contact):
    func_name, parameters = None, None

    if ' ' in content:
        func_name, parameters = content.split(' ', 1)
    else:
        if '.' in content:
            func_name, parameters = content.split('.', 1)
        else:
            func_name = content

    alter_dict = db.name(nickname).get()

    if alter_dict:
        if (func_name + '_alt') in alter_dict:
            func_name = alter_dict[func_name + '_alt']

    if func_name in _registered_actions:
        return do_action(func_name, parameters, nickname, contact)

    if func_name in lib.function_dict:
        return execute_simple_function(lib.get(func_name), parameters)

    faya_dict = faya_db.get()

    if content in faya_dict:
        return faya_dict[content]

    blur = faya_db_b.get()

    for key_word in blur:
        if key_word in content:
            return blur[key_word]

    if_way = simple_if(nickname, content)

    if if_way:
        return if_way
    else:
        return 0

if __name__ == "__main__":
    print(scenario('haru', 'unicodeDecode s7\x007\x9c\x90r\x02\x8cb\x02\xe3n', 'somebody'))
