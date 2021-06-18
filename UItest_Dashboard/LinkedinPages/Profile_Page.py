import os
import tarfile
import urllib
import shutil
import datetime
import requests
from pandas import DataFrame, ExcelWriter
import time
import logging
from collections import defaultdict
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JobPage():
    filename = os.path.abspath('../../UItest_Dashboard/Automation_Results/report.log.')
    logging.basicConfig(filename=filename, level=logging.INFO)

    def __init__(self, driver):
        self.driver = driver

    def click_first_posted_job(self):
        logging.info("Clicking first job")
        time.sleep(5)
        self.driver.find_element_by_xpath("//h3[contains(text(),'Posted Jobs')]/../ul/li").click()

    # def click_ratings_Button(self):
    #     logging.info("Choosing Good fit option..")
    #     time.sleep(6)
    #     self.driver.find_element_by_xpath("//*[@data-control-name='rating_facet_toggle']/span").click()
    #     self.driver.find_element_by_xpath("//*[@data-control-name='rating_facet_toggle']/span/../../div").click()


    def export_data_to_excel(self, employee_dict):
        now = str(datetime.datetime.now())[:19]
        now = now.replace(":", "_")
        myDF = DataFrame(employee_dict)        
        writer = ExcelWriter(os.path.abspath("..//..//UItest_Dashboard//Automation_Results//Employee_details-" +str(now)+ ".xlsx"))
        myDF.to_excel(writer)
        writer.save()

    def click_More_tab(self):
        time.sleep(4)
        self.driver.find_element_by_xpath("//*[@data-control-name='hiring_applicant_rate']//span/../../../../div[3]//span[1]").click()

        
    def fetch_candidate_details(self):
        logging.info("Extracting candidates details ..")
        time.sleep(8)
        self.driver.find_element_by_xpath("//h4/span[text()='Messaging']").click()
        candidate_dictionary = defaultdict(list)        
        pages = self.driver.find_elements_by_xpath("//li[contains(@class,'artdeco-pagination__indicator')]")
        totalpages = len(pages)+2
        logging.info("Total Pages are :"+str(totalpages))        
        try:  
            for page in range(2,totalpages):
                #self.driver.refresh()
                vars = 0
                vare = 100
                for index in range(1,26) :
                    candidate = self.driver.find_element_by_xpath('//li[contains(@class,"hiring-applicants__list-item")]['+str(index)+']')
                    ActionChains(self.driver).move_to_element(candidate).perform()
                    candidate.click()
                    time.sleep(1)
                    try:
                        element = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, "//button/span[text()='Good fit']"))
                        )
                        rate_as_validation_check = element.text
                        if "Good fit" in rate_as_validation_check:
                            # self.driver.find_element_by_xpath(
                            # "//*[@data-control-name='hiring_applicant_rate']//span/../../../../div[3]//span[1]").click()
                            self.driver.find_element_by_xpath(
                                "//*[@data-control-name='hiring_applicant_message']/../div[3]//span").click()
                            time.sleep(3)
                            # emp_details = self.driver.find_element_by_xpath(
                            # "//*[@data-control-name='hiring_applicant_rate']//span/../../../../div[3]/div").text
                            emp_details_email = self.driver.find_element_by_xpath(
                                 "//div[@class='artdeco-dropdown__content-inner']/ul/li[2]/a/div/span[2]").text
                            emp_details_phone = self.driver.find_element_by_xpath(
                                " //div[@class='artdeco-dropdown__content-inner']/ul/li[3]/div/div/span[2]").text
                            # candidate_details_list = str(
                            # emp_details).split("\n")
                            candidate_dictionary['EmailId'].append(emp_details_email)
                            candidate_dictionary['PhoneNumber'].append(emp_details_phone)
                            time.sleep(3)
                            try:                            
                                ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath("//a[text()='Download']")).perform()
                                self.driver.find_element_by_xpath("//a[text()='Download']").click()    
                            except Exception as e:                                            
                                ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath('//a[contains(@class,"ui-attachment__download-button")]')).perform()
                                self.driver.find_element_by_xpath('//a[contains(@class,"ui-attachment__download-button")]').click()
                            time.sleep(3)
                    except Exception as e:
                        logging.error(str(e))
                    script = "window.scrollTo("+ str(vars) +","+ str(vare) + ")"
                    self.driver.execute_script(script)
                                                        
                    vars = int(vars)+100
                    vare = int(vare)+100
            
                self.driver.find_element_by_xpath("//button[@aria-label='Page "+str(page)+"']").click()
                time.sleep(5)
        except Exception as e:
            logging.error(str(e))
        
        return candidate_dictionary


    def fetching_candidates_details(self):
        logging.info("Extracting candidates details ..")        
        candidate_dictionary = defaultdict(list)
        time.sleep(3)
        self.driver.maximize_window()
        self.driver.find_element_by_xpath(
            "//*[@class='msg-overlay-bubble-header__controls display-flex']//*[@type='chevron-down-icon']").click()
        time.sleep(3)
        list_candidates = self.driver.find_element_by_xpath("//*[@class='hiring-applicants__list-container']/ul")
        count_of_child = len(list_candidates.find_elements_by_xpath("./li"))
        for i in range(1,count_of_child):
            self.driver.find_element_by_xpath(
                "//ul[@class='artdeco-list']/li[%d]" % (i,)).click()
            rate_as_validation_check= self.driver.find_element_by_xpath("//*[@data-control-name='hiring_applicant_rate']//span").text
            if "Good fit" in rate_as_validation_check:
                try:
                    time.sleep(3)
                    self.driver.find_element_by_xpath(
                        "//*[@data-control-name='hiring_applicant_rate']//span/../../../../div[3]//span[1]").click()
                    emp_details = self.driver.find_element_by_xpath(
                        "//*[@data-control-name='hiring_applicant_rate']//span/../../../../div[3]/div").text
                    candidate_details_list = str(
                        emp_details).split("\n")
                    candidate_dictionary['EmailId'].append(candidate_details_list[2])
                    candidate_dictionary['PhoneNumber'].append(candidate_details_list[5])
                    #url =self.driver.current_url
                    self.fetch_data_from_profile()
                except IndexError:
                    print("Handling Index error")
        return candidate_dictionary


    def fetch_data_from_profile(self):
        time.sleep(2)
        try:
            if self.driver.find_element_by_xpath("//*[@data-control-name='hiring_applicant_resume_pdf_download']") :
                self.driver.find_element_by_xpath("//*[@data-control-name='hiring_applicant_resume_pdf_download']").click()
            else:
                self.driver.execute_script("window.scrollTo(0, 1000)")
                element=self.driver.find_element_by_xpath("//*[contains(@class, 'ui-attachment__download-button display-flex justify-center align-items-center')][last()]").click()
                element.location_once_scrolled_into_view
        except NoSuchElementException:
            pass









