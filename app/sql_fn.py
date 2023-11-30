import mysql.connector
import os


def conn_db():
    conn = mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        passwd=os.environ["DB_PASSWORD"],
        db=os.environ["DB_NAME"],
    )
    return conn


# (1) : コメントが送信されたら20ポイントを付与する
# (2) : コメントにスタンプが付いたら10ポイントを付与する
# (3) : コメントにスタンプを付けたら10ポイントを付与する
# (x) : ユーザーが存在しなかったら作成する OK
# (x) : ポイントテーブルにデータが存在しなかったら作成する OK

# try:
#     conn_db()
#     print("接続成功")
# except:
#     print("接続失敗")


def fetch_sql(qurey, param):
    try:
        conn = conn_db()
        cur = conn.cursor()
        cur.execute(qurey, param)
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if result:
            return result[0]
    except Exception as e:
        print(e)


def execute_sql(qurey, param):
    try:
        conn = conn_db()
        cur = conn.cursor()
        cur.execute(qurey, param)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)


def add_point_on_message_send(id: int):
    execute_sql("UPDATE points SET point = point + 20 WHERE user_id = %s", (id,))


def add_point_on_reaction(id: int):
    execute_sql("UPDATE points SET point = point + 10 WHERE user_id = %s", (id,))


def sub_point_on_reaction(id: int):
    execute_sql("UPDATE points SET point = point - 10 WHERE user_id = %s", (id,))


def create_user(id: int, user_name: str):
    execute_sql("INSERT INTO users (user_discord_id, user_name) VALUES (%s, %s)", (id, user_name))


def create_point(id: int):
    execute_sql("INSERT INTO points (user_id) VALUES (%s)", (id,))


def get_point(id: int) -> int:
    point = fetch_sql("SELECT point FROM points WHERE user_id = %s", (id,))
    return point


def move_point_on_given(from_id: int, to_id: int, value: int):
    execute_sql(
        "UPDATE points SET point = point - %s WHERE user_id = %s",
        (
            value,
            from_id,
        ),
    )
    execute_sql("UPDATE points SET point = point + %s WHERE user_id = %s", (value, to_id))


# select文でusersテーブルからユーザー情報を取ってくる関数の定義
def get_user(id: int, user_name: str):
    result = fetch_sql("SELECT * FROM users WHERE user_discord_id = %s", (id,))
    if result is None:
        create_user(id, user_name)
        create_point(id)
        return
    else:
        return
