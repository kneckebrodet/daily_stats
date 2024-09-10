## [インストールとセットアップ / INSTALLATION AND SETUP]

### 新しいフォルダの作成 / Create new folder：
```
mkdir daily_stats

cd daily_stats/

全ての.pyファイルをこのフォルダへ移動する / Place all the .py files in this folder
```
### 仮想環境の作成 / Create virtual environment
```
python -m venv venv
```
仮想環境に入る / Enter v.environment:
```
venv\Scripts\activate
```
必要なライブラリをインストール　/ Install necessary libraries
```
pip install --upgrade setuptools
```
```
pip install -r requirements.txt
```

## MySQLデータベースをセットアップ / setup MySQL database:

CREATE DATABASE daily_stats;

USE daily_stats;

CREATE TABLE users (user_id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(20));
INSERT INTO users (username) VALUES ("admin");

CREATE TABLE wakeup_times (user_id INT, date VARCHAR(255), time VARCHAR(255));

CREATE TABLE bed_times (user_id INT, date VARCHAR(255), time VARCHAR(255));

CREATE TABLE user_data (user_id INT, date VARCHAR(255), sleep VARCHAR(255), weight FLOAT, walking INT, exercise INT, skillup INT, reading INT, meditation TINYINT(1), ifast TINYINT(1));

CREATE TABLE to_do_lists (user_id INT, task VARCHAR(255), detail VARCHAR(255));

SHOW TABLES;
```
+-----------------------+
| Tables_in_daily_stats |
+-----------------------+
| bed_times             |
| to_do_lists           |
| user_data             |
| users                 |
| wakeup_times          |
+-----------------------+
5 rows in set (0.00 sec)
```

テーブルの作成が完成であれば、「database.py」のファイルでデータベースのuserとpasswordを入力して:
<!-- def __init__(self):
        self.db = mysql.connector.connect(
            user='',
            password='',
            host='localhost',
            database='daily_stats'
        ) 
-->

テストデータを入れて、アプリケーションが問題なく動くのを確認する：
Insert test data to check that app is working correctly:

python insert_test_data.py

python main.py

「admin」というユーザー名でログインしてグラフを確認
