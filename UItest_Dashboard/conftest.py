import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import json
import pytest

from utils.update_chromedriver import getBrowserVesionWindows, getChromeDriverVesionWindows, downloadChromeDriverZip, \
    killProcess


def pytest_runtest_setup():
    removing_file_previous_run()
    script_dir = os.path.dirname(__file__)
    script_dir = os.path.abspath(os.path.join(script_dir, os.pardir)).replace("\\", "/").replace("/UItest_Dashboard",
                                                                                                 "")
    script_dir = script_dir + "/driver_path"
    with open('config.json', 'r') as data:
        config = json.load(data)
    ver1 = getBrowserVesionWindows()
    getChromeDriverVesionWindows()
    killProcess("windows")
    downloadChromeDriverZip(ver1, script_dir, "windows")

    '''
    Set up for each test case pre-execution
    '''
    #config file
    print("Launching Url..")
    with open('../../UItest_Dashboard/tests/config.json') as data:
        config = json.load(data)

    '''
    Select the driver using the config.json file.
    To add support for a new driver just add it here.
    '''
    global driver

    if config["linkedin"]["driver"] == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--start-maximized")
        download_dir = os.path.abspath(r"..\..\UItest_Dashboard\Automation_Results\\")
        print(download_dir)
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": download_dir,  # IMPORTANT - ENDING SLASH V IMPORTANT
                 "directory_upgrade": True}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=chrome_options, executable_path="../../driver_path/chromedriver.exe")
        #driver.implicitly_wait(30)
        print("Chrome browser selected..")
    elif config["connect"]["driver"] == "firefox":
        driver = webdriver.Firefox()
        print("Firefox browser selected..")
    else:
        print("invalid driver, please check the driver configuration in config.json or conftest.py")

    #Set up of the driver
    driver.get(config["linkedin"]["base_url"])
    # driver.maximize_window()
    #assert driver.current_url == config["connect"]["base_url"]
    assert config["linkedin"]["base_url"] in driver.current_url
    return driver

#@pytest.fixture(scope='session')
def removing_file_previous_run():
    script_dir = os.path.dirname(__file__)
    script_dir = os.path.abspath(os.path.join(script_dir, os.pardir)).replace("\\", "/")
    script_dir = script_dir + '/UItest_Dashboard/Automation_Results/'
    files = os.listdir(script_dir)
    for file in files:
        if file.endswith(".pdf"):
            os.remove(script_dir + '/' + file)
            print("File Removed!")
        if file.endswith(".xlsx"):
            os.remove(script_dir + '/' + file)
            print("File Removed!")
        if file.endswith(".docx"):
            os.remove(script_dir + '/' + file)
            print("File Removed!")
        if file.endswith(".doc"):
            os.remove(script_dir + '/' + file)
            print("File Removed!")
        else:
            pass

# @pytest.fixture(scope='session')
# def removing_file_previous_run():
#     script_dir = os.path.dirname(__file__)
#     script_dir = os.path.abspath(os.path.join(script_dir, os.pardir)).replace("\\", "/")
#     script_dir = script_dir + '/Automation_Results'
#     files = os.listdir(script_dir)
#     for file in files:
#         if file.endswith(".pdf"):
#             os.remove(script_dir + '/' + file)
#             print("File Removed!")
#         if file.endswith(".xlsx"):
#             os.remove(script_dir + '/' + file)
#             print("File Removed!")
#         if file.endswith(".docx"):
#             os.remove(script_dir + '/' + file)
#             print("File Removed!")
#         if file.endswith(".doc"):
#             os.remove(script_dir + '/' + file)
#             print("File Removed!")
#         else:
#             pass

@pytest.fixture(scope='session', autouse=True)
def ptest_driver():
    global driver
    '''
    Hook for passing down the driver
    '''
    # return pytest_runtest_setup()
    return driver
