# важно чтобы сначала импортировались методы работы с бд, а потом уже с граф интерфейсом иначе не работает
from win_main import *
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.connect()
    app = QApplication(sys.argv)
    # qdarktheme.setup_theme("lightslu")
    db_conn = db_manager.connection
    main_window = MainWindow(db_conn)
    main_window.show()
    exit_code = app.exec_()  # Ждёт, пока пользователь закроет окно

    db_manager.close()  # <-- закрытие БД после выхода из приложения

    sys.exit(exit_code)







