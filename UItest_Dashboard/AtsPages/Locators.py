from selenium.webdriver.common.by import By


class LocatorsPage():

    # Login Page locators
    button_login = (By.XPATH, "//*[@id = '__button2-BDI-content']")
    txt_username = (By.NAME, "username")
    txt_password = (By.NAME, "password")
    Btn_loginBtn = (By.ID, "login-submit")


