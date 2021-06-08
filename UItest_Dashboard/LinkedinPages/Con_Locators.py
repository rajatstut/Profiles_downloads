from selenium.webdriver.common.by import By


class LocatorsPage():

    # Login Page locators
    button_signin = (By.XPATH, "//*[@class='join-form__form-body-subtext']/button")
    txt_username = (By.ID, "login-email")
    txt_password = (By.ID, "login-password")
    Btn_loginBtn = (By.ID, "login-submit")
