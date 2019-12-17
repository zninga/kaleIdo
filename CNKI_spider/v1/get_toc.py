"""
  获取论文目录信息
"""
import pickle
import time
from argparse import ArgumentParser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ap = ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="输入文件名")
ap.add_argument("-o", "--output", required=True, help="输出文件名")
args = vars(ap.parse_args())

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument('blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(options=chrome_options)

# 得到来自get_items.py的检索结果信息
with open(args["input"], "rb") as f:
    results = pickle.load(f)
y = 0
try:
    url = "https://kns.cnki.net/kns/brief/result.aspx?dbprefix=CDMD"
    driver.get(url)

    # 切换到专业检索板块
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#\\31 _4"))).click()
    time.sleep(2)

    for i, r in enumerate(results):
        # 简单使用标题和作者进行检索
        try:
            cmd = f"TI={r['title']} AND AU={r['author']}"

            # 只进行3次获取尝试
            for try_times in range(3):
                try:
                    # 填充检索框并进行检索
                    driver.execute_script(
                        f"document.querySelector('#expertvalue').value='{cmd}'"
                    )
                    driver.execute_script(
                        "document.querySelector('#btnSearch').click();")

                    time.sleep(2)

                    # 切换到搜索结果frame
                    driver.switch_to.frame("iframeResult")

                    # 点击检索结果链接进入详情页
                    driver.execute_script(
                        "document.querySelector('#ctl00 > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > a').click();"
                    )

                    # 切换到详情页
                    driver.switch_to.window(driver.window_handles[-1])

                    # 点击目录页
                    driver.execute_script(
                        "document.querySelector('#DownLoadParts > a:nth-child(3)').click();"
                    )

                    # 切换到目录页
                    driver.switch_to.window(driver.window_handles[-1])

                    # 获取目录
                    results[i]["toc"] = driver.execute_script(
                        "return document.querySelector('body > div.wrapper.section1 > div.trends > div > table').innerText"
                    )

                    # 关闭此次检索的详情页和目录页
                    driver.close()
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.close()

                    # 回到检索页
                    driver.switch_to.window(driver.window_handles[-1])
                    break
                except:
                    # 失败的话重新打开进行检索
                    print(f"Retry: {try_times}")
                    driver.quit()
                    driver = webdriver.Chrome(options=chrome_options)
                    url = "https://kns.cnki.net/kns/brief/result.aspx?dbprefix=CDMD"
                    driver.get(url)
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, "#\\31 _4"))).click()
                    time.sleep(2)

            info = f"{r['year']} - {r['school']} - {r['title']} - {r['author']} - {r['degree']}"
            if "toc" in r:
                y += 1
                print(f"[No.{i:04d}] [Y] - [{info}]")
            else:
                print(f"[No.{i:04d}] [N] - [{info}]")
        except:
            pass
    driver.quit()
except:
    print(f"[Done!] Succeed: {y} items")
    with open(args["output"], "wb") as f:
        pickle.dump(results, f)