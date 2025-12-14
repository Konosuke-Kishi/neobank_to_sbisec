# ======================================================
# ライブラリ
# ======================================================
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config import CONFIG
import time, datetime, logging, os
import chromedriver_autoinstaller

# ======================================================
# 設定ファイル（config.py）の読み込み
# ======================================================
# 使用するブラウザの種類
USE_BROWSER = CONFIG['useBrowser']
# Chromeユーザプロファイルの格納先パス
CHROME_USER_DATA_DIR = CONFIG['chromeUserDataDir']
# Firefoxユーザプロファイルの格納先パス
FIREFOX_USER_DATA_DIR = CONFIG['FirefoxUserDataDir']
# SBI証券情報
SBI_SEC_USERNAME = CONFIG['sbisecUserName']
SBI_SEC_PASSWORD = CONFIG['sbisecPassword']
SBI_SEC_TRAN_PWD = CONFIG['sbisecTranPassword']
SBI_SEC_MONEYAMT = CONFIG['sbisecAmountOfMoney']
# NEOBANK情報
NEOBANK_USERNAME = CONFIG['neobankUserName']
NEOBANK_PASSWORD = CONFIG['neoBankPassword']
NEOBANK_TRAN_PWD = CONFIG['neobankTranPassword']
# XPATH一覧
XPATH_INPUT_AMOUNT = CONFIG['xpath_input_amount']
XPATH_INPUT_TRANPW = CONFIG['xpath_input_tran_pw']
XPATH_CHK_TRAN = CONFIG['xpath_check_tran']
XPATH_EXE_TRAN = CONFIG['xpath_execute_tran']
XPATH_CMT_TRAN = CONFIG['xpath_commit_tran']
XPATH_LOGIN_BUTTON = CONFIG['xpath_login_button']
XPATH_AUTH_BUTTON = CONFIG['xpath_auth_button']

# ======================================================
# ログ削除メソッド(cron.pyから呼び出される)
# ======================================================
# 月初にログを削除する
def delete_auto_payment_log():
  # 今日の日付を取得
  today = datetime.date.today()
  # 今月の初日を取得
  first_date_month = today.replace(day=1)
  # 月初ならログファイル削除
  if(today == first_date_month):
    os.remove('./auto_payment.log')

# ======================================================
# ドライバの設定
# ======================================================
# 使用するブラウザのバージョンと一致するdriverをダウンロードし
# ブラウザごとにオプション・プロファイルを設定する
if(USE_BROWSER == "Firefox"):
  executable_path = "/usr/local/bin/geckodriver"
  options = webdriver.FirefoxOptions()
  options.add_argument('--disable-popup-blocking')
  options.add_argument("-profile")
  options.add_argument(FIREFOX_USER_DATA_DIR)
  service = webdriver.firefox.service.Service(executable_path=executable_path)
else:
  executable_path = chromedriver_autoinstaller.install()
  options = webdriver.ChromeOptions()
  options.add_argument('--disable-popup-blocking')
  options.add_argument("--user-data-dir=" + CHROME_USER_DATA_DIR)
  service = webdriver.chrome.service.Service(executable_path=executable_path)

