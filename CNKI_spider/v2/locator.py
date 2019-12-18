from selenium.webdriver.common.by import By


class MainPageLocators(object):
    """主页元素定位"""

    # 专业检索选项卡
    EXPERT_SEARCH_TAB = (By.CSS_SELECTOR, "#\\31 _4")


class ExpertSearchPageLocators(object):
    """专业检索页元素定位"""

    # 专业表达式搜索框
    EXPERT_SEARCH_TEXTAREA = (By.CSS_SELECTOR, "#expertvalue")

    # 检索按钮
    SEARCH_BTN = (By.CSS_SELECTOR, "#btnSearch")


class SearchResultsPageLocators(object):
    """搜索结果页元素定位"""

    # 每页显示10条
    ITEMS_10_PER_PAGE_A = (By.CSS_SELECTOR,
                           "#id_grid_display_num > a:nth-child(1)")

    # 每页显示20条
    ITEMS_20_PER_PAGE_A = (By.CSS_SELECTOR,
                           "#id_grid_display_num > a:nth-child(2)")

    # 每页显示50条
    ITEMS_50_PER_PAGE_A = (By.CSS_SELECTOR,
                           "#id_grid_display_num > a:nth-child(3)")

    # 搜索结果条数
    NUMBER_OF_RESULTS_DIV = (
        By.CSS_SELECTOR,
        "#J_ORDER > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > div > div"
    )

    # 当前页和总页数
    CUR_AND_TOTAL_PAGE_SPAN = (
        By.CSS_SELECTOR,
        "#J_ORDER > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > div > span.countPageMark"
    )

    # 基本分页URL格式
    PAGING_BASE_URL_A = (
        By.CSS_SELECTOR,
        "#ctl00 > table > tbody > tr:nth-child(3) > td > table > tbody > tr > td > div > a:nth-child(3)"
    )

    # 所有的搜索结果
    RESULTS_TR_s = (
        By.CSS_SELECTOR,
        "#ctl00 > table > tbody > tr:nth-child(2) > td > table > tbody > tr")


class DetailsItemLocators(object):
    """搜索的每一条结果的条目信息"""

    ALL_ATTR_TD_s = (By.CSS_SELECTOR, "td")
    # 标题
    TITLE_A = (By.CSS_SELECTOR, "td:nth-child(2) > a")

    # 作者
    AUTHOR_A = (By.CSS_SELECTOR, "td.author_flag > a")

    # 学校
    SCHOOL_A = (By.CSS_SELECTOR, "td:nth-child(4) > a")

    # 学位
    DEGREE_TD = (By.CSS_SELECTOR, "td:nth-child(5)")

    # 年份
    YEAR_TD = (By.CSS_SELECTOR, "td:nth-child(6)")


class DetailsPageLocators(object):
    """论文详情页元素定位"""

    # 标题
    TITLE_H2 = (By.CSS_SELECTOR, "#mainArea > div.wxmain > div.wxTitle > h2")

    # 作者
    AUTHOR_A = (By.CSS_SELECTOR,
                "#mainArea > div.wxmain > div.wxTitle > div.author > span > a")

    # 学校
    SCHOOL_A = (By.CSS_SELECTOR,
                "#mainArea > div.wxmain > div.wxTitle > div.orgn > span > a")

    # 摘要
    ABSTRACT_SPAN = (By.CSS_SELECTOR, "#ChDivSummary")

    # 关键词
    KEYWORDS_A_s = (
        By.CSS_SELECTOR,
        "#mainArea > div.wxmain > div.wxInfo > div.wxBaseinfo > p:nth-child(3) > a"
    )

    # 导师
    ADVISOR_A = (
        By.CSS_SELECTOR,
        "#mainArea > div.wxmain > div.wxInfo > div.wxBaseinfo > p:nth-child(4) > a"
    )

    # 分类号
    CATALOG_P = (
        By.CSS_SELECTOR,
        "#mainArea > div.wxmain > div.wxInfo > div.wxBaseinfo > p:nth-child(5)"
    )

    # 整本下载
    DOWNLOAD_FULL_PAPER_A = (By.CSS_SELECTOR,
                             "#DownLoadParts > a:nth-child(1)")
    # 分页下载
    DOWNLOAD_PAGES_A = (By.CSS_SELECTOR, "#DownLoadParts > a:nth-child(2)")

    # 分章下载
    DOWNLOAD_CHAPTERS_A = (By.CSS_SELECTOR, "#DownLoadParts > a:nth-child(3)")

    # 在线阅读
    READ_ONLINE_A = (By.CSS_SELECTOR, "#DownLoadParts > a:nth-child(4)")


class ContentsPageLocators(object):
    CONTENTS_TABLE = (By.CSS_SELECTOR,
                      "body > div.wrapper.section1 > div.trends > div > table")