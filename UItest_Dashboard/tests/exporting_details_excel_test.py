import os

import pytest

from UItest_Dashboard.AtsPages.ATS_HomePage import ATS_HomePage
from UItest_Dashboard.LinkedinPages.Con_LoginPage import LoginPage
from UItest_Dashboard.LinkedinPages.Con_HomePage import HomePage
from UItest_Dashboard.LinkedinPages.Profile_Page import JobPage
from UItest_Dashboard.AtsPages.ATS_LoginPage import ATS_LoginPage
import json

from utils.update_chromedriver import getBrowserVesionWindows, getChromeDriverVesionWindows, downloadChromeDriverZip


def test_basicFunctionality(ptest_driver):
    with open('config.json', 'r') as data:
        config = json.load(data)
    loginPage = LoginPage(ptest_driver)

    loginPage.removing_file_previous_run()
    loginPage.click_sign_in(ptest_driver)
    loginPage.send_credentials(config["linkedin"]["user"], config["linkedin"]["password"])
    homePage = HomePage(ptest_driver)
    homePage.click_Jobs()
    homePage.click_My_Jobs()
    homePage.click_Posted_Jobs()
    jobpage = JobPage(ptest_driver)
    jobpage.click_first_posted_job()
    jobpage.click_ratings_Button()
    candidate_details = jobpage.fetch_candidate_details()
    jobpage.export_data_to_excel(dict(candidate_details))

    ats_loginPage = ATS_LoginPage(ptest_driver)
    ats_loginPage.ats_url()
    ats_loginPage.send_credentials(config["ats"]["user"],config["ats"]["password"])
    ats_homePage = ATS_HomePage(ptest_driver)
    ats_homePage.click_Home_button()
    ats_homePage.click_careers_option()
    ats_homePage.searching_job()
    ats_homePage.referral_details(candidate_details)
    loginPage.close_instance()
