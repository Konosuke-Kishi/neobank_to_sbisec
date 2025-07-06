# SBI証券自動入金ツール

SBI証券に毎日入金するのを自動化しました。<br>

## 使い方

### 1. ソースコードをクローン

```
git clone https://github.com/Konosuke-Kishi/neobank_to_sbisec.git
```

### 2. 事前準備

2025/05/31からSBI証券のログイン時にデバイス認証が必須となるため <br>
事前にseleniumを使う環境のChromeでデバイス認証を通す必要がある。<br>
認証済みプロファイルをSeleniumで指定する手順は下記。

①Chromeでデバイス認証を通したら、プロファイルのパスを調べる<br>
②認証を通したユーザプロファイルの中身(Defaultフォルダ)をコピーする<br>
③上記のパスに適当な名前(Seleniumとか)で新しいフォルダを作成しペーストすればOK。<br>
※後述手順でconfig.pyにプロファイルのパスを指定するのを忘れずに！

### 3. 設定ファイルの編集

config.pyを開いて、下記必須の設定値を入力してください。<br>

```
CONFIG = {
    # Chromeユーザプロファイルの格納先パス（必須）
    'chromeUserDateDir': '<2. 事前準備で作成したプロファイルの格納パス>',
    # SBI証券情報（必須）
    'sbisecUserId': '<SBI証券のログインID>',
    'sbisecPassword': '<SBI証券のログインパスワード>',
    'sbisecTranPassword': '<SBI証券の取引パスワード>',
    'sbisecAmountOfMoney': 10000, #入金金額
    # NEOBANK認証情報（必須）
    'neobankUserId': '<NEOBANKのログインメールアドレス>',
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

定期実行する場合はcron.pyを実行することでエラーの内容をLINEに通知することができる<br>
config.pyに必要なクレデンシャル情報を設定すればnotify.pyからLINEへ通知が飛ぶ<br>