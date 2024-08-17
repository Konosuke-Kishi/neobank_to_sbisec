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

    # SBI証券のトップページを開く
    driver.get("https://site3.sbisec.co.jp/ETGate/")
    time.sleep(2)
    login.sbiSecLoginFlow(driver)
    time.sleep(2)
    action.inputMoney(driver)
    time.sleep(2)
    login.neoBankLoginFlow(driver)
    time.sleep(2)
    action.transactionCommit(driver)
    time.sleep(2)  

    driver.quit()

  if __name__ == "__main__":
      main()
