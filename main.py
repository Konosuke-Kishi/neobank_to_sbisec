# ======================================================
# ライブラリ
# ======================================================
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, chromedriver_autoinstaller, geckodriver_autoinstaller
from notify import line_notify
from config import CONFIG

# ======================================================
# 設定ファイル（config.py）の読み込み
# ======================================================
# 使用するブラウザの種類
USE_BROWSER = CONFIG['useBrowser']
# ヘッドレスブラウザを使用するかどうか
USE_HEADLESS_BROWSER = CONFIG['useHeadlessBrowser']
# Chromeユーザプロファイルの格納先パス
CHROME_USER_DATA_DIR = CONFIG['chromeUserDataDir']
# Firefoxユーザプロファイルの格納先パス
FIREFOX_USER_DATA_DIR = CONFIG['firefoxUserDataDir']
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
XPATH_CLOSE_BUTTON = CONFIG['xpath_close_button']
# 待機時間
ELEMENT_WAIT_TIME = 20
DEVICE_AUTH_WAIT_TIME = 60

# ==============================================================
# TODO: TimedRotatingFileHandlerを使用してログローテーションを実装する
# ==============================================================

# ======================================================
# ドライバの設定
# ======================================================
def create_driver():
  if(USE_BROWSER == "Firefox"):
    executable_path = geckodriver_autoinstaller.install()
    options = webdriver.FirefoxOptions()
    options.add_argument('--disable-popup-blocking')
    options.add_argument("-profile")
    options.add_argument(FIREFOX_USER_DATA_DIR)
    options.headless = USE_HEADLESS_BROWSER
    service = webdriver.firefox.service.Service(executable_path)
    return webdriver.Firefox(service=service, options=options)
  if(USE_BROWSER == "Chrome"):
    executable_path = chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-popup-blocking')
    options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")
    options.headless = USE_HEADLESS_BROWSER
    service = webdriver.chrome.service.Service(executable_path)
    return webdriver.Chrome(service=service, options=options)

# ======================================================
# 定額自動入金のメイン処理
# ======================================================
def auto_payment():
  # driverの設定
  driver = create_driver()
  # ======================================================
  # 1. SBI証券ログイン処理
  # ======================================================
  # SBI証券のログインページを開く
  driver.get("https://login.sbisec.co.jp/login/entry")
  # SBI証券のユーザ名入力
  userid = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.NAME, "username")))
  userid.send_keys(SBI_SEC_USERNAME)
  # SBI証券のログインパスワード入力
  password = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.NAME, "password")))
  password.send_keys(SBI_SEC_PASSWORD)
  # SBI証券のログインボタン押下
  WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.ID, "pw-btn"))).click()

  # ==============================================
  # TODO: 初回のみここでデバイス認証が必要になる
  # ==============================================
  # メール認証未済であれば送信ボタン押下
  time.sleep(ELEMENT_WAIT_TIME)
  send_email_buttons = driver.find_elements(By.ID, "sendEmailButton")
  if send_email_buttons:
    send_email_buttons[0].click()
  else: pass
  # チェックボックス押下
  time.sleep(ELEMENT_WAIT_TIME)
  auth_check = driver.find_elements(By.ID, "authCheck")
  if auth_check:
    auth_check[0].click()
  else: pass
  # 認証番号をLINEでスマホに通知
  auth_number = driver.find_elements(By.ID, "authCode")
  if auth_number:
    auth_number_text = auth_number[0].text.strip() or False
    msg = f"デバイス認証コードは\n{auth_number_text}"
    line_notify(msg)
  else: pass
  # デバイス認証完了後、登録ボタン押下
  time.sleep(DEVICE_AUTH_WAIT_TIME)
  otp_register_button = driver.find_elements(By.ID, "otpRegisterButton")
  if otp_register_button:
    otp_register_button[0].click()
  else: pass


  # ======================================================
  # 2. SBI証券振込指示処理
  # ======================================================
  # SBI証券の入金ボタンを押下
  WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "入金"))).click()
  # SBI証券の入金額を入力
  input_money = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.XPATH, XPATH_INPUT_AMOUNT)))
  input_money.send_keys(SBI_SEC_MONEYAMT)
  # SBI証券の取引パスワード入力
  input_tran_passwd = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.XPATH, XPATH_INPUT_TRANPW)))
  input_tran_passwd.send_keys(SBI_SEC_TRAN_PWD)
  # SBI証券の入金指示確認ボタン押下
  insert_money_check = WebDriverWait(driver,  ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.XPATH, XPATH_CHK_TRAN)))
  insert_money_check.send_keys(Keys.SPACE)
  # SBI証券の入金指示ボタン押下
  insert_money_execute = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.XPATH, XPATH_EXE_TRAN)))
  insert_money_execute.send_keys(Keys.SPACE)

  # ======================================================
  # 3. 住信SBIネット銀行ログイン処理
  # ======================================================
  # 現在のウィンドウハンドルを保存
  main_window_handle = driver.current_window_handle
  # 新しいウィンドウが開くのを待つ
  WebDriverWait(driver, ELEMENT_WAIT_TIME).until(EC.number_of_windows_to_be(2))
  # 新しいウィンドウへ切り替え
  for handle in driver.window_handles:
      if handle != main_window_handle:
          driver.switch_to.window(handle)
          break
  # 支店選択
  WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.ID, "CCC"))).click()
  # 住信SBIネット銀行のユーザ名を入力
  username = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@id='username']")))
  username.send_keys(NEOBANK_USERNAME)
  # ログインボタン押下
  WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.XPATH, XPATH_LOGIN_BUTTON))).click()
  # 住信SBIネット銀行のログインパスワード入力
  neopassword = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.ID, "loginPwd")))
  neopassword.send_keys(NEOBANK_PASSWORD)
  # ログインボタン押下
  WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.XPATH, XPATH_AUTH_BUTTON))).click()

  # ======================================================
  # 4. 住信SBIネット銀行入金確定処理
  # ======================================================
  # 住信SBIネット銀行の確定するボタン押下
  WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.XPATH, XPATH_CMT_TRAN))).click()
  # 住信SBIネット銀行の取引パスワード入力 
  tra_passwd = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.ID, "transPW")))
  tra_passwd.send_keys(NEOBANK_TRAN_PWD)
  # 住信SBIネット銀行の認証ボタン押下
  WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.XPATH, XPATH_AUTH_BUTTON))).click()
  # 住信SBIネット銀行の閉じるボタン押下
  WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.XPATH, XPATH_CLOSE_BUTTON))).click()
  # 処理終了
  driver.quit()