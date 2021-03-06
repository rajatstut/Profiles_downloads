import os
import time
import glob
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from UItest_Dashboard.CommonPages.basePage import BasePage
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from UItest_Dashboard.AtsPages.Locators import LocatorsPage
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import walk

class ATS_HomePage():
    logging.basicConfig(level=logging.INFO)

    '''
    Page object for the login page
    '''


    def __init__(self, driver):
        self.driver = driver
        # with open('config.json', 'r') as data:
        #     config = json.load(data)
        # self.con_url =driver.get(config["ats"]["base_url"])

    def click_Home_button(self):
        time.sleep(3)
        self.driver.find_element_by_xpath("//*[@id ='customHeaderModulePickerBtn-BDI-content']").click()
        logging.info("Home button clicked..")

    def click_careers_option(self):
        time.sleep(3)
        self.driver.find_element_by_xpath("//*[@id = 'customHeaderModulePickerBtn-menuPopover-scroll']//a[2]").click()
        logging.info("Careers clicked..")

    def searching_job(self):
        time.sleep(2)
        with open('config.json', 'r') as data:
            config = json.load(data)
        self.driver.find_element_by_xpath("//*[@name='reqnumber']").send_keys(config["ats"]["requisition_ID"])
        time.sleep(3)
        self.driver.find_element_by_xpath("//*[@class='activeAccessible fioriBtn active']//button").click()
        time.sleep(5)

    def referring_friend(self):
        element = WebDriverWait(self.driver, 15).until(
                                EC.presence_of_element_located((By.XPATH, "//*[@class='sfContextualMenu globalPortletLinkTextColor']/*[contains(text(),'Select Action')]"))
                            )

        element.click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@class='sf-PopMenu']/li[4]").click()
        time.sleep(3)

    def referral_details(self, candidate_details):
        for i in range(len(candidate_details['Name'])):
            self.referring_friend()
            cand_name = str(candidate_details['Name'][i]).split(" ")
            self.driver.find_element_by_xpath("//*[@title = 'First Name']").send_keys(cand_name[0])
            self.driver.find_element_by_xpath("//*[@title = 'Last Name']").send_keys(cand_name[1])
            self.driver.find_element_by_xpath("//*[@title = 'Email']").send_keys(candidate_details['EmailId'][i])
            self.driver.find_element_by_xpath("//*[@title = 'Phone']").send_keys(candidate_details['PhoneNumber'][i])
            select = Select(self.driver.find_element_by_xpath("//*[@class='sfCascadingPicklist']/select"))
            select.select_by_visible_text("India")
            logging.info("Country selected")

            script_dir = os.path.dirname(__file__)
            script_dir = os.path.abspath(os.path.join(script_dir, os.pardir)).replace("\\", "/")
            script_dir = script_dir + "/Automation_results"
            files_details = next(walk(script_dir), (None, None, []))[2]
            for j in range(len(files_details)):                
                if cand_name[0] in str(files_details[j]) and cand_name[1] in str(files_details[j]) :
                    self.driver.find_element_by_xpath("//*[@name = 'fileData1']").send_keys(script_dir+ "/"+ files_details[j])
                else:
                    print("Records can't be submitted")

            self.driver.find_element_by_xpath("//span[contains(@class,'sfDialogBoxButtonWrapper')]//button[text()='Send']").click()
            time.sleep(2)
            '''
            message = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[@class='important-focus-msg']")))
            '''
            try:
                message = self.driver.find_element_by_xpath("//*[@class='panelContent globalPortletBody']").text
            except:
                print("Okay")
            #if "successfully" in message.text:
            if "exists" in message:
                self.driver.find_element_by_xpath("//*[@class='buttonset sfDialogBoxButtonWrapper active']/span").click()
                print ("Profile exists")
                self.driver.find_element_by_xpath("//button[text()='Cancel']").click()
                time.sleep(4)
            else:
                self.driver.find_element_by_xpath("//button[text()='Cancel']").click()
                time.sleep(4)

    def check_login(self):
        logging.info("Validating url..")
        assert self.con_url in self.driver.current_url

    def close_instance(self):
        self.driver.close()
        logging.info("Closing instance..")
