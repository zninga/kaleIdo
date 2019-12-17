import pickle
import re
import time
from argparse import ArgumentParser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from locators import *
from page import *

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
# cmd = "SU=深度学习"
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


def run():
    result = []
    start_page = 1
    while True:
        driver = webdriver.Chrome(options=chrome_options)
        url = "https://kns.cnki.net/kns/brief/result.aspx?dbprefix=CDMD"
        driver.get(url)

        # 切换到专业检索板块
        main_page = MainPage(driver)
        main_page.click_expert_search_tab()

        # 填充检索框并进行检索
        time.sleep(2)
        expert_search_page = ExpertSearchPage(driver)
        expert_search_page.set_expert_search_textarea(cmd)
        expert_search_page.click_search_btn()

        # 切换到检索结果frame
        time.sleep(2)
        driver.switch_to.frame("iframeResult")

        # 每页显示结果50条
        search_results_page = SearchResultsPage(driver)
        search_results_page.click_items_per_page(50)

        time.sleep(2)
        # 获取结果条数
        number_of_results = search_results_page.get_number_of_results_div()

        if number_of_results <= 50:
            total_page = 1
            print(
                f"{'='*10} 找到 {number_of_results:,} 条结果, 共 {total_page} 页 {'='*10} "
            )
            result = search_results_page.get_results_tr_s()
            break

        # 获取总页数
        _, total_page = search_results_page.get_cur_and_total_page_span()

        # 获取基本分页url
        paging_url = search_results_page.get_paging_base_url_a()

        print(
            f"{'='*10} 找到 {number_of_results:,} 条结果, 共 {total_page} 页 {'='*10} "
        )
        for page in range(start_page, total_page + 1):
            print(f"Getting No.[{page}/{total_page}] page...")
            # 根据基本分页url构造每一页url
            paging_url = re.sub("(?<=curpage=)[0-9]+", str(page), paging_url)
            driver.get(paging_url)

            # 获取当前页的检索结果
            search_results_page = SearchResultsPage(driver)
            time.sleep(2)
            papers = search_results_page.get_results_tr_s()

            # 如果服务器限制, 关闭此次检索, 重新从此次失败的页面开始检索
            if not len(papers) > 0:
                driver.quit()
                # 重新尝试时的开始分页为上次检索失败分页
                start_page = page
                print(
                    f"Getting No.{page} page Failed! Reconnecting to CNKI...")
                break

            result.extend(papers)
            print(
                f"完成进度:　[{len(papers)}] [{len(result)}/{number_of_results}]\n")
        else:
            driver.quit()
            print("Done!")
            break
    return result


def save_result(file_path, result):
    with open(file_path, "wb") as f:
        pickle.dump(result, f)


def main():
    result = run()
    save_result(args["output"], result)


if __name__ == "__main__":
    main()