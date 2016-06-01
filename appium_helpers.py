# -*- coding: utf-8 -*-
from appium import webdriver
from appium.webdriver import errorhandler
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from abc import ABCMeta
from abc import abstractmethod
from subprocess import check_output
from subprocess import CalledProcessError
from os import getcwd
from os import environ


def get_capabilities(options={}):
    """
    Try to use the capabilities defined in ENV variable or
    then use capabilities defined in 'options' or
    then use defaults
    """
    return {
        "ipa" : environ.get("APPIUM_APPFILE") or options.get("ipa"),
        "automationName" : environ.get("APPIUM_AUTOMATION") or options.get("automationName"),
        "deviceName" : environ.get("APPIUM_DEVICE") or options.get("deviceName", "Local Device"),
        "platformName" : environ.get("APPIUM_PLATFORM") or options.get("platformName"),
        "bundleId" : environ.get("APPIUM_BUNDLE_ID") or options.get("bundleId"),
        "newCommandTimeout" : environ.get("NEW_COMMAND_TIMEOUT") or options.get("newCommandTimeout", 60),
        "defaultCommandTimeout" : environ.get("DEFAULT_COMMAND_TIMEOUT") or options.get("defaultCommandCommandTimeout", 500),
        "testdroid_testTimeout" : environ.get("TESTDROID_TEST_TIMEOUT") or options.get("testdroid_testTimeout", 600),
        "screenshotWaitTimeout" : environ.get("SCREENSHOT_WAIT_TIMEOUT") or options.get("screenshotWaitTimeout", 3)
    }

def get_driver(driver=webdriver, addr='http://localhost:4723/wd/hub', capabilities={}):
    # TODO WebDriverException (session already ongoing)
    # TODO URLError (no appium session)
    return driver.Remote(addr, capabilities)

class PlatformBase(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def __init__(self, driver):
        self.driver = driver
    @abstractmethod
    def __getattr__(self, name):
        def _missing(*args, **kwargs):
            print("object %r and method %r" % (self, name))
            print("args: %r kwargs: %r" % (args, kwargs))
        return _missing

class Android(PlatformBase):
    pass

#### iOS Keywords #####
class iOS(PlatformBase):
    @staticmethod
    def find_buttons(driver, name):
        s = '.elements()["{}"]'.format(name)
        return driver.find_elements_by_ios_uiautomation(s)

    @staticmethod
    def find_button(driver, name):
        s = '.elements()["{}"]'.format(name)
        return driver.find_element_by_ios_uiautomation(s)

    @staticmethod
    def find_and_wait_button(driver, name, wait_time=5):
        s = '.elements()["{}"]'.format(name)
        return iOS.wait_by(driver,
                           EC.presence_of_element_located,
                           By.IOS_UIAUTOMATION,
                           s,
                           wait_time)

    @staticmethod
    def find_and_wait_text_from_webview(driver, name, wait_time=5):
        s = '.scrollViews()[0].webViews()[0].staticTexts()["{}"]'.format(name)
        return iOS.wait_by(driver,
                           EC.presence_of_element_located,
                           By.IOS_UIAUTOMATION,
                           s,
                           wait_time)

    @staticmethod
    def find_all_webview_elements_by_xpath(driver):
        return driver.find_elements_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/*')

    @staticmethod
    def find_element_by_xpath(driver, xpath):
        return driver.find_element_by_xpath(xpath)

    @staticmethod
    def find_webview_elements_by_xpath(driver, xpath):
        return driver.find_elements_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAWebView[1]/' + xpath)

    @staticmethod
    def find_all_elements_by_xpath(driver):
        return driver.find_elements_by_xpath('//*[not(*)]')

    @staticmethod
    def find_all_window_elements_by_xpath(driver):
        return driver.find_elements_by_xpath('//UIAApplication[1]/UIAWindow[1]/*')

    @staticmethod
    def find_all_window_elements(driver):
        return driver.find_elements_by_ios_uiautomation('.elements()')

    @staticmethod
    def wait_by(driver, expected_condition, by_method, element_identifier, wait_time=5):
        """
        See: http://selenium-python.readthedocs.io/waits.html
        Args:
            driver: instance of Appium.webdriver
            expected_condition: what we condition we expect to happen
            by_method: by with what Appium.webdriver.method we try to find the element
            element_identifier: depending on 'by_method' what indentifier we try to use to locate the elem
            wait_time: time to wait element to appear

        Returns: instance of appium.webdriver.webelement or TimeoutException
        """
        return WebDriverWait(driver, wait_time).until(expected_condition((by_method, element_identifier)))

    @staticmethod
    def toggle_orientation(driver):
        def change_orientation(driver, orientation):
            driver.orientation = orientation

        current_orientation = driver.orientation
        if current_orientation == "PORTRAIT":
            return change_orientation(driver, "LANDSCAPE")
        else:
            return change_orientation(driver, "PORTRAIT")

    @staticmethod
    def get_xml_tree(driver):
        return driver.execute_script('au.mainApp().getTreeForXML()')

    @staticmethod
    def screenshot_fast(driver, name, dir=getcwd()+'/screenshots'):
        """
        Takes PNG screenshot using command idevicescreenshot.
        """

        #TODO: we need to define the device we launch the appium-server against in ENV
        #      This will fail if multiple devices are present
        udid = check_output(["idevice_id", "-l"]).decode("utf-8").strip('\n')
        name = str(name) + '.png'

        try:
            out = check_output(["idevicescreenshot", "-u", str(udid), dir+'/'+name])
        except CalledProcessError as e:
            print("Error taking screenshot {} in {} with error {}".format(name, dir, e.output))
            return False
        return True

    @staticmethod
    def screenshot(driver, name, dir=getcwd()+'/screenshots'):
        """
        Screenshotting is super slow - use it seldom
        """
        name = str(name) + '.png'
        return driver.save_screenshot(dir + "/" + name)
