from tools import gethtml, echo_log, bot, bd_upload, downloader
from config import host, group_id, sec
import time
from lxml.html import etree


class Openrec:
    def __init__(self, oprec_id, enable_proxy, proxy, ddir):
        self.oprec_id = oprec_id
        self.enable_proxy = enable_proxy
        self.ddir = ddir
        if enable_proxy == 1:
            self.dl_proxy = '--https-proxy ' + f'"http://{proxy}"'
            self.proxy = proxy
        else:
            self.proxy = ''
            self.dl_proxy = ''

    def is_live(self):
        html = gethtml(f'https://www.openrec.tv/user/{self.oprec_id}', self.enable_proxy, self.proxy)
        dom = etree.HTML(html)
        is_live = dom.xpath('/html/body/div[1]/div[2]/div[18]/div[2]/div/div[3]/ul/li[1]/div/text()')[0]
        if 'Live' in is_live:
            info = dom.xpath('/html/body/div[1]/div[2]/div[18]/div[2]/div/div[3]/ul/li[1]/ul/li/a[2]')[0]
            ref = info.xpath('@href')[0]
            title = dom.xpath('/html/body/div[1]/div[2]/div[18]/div[2]/div/div[3]/ul/li[1]/ul/li/a[2]/text()')[0]
            return {'Title': title, 'Ref': ref}

    def check(self):
        is_live = self.is_live()
        if is_live:
            downloader(is_live['Ref'], is_live['Title'], self.dl_proxy)
            echo_log('Openrec' + time.strftime('|%m-%d %H:%M:%S|', time.localtime(time.time())) +
                     f"{is_live['title']} was already downloaded")
            bot(host, group_id, f"{is_live['title']} is already downloaded")
            share = bd_upload(f"{is_live['title']}.ts")
            bot(host, group_id, share)
        else:
            echo_log('Openrec' + time.strftime('|%m-%d %H:%M:%S|', time.localtime(time.time())) +
                     f'Not found Live, after {sec}s checking')
