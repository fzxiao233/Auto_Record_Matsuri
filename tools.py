import json
import sqlite3
import subprocess
from os import mkdir, name
from time import strftime, localtime, time, sleep
from urllib import request

from config import ddir, sec_error, enable_bot, enable_upload, host, group_id, quality, proxy, enable_proxy


def fetch_html(url):
    if enable_proxy == 1:
        proxy_support = request.ProxyHandler({'http': '%s' % proxy, 'https': '%s' % proxy})
        opener = request.build_opener(proxy_support)
        request.install_opener(opener)
    # 此处一定要注明Language, 见commit cda7031
    fake_headers = {
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
    }
    req = request.Request(url, headers=fake_headers)
    response = request.urlopen(req)
    html = response.read()
    html = html.decode('utf-8', 'ignore')
    return html


def m_error(msg):
    echo_log(f'{msg}. After {sec_error}s retrying')
    sleep(sec_error)


def echo_log(log):
    today = strftime('%m-%d', localtime(time()))
    print(log)
    while True:
        try:
            with open(rf"./log/log-{today}.log", 'a') as logs:
                logs.write(log + "\n")
            break
        # 没有log文件夹的话就新建一个
        except FileNotFoundError:
            mkdir("log")


# 关于机器人HTTP API https://cqhttp.cc/docs/4.7/#/API
def bot(message):
    if enable_bot:
        # 此处要重定义opener，否则会使用代理访问
        opener1 = request.build_opener()
        request.install_opener(opener1)
        # 传入JSON时，应使用这个UA
        headers = {'Content-Type': 'application/json'}
        # 将消息输入dict再转为json
        # 此处不应该直接使用HTTP GET的方式传入数据
        _msg = {
            'group_id': group_id,
            'message': message
        }
        msg = json.dumps(_msg).encode('utf-8')
        req = request.Request(f'http://{host}/send_group_msg', headers=headers, data=msg)
        request.urlopen(req)


def bd_upload(file):
    if enable_upload:
        if 'nt' in name:
            command = [".\\BaiduPCS-Go\\BaiduPCS-Go.exe", "upload"]
            command2 = ['.\\BaiduPCS-GO\\BaiduPCS-Go.exe', "share", "set"]
        else:
            command = ["./BaiduPCS-Go/BaiduPCS-Go", "upload"]
            command2 = ['./BaiduPCS-GO/BaiduPCS-Go', "share", "set"]
            # 此处一定要注明encoding

        command.append(f"{ddir}/{file}")
        command.append("/")
        command2.append(file)
        subprocess.run(command)
        s = subprocess.run(command2, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           encoding='utf-8', universal_newlines=True)
        line = s.stdout
        return line


def downloader(link, title, enable_proxy, dl_proxy, quality='best'):
    co = ["streamlink", "--hls-live-restart", "--loglevel", "trace", "--force"]
    if enable_proxy:
        co.append('--http-proxy')
        co.append(f'http://{dl_proxy}')
        co.append('--https-proxy')
        co.append(f'https://{dl_proxy}')
    co.append("-o")
    co.append(f"{ddir}/{title}.ts")
    co.append(link)
    co.append(quality)
    subprocess.run(co)
    # 不应该使用os.system


def process_video(is_live, model):
    bot(f"A live, {is_live.get('Title')}, is streaming. url:  https://www.youtube.com/watch?v={is_live['Ref']}")
    echo_log(model + strftime('|%m-%d %H:%M:%S|', localtime(time())) +
             'Found A Live, starting downloader')
    if model == 'Youtube':
        downloader(r"https://www.youtube.com/watch?v=" + is_live['Ref'], is_live['Title'],
                   enable_proxy, proxy, quality)
    else:
        downloader(is_live['Ref'], is_live['Title'], enable_proxy, proxy)
    echo_log(model + strftime("|%m-%d %H:%M:%S|", localtime(time())) +
             f"{is_live['Title']} was already downloaded")
    bot(f"{is_live['Title']} is already downloaded")
    share = bd_upload(f"{is_live['Title']}.ts")
    echo_log(share)
    bot(share)


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('ref.db')
        self.cursor = self.conn.cursor()

    def select(self):
        self.cursor.execute('SELECT ID,REF FROM Youtube')
        values = self.cursor.fetchall()
        if values:
            return values

    def delete(self, _id):
        self.cursor.execute(f'DELETE FROM Youtube WHERE ID = {_id};')
        self.conn.commit()
        echo_log(f"ID: {_id} has been delete")
