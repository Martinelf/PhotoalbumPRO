from ui_dialog import *
import os
import mysql.connector
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS


def get_creation_date(image_path):
    try:
        # Открываем изображение с помощью Pillow
        image = Image.open(image_path)

        # Получаем EXIF данные
        exif_data = image._getexif()
        if exif_data is not None:
            for tag, value in exif_data.items():
                if TAGS.get(tag) == 'DateTime':
                    return value  # Дата и время из EXIF
        return None  # Если дата не найдена, возвращаем None
    except Exception as e:
        print(f"Ошибка при обработке {image_path}: {e}")
        return None


def insert_photos_to_db(folder_path, cursor):
    # Перебираем все файлы в папке
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            # Формируем полный путь к изображению
            file_path = folder_path + '/' + filename

            # Извлекаем дату создания из метаданных EXIF
            creation_date = get_creation_date(file_path)
            if not creation_date:
                creation_date = datetime.now()  # Если дата не найдена, используем текущее время
            else:
                # Преобразуем строку из EXIF в объект datetime, если нужно
                try:
                    creation_date = datetime.strptime(creation_date, "%Y:%m:%d %H:%M:%S")
                except ValueError:
                    creation_date = datetime.now()  # В случае ошибки преобразования

            # Вставляем данные в таблицу
            description = ""  # Можно заменить на реальное описание, если оно доступно
            cursor.execute(
                """
                INSERT INTO photos (file_path, creation_date, locationID, description)
                VALUES (%s, %s, %s, %s)
                """,
                (file_path, creation_date, 1, description)  # locationID можно заменить на нужное значение
            )

class EditFolderListDialog(QDialog, Ui_Dialog):
    def __init__(self, db_connection):
        super().__init__()
        self.setupUi(self)

        self.buttonAdd.clicked.connect(self.add_folder)
        self.buttonRemove.clicked.connect(self.remove_folder)

        self.db_connection = db_connection
        self.display_folders()

    def display_folders(self):
        self.listWidget.clear()
        if not self.db_connection.is_connected():
            self.db_connection.reconnect()
            print("Соединение с БД восстановлено.")
        try:
            query = "SELECT file_path FROM photos"

            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
                file_paths = cursor.fetchall()

                # Вычисляем уникальные папки
                folders = set()
                for path_tuple in file_paths:
                    full_path = path_tuple[0]  # file_path из запроса
                    folder_path = os.path.dirname(full_path)  # Путь до папки
                    folders.add(folder_path)

                # Заполняем listWidget уникальными папками
                for folder in sorted(folders):  # Можно сортировать для удобства
                    self.listWidget.addItem(folder)

                print(f"Количество уникальных папок: {len(folders)}")

        except mysql.connector.Error as err:
            print(f"Ошибка при обновлении базы данных: {err}")

    from PyQt5.QtWidgets import QMessageBox

    def add_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder_path:
            # Подтверждающий диалог
            confirm = QMessageBox.question(
                self,
                "Подтверждение добавления",
                f"Вы уверены, что хотите добавить все файлы из папки:\n{folder_path}?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if confirm == QMessageBox.Yes:
                with self.db_connection.cursor() as cursor:
                    try:
                        # Вставляем файлы из выбранной папки в базу
                        insert_photos_to_db(folder_path, cursor)

                        # Фиксируем изменения в базе данных
                        self.db_connection.commit()
                        print(f"Файлы из папки {folder_path} успешно добавлены в базу.")

                        # Обновляем список папок
                        self.display_folders()
                    except Exception as e:
                        print(f"Ошибка при добавлении файлов из папки: {e}")

    def get_selected_folder(self):
        selected_items = self.listWidget.selectedItems()
        if selected_items:
            return selected_items[0].text()  # Возвращает текст выбранного элемента
        return None

    def remove_folder(self):
        selected_folder = self.get_selected_folder()
        if selected_folder:
            # Подтверждающий диалог
            confirm = QMessageBox.question(
                self,
                "Подтверждение удаления",
                f"Вы уверены, что хотите удалить все файлы из папки:\n{selected_folder}?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if confirm == QMessageBox.Yes:
                with self.db_connection.cursor() as cursor:
                    try:
                        # Удаляем записи из photo_tags, связанные с файлами в указанной папке
                        delete_tags_query = """
                        DELETE FROM photo_tags
                        WHERE photoID IN (
                            SELECT photoID FROM photos WHERE file_path LIKE %s
                        )
                        """
                        cursor.execute(delete_tags_query, (f"{selected_folder}%",))

                        # Удаляем записи из photo_people, связанные с файлами в указанной папке
                        delete_people_query = """
                        DELETE FROM photo_people
                        WHERE photoID IN (
                            SELECT photoID FROM photos WHERE file_path LIKE %s
                        )
                        """
                        cursor.execute(delete_people_query, (f"{selected_folder}%",))

                        # Удаляем записи из photos
                        delete_photos_query = "DELETE FROM photos WHERE file_path LIKE %s"
                        cursor.execute(delete_photos_query, (f"{selected_folder}%",))

                        # Фиксируем изменения
                        self.db_connection.commit()
                        print(f"Файлы из папки {selected_folder} успешно удалены из базы.")

                        # Обновляем список папок
                        self.display_folders()
                    except Exception as e:
                        print(f"Ошибка при удалении файлов из папки: {e}")
        else:
            print("Папка не выбрана.")






