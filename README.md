# PicDL_cluster

# 使い方
twitterでのログイン情報を入れた`keys.py`を作る
```
echo -e "username='your username'\npassword='your password'" > keys.py
```
画像を保存するディレクトリ`img/`を作る
```
mkdir img
```
必要な環境のインストール
```
pip install -r requirements.txt
```

ダウンローダーの実行
```
python downloader.py
```