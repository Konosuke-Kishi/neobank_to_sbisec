from selenium import webdriver
from selenium.webdriver.common.by import By
from config import CONFIG
import time
import sys

class Login:

    SBI_SEC_LOGIN_ID = CONFIG['userId']
    SBI_SEC_PASSWORD = CONFIG['password']
    NEOBANK_USERNAME = CONFIG['mailAddress']
    NEOBANK_PASSWORD = CONFIG['neoBankPassword']

    def sbiSecLoginFlow(self, driver: webdriver):
        # ユーザ名入力
        userid = driver.find_element(by=By.NAME, value="user_id")
        userid.send_keys(self.SBI_SEC_LOGIN_ID)
        # パスワード入力
        password = driver.find_element(by=By.NAME, value="user_password")
        password.send_keys(self.SBI_SEC_PASSWORD)
        # ログインボタン押下
        driver.find_element(by=By.NAME, value="ACT_login").click()

    def neoBankLoginFlow(self, driver: webdriver):
        # ウィンドウハンドルを取得する
        newhandles = driver.window_handles
        # driverでの操作できるウインドウを切り替える
        driver.switch_to.window(newhandles [1])
        # 支店選択
        args = sys.argv
        if args[1] == "t":
            driver.find_element(by=By.ID, value="tneobank-login").click()
        else:
            driver.find_element(by=By.ID, value="dlbneobank-login").click()  
        time.sleep(2)
        # ユーザ名入力
        username = driver.find_element(by=By.ID, value="userNameNewLogin")
        username.send_keys(self.NEOBANK_USERNAME)
        # パスワード入力
        neopassword = driver.find_element(by=By.ID, value="loginPwdSet")
        neopassword.send_keys(self.NEOBANK_PASSWORD)
        # ログインボタン押下
        driver.find_element(by=By.CLASS_NAME, value="m-btnEm-l").click()
    