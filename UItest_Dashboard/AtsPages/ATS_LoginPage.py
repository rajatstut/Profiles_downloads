import os
import time

from UItest_Dashboard.CommonPages.basePage import BasePage
import json
import pytest
from UItest_Dashboard.AtsPages.Locators import LocatorsPage
import logging

class ATS_LoginPage():
    logging.basicConfig(level=logging.INFO)

    '''
    Page object for the login page
    '''


    def __init__(self, driver):
        self.driver = driver
        with open('config.json', 'r') as data:
            config = json.load(data)
        self.con_url =driver.get(config["ats"]["base_url"])

    def ats_url(self):
        with open('config.json', 'r') as data:
            config = json.load(data)
        #self.driver.get(config["ats"]["base_url"])
        self.driver.get("https://hcm44.sapsf.com/login#/login")

    def removing_file_previous_run(self):
        script_dir = os.path.dirname(__file__)
        script_dir = os.path.abspath(os.path.join(script_dir, os.pardir)).replace("\\", "/")
        script_dir = script_dir + '/Automation_Results'
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
            else:
                pass
        logging.info("All existing files deleted..")


    def click_Login_in(self):
        logging.info("clicking sign-in button")
        time.sleep(10)
        self.driver.find_element(by=LocatorsPage.button_login[0], value = LocatorsPage.button_login[1]).click()
        logging.info("sign-in button clicked")

    def enter_companyID(self):
        logging.info("Entering company's id")
        self.driver.find_element_by_xpath("//*[@id = '__input0-inner']").send_keys("incedotech")
        time.sleep(8)
        self.driver.find_element_by_xpath("//*[@id ='__button0-inner']/span").click()
        time.sleep(2)

    def send_credentials(self, usr, passw):
        logging.info("Passing credentials...")
        self.enter_companyID()
        self.driver.find_element(by=LocatorsPage.txt_username[0], value=LocatorsPage.txt_username[1]).send_keys(usr)
        logging.info("Username entered")
        self.driver.find_element(by=LocatorsPage.txt_password[0], value=LocatorsPage.txt_password[1]).send_keys(passw)
        logging.info("Password entered")
        self.driver.find_element(by=LocatorsPage.button_login[0], value=LocatorsPage.button_login[1]).click()
        logging.info("Login in button clicked")
        time.sleep(8)

    # def valid_login(self):
    #     with open('E:/End-to-End/UItest_Dashboard/tests/config.json') as data:
    #          config = json.load(data)
    #     self.send_credentials(config["connect"]["user"], config["connect"]["password"])

    def check_login(self):
        logging.info("Validating url..")
        assert self.con_url in self.driver.current_url

    def close_instance(self):
        self.driver.close()
        logging.info("Closing instance..")
