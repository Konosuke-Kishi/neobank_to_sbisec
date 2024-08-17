from selenium import webdriver
from selenium.webdriver.common.by import By
from config import CONFIG
import time

class Action:
  
    MONEY = CONFIG['amountOfMoney']
    SBISEC_TRANSACTION_PASSWORD = CONFIG['sbisecTransactionPassword']
    NEOBANK_TRANSACTION_PASSWORD = CONFIG['neobankTransactionPassword']

    def inputMoney(self, driver: webdriver):
        # 入金ボタンを押下 
        driver.find_element(by=By.XPATH, value='//*[@id="link02M"]/ul/li[4]/a/img').click()
        time.sleep(2)
        # 入金額指定
        insert_money = driver.find_element(by=By.NAME, value="FML_TRANSFER_AMOUNT")
        insert_money.send_keys(self.MONEY)
        # 取引パスワード入力
        tra_passwd = driver.find_element(by=By.ID, value="inpPass")
        tra_passwd.send_keys(self.SBISEC_TRANSACTION_PASSWORD)
        # 次へボタン押下
        driver.find_element(by=By.XPATH, value='//*[@id="MAINAREA02_780"]/form[1]/div/div/div/div/div/div[2]/a/img').click()
        time.sleep(2)
        # 振込指示ボタン押下
        driver.find_element(by=By.XPATH, value='//*[@id="MAINAREA02_780"]/div[4]/ul/li[1]/form/a/input').click()

    def transactionCommit(self, driver: webdriver):
        # 取引パスワード入力
        tra_passwd = driver.find_element(by=By.ID, value="toriPwd")
        tra_passwd.send_keys(self.NEOBANK_TRANSACTION_PASSWORD)
        # 確定ボタン押下
        driver.find_element(by=By.XPATH, value='/html/body/app/div/ng-component/div/main/ng-component/section[2]/div/ul/li/nb-button/a').click()
