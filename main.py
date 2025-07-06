# ======================================================
# ライブラリ
# ======================================================
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config import CONFIG
import chromedriver_binary_sync, time, datetime, logging, os
# ======================================================
# 設定ファイル（config.py）の読み込み
# ======================================================
# Chromeユーザプロファイルの格納先パス
CHROME_USER_DATA_DIR = CONFIG['chromeUserDateDir']
# SBI証券情報
SBI_SEC_LOGIN_ID = CONFIG['sbisecUserId']
SBI_SEC_PASSWORD = CONFIG['sbisecPassword']
SBI_SEC_TRAN_PWD = CONFIG['sbisecTranPassword']
SBI_SEC_MONEYAMT = CONFIG['sbisecAmountOfMoney']
# NEOBANK情報
NEOBANK_USERNAME = CONFIG['neobankUserId']
NEOBANK_PASSWORD = CONFIG['neoBankPassword']
NEOBANK_TRAN_PWD = CONFIG['neobankTranPassword']
# XPATH一覧
XPATH_INPUT_AMOUNT = CONFIG['xpath_input_amount']
XPATH_INPUT_TRANPW = CONFIG['xpath_input_tran_pw']
XPATH_CHK_TRAN = CONFIG['xpath_check_tran']
XPATH_EXE_TRAN = CONFIG['xpath_execute_tran']
XPATH_CMT_TRAN = CONFIG['xpath_commit_tran']
# ======================================================
# ログの設定
# ======================================================
logging.basicConfig(
  # ログを保存するファイル名
  filename='auto_payment.log',
  # ログレベル（INFO以上を記録）
  level=logging.INFO,
  # ログ出力のフォーマット形式
  format='%(asctime)s - %(levelname)s - %(message)s'
)
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
# Chrome起動設定
# ======================================================
# 現在のChromeのバージョンと一致するdriverをダウンロード
chromedriver_binary_sync.download()
# オプションの設定
options = webdriver.ChromeOptions()
# Chromeプロファイルの指定
options.add_argument("--user-data-dir=" + CHROME_USER_DATA_DIR)
# ポップアップウィンドウの許可設定
options.add_argument('--disable-popup-blocking')

# ======================================================
# 定額自動入金のメイン処理
# ======================================================
def auto_payment():

  # ======================================================
  # 1. SBI証券ログイン処理
  # ======================================================
  # Chromeブラウザを開く
  logging.info("==========処理開始==========")
  driver = webdriver.Chrome(options=options)
  logging.info("WebDriver：ブラウザ起動完了")
  # SBI証券のトップページを開く
  driver.get("https://site3.sbisec.co.jp/ETGate/")
  logging.info("WebDriver：サイトアクセス成功")
  time.sleep(2)
  # SBI証券のユーザ名入力
  userid = driver.find_element(by=By.NAME, value="user_id")
  userid.send_keys(SBI_SEC_LOGIN_ID)
  logging.info("SBI証券：ユーザネーム入力")
  # SBI証券のログインパスワード入力
  password = driver.find_element(by=By.NAME, value="user_password")
  password.send_keys(SBI_SEC_PASSWORD)
  logging.info("SBI証券：ログインパスワード入力")
  # SBI証券のログインボタン押下
  driver.find_element(by=By.NAME, value="ACT_login").click()
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
  driver.find_element(by=By.ID, value="tneobank-login").click()
  time.sleep(2)
  logging.info("NEOBANK：支店選択")
  # 住信SBIネット銀行のユーザネームを入力
  username = driver.find_element(by=By.ID, value="userNameNewLogin")
  username.send_keys(NEOBANK_USERNAME)
  logging.info("NEOBANK：ユーザネーム入力")
  # 住信SBIネット銀行のログインパスワード入力
  neopassword = driver.find_element(by=By.ID, value="loginPwdSet")
  neopassword.send_keys(NEOBANK_PASSWORD)
  logging.info("NEOBANK：ログインパスワード入力")
  # ログインボタン押下
  driver.find_element(by=By.CLASS_NAME, value="m-btnEm-l").click()
  logging.info("NEOBANK：ログイン成功")
  time.sleep(2)

  # ======================================================
  # 4. 住信SBIネット銀行入金確定処理
  # ======================================================
  # 住信SBIネット銀行の取引パスワード入力
  tra_passwd = driver.find_element(by=By.ID, value="toriPwd")
  tra_passwd.send_keys(NEOBANK_TRAN_PWD)
  logging.info("NEOBANK：取引パスワード入力")
  # 住信SBIネット銀行の確定ボタン押下
  driver.find_element(by=By.XPATH, value=XPATH_CMT_TRAN).click()
  logging.info("NEOBANK：取引確定完了")
  # 処理終了
  logging.info("WebDriver：ブラウザを閉じる")
  driver.quit()
  logging.info("==========処理終了==========")