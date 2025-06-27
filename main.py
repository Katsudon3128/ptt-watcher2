import PyPtt
import time
import csv
import sqlite3
import signal
import sys

# 定義中止函數
def handler(signum, frame):
    print("程式終止")
    conn.close()
    ptt_bot.logout()
    sys.exit(0)

# 設置 Ctrl+C 觸發中止
signal.signal(signal.SIGINT, handler)
print("輸入 Ctrl+C 中止...")

try:
    ptt_bot = PyPtt.API()

    try:
        ptt_bot.login(ptt_id='{id}', ptt_pw='{pwd}', kick_other_session=True)
        
        conn = sqlite3.connect('db/ptt_watcher.db')
        c = conn.cursor()

        all_boards = open('all_boards.csv')
        reader = csv.reader(all_boards)
        board_list = list(reader)
        all_boards.close()

        while True:
            column_to_add = 'log_time'
            data_to_add = 'datetime(\'now\',\'localtime\')'
            for i in range(len(board_list)):
                board_info = ptt_bot.get_board_info(board=board_list[i][0])
                column_to_add += ',' + board_list[i][0].replace('-','_')
                data_to_add += ',' + str(board_info['online_user'])
            
            sql_str = "INSERT INTO board_online_usr_log (" + column_to_add + ") \
            VALUES (" + data_to_add + ")"
            c.execute(sql_str)
            conn.commit()
            time.sleep(3)
    except :
        print('error')
    finally:
        conn.close()
        ptt_bot.logout()
except KeyboardInterrupt:
    pass
