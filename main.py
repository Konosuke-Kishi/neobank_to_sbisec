from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from login import Login
from action import Action
import time

class Main:
    
  def main():
    login = Login()
    action = Action()
    options = Options()
    ## ヘッドレス設定
    options.add_argument("--headless=new")
    service = Service(executable_path="/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://site3.sbisec.co.jp/ETGate/?OutSide=on&_ControlID=WPLETsmR001Control&_DataStoreID=DSWPLETsmR001Control&sw_page=Banking&cat1=home&cat2=none&getFlg=on&int_pr1=150313_cmn_gnavi:3_dmenu_01")
    time.sleep(3)
    login.sbiSecLoginFlow(driver)
    time.sleep(3)
    action.inputMoney(driver)
    time.sleep(3)
    login.neoBankLoginFlow(driver)
    time.sleep(3)
    action.transactionCommit(driver)
    time.sleep(3)  

    driver.quit()

  if __name__ == "__main__":
      main()
