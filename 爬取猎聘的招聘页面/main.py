import json
import time
from copy import copy
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import os.path

class WebCrawlerBot(object):
    """docstring for WebCrawlerBot"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        }
        self.weibo_hot_list = []
        self.liepin_urls = {}
        self.session = requests.Session()
    def set_cookie(self, cookie):
        self.headers["cookie"] = cookie

    def get_liepin(self, keyword, start_page, end_page=None):
        if keyword not in self.liepin_urls:
            req = self.session.get(
                f"https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&d_sfrom=search_fp&key={quote_plus(keyword)}",
                headers=self.headers,
            )
            soup = BeautifulSoup(req.text, "lxml")
            self.liepin_urls[keyword] = "https://www.liepin.com"
            self.liepin_urls[keyword] += "&d_curPage={d_curPage}".join(
                soup.select(".pagerbar a")[3]["href"].split("&d_curPage=")
            )
            self.liepin_urls[keyword] = (
                    self.liepin_urls[keyword].split("&curPage=")[0] + "&curPage={curPage}"
            )
        if end_page is None:
            end_page = start_page + 1
        results = []
        for page in range(start_page, end_page):
            time.sleep(1)
            if page > 0:
                url = self.liepin_urls[keyword].format(d_curPage=page - 1, curPage=page)
            else:
                url = self.liepin_urls[keyword].format(d_curPage=page + 1, curPage=page)
            req = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(req.text, "lxml")
            for item in soup.select(".sojob-item-main"):
                job_name = item.select("h3 a")[0].text.strip()
                job_company = item.select(".company-name")[0].text.strip()
                job_field = item.select(".field-financing")[0].text.strip()
                job_salary = item.select(".condition .text-warning")[0].text.strip()
                if job_salary == "面议":
                    annual_salary = -1
                else:
                    if "-" in job_salary:
                        min_salary = int(job_salary[: job_salary.index("-")])
                        if "k" in job_salary:
                            max_salary = int(
                                job_salary[
                                job_salary.index("-") + 1 : job_salary.index("k")
                                ]
                            )
                        elif "万" in job_salary:
                            max_salary = (
                                    int(
                                        job_salary[
                                        job_salary.index("-")
                                        + 1 : job_salary.index("万")
                                        ]
                                    )
                                    * 10
                            )
                        else:
                            max_salary = min_salary
                        months = (
                            int(job_salary[job_salary.index("·") + 1 : -1])
                            if "·" in job_salary
                            else 12
                        )
                        annual_salary = (min_salary + max_salary) / 2 * months * 1000
                    else:
                        if "k" in job_salary:
                            monthly_salary = int(job_salary.split("k")[0])
                        elif "万" in job_salary:
                            monthly_salary = (
                                    int(
                                        job_salary[
                                        job_salary.index("-")
                                        + 1 : job_salary.index("万")
                                        ]
                                    )
                                    * 10
                            )
                        else:
                            monthly_salary = 0
                        months = (
                            int(job_salary[job_salary.index("·") + 1 : -1])
                            if "·" in job_salary
                            else 12
                        )
                        annual_salary = monthly_salary * months * 1000
                job_area = item.select(".condition .area")[0].text.strip()
                job_edu = item.select(".condition .edu")[0].text.strip()
                job_experience = item.select(".condition span")[-1].text.strip()
                results.append(
                    [
                        job_name,
                        job_company,
                        job_field,
                        job_salary,
                        annual_salary,
                        job_area,
                        job_edu,
                        job_experience,
                    ]
                )
        return results