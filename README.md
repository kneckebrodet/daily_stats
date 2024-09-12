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
### 仮想環境に入る / Enter v.environment:
```
venv\Scripts\activate
```
### 必要なライブラリのインストール / Install necessary libraries
```
pip install --upgrade setuptools
```
```
pip install -r requirements.txt
```

### MySQLデータベースのセットアップ / setup MySQL database:
```
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

### テーブルの作成が完成であれば、「database.py」のファイルでデータベースのuserとpasswordを入力して:
### When all the tables are created, fill in the database user and password in the 「database.py」file:
```
def __init__(self):
        self.db = mysql.connector.connect(
            user='',
            password='',
            host='localhost',
            database='daily_stats'
) 
```

### テストデータを入れて、アプリケーションがちゃんと動くのを確認する：
### Insert test data to check that app is working correctly:
```
python insert_test_data.py

python main.py
```
「admin」というユーザー名でログインしてグラフを確認 / At first, login as 「admin」to check that everything works and to create users.

<p>
　<h2>①　グラフが問題なく動くチェック / Check that Graph is working</h2>
  <img src="https://github.com/user-attachments/assets/f0f26812-97d6-4d5a-88d1-d9bd9b5e8d10" alt="img" width="200" height="auto" />
  <img src="https://github.com/user-attachments/assets/d09eb7ad-cb0a-4906-9826-0b2fb8bee66e" alt="img" width="200" height="auto" />
  <img src="https://github.com/user-attachments/assets/d096e0bc-1673-4fc2-8894-43ec1c9b8f7e" alt="img" width="200" height="auto" />
</p>
<p>
  <img src="https://github.com/user-attachments/assets/d3f8b1ab-d128-44d2-ada4-77a9a226ad36" alt="img" width="200" height="auto" />
  <img src="https://github.com/user-attachments/assets/736b28b9-5a7e-4f69-ae3f-012607269439" alt="img" width="200" height="auto" />
  <img src="https://github.com/user-attachments/assets/d580b707-55ae-4469-be77-a22eb3dfcd89" alt="img" width="200" height="auto" />
</p>

<p>
　<h2>②　ユーザー作成 (アドミンしかできないこと）/ Create user (only possible as admin)</h2>
  <img src="https://github.com/user-attachments/assets/fec74d0e-fdd9-4d6c-97ce-720187827dd2" alt="img" width="200" height="auto" />
  <img src="https://github.com/user-attachments/assets/b3f1ba7e-436e-4e3c-9cac-164cbca98379" alt="img" width="200" height="auto" />
  <img src="https://github.com/user-attachments/assets/15608449-e9bf-42a7-851d-74868cd3f491" alt="img" width="200" height="auto" />
</p>

<p>
  <h2>③　アプリがちゃんと動いて、自分のユーザー作成が完了であれば、アプリが使えます / When everything is working and you have created your own user, you can start using the app </h2>
  <h3> Add notes/to-dos</h3>
  <img src="https://github.com/user-attachments/assets/a44131cb-0546-46f0-ba04-25938da596ed" alt="img" width="200" height="auto" />
  <img src="https://github.com/user-attachments/assets/6cf6515f-c802-484f-8e6b-8562a07cf1fe" alt="img" width="200" height="auto" />
  <img src="https://github.com/user-attachments/assets/f9987a8c-25a4-4e6b-933a-fd46dcec2e0b" alt="img" width="200" height="auto" />
</p>
