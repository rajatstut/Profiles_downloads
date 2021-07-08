import os
import tarfile
import urllib
import shutil
import glob
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

    def click_ratings_Button(self):
        logging.info("Choosing Good fit option..")
        time.sleep(6)
        self.driver.find_element_by_xpath("//*[@data-control-name='rating_facet_toggle']").click()
        time.sleep(6)
        self.driver.find_element_by_xpath("//*[@data-control-name='rating_facet_toggle']/span/../..//li[1]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath(
            "//*[@data-control-name='rating_facet_toggle']/span/../..//li[3]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@data-control-name='rating_facet_toggle']/span/../..//div//button[@data-control-name='rating_facet_toggle_show_results']").click()
        time.sleep(2)

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


    def wait_for_downloads(self):
        logging.info("Waiting for downloads")
        time.sleep(3)
        filespath = os.path.abspath('..//Automation_Results//')
        list_of_files = glob.glob(filespath+"//*.crdownload")
        while len(list_of_files) != 0 :
            time.sleep(5)
            list_of_files = glob.glob(filespath+"//*.crdownload")         



    def rename_filename_with_candidate(self, filename):
        filespath = os.path.abspath('..//Automation_Results//')
                
        list_of_files = glob.glob(filespath+"//*.pdf")
        list_of_files.extend(glob.glob(filespath+"//*.docx"))
        list_of_files.extend(glob.glob(filespath+"//*.doc"))
        print(list_of_files)        
        latest_file = max(list_of_files, key=os.path.getctime)
        logging.info("file is: " +str(latest_file))      
        if latest_file.endswith('.pdf'):  
            os.rename(latest_file, filespath+"//"+filename+".pdf")
        elif latest_file.endswith('.doc'): 
            os.rename(latest_file, filespath+"//"+filename+".doc")
        else:        
            os.rename(latest_file, filespath+"//"+filename+".docx")


    def fetch_candidate_details(self):
        logging.info("Extracting candidates details ..")
        time.sleep(8)
        self.driver.find_element_by_xpath("//h4/span[text()='Messaging']").click()
        candidate_dictionary = defaultdict(list)
        if self.driver.find_elements_by_xpath("//li[contains(@class,'artdeco-pagination__indicator')]"):
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
                                self.driver.find_element_by_xpath(
                                    "//*[@data-control-name='hiring_applicant_message']/../div[3]//span").click()
                                time.sleep(3)
                                emp_details_email = self.driver.find_element_by_xpath(
                                     "//div[@class='artdeco-dropdown__content-inner']/ul/li[2]/a/div/span[2]").text
                                emp_details_phone = self.driver.find_element_by_xpath(
                                    " //div[@class='artdeco-dropdown__content-inner']/ul/li[3]/div/div/span[2]").text
                                emp_details_name =self.driver.find_element_by_xpath("//*[@class='ph5 pt5 pb3 display-flex justify-space-between']//h1").text
                                emp_details_name =(emp_details_name.split(" application"))
                                candidate_dictionary['Name'].append((emp_details_name[0])[:-2])
                                candidate_dictionary['EmailId'].append(emp_details_email)
                                candidate_dictionary['PhoneNumber'].append(emp_details_phone)
                                time.sleep(3)
                                try:
                                    ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath("//a[text()='Download']")).perform()
                                    self.driver.find_element_by_xpath("//a[text()='Download']").click()
                                    self.wait_for_downloads()
                                    cand_name = str(candidate_dictionary['Name'][index-1]).split(" ")                                    
                                    newfilename = cand_name[0]+"_"+cand_name[1]
                                    logging.info(newfilename)
                                    self.rename_filename_with_candidate(newfilename)
                                except Exception as e:
                                    ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath('//a[contains(@class,"ui-attachment__download-button")]')).perform()
                                    self.driver.find_element_by_xpath('//a[contains(@class,"ui-attachment__download-button")]').click()
                                    self.wait_for_downloads()
                                    cand_name = str(candidate_dictionary['Name'][index-1]).split(" ")                                    
                                    newfilename = cand_name[0]+"_"+cand_name[1]                                    
                                    logging.info(newfilename)
                                    self.rename_filename_with_candidate(newfilename)
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
        else:
            vars = 0
            vare = 100
            no_of_applicants = self.driver.find_element_by_xpath("//div[@class='hiring-applicants__content']//span").text
            no_of_applicants = str(no_of_applicants).split("(")
            no_of_applicants=int(((no_of_applicants[0:2])[1].split(" "))[0])
            for index in range(1, no_of_applicants+1):
                candidate = self.driver.find_element_by_xpath(
                    '//li[contains(@class,"hiring-applicants__list-item")][' + str(index) + ']')
                ActionChains(self.driver).move_to_element(candidate).perform()
                candidate.click()
                time.sleep(1)
                try:
                    element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//button/span[text()='Good fit']"))
                    )
                    rate_as_validation_check = element.text
                    if "Good fit" in rate_as_validation_check:
                        self.driver.find_element_by_xpath(
                            "//*[@data-control-name='hiring_applicant_message']/../div[3]//span").click()
                        time.sleep(3)
                        emp_details_email = self.driver.find_element_by_xpath(
                            "//div[@class='artdeco-dropdown__content-inner']/ul/li[2]/a/div/span[2]").text
                        emp_details_phone = self.driver.find_element_by_xpath(
                            " //div[@class='artdeco-dropdown__content-inner']/ul/li[3]/div/div/span[2]").text
                        emp_details_name = self.driver.find_element_by_xpath(
                            "//*[@class='ph5 pt5 pb3 display-flex justify-space-between']//h1").text
                        emp_details_name = emp_details_name.split(" application")
                        candidate_dictionary['Name'].append((emp_details_name[0])[:-2])
                        candidate_dictionary['EmailId'].append(emp_details_email)
                        candidate_dictionary['PhoneNumber'].append(emp_details_phone)
                        time.sleep(3)
                        try:
                            ActionChains(self.driver).move_to_element(
                                self.driver.find_element_by_xpath("//a[text()='Download']")).perform()
                            self.driver.find_element_by_xpath("//a[text()='Download']").click()
                            self.wait_for_downloads()
                            cand_name = str(candidate_dictionary['Name'][index-1]).split(" ")                            
                            newfilename = cand_name[0]+"_"+cand_name[1]
                            logging.info(newfilename)
                            self.rename_filename_with_candidate(newfilename)
                        except Exception as e:
                            ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath(
                                '//a[contains(@class,"ui-attachment__download-button")]')).perform()
                            self.driver.find_element_by_xpath(
                                '//a[contains(@class,"ui-attachment__download-button")]').click()
                            self.wait_for_downloads()
                            cand_name = str(candidate_dictionary['Name'][index-1]).split(" ")
                            newfilename = cand_name[0]+"_"+cand_name[1]
                            logging.info(newfilename)
                            self.rename_filename_with_candidate(newfilename)
                        time.sleep(3)

                except Exception as e:
                    logging.error(str(e))
                script = "window.scrollTo(" + str(vars) + "," + str(vare) + ")"
                self.driver.execute_script(script)

                vars = int(vars) + 100
                vare = int(vare) + 100

                #self.driver.find_element_by_xpath("//button[@aria-label='Page " + str(page) + "']").click()
                time.sleep(5)
            # except Exception as e:
            #    logging.error(str(e))

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



# obj = JobPage("driver")
# obj.rename_filename_with_candidate("myfile.pdf")
# obj.wait_for_downloads()




