import PyPtt
import time
import csv
import sqlite3
import signal
import sys
import requests
from bs4 import BeautifulSoup

# 取得看板列表
def getBoardList():
    all_boards = open('all_boards.csv')
    reader = csv.reader(all_boards)
    result = list(reader)
    all_boards.close()
    return result

def addBoardColumn(boardName, conn):
    addBoardColumn_c = conn.cursor()
    addBoardColumn_c.execute("ALTER TABLE board_online_usr_log ADD COLUMN [" + boardName.replace('-','_') + "] INT DEFAULT 0;")
    conn.commit()

def addBoardData(boardName):
    addBoardData_file = open('all_boards.csv', mode='a', newline='')
    addBoardData_writer = csv.writer(addBoardData_file)
    addBoardData_writer.writerow([boardName])
    addBoardData_file.close()

# 新增看板
def addBoard(boardName, conn):
    addBoardColumn(boardName, conn)
    addBoardData(boardName)

# 新增新的熱門看板
def addNewPopularBoard(conn):
    board_list = getBoardList()
    hotpage = requests.get("https://www.ptt.cc/bbs/index.html")
    main = BeautifulSoup(hotpage.text, 'html.parser')
    board_find = main.find_all('a', class_='board', limit=100)
    print(':::新增以下看板:::')
    for i in range(len(board_find)):
        board_find_text = board_find[i].find('div', class_ = 'board-name').text
        for j in range(len(board_list)):
            # 如果已經存在就結束這輪檢查
            if board_list[j][0] == board_find_text:
                break
            # 如果檢查到最後一筆都沒有結束代表不存在，需要新增
            if j == len(board_list)-1:
                print(board_find_text)
                addBoard(board_find_text, conn)

# 定義中止函數
def handler(signum, frame):
    print("程式終止")
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

        board_list = getBoardList()

        while True:
            try:
                column_to_add = 'log_time'
                data_to_add = 'datetime(\'now\',\'localtime\')'
                for i in range(len(board_list)):
                    board_info = ptt_bot.get_board_info(board=board_list[i][0])
                    column_to_add += ',[' + board_list[i][0].replace('-','_') + ']'
                    data_to_add += ',' + str(board_info['online_user'])
                
                sql_str = "INSERT INTO board_online_usr_log (" + column_to_add + ") \
                VALUES (" + data_to_add + ")"
                c.execute(sql_str)
                conn.commit()
                current_time = time.localtime()
                if 0 <= current_time.tm_sec <= 6:
                    addNewPopularBoard(conn)
                    board_list = getBoardList()
                time.sleep(5)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        ptt_bot.logout()
except KeyboardInterrupt:
    pass
