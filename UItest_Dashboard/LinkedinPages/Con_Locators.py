from selenium.webdriver.common.by import By


class LocatorsPage():

    # Login Page locators
    button_signin = (By.XPATH, "//*[@class='authwall-join-form__swap-cta']/button")
    txt_username = (By.ID, "session_key")
    txt_password = (By.ID, "session_password")
    Btn_loginBtn = (By.XPATH, "//*[@class='sign-in-form__submit-button']")
    # txt_username = (By.ID, "session_key")
    # txt_password = (By.ID, "session_password")
    # Btn_loginBtn = (By.XPATH, "//*[@class='sign-in-form__submit-button']")
