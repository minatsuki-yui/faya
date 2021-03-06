import requests
import re
import json
import time


def get(data):
    s = requests.session()
    s.keep_alive = False
    headers = {'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
               'Accept': '*/*',
               'Referer': 'https://www.ickd.cn/auto.html'
               }

    cookies = {
        'Hm_lvt_39418dcb8e053c84230016438f4ac86c': '0',
        'Hm_lpvt_39418dcb8e053c84230016438f4ac86c': '-1'
    }

    data1 = requests.get(f'https://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text={data}', headers=headers,
                         cookies=cookies).json()
    postData = data1.get('auto', '')
    if postData:
        postType = postData[0]['comCode']
    else:
        return '未知公司'
    stamp = int(time.time() * 1000)

    link = f'https://biz.trace.ickd.cn/auto/{data}?mailNo={data}&spellName=&exp-textName=&ts=123456&enMailNo=123456789&callback=_jqjsp&_{stamp}='
    raw = s.get(link, headers=headers, cookies=cookies).text
    print(raw)

    callback = re.findall('{[\s\S]+}', raw)
    if not callback:
        return '运单号错了或者暂无数据(´-ω-`)'
    # msg = '最近更新:\n'

    msg = ''

    # for port in data2[:3]:
    #    msg = '时间: ' + port['time'] + '\n信息: ' + port['context'] + '\n' + msg
    msg = f'{postType}运输 最近更新:\n' + msg
    # return msg
    dict_reg = re.compile('{.+?}')
    ports = re.findall(dict_reg, callback[0])

    if len(ports) < 3:
        info = json.loads(ports[-1])
        key = list(info)
        msg += f"{info[key[0]]}, {info[key[1]]}\n"
        return msg

    for port in ports[-3:]:
        info = json.loads(port)
        key = list(info)
        msg += f"{info[key[0]]}, {info[key[1]]}\n"
    return msg


if __name__ == '__main__':
    print(get('......'))
