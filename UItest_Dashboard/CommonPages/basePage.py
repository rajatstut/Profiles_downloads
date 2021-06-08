from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import json
import csv
from UItest_Dashboard.LinkedinPages.Con_Locators import LocatorsPage


class BasePage(object):

    def __init(self, Name):
        self.Name = Name


    '''
    Base class with some common used methods for every page object to inherit
    '''

    with open('../../UItest_Dashboard/tests/config.json') as data:
        config = json.load(data)
    base_url = config["linkedin"]["base_url"]

    def current_url(self):
        '''
        Method for getting the current browser url
        :return: url
        '''
        return self.driver.current_url

    def open(self, url):
        '''
        Method for opening a url
        :param url: url to open
        '''
        self.driver.get(url)

    def close(self, url):
        self.driver.close

    def wait(self, loc):
        '''
        Method for waiting until the element is clickable
        :param loc: element to wait for
        :return: throws a error with the element if the method can't find it
        '''
        try:
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(loc))
        except:
            print ("can't find the element " + str(loc))


    def check_if_element_was_removed(self, *loc):
        '''
        Method for checking if an element was removed from the page
        :param loc: locator of the element
        :return: raise an error if the elements is in the page
        '''

        try:
            self.driver.find_element(*loc)
        except NoSuchElementException:
            return False
        return True

    def check_if_element_is_visible(self, loc):
        '''
        Method for checking the visibility of an given element
        :param loc: locator of the element
        :return: raise an assertion erorr if the element is not visible
        '''
        self.wait(loc)
        assert self.driver.find_element(*loc).is_displayed() == True

    def close(self):
        '''
        method for closing the browser
        '''
        self.driver.close()

    def wait_for_elements(self, obj):
        '''
        Method for waiting until all elements in the list elements of a given object are find
        :param obj: object from where the method get the list elments
        :return: raise an error with the element the method can't find
        '''
        i = 0

        while i < len(obj.elements):

            try:
                WebDriverWait(self.driver, 30).until(
                    EC.visibility_of_element_located(obj.elements[i]))
            except:
                print("cant find the element number: " + str(i))

            i += 1

    def wait_imp(self):
        '''
        Method for implicitly waiting
        '''
        self.driver.implicitly_wait(3)


    def frame_switch(self):
        self.driver.switch_to.frame(self.driver.find_element(LocatorsPage.frame_dashboard[0]),LocatorsPage.frame_dashboard[1])

    def switch_back(self):
        self.driver.switch_to.default_content()




