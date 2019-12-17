import re

from element import BaseSearchElement
from entity import Paper
from locators import *


class SearchTextElement(BaseSearchElement):
    """搜索框描述符类"""
    def __init__(self, locator):
        self.locator = locator


class BasePage(object):
    """页面基类"""
    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):
    """主页"""
    def click_expert_search_tab(self):
        """点击专业检索选项卡"""
        element = self.driver.find_element(*MainPageLocators.EXPERT_SEARCH_TAB)
        element.click()


class ExpertSearchPage(BasePage):
    """专业检索页"""
    cmd = SearchTextElement(ExpertSearchPageLocators.EXPERT_SEARCH_TEXTAREA)

    def set_expert_search_textarea(self, cmd):
        """设置检索表达式"""
        self.cmd = cmd

    def get_expert_search_textarea(self):
        """获取检索表达式"""
        return self.cmd

    def click_search_btn(self):
        """点击检索按钮"""
        element = self.driver.find_element(
            *ExpertSearchPageLocators.SEARCH_BTN)
        element.click()


class SearchResultsPage(BasePage):
    """搜索结果页"""
    def click_items_per_page(self, num):
        """每页显示结果条数"""
        if num == 10:
            element = self.driver.find_element(
                *SearchResultsPageLocators.ITEMS_10_PER_PAGE_A)
        elif num == 20:
            element = self.driver.find_element(
                *SearchResultsPageLocators.ITEMS_20_PER_PAGE_A)
        elif num == 50:
            element = self.driver.find_element(
                *SearchResultsPageLocators.ITEMS_50_PER_PAGE_A)
        else:
            raise ValueError("items in each page should be in (10, 20, 50)")
        element.click()

    def get_number_of_results_div(self):
        """获取检索结果条数"""
        element = self.driver.find_element(
            *SearchResultsPageLocators.NUMBER_OF_RESULTS_DIV)
        return int(element.text.split()[1].replace(",", ""))

    def get_cur_and_total_page_span(self):
        """获取当前页和总页数"""
        element = self.driver.find_element(
            *SearchResultsPageLocators.CUR_AND_TOTAL_PAGE_SPAN)
        return [int(n) for n in element.text.split("/")]

    def get_paging_base_url_a(self):
        """获取基本分页URL构造"""
        element = self.driver.find_element(
            *SearchResultsPageLocators.PAGING_BASE_URL_A)
        return element.get_attribute("href")

    def get_results_tr_s(self):
        """获取每条检索结果元信息"""
        try:
            elements = self.driver.find_elements(
                *SearchResultsPageLocators.RESULTS_TR_s)
            print(f"[{len(elements) - 1:,}] results")
            papers = []
            for i, elem in enumerate(elements):
                if i == 0: continue  # 跳过表格头
                # title = elem.find_element(*DetailsItemLocators.TITLE_A)
                # author = elem.find_element(*DetailsItemLocators.AUTHOR_A)
                # school = elem.find_element(*DetailsItemLocators.SCHOOL_A)
                # degree = elem.find_element(*DetailsItemLocators.DEGREE_TD)
                # year = elem.find_element(*DetailsItemLocators.YEAR_TD)
                # paper = Paper(title.text, author.text, school.text, degree.text,
                #               year.text)

                attrs = elem.find_elements(*DetailsItemLocators.ALL_ATTR_TD_s)
                attrs = [attr.text for attr in attrs[1:6]]

                print(f"  No.{i:02} - {' - '.join(attrs)}")

                attrs[-1] = int(attrs[-1].replace("年", ""))
                paper = {}
                keys = ["title", "author", "school", "degree", "year"]
                paper = {key: value for key, value in zip(keys, attrs)}
                papers.append(paper)
        except Exception as e:
            print(e)

        return papers


class DetailsPage(BasePage):
    """详情页"""
    def get_attribute(self, locator):
        """获取页面属性, 包括 [标题, 作者, 学校, 摘要, 关键词, 导师, 分类号]"""
        element = self.driver.find_element(*locator)
        return element.text

    def click_download_chapters_a(self):
        """点击分章下载打开目录页"""
        element = self.driver.find_element(
            DetailsPageLocators.DOWNLOAD_CHAPTERS_A)
        element.click()
