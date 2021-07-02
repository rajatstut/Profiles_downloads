import os
import time

from UItest_Dashboard.CommonPages.basePage import BasePage
import json
import pytest
from UItest_Dashboard.LinkedinPages.Con_Locators import LocatorsPage
import logging

class LoginPage():
    logging.basicConfig(level=logging.INFO)

    '''
    Page object for the login page
    '''


    def __init__(self, driver):
        self.driver = driver
        self.con_url = BasePage.base_url

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


    def click_sign_in(self,driver):
        logging.info("clicking sign-in button")
        time.sleep(10)
        self.driver.find_element(by=LocatorsPage.button_signin[0], value = LocatorsPage.button_signin[1]).click()
        logging.info("sign-in button clicked")

    def send_credentials(self, usr, passw):
        logging.info("Passing credentials...")
        self.driver.find_element(by=LocatorsPage.txt_username[0], value=LocatorsPage.txt_username[1]).send_keys(usr)
        logging.info("Username entered")
        self.driver.find_element(by=LocatorsPage.txt_password[0], value=LocatorsPage.txt_password[1]).send_keys(passw)
        logging.info("Password entered")
        self.driver.find_element(by=LocatorsPage.Btn_loginBtn[0], value=LocatorsPage.Btn_loginBtn[1]).click()
        logging.info("Login in button clicked")

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
