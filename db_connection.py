import mysql.connector
import subprocess
import os
import time
import sys


class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

        base_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
        self.bat_dir = os.path.join(base_dir, "MySQL-5.5-Portable")
        self.start_bat = os.path.join(self.bat_dir, "StartServer.bat")
        self.stop_bat = os.path.join(self.bat_dir, "StopServer.bat")
        self.proc = None

        self.mysql_dir = os.path.join(base_dir, "MySQL-5.5-Portable", "mysql-5.5")
        self.mysqld_path = os.path.join(self.mysql_dir, "bin", "mysqld.exe")

    def connect(self):
        self.proc = subprocess.Popen(
            [self.mysqld_path, '--console'],
            cwd=os.path.dirname(self.mysqld_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW  # чтобы не блокировался основной процесс
        )

        time.sleep(3)

        try:
            config = {
                'host': '127.0.0.1',
                'user': 'root',
                'password': '',
                'database': 'pixmanager',
                'use_pure': True,  # <--- ВАЖНО
            }
            self.connection = mysql.connector.connect(**config)
            # self.connection = mysql.connector.connect(
            #     host="127.0.0.1",
            #     user="root",
            #     password="",
            #     database="pixmanager",
            #     connection_timeout=10,
            #     port=3306,
            #     auth_plugin='mysql_native_password'
            # )

            print("Подключение есть!")
            self.cursor = self.connection.cursor()

            # print("Подключение выполнено.")
        except Exception as err:
            print(f"ошибка: {err}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

        subprocess.call(["taskkill", "/F", "/IM", "mysqld.exe"])



if __name__ == "__main__":
    # код для проверки
    db_manager = DatabaseManager()
    db_manager.connect()  # Подключаемся к базе данных
    db_manager.close()