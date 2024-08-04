# SBI証券自動入金ツール

SBI証券に毎日入金するのを自動化しました。<br>

## 使い方

### 1. ソースコードをクローン

```
git clone https://github.com/Konosuke-Kishi/neobank_to_sbisec.git
```

### 2. ChromeDriverをインストール

下記URLから、あなたが使用しているGoogle Chromeのバージョンと一致する<br>
ChromeDriverをインストールしてください。<br>

https://chromedriver.chromium.org/downloads

インストールした後は、クローンしたソースコード群と同階層に移動させてください。<br>
そして、main.pyを開いて、下記コードにChromeDriverのパスを入力してください。

```
 # webdriver準備
service = Service(executable_path="ChromeDriverのパス")
```

### 3. クレデンシャル情報設定

config.pyを開いて、各種クレデンシャル情報を入力してください。<br>

```
CONFIG = {
    'userId': '123-4567890',　#SBI証券のログインID(支店番号3桁＋口座番号7桁)
    'password': 'sbisec_password',　#SBI証券のログインパスワード
    'mailAddress': 'test@gmail.com',　#NEOBANKのログインメールアドレス(第一生命支店・Vポイント支店共通)
    'neoBankPassword': 'neobank_password',　#NEOBANKのログインパスワード(第一生命支店・Vポイント支店共通)
    'amountOfMoney': 10000, #入金金額
    'sbisecTransactionPassword': 'sbisec_transaction_password',　#SBI証券の取引パスワード
    'neobankTransactionPassword': 'neobank_transaction_password'　#NEOBANKの取引パスワード(第一生命支店・Vポイント支店共通)
}
```

### 4. 準備完了！

これで、スクリプトの準備が完了しました。
下記コマンドを入力すれば、自動入金作業が動作するはずです。

```
# VNEOBANKの場合
python3 main.py t

# 第一生命NEOBANKの場合
python3 main.py d
```

### ※ヘッドレスモード

初期状態では、ヘッドレスモードで起動します。<br>
もし、Google ChromeのGUIで起動したい場合は、main.pyのヘッドレス設定を<br>
下記コードに変更してください。

```
## ヘッドレス設定
service = Service(executable_path="ChromeDriverのパス")
driver = webdriver.Chrome(service=service, options=options)
```
