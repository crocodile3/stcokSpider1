from lxml import etree

import requests


class EastMoney:
    def __init__(self):
        self.domain = 'http://guba.eastmoney.com/'
        self.all_codes_url = ['http://guba.eastmoney.com/remenba.aspx?type=1&tab=1',
                              'http://guba.eastmoney.com/remenba.aspx?type=1&tab=2']
        self.all_codes = self.get_all_codes()

    @staticmethod
    def achieve_zw_content(content_url):
        """
        获取正文评论内容
        :return:
        """
        content_list = []
        page_urls_format = content_url.replace('.html', '_{page}.html')
        page = 1
        while True:
            url = page_urls_format.format(page=page)
            res = requests.get(url)
            page += 1
            if res.status_code == 200:
                html = res.content.decode()
                tree = etree.HTML(html)
                data_list = tree.xpath('//div[@id="zwlist"]/div')
                if len(data_list) > 0:
                    for data in data_list:
                        content = data.xpath('.//div[@class="short_text"]/text()')[0] if data.xpath(
                            './/div[@class="zwlitext  stockcodec"]/div[@class="short_text"]/text()') else None
                        if content:
                            content = content.strip()
                            content_list.append(content)
                else:
                    break
        return content_list

    def get_all_codes(self):
        """
        获取所有股票代码,以及链接
        :return:
        """
        post_bar_urls = []
        for url in self.all_codes_url:
            res = requests.get(url)
            if res.status_code == 200:
                html = res.content.decode()
                tree = etree.HTML(html)
                data_list = tree.xpath("//ul[contains(@class,'ngblistul2')]/li")  # 沪市
                for data in data_list:
                    code = data.xpath('./a/text()')[0]
                    href = data.xpath('./a/@href')[0]
                    post_bar_url = self.domain + href
                    post_bar_urls.append(post_bar_url)
        return post_bar_urls

    def achieve_post_bar_content(self):
        """
        获取所有股吧的内容
        :return:
        """
        post_bar_urls = self.get_all_codes()
        for post_bar_url in post_bar_urls:
            res = requests.get(post_bar_url)
            if res.status_code == 200:
                html = res.content.decode()
                tree = etree.HTML(html)
                data_list = tree.xpath('//div[@id="articlelistnew"]/div[contains(@class,"articleh normal_post")]')
                for data in data_list:
                    scan_cnt = data.xpath('./span[@class="l1 a1"]/text()')[0]  # 浏览量
                    comment_cnt = data.xpath('./span[@class="l2 a2"]/text()')[0]  # 评论数
                    title = data.xpath('./span[@class="l3 a3"]/a/text()')[0]  # 标题
                    href = data.xpath('./span[@class="l3 a3"]/a/@href')[0]  # 链接
                    content_url = 'http://guba.eastmoney.com' + href
                    post_date = data.xpath('./span[@class="l5 a5"]/text()')[0]  # 发帖时间
                    comment_list = self.achieve_zw_content(content_url)
                    # todo 获取贴吧的内容
                    info = dict(
                        scan_cnt=scan_cnt,
                        comment_cnt=comment_cnt,
                        title=title,
                        href=href,
                        post_date=post_date,
                        comment_list=comment_list
                    )
                    return info


if __name__ == '__main__':
    spider = EastMoney()
    spider.achieve_post_bar_content()
