# -*- coding: utf-8 -*-
from abc import ABCMeta
from abc import abstractmethod
from subprocess import check_output
from subprocess import CalledProcessError
from os import getcwd
from os import environ
from os.path import exists
from os import makedirs
from inspect import signature
from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

def get_capabilities(options=None):
    """
    Try to use the capabilities defined in ENV variable or
    then use capabilities defined in 'options' or
    then use defaults
    """
    if not options:
        options = {}
    return {
        "app": environ.get("APPIUM_APPFILE") or options.get("app"),
        "automationName": environ.get("APPIUM_AUTOMATION") or options.get("automationName"),
        "deviceName": environ.get("APPIUM_DEVICE") or options.get("deviceName", "Local Device"),
        "platformName": environ.get("APPIUM_PLATFORM") or options.get("platformName"),
        "bundleId": environ.get("APPIUM_BUNDLE_ID") or options.get("bundleId"),
        "newCommandTimeout": environ.get("NEW_COMMAND_TIMEOUT") or options.get("newCommandTimeout", 60),
        "defaultCommandTimeout": environ.get("DEFAULT_COMMAND_TIMEOUT") or options.get("defaultCommandCommandTimeout", 500),
        "testdroid_testTimeout": environ.get("TESTDROID_TEST_TIMEOUT") or options.get("testdroid_testTimeout", 600),
        "screenshotWaitTimeout": environ.get("SCREENSHOT_WAIT_TIMEOUT") or options.get("screenshotWaitTimeout", 3)
    }


def get_capabilities_15(options=None):
    """
    Try to use Capabilities for Appium v 1.5
    """
    if not options:
        options = {}
    return {
        "app": environ.get("APPIUM_APPFILE") or options.get("app"),
        "automationName": environ.get("APPIUM_AUTOMATION_15") or options.get("automationName", "Appium"),
        "udid": environ.get("IDEVICE_UDID") or options.get("udid", None),
        "deviceName": environ.get("APPIUM_DEVICE") or options.get("deviceName", "Local Device"),
        "defaultDevice": True,
        "platformName": environ.get("APPIUM_PLATFORM") or options.get("platformName"),
        "bundleId": environ.get("APPIUM_BUNDLE_ID") or options.get("bundleId"),
        "newCommandTimeout": environ.get("NEW_COMMAND_TIMEOUT") or options.get("newCommandTimeout", 60),
        "defaultCommandTimeout": environ.get("DEFAULT_COMMAND_TIMEOUT") or options.get("defaultCommandCommandTimeout", 500),
        "testdroid_testTimeout": environ.get("TESTDROID_TEST_TIMEOUT") or options.get("testdroid_testTimeout", 600),
        "screenshotWaitTimeout": environ.get("SCREENSHOT_WAIT_TIMEOUT") or options.get("screenshotWaitTimeout", 3)
    }


def get_driver(driver=webdriver, addr='http://localhost:4723/wd/hub', capabilities=None):
    """
    Get the Appium Driver
    **Note**
        We assume the App/Ipa has been installed in the device
        before calling this method
    """
    if not capabilities:
        capabilities = {}
    try:
        return driver.Remote(addr, capabilities)
    except Exception as e:
        print("\n\nError starting Appium session: '{}'\n\n".format(e))
        return None

#### Common Keywords #####


