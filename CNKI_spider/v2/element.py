from selenium.webdriver.support.ui import WebDriverWait


class BaseSearchElement(object):
    """搜索框描述符类"""
    def __set__(self, instance, value):
        driver = instance.driver
        WebDriverWait(
            driver,
            100).until(lambda driver: driver.find_element(*self.locator))
        driver.find_element(*self.locator).clear()
        driver.find_element(*self.locator).send_keys(value)

    def __get__(self, instance, owner):
        driver = instance.driver
        WebDriverWait(
            driver,
            100).until(lambda driver: driver.find_element(*self.locator))
        return driver.find_element(*self.locator).get_attribute("value")