# ======================================================
# 定額自動入金のメイン処理
# ======================================================
def auto_payment():

  # ======================================================
  # 0. 起動設定
  # ======================================================
  # ログ出力設定
  logging.basicConfig(
  # ログを保存するファイル名
  filename='auto_payment.log',
  # ログレベル（INFO以上を記録）
  level=logging.INFO,
  # ログ出力のフォーマット形式
  format='%(asctime)s - %(levelname)s - %(message)s'
  )
  # ブラウザを開く
  logging.info("==========処理開始==========")
  # 使用するブラウザによって分岐
  if(USE_BROWSER == "Firefox"):
    driver = webdriver.Firefox(options=options, service=service)
  else:
    driver = webdriver.Chrome(options=options, service=service)
  logging.info("WebDriver：ブラウザ起動完了")

  # ======================================================
  # 1. SBI証券ログイン処理
  # ======================================================
  # SBI証券のログインページを開く
  driver.get("https://login.sbisec.co.jp/login/")
  logging.info("WebDriver：サイトアクセス成功")
  time.sleep(2)
  # SBI証券のユーザ名入力
  userid = driver.find_element(by=By.NAME, value="username")
  userid.send_keys(SBI_SEC_USERNAME)
  logging.info("SBI証券：ユーザ名入力")
  # SBI証券のログインパスワード入力
  password = driver.find_element(by=By.NAME, value="password")
  password.send_keys(SBI_SEC_PASSWORD)
  logging.info("SBI証券：ログインパスワード入力")
  # SBI証券のログインボタン押下
  driver.find_element(by=By.ID, value="pw-btn").click()
  logging.info("SBI証券：ログイン成功")
  time.sleep(2)

  # ======================================================
  # 2. SBI証券振込指示処理
  # ======================================================
  # SBI証券の入金ボタンを押下
  driver.find_element(by=By.LINK_TEXT, value='入金').click()
  logging.info("SBI証券：入金ページ遷移")
  time.sleep(2)
  # SBI証券の入金額を入力
  input_money = driver.find_element(by=By.XPATH, value=XPATH_INPUT_AMOUNT)
  input_money.send_keys(SBI_SEC_MONEYAMT)
  logging.info("SBI証券：金額入力")
  # SBI証券の取引パスワード入力
  input_tran_passwd = driver.find_element(by=By.XPATH, value=XPATH_INPUT_TRANPW)
  input_tran_passwd.send_keys(SBI_SEC_TRAN_PWD)
  logging.info("SBI証券：取引パスワード入力")
  # SBI証券の入金指示確認ボタン押下
  insert_money_check = driver.find_element(by=By.XPATH, value=XPATH_CHK_TRAN)
  insert_money_check.send_keys(Keys.SPACE)
  logging.info("SBI証券：入金指示確認ボタン押下")
  time.sleep(2)
  # SBI証券の入金指示ボタン押下
  insert_money_execute = driver.find_element(by=By.XPATH, value=XPATH_EXE_TRAN)
  insert_money_execute.send_keys(Keys.SPACE)
  logging.info("SBI証券：入金指示完了")
  time.sleep(2)

  # ======================================================
  # 3. 住信SBIネット銀行ログイン処理
  # ======================================================
  # ウインドウを切り替える
  newhandles = driver.window_handles
  driver.switch_to.window(newhandles[1])
  logging.info("NEOBANK：ウィンドウ切替成功")
  # 支店選択
  driver.find_element(by=By.LINK_TEXT, value="Vポイント支店").click()
  logging.info("NEOBANK：支店選択")
  time.sleep(2)
  # 住信SBIネット銀行のユーザ名を入力
  username = driver.find_element(by=By.XPATH, value="//input[@id='username']")
  username.send_keys(NEOBANK_USERNAME)
  logging.info("NEOBANK：ユーザ名入力")
  # ログインボタン押下
  driver.find_element(by=By.XPATH, value=XPATH_LOGIN_BUTTON).click()
  logging.info("NEOBANK：ログインボタン押下")
  time.sleep(3)
  # 住信SBIネット銀行のログインパスワード入力
  neopassword = driver.find_element(by=By.ID, value="loginPwd")
  neopassword.send_keys(NEOBANK_PASSWORD)
  logging.info("NEOBANK：ログインパスワード入力")
  # ログインボタン押下
  driver.find_element(by=By.XPATH, value=XPATH_AUTH_BUTTON).click()
  logging.info("NEOBANK：ログイン成功")
  time.sleep(3)

  # ======================================================
  # 4. 住信SBIネット銀行入金確定処理
  # ======================================================
  # 住信SBIネット銀行の入金確定ボタン押下
  driver.find_element(by=By.CLASS_NAME, value="m-btnEm-l").click()
  logging.info("NEOBANK：入金確定ボタン押下")
  time.sleep(2)
  # 住信SBIネット銀行の取引パスワード入力
  tra_passwd = driver.find_element(by=By.ID, value="transPW")
  tra_passwd.send_keys(NEOBANK_TRAN_PWD)
  logging.info("NEOBANK：取引パスワード入力")
  # 住信SBIネット銀行の認証ボタン押下
  driver.find_element(by=By.XPATH, value=XPATH_AUTH_BUTTON).click()
  logging.info("NEOBANK：取引確定完了")
  time.sleep(3)
  # 処理終了
  logging.info("WebDriver：ブラウザを閉じる")
  driver.quit()
  logging.info("==========処理終了==========")