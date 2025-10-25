# SBI 証券自動入金ツール

SBI 証券に毎日入金するのを自動化しました。<br>

## 使い方

### 1. ソースコードをクローン

```
git clone https://github.com/Konosuke-Kishi/neobank_to_sbisec.git
```

### 2. 事前準備

2025/05/31 から SBI 証券のログイン時にデバイス認証が必須となるため <br>
事前に selenium を使う環境の Chrome でデバイス認証を通す必要がある。<br>
認証済みプロファイルを Selenium で指定する手順は下記。

①Chrome でデバイス認証を通したら、プロファイルのパスを調べる<br>
② 認証を通したユーザプロファイルの中身(Default フォルダ)をコピーする<br>
③ 上記のパスに適当な名前(Selenium とか)で新しいフォルダを作成しペーストすれば OK。<br>
※後述手順で config.py にプロファイルのパスを指定するのを忘れずに！

### 3. 設定ファイルの編集

config.py を開いて、下記必須の設定値を入力してください。<br>

```
CONFIG = {
    # Chromeユーザプロファイルの格納先パス（必須）
    'chromeUserDateDir': '<2. 事前準備で作成したプロファイルの格納パス>',
    # SBI証券情報（必須）
    'sbisecUserName': '<SBI証券のユーザ名(ログインID)>',
    'sbisecPassword': '<SBI証券のログインパスワード>',
    'sbisecTranPassword': '<SBI証券の取引パスワード>',
    'sbisecAmountOfMoney': 10000, #入金金額
    # NEOBANK認証情報（必須）
    'neobankUserName': '<NEOBANKのユーザ名(ログインメールアドレス)>',
    'neoBankPassword': '<NEOBANKのログインパスワード>',
    'neobankTranPassword': '<NEOBANKの取引パスワード>',
    ...
}
```

### 4. 準備完了！

これで、スクリプトの準備が完了しました。<br>
下記コマンドを入力すれば、自動入金作業が動作するはずです。

```
python3 main.py
```

### 5.定期実行の設定

定期実行する場合は cron.py を実行することでエラーの内容を LINE に通知することができる<br>
config.py に必要なクレデンシャル情報を設定すれば notify.py から LINE へ通知が飛ぶ<br>
