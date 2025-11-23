import os
import re
import scrapy
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin

from proj.items import FileInfoItem
from proj import settings
# from proj.config import settings


class EnvironmentProtectSpider(scrapy.Spider):
    id = "LEG-006"
    name = "环境保护与ESG合规"
    BASE_URL = "https://www.mee.gov.cn"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 未解决文件路径分配
        self.url_names = ["环境保护法", "ESG"]  # , "环境保护法律条例
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.remote_dir = f"{self.id} {self.name}/{timestamp}"
        self.output_dir = f"{settings.TMP_DIR}/{self.remote_dir}"
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    async def start(self):

        for url_name in self.url_names:

            if url_name == "环境保护法":
                searchword = '环境保护法'
                page = 1
                channelid = 270514
                chnls = 5
                url = f"{self.BASE_URL}/was5/web/search?channelid={channelid}&searchword={searchword}&page={page}&chnls={chnls}"

            else:
                searchword = 'ESG'
                page = 1
                channelid = 270514
                url = f"{self.BASE_URL}/was5/web/search?channelid={channelid}&searchword={searchword}&page={page}"

            yield scrapy.Request(
                url=url,
                callback=self.parse,
                dont_filter=True,
                cb_kwargs={
                    'main_sort': url_name,
                    'searchword': searchword,
                    'channelid': channelid,
                    'chnls': chnls,
                    'current_page': page,
                }
            )
            

    def get_page_number(self, text):
        # 从文本中提取页码数字
        if not text:
            return 1

        match = re.search(r'\d+', str(text))
        return int(match.group()) if match else 1

    def parse(self, response, **kwargs):

        main_sort = kwargs.get('main_sort')
        current_page = kwargs.get('current_page', 1)
        searchword = kwargs.get('searchword')
        channelid = kwargs.get('channelid')
        chnls = kwargs.get('chnls')


        # 提取总页数
        page_info = response.xpath('//div[@class="page-large"]//span/text()')
        total_pages = 1
        if page_info and len(page_info) > 1:
            total_pages = self.get_page_number(page_info[1])
            print(
                f"当前分类: {main_sort}, 当前页码: {current_page}, 总页数: {total_pages}")

        # 解析当前页的内容
        ul = response.xpath('//ul[@id="list2"]/li')
        if not ul:
            self.logger.warning(f"在 {main_sort} 的第 {current_page} 页没有找到列表内容")

        for li in ul:
            url_title_elem = li.xpath('./a/h2/text()')
            url_elem = li.xpath('./a/@href')

            if not url_title_elem or not url_elem:
                continue  

            url_title = url_title_elem.get().strip() if url_title_elem else ""
            url = url_elem.get() if url_elem else ""

            # 确保URL是完整的
            if not url.startswith('http'):
                url = urljoin(self.BASE_URL, url)

            print(f"正在爬取：{main_sort}，第{current_page}页，{url_title}，{url}")

            yield scrapy.Request(
                url=url,
                callback=self.parse_detail,
                cb_kwargs={
                    'main_sort': main_sort,
                    'url_title': url_title,
                    'original_url': url,
                }
            )

        # 翻页逻辑：如果当前页小于总页数，生成下一页请求
        if current_page < total_pages:
            next_page = current_page + 1

            # 构建下一页URL
            if chnls is not None:
                next_url = f"{self.BASE_URL}/was5/web/search?channelid={channelid}&searchword={searchword}&page={next_page}&chnls={chnls}"
            else:
                next_url = f"{self.BASE_URL}/was5/web/search?channelid={channelid}&searchword={searchword}&page={next_page}"

            print(f"翻页到: {main_sort} 第{next_page}页")

            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                cb_kwargs={
                    'main_sort': main_sort,
                    'searchword': searchword,
                    'channelid': channelid,
                    'chnls': chnls,
                    'current_page': next_page,
                }
            )
    def parse_detail(self, response, **kwargs):

        main_sort = kwargs.get('main_sort')
        original_url = kwargs.get('original_url')

        # 为每个分类创建子目录
        category_dir = os.path.join(self.output_dir, main_sort)
        Path(category_dir).mkdir(parents=True, exist_ok=True)


        # 提取标题
        file_title = response.xpath('//div[@class="neiright_Box"]/h2/text()')
        if file_title:
            file_title = file_title.get().strip()
        else:
            file_title_elem = response.xpath('//div[@class="xqy_title"]/text()')
            file_title = file_title_elem.get().strip() if file_title_elem else "未知标题"

         # 提取发布日期
        publish_date_elem = response.xpath('//span[@class="xqLyPc time"]/text()')
        if publish_date_elem:
            publish_date = publish_date_elem.get().strip()
        else:
            publish_date_elem = response.xpath('//div[@class="xqy_time"]/span[1]/text()')
            publish_date = publish_date_elem.get().strip() if publish_date_elem else "未知日期"


        # 提取发布单位
        issuing_authority_elem = response.xpath('//span[@class="xqLyPc"]/text()')
        if issuing_authority_elem:
            issuing_authority = issuing_authority_elem.get().strip()[3:]
        else:
            issuing_authority_elem = response.xpath('//div[@class="xqy_time"]/span[2]/text()')
            issuing_authority = issuing_authority_elem.get().strip() if issuing_authority_elem else "未知单位"

        # 清理文件名中的非法字符
        safe_filename = re.sub(r'[<>:"/\\|?*]', '_', file_title)
        # 限制文件名长度
        safe_filename = safe_filename[:100] + '.txt' if len(
            safe_filename) > 100 else safe_filename + '.txt'
        # 完整的本地文件路径
        local_path = os.path.join(category_dir, f"{file_title}.txt")

        # 文本内容
        text_elem = response.xpath('//div[@class="neiright_JPZ_GK_CP"]//text()[not(ancestor::style)]')
        if not text_elem:
            text_elem = response.xpath('//div[@class="TRS_Editor"]//text()[not(ancestor::style)]')
        if not text_elem:
            text_elem = response.xpath('//div[@class="Epro_Editor"]//text()[not(ancestor::style)]')

        if text_elem:
            text = ''.join(text_elem.getall()).strip()
        else:
            text = "无内容"

        # 保存文件
        try:
            with open(local_path, 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception as e:
            self.logger.error(f"保存文件失败: {local_path}, 错误: {e}")
            return

        remote_path = f"{self.remote_dir}/{main_sort}/{safe_filename}"

        file_metadata = {
            "publish_date": publish_date,
            "effective_date": publish_date,
            "valid_from": publish_date,
            "valid_to": "",
            "title": file_title,
            "issuing_authority": issuing_authority,
            "document_number": "",
            "is_valid": "全文有效"

        }

        other_metadata = {
            "category": main_sort,
            "title": file_title,
            "source_url": original_url
        }

        item = FileInfoItem(
            file_name=safe_filename.replace('.txt', ''),
            local_path=local_path,
            remote_path=remote_path,
            file_metadata=file_metadata,
            other_metadata=other_metadata
        )
        self.logger.info(f"成功下载: {item['file_name']}")
        yield item