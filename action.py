from selenium import webdriver
from selenium.webdriver.common.by import By
from config import CONFIG
import time

class Action:
  
    MONEY = CONFIG['amountOfMoney']
    SBISEC_TRANSACTION_PASSWORD = CONFIG['sbisecTransactionPassword']
    NEOBANK_TRANSACTION_PASSWORD = CONFIG['neobankTransactionPassword']

    def inputMoney(self, driver: webdriver):
        # 入金額指定
        insert_money = driver.find_element(by=By.NAME, value="FML_TRANSFER_AMOUNT")
        insert_money.send_keys(self.MONEY)
        #取引パスワード入力
        tra_passwd = driver.find_element(by=By.ID, value="inpPass")
        tra_passwd.send_keys(self.SBISEC_TRANSACTION_PASSWORD)
        driver.find_element(by=By.XPATH, value="//img[contains(@alt,'次へ（入金指示確認）')]").click()
        time.sleep(2)
        driver.find_element(by=By.XPATH, value="//input[contains(@alt,'振込指示')]").click()
        time.sleep(2)
        # ウィンドウハンドルを取得する
        newhandles = driver.window_handles
        # driverでの操作できるウインドウを切り替える
        driver.switch_to.window(newhandles [1])

    def transactionCommit(self, driver: webdriver):
        #取引パスワード入力
        tra_passwd = driver.find_element(by=By.ID, value="toriPwd")
        tra_passwd.send_keys(self.NEOBANK_TRANSACTION_PASSWORD)
        driver.find_element(by=By.XPATH, value="//nb-button[contains(@nblabel,'確定する')]").click()
