# ======================================================
# ライブラリ
# ======================================================
from main import auto_payment
from notify import line_notify
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
# ======================================================
# 定期実行用スクリプト
# ======================================================
if __name__ == '__main__':
    try:
      auto_payment()
    # 要素が見つからない場合
    except NoSuchElementException:
      line_notify("要素が見つかりませんでした")
    # 処理が遅く、タイムアウトしてしまった場合
    except TimeoutException:
      line_notify("操作がタイムアウトしました")
    # WebDriver関連のエラーの場合
    except WebDriverException:
      line_notify("WebDriverエラーが発生しました")
    # それ以外のエラーの場合
    except Exception as e:
      line_notify(f"予期しないエラーが発生しました\n{e}")
    # 正常に処理が終了した場合
    else:
      line_notify("正常に処理が完了しました")