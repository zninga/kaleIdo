"""
  按照检索表达式获取知网硕博论文检索结果, 包含:
    1. 标题
    2. 作者
    3. 学校
    4. 学位类型
    5. 年份
"""
import pickle
import re
import time
from argparse import ArgumentParser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ap = ArgumentParser()
ap.add_argument("-su", "--subject", type=str, nargs="+", help="主题")
ap.add_argument("-ky", "--keyword", type=str, nargs="+", help="关键词")
ap.add_argument("-s", "--school", type=str, nargs="+", help="学位授予单位")
ap.add_argument("-fy",
                "--from_year",
                type=str,
                default="2010",
                help="学位授予年度(开始范围)")
ap.add_argument("-ty",
                "--to_year",
                type=str,
                default="2019",
                help="学位授予年度(截止范围)")
ap.add_argument("-o", "--output", required=True, help="输出文件名")
args = vars(ap.parse_args())

# 生成检索表达式
# cmd = "SU=深度学习卷积神经网络 AND PT BETWEEN(2017,2017)"
cmd = [
    "SU=" + "+".join(args["subject"]), "KY=" + "+".join(args["keyword"]),
    "DF=" + "+".join(args["school"]),
    f"PT BETWEEN({args['from_year']},{args['to_year']})"
]
cmd = " AND ".join(cmd)
print(cmd)

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument('blink-settings=imagesEnabled=false')

results = []
start_page = 1
while True:
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://kns.cnki.net/kns/brief/result.aspx?dbprefix=CDMD"
    driver.get(url)

    # 切换到专业检索板块
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#\\31 _4"))).click()

    time.sleep(2)

    # 填充检索框并进行检索
    driver.execute_script(
        f"document.querySelector('#expertvalue').value='{cmd}'")
    driver.execute_script("document.querySelector('#btnSearch').click();")

    time.sleep(2)

    # 切换到检索结果frame
    driver.switch_to.frame("iframeResult")

    # 每页显示结果50条
    driver.execute_script(
        "document.querySelector('#id_grid_display_num > a:nth-child(3)').click();"
    )

    time.sleep(2)

    # 获取基本分页url
    page_url = driver.find_element_by_css_selector(
        "#ctl00 > table > tbody > tr:nth-child(3) > td > table > tbody > tr > td > div > a:nth-child(3)"
    ).get_attribute("href")

    # 获取总页数
    total_page = int(
        driver.find_element_by_css_selector(
            "#J_ORDER > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > div > span.countPageMark"
        ).text.split("/")[-1])

    for page in range(start_page, total_page + 1):
        # 根据基本分页url构造每一页url
        page_url = re.sub("(?<=curpage=)[0-9]+", str(page), page_url)
        driver.get(page_url)

        # 获取当前页的检索结果
        items = driver.find_elements_by_css_selector(
            "#ctl00 > table > tbody > tr:nth-child(2) > td > table > tbody > tr"
        )

        # 如果服务器限制, 关闭此次检索, 重新从此次失败的页面开始检索
        if not len(items) > 0:
            driver.quit()
            # 重新尝试时的开始分页为上次检索失败分页
            start_page = page
            print("Reconnecting to CNKI...")
            break

        for tr in range(1, len(items)):
            tr_td = items[tr].find_elements_by_tag_name("td")
            tr_td_a = tr_td[1].find_element_by_tag_name("a")

            r = {}
            r["title"] = tr_td_a.text
            r["author"] = tr_td[2].text
            r["school"] = tr_td[3].text
            r["degree"] = tr_td[4].text
            r["year"] = tr_td[5].text
            info = f"{r['year']} - {r['school']} - {r['title']} - {r['author']} - {r['degree']}"

            results.append(r)
            print(f"[No.{len(results):04d}] - [{info}]")
    else:
        driver.quit()
        print("Done!")
        break

with open(args["output"], "wb") as f:
    pickle.dump(results, f)