class PlatformBase(object):
    """
    Appium Base Class for common functionality between iOS and Android
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        print("PlatformBase initted")
        # create Screenshot dir
        screenshot_dir = getcwd() + '/screenshots'
        if not exists(screenshot_dir):
            makedirs(screenshot_dir)

    def __getattr__(self, name):
        def _missing(*args, **kwargs):
            print("object %r and method %r" % (self, name))
            print("args: %r kwargs: %r" % (args, kwargs))
        return _missing

    @staticmethod
    def screenshot(driver, name, directory=getcwd()+'/screenshots'):
        """
        Screenshotting is super slow - use it seldom
        """
        name = str(name) + '.png'
        return driver.save_screenshot(directory + "/" + name)

    @staticmethod
    def get_window_size(driver):
        """
        Returns the height, width of the current window size as int
        """
        res = driver.get_window_size()

        return int(res['height']), int(res['width'])

    @staticmethod
    def get_element_location(element):
        """
        Return the element location (h,w) as int
        """
        element_coord = element.location
        return int(element_coord['y']), int(element_coord['x'])

    @staticmethod
    def click_retry_with_elem_coordinates(driver, element):
        """
        Tries to click button, and in case of ServerSideError tries
        to tap the element coordinates
        """
        try:
            element.click()
        except WebDriverException as e:
            print("Element couldn't be clicked, error: '{}'".format(e))
            h, w = PlatformBase.get_element_location(element)
            print("Will try to tap the element location w:{}, h:{}".format(w, h))
            return driver.tap([(w, h)])


#### Android Keywords #####
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
            element_identifier: depending on 'by_method' what indentifier we try
            to use to locate the elem
            wait_time: time to wait element to appear

        Returns: instance of appium.webdriver.webelement or TimeoutException
        """
        return WebDriverWait(driver, wait_time).until(expected_condition((by_method, element_identifier)))

    @staticmethod
    def toggle_orientation(driver):
        current_orientation = driver.orientation
        if current_orientation == "PORTRAIT":
            driver.orientation = "LANDSCAPE"
        else:
            driver.orientation = "PORTRAIT"

    @staticmethod
    def get_xml_tree(driver):
        return driver.execute_script('au.mainApp().getTreeForXML()')

    @staticmethod
    def get_udid():
        """
        Gets list of connected iDevice udid's
        """
        return check_output(["idevice_id", "-l"]).decode("utf-8").strip('\n').split()

    @staticmethod
    def screenshot_fast(driver, name, directory=getcwd()+'/screenshots', udid=None):
        """
        Takes PNG screenshot using command idevicescreenshot
        """
        if not udid:
            udid = environ.get("IDEVICE_UDID") or iOS.get_udid()[-1]

        name = str(name) + '.png'

        try:
            check_output(["idevicescreenshot", "-u", str(udid), directory+'/'+name])
        except CalledProcessError as err:
            print("Error taking screenshot {} in {} with error {}".format(name, dir, err.output))
            return False
        return True

    @staticmethod
    def install_package(package_path, udid=None):
        """
        Install package to the device using 'ideviceinstaller'
        """
        if not udid:
            udid = environ.get("IDEVICE_UDID") or iOS.get_udid()[-1]
        if not exists(package_path):
            print("Package '{}' doesn't exist".format(package_path))
            return False

        try:
            check_output(["ideviceinstaller", "-u", str(udid), "-i", package_path])
            return True
        except CalledProcessError as err:
            print("Error installing package to {} the device {}, msg: {}".format(package_path,
                                                                                 udid,
                                                                                 err))

class NiacinWebDriver(WebDriver):
    def __init__(self, command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=None, browser_profile=None, proxy=None, keep_alive=False):
        print("initting Appium WebDriver..")
        super().__init__(command_executor, desired_capabilities, browser_profile, proxy, keep_alive)

        platform = desired_capabilities['platformName']
        if platform.lower() == "ios":
            print("initting platform as iOS")
            self.platform = iOS()
        elif platform.lower() == "android":
            print("initting platform as Android")
            self.platform = Android()

    def __getattr__(self, function_name):
        def __missing(*args, **kwargs):
            """
            Function to try to check does the function exists in
            the platform instance. If it does then we check does it take
            WebDriver instance and then we inject NiacinWebDriver instance
            as the first element in args (whether there are args or not)
            """
            func = getattr(self.platform, function_name)
            func_args = list(signature(func).parameters.keys())

            if not args and "driver" in func_args:
                args = args + (self, )
            elif "driver" in func_args and not isinstance(self, type(args[0])):
                args = (self, args)
            return func(*args, **kwargs)
        return __missing
