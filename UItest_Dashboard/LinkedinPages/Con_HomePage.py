
from UItest_Dashboard.LinkedinPages.Con_Locators import LocatorsPage
import time
import logging



class HomePage():
    logging.basicConfig(level=logging.INFO)

    '''
    Page object for the Home page
    '''


    def __init__(self, driver):
        self.driver = driver

    def homePage_logout(self):
        self.driver.find_element(LocatorsPage.arrow_administrator[0],LocatorsPage.arrow_administrator[1]).click()
        time.sleep(2)
        self.driver.find_element(LocatorsPage.link_Logout[0], LocatorsPage.link_Logout[1]).click()
        logging.info("Logged out successfully..")

    def click_App(self, appName):
        logging.info("Clicking " + appName+" app")
        self.driver.find_element_by_xpath("//*[contains(text(),'"+appName+"')]").click()

    def click_Jobs(self):
        logging.info("Clicking Jobs button")
        time.sleep(12)
        self.driver.find_element_by_xpath("//*[@class='global-nav__primary-link-text']/../../../li[3]").click()

    def click_My_Jobs(self):
        logging.info("Clicking My Jobs..")
        time.sleep(10)
        self.driver.find_element_by_xpath("//*[@href = 'https://www.linkedin.com/my-items/saved-jobs']/span[1]").click()

    def click_Posted_Jobs(self):
        logging.info("Clicking Posted Jobs..")
        time.sleep(8)
        self.driver.find_element_by_xpath("//a[@data-control-name='myitems_all_postedjobs']").click()

    def click_closed_jobs(self):
        logging.info("Clicking closed jobs..")
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@class='search-reusables__primary-filter'][3]/button").click()
