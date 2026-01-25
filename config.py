# ======================================================
# 設定ファイル
# ======================================================
CONFIG = {
    # 使用するブラウザの種類
    'useBrowser': 'Chrome',
    # Chromeユーザプロファイルの格納先パス（必須）
    'chromeUserDataDir': '/Users/<Macのユーザ名>/Library/Application Support/Google/Chrome/Selenium', #左記はMacの例
    # Firefoxユーザプロファイルの格納先パス（必須）
    'FirefoxUserDataDir': '/Users/<Macのユーザ名>/Library/Application Support/Firefox/Profiles/xxxxxxxx.selenium-client.profile', #左記はMacの例
    # SBI証券情報（必須）
    'sbisecUserName': '<SBI証券のユーザ名(ログインID)>', #例：123-4567890(支店番号3桁＋口座番号7桁)
    'sbisecPassword': '<SBI証券のログインパスワード>',
    'sbisecTranPassword': '<SBI証券の取引パスワード>',
    'sbisecAmountOfMoney': 10000, #入金金額
    # NEOBANK認証情報（必須）
    'neobankUserName': '<NEOBANKのユーザ名(ログインメールアドレス)>',
    'neoBankPassword': '<NEOBANKのログインパスワード>',
    'neobankTranPassword': '<NEOBANKの取引パスワード>',
    # LINE Messaging API情報（任意）
    'lineUserId': '<LINE Messaging API設定で払い出したユーザID>',
    'lineChannelToken': '<LINE Messaging API設定で払い出したチャネルアクセストークン（長期）>',
    # XPATH一覧（変更しない）
    'xpath_page_link': '//*[@id="mymenuSec"]/div/div[2]/div/div[2]/div[3]/a[1]',
    'xpath_input_amount': '/html/body/main/section/article/section/div/div[7]/div[1]/div/div/input',
    'xpath_input_tran_pw': '/html/body/main/section/article/section/div/div[9]/div/input',
    'xpath_check_tran': '/html/body/main/section/article/section/div/div[9]/button',
    'xpath_execute_tran': '/html/body/main/section/article/section/div/div[3]/div[2]/button[2]',
    'xpath_commit_tran': '/html/body/app/div/ng-component/div/main/ng-component/section[2]/div/ul/li/nb-button/a',
    'xpath_login_button': '/html/body/app/div/ng-component/div/main/ng-component/form/div/section/ul/li[1]/a',
    'xpath_auth_button': '/html/body/div[2]/div[2]/div/mat-dialog-container/wplauthcommon/div/section/form/div/ul/li/button'
}