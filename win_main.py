from db_connection import *
from ui_main import *
from win_dialog import *
from diagrams import *

from PyQt5.QtGui import QDesktopServices
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt, QDateTime

import os
import sys
import datetime
import re

import subprocess

from collections import defaultdict

from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors

from PIL import Image as PILImage


class MainWindow(QMainWindow, Ui_MainWindow):
    # константы для хранения метаданных о фото внутри элементов listWidget
    ROLE_PIXMAP = Qt.UserRole
    ROLE_IMAGE_NAME = 0
    ROLE_PATH = 4
    ROLE_DATE = 5
    ROLE_LOCATION = 6
    ROLE_PEOPLE = 7
    ROLE_TAGS = 8
    ROLE_DESCRIPTION = 9
    ROLE_PHOTO_ID = 11
    ROLE_IS_FAVORITE = 12

    default_face = ''

    def __init__(self, db_connection):
        super().__init__()
        self.setupUi(self)
        self.setup_connections()
        self.db_connection = db_connection  # Храним соединение, а не курсор

        self.faces = []
        self.filtered = False

        self.comboboxes = [self.comboBox, self.comboBox_2, self.comboBox_3, self.comboBox_4, self.comboBox_5]

        for cb in self.comboboxes:
            cb.currentIndexChanged.connect(self.update_comboboxes)

        self.load_all_images()

        self.album_displayed = "all"

    def update_comboboxes(self):
        # Собираем все выбранные элементы
        selected_items = {combo.currentText() for combo in self.comboboxes if combo.currentIndex() != -1}
        for combo in self.comboboxes:
            current_text = combo.currentText()

            combo.blockSignals(True)  # Отключаем сигналы временно
            combo.clear()

            # Добавляем элементы, которые ещё не выбраны, плюс текущий
            for face in self.faces:
                if face not in selected_items or face == current_text or face == self.default_face:
                    combo.addItem(face)

            combo.setCurrentText(current_text)  # Восстанавливаем текущий элемент
            combo.blockSignals(False)  # Включаем сигналы обратно

    def setup_connections(self):
        # Подключение сигнала itemSelectionChanged к обработчику
        self.listWidget.itemSelectionChanged.connect(self.update_labels)
        self.buttonFilterTags.clicked.connect(self.filter_by_tags)
        # self.buttonFilterDate.clicked.connect(self.filter_by_date)
        # self.buttonFilterFaces.clicked.connect(self.filter_by_faces)
        self.buttonLoadAll.clicked.connect(self.load_all_images)
        self.buttonLoadFavorite.clicked.connect(self.load_favorite)

        self.buttonFilterAll.clicked.connect(self.filter_by_all)
        self.buttonResetFilters.clicked.connect(self.reset_filters)
        self.buttonAddToFav.clicked.connect(self.add_remove_favorite)

        # редактирование инфополей
        self.labelDate.mouseDoubleClickEvent = self.enable_editing_date
        self.dateTimeEdit.editingFinished.connect(self.finish_editing_date)

        self.labelDescription.mouseDoubleClickEvent = self.enable_editing_description
        # self.textEditDescription.focusOutEvent = self.finish_editing_description тут нужно подумать пон

        self.labelLocation.mouseDoubleClickEvent = self.enable_editing_location
        # self.editLocation.editingFinished.connect(self.finish_editing_date)

        self.labelPeople.mouseDoubleClickEvent = self.enable_editing_people
        # self.editLocation.editingFinished.connect(self.finish_editing_date)

        self.labelTags.mouseDoubleClickEvent = self.enable_editing_tags
        # self.editLocation.editingFinished.connect(self.finish_editing_date)

        self.buttonToggleSearch.clicked.connect(self.toggle_search)

        """Открытие окна добавления/удаления папок"""
        self.editFolderList.triggered.connect(self.open_edit_folder_list_dialog)

        self.actionDiagrams.triggered.connect(self.show_window_diagrams)
        self.actionPhotoReport.triggered.connect(self.make_photo_report)
        self.actionAlbumReport.triggered.connect(self.make_album_report)
        self.actionPhotoesListReport.triggered.connect(self.make_photos_list_report)
        self.listWidget.itemDoubleClicked.connect(self.open_image)

    def toggle_search(self):
        """Переключение видимости панели поиска"""
        dock = self.dockSearch  # Имя, заданное в Qt Designer
        dock.setVisible(not dock.isVisible())
        if dock.isVisible():
            self.setFixedSize(1240, 600)
        else:
            self.setFixedSize(1080, 600)

    def make_photo_report(self):
        """создание отчета по конкретной фотографии"""
        # Регистрация шрифта с поддержкой русского языка
        font_path = "FreeSans.ttf"  # Замените на путь к шрифту
        if not os.path.exists(font_path):
            QMessageBox.critical(self, "Ошибка", f"Шрифт не найден: {font_path}")
            return
        pdfmetrics.registerFont(TTFont("FreeSans", font_path))
        styles = {
            "Normal": ParagraphStyle(
                name="Normal",
                fontName="FreeSans",
                fontSize=12,
                leading=14
            ),
            "Title": ParagraphStyle(
                name="Title",
                fontName="FreeSans",
                fontSize=16,
                leading=18,
                spaceAfter=10
            )
        }

        selected_items = self.listWidget.selectedItems()
        if selected_items:
            # Получаем данные из выбранного элемента
            path = selected_items[0].data(self.ROLE_PATH)
            description = selected_items[0].data(self.ROLE_DESCRIPTION)
            people = selected_items[0].data(self.ROLE_PEOPLE)
            tags = selected_items[0].data(self.ROLE_TAGS)
            location = selected_items[0].data(self.ROLE_LOCATION)
            date = selected_items[0].data(self.ROLE_DATE)


            # Создание PDF-отчёта
            try:
                # Путь для сохранения отчёта
                output_file = f"reports/photos/photo_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

                # Настройка документа
                doc = SimpleDocTemplate(output_file, pagesize=A4)
                elements = []

                # Добавляем изображение с сохранением пропорций
                try:
                    # Открываем изображение с помощью PIL
                    img = PILImage.open(path)
                    img_width, img_height = img.size

                    # Ограничения для размера изображения (максимальная ширина и высота)
                    max_width = 150 * mm  # Максимальная ширина
                    max_height = 150 * mm  # Максимальная высота

                    # Рассчитаем масштаб, чтобы сохранить пропорции
                    scale = min(max_width / img_width, max_height / img_height, 1)
                    display_width = img_width * scale
                    display_height = img_height * scale

                    # Добавляем изображение в PDF
                    img_element = Image(path, width=display_width, height=display_height)
                    elements.append(img_element)
                    elements.append(Spacer(1, 12))
                except Exception as e:
                    elements.append(Paragraph("Ошибка при загрузке изображения: " + str(e), styles["Normal"]))

                # Добавляем дату
                if date:
                    elements.append(Paragraph(f"<b>Дата:</b> {date}", styles["Normal"]))
                elements.append(Spacer(1, 12))

                # Добавляем локацию
                if location:
                    elements.append(Paragraph(f"<b>Местоположение:</b> {location}", styles["Normal"]))
                elements.append(Spacer(1, 12))

                # Добавляем список людей
                if people:
                    people_text = "<br/>".join(f"- {person}" for person in people.split(","))
                    elements.append(Paragraph(f"<b>Список людей:</b><br/>{people_text}", styles["Normal"]))
                elements.append(Spacer(1, 12))

                # Добавляем теги
                if tags:
                    tags_text = "<br/>".join(f"- {tag}" for tag in tags.split(","))
                    elements.append(Paragraph(f"<b>Теги:</b><br/>{tags_text}", styles["Normal"]))
                elements.append(Spacer(1, 6))

                # Добавляем описание
                elements.append(Paragraph(f"<b>Описание:</b> {description}", styles["Normal"]))
                elements.append(Spacer(1, 12))


                # Сохранение отчёта
                doc.build(elements)
                QMessageBox.information(self, "Успех", f"Отчёт сохранён по адресу {output_file}.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось создать отчёт: {str(e)}")
        else:
            QMessageBox.warning(self, "Ошибка", "Не выбрано ни одного элемента.")

    def make_album_report(self):
        """Создание отчёта по всему альбому"""
        if not self.db_connection.is_connected():
            self.db_connection.reconnect()
            # print("Соединение с БД восстановлено.")
        # Регистрация шрифта с поддержкой русского языка
        font_path = "FreeSans.ttf"  # Замените на путь к шрифту
        if not os.path.exists(font_path):
            QMessageBox.critical(self, "Ошибка", f"Шрифт не найден: {font_path}")
            return
        pdfmetrics.registerFont(TTFont("FreeSans", font_path))
        styles = {
            "Normal": ParagraphStyle(
                name="Normal",
                fontName="FreeSans",
                fontSize=12,
                leading=14
            ),
            "Title": ParagraphStyle(
                name="Title",
                fontName="FreeSans",
                fontSize=16,
                leading=18,
                spaceAfter=10
            )
        }

        try:
            # Запрос данных из базы
            cursor = self.db_connection.cursor()

            # Общее количество фотографий
            cursor.execute("SELECT COUNT(*) FROM photos")
            total_photos = cursor.fetchone()[0]

            # Количество избранных фотографий
            cursor.execute("SELECT COUNT(*) FROM photos WHERE isFavorite = 1")
            favorite_photos = cursor.fetchone()[0]

            # Данные из представлений
            cursor.execute("SELECT tag_name, photo_count FROM view_tag_stats")
            tag_stats = cursor.fetchall()

            cursor.execute("SELECT person_name, photo_count FROM view_people_stats")
            photo_stats = cursor.fetchall()

            cursor.execute("SELECT location_name, photo_count FROM view_location_stats")
            location_stats = cursor.fetchall()

            # Создание PDF-отчёта
            output_file = f"reports/albums/album_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            doc = SimpleDocTemplate(output_file, pagesize=A4)
            elements = []

            # Заголовок
            elements.append(Paragraph("Отчёт по текущему состоянию альбома", styles["Title"]))
            elements.append(Spacer(1, 12))

            # Текущее время
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elements.append(Paragraph(f"<b>Текущее время:</b> {current_time}", styles["Normal"]))
            elements.append(Spacer(1, 12))

            # Статистика фотографий
            elements.append(Paragraph(f"<b>Общее количество фотографий:</b> {total_photos}", styles["Normal"]))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"<b>Количество избранных фотографий:</b> {favorite_photos}", styles["Normal"]))
            elements.append(Spacer(1, 12))

            # Таблица тэгов
            if tag_stats:
                elements.append(Paragraph("<b>Статистика по тэгам:</b>", styles["Normal"]))
                data = [["Тэг", "Количество"]] + [[tag, count] for tag, count in tag_stats]
                table = Table(data, colWidths=[100, 50])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'FreeSans'),  # Задаём шрифт для всех ячеек
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 12))

            # Таблица фото
            if photo_stats:
                elements.append(Paragraph("<b>Статистика по фотографиям:</b>", styles["Normal"]))
                data = [["Описание", "Количество"]] + [[description, count] for description, count in photo_stats]
                table = Table(data, colWidths=[200, 50])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'FreeSans'),  # Задаём шрифт для всех ячеек
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 12))

            # Таблица локаций
            if location_stats:
                elements.append(Paragraph("<b>Статистика по местоположениям:</b>", styles["Normal"]))
                data = [["Местоположение", "Количество"]] + [[location, count] for location, count in location_stats]
                table = Table(data, colWidths=[200, 50])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'FreeSans'),  # Задаём шрифт для всех ячеек
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(table)

            # Сохранение отчёта
            doc.build(elements)
            QMessageBox.information(self, "Успех", f"Отчёт сохранён по адресу {output_file}.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать отчёт: {str(e)}")

    def make_photos_list_report(self):
        """Создание отчёта по фотографиям"""
        if not self.db_connection.is_connected():
            self.db_connection.reconnect()
            # print("Соединение с БД восстановлено.")

        # Регистрация шрифта с поддержкой русского языка
        font_path = "FreeSans.ttf"  # Замените на путь к шрифту
        if not os.path.exists(font_path):
            QMessageBox.critical(self, "Ошибка", f"Шрифт не найден: {font_path}")
            return
        pdfmetrics.registerFont(TTFont("FreeSans", font_path))

        styles = {
            "Normal": ParagraphStyle(
                name="Normal",
                fontName="FreeSans",
                fontSize=12,
                leading=14
            ),
            "Title": ParagraphStyle(
                name="Title",
                fontName="FreeSans",
                fontSize=16,
                leading=18,
                spaceAfter=10
            )
        }

        try:
            # Запрос данных из базы
            cursor = self.db_connection.cursor()

            # Получение данных из таблицы photos
            cursor.execute("SELECT photoID, file_path, isFavorite FROM photos")
            photos_data = cursor.fetchall()

            # Создание PDF-отчёта
            output_file = f"reports/photos_list/photos_list_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            doc = SimpleDocTemplate(output_file, pagesize=A4)
            elements = []

            # Заголовок
            elements.append(Paragraph("Отчёт по фотографиям", styles["Title"]))
            elements.append(Spacer(1, 12))

            # Текущее время
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elements.append(Paragraph(f"<b>Текущее время:</b> {current_time}", styles["Normal"]))
            elements.append(Spacer(1, 12))

            # Таблица фотографий
            if photos_data:
                elements.append(Paragraph("<b>Список фотографий:</b>", styles["Normal"]))
                data = [["ID фотографии", "Путь к файлу", "В избранном?"]]  # Заголовки на русском
                for photo in photos_data:
                    photo_id, creation_path, is_favorite = photo
                    favorite_status = "да" if is_favorite == 1 else "нет"  # Преобразование значений isFavorite
                    data.append([photo_id, creation_path, favorite_status])

                # Создание таблицы
                table = Table(data, colWidths=[50, 250, 50])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'FreeSans'),  # Задаём шрифт для всех ячеек
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(table)

            # Сохранение отчёта
            doc.build(elements)
            QMessageBox.information(self, "Успех", f"Отчёт сохранён по адресу {output_file}.")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать отчёт: {str(e)}")

    def fetch_location_data(self):
        if not self.db_connection.is_connected():
            self.db_connection.reconnect()
            # print("Соединение с БД восстановлено.")
        with self.db_connection.cursor() as cursor:
            # Получаем данные из таблиц locations и photos
            query = """
               SELECT locations.location_name, COUNT(photos.locationID) AS photo_count
               FROM locations
               LEFT JOIN photos ON locations.locationID = photos.locationID
               GROUP BY locations.locationID
               """
            cursor.execute(query)
            result = cursor.fetchall()

            # Преобразуем данные в удобный формат
            locations = [row[0] for row in result]
            photo_counts = [row[1] for row in result]

            return locations, photo_counts

    # Функция для получения данных о частоте людей на фотографиях по датам
    def fetch_people_on_photos_by_year(self):
        if not self.db_connection.is_connected():
            self.db_connection.reconnect()
            # print("Соединение с БД восстановлено.")
        with self.db_connection.cursor() as cursor:
            query = """
                SELECT
                    p.name AS person_name,
                    EXTRACT(YEAR FROM ph.creation_date) AS year,
                    COUNT(pp.photoID) AS photo_count
                FROM
                    photo_people pp
                JOIN
                    people p ON pp.personID = p.personID
                JOIN
                    photos ph ON pp.photoID = ph.photoID
                GROUP BY
                    p.name, EXTRACT(YEAR FROM ph.creation_date)
                ORDER BY
                    year, p.name;
                """
            cursor.execute(query)
            result = cursor.fetchall()

        # Преобразуем данные в удобный формат
        people_data = defaultdict(lambda: defaultdict(int))  # person_name -> {year: count}
        years = set()

        for row in result:
            person_name = row[0]
            year = row[1]
            photo_count = row[2]
            people_data[person_name][year] += photo_count
            years.add(year)

        # Сортируем года
        sorted_years = sorted(years)

        return people_data, sorted_years

    def fetch_popular_tags(self):
        query = """
        SELECT 
            t.tag_name, 
            COUNT(pt.photoID) AS tag_count
        FROM 
            photo_tags pt
        JOIN 
            tags t ON pt.tagID = t.tagID
        GROUP BY 
            t.tag_name
        ORDER BY 
            tag_count DESC;
        """
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        # Преобразуем данные в формат для круговой диаграммы
        tags = []
        tag_counts = []

        for row in result:
            tags.append(row[0])
            tag_counts.append(row[1])

        return tags, tag_counts

    def show_window_diagrams(self):
        # Получаем данные для первого графика (место и количество фотографий)
        locations, photo_counts = self.fetch_location_data()

        # Получаем данные для второй диаграммы (частота людей на фотографиях по годам)
        people_data, sorted_years = self.fetch_people_on_photos_by_year()

        # Получаем данные для третьей диаграммы (популярные теги)
        tag_names, tag_counts = self.fetch_popular_tags()

        # Передаем все данные в show_diagrams для построения всех графиков
        show_diagrams(locations, photo_counts, people_data, sorted_years, tag_names, tag_counts)

    def open_edit_folder_list_dialog(self):
        # Создаем экземпляр отдельного класса для второго окна
        dialog = EditFolderListDialog(self.db_connection)
        dialog.exec_()  # Открываем как модальное окно
        self.load_all_images()

    def open_image(self, item):
        # Получаем путь к изображению из пользовательской роли
        image_path = item.data(self.ROLE_PATH)
        if image_path:
            QDesktopServices.openUrl(QUrl.fromLocalFile(image_path))

    """методы редактирования даты"""
    def enable_editing_date(self, event):

        self.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        date_str = self.labelDate.text()
        new_date_time = QDateTime.fromString(date_str, "yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit.setDateTime(new_date_time)

        self.stackedDate.setCurrentWidget(self.editDate)

        self.dateTimeEdit.setFocus()

    def finish_editing_date(self):
        new_date_time = self.dateTimeEdit.dateTime().toPyDateTime()

        selected_items = self.listWidget.selectedItems()

        date_str = new_date_time.strftime("%Y-%m-%d %H:%M:%S")
        self.labelDate.setText(date_str)

        if selected_items:
            self.listWidget.selectedItems()[0].setData(self.ROLE_DATE, new_date_time)
            photo_id = selected_items[0].data(self.ROLE_PHOTO_ID)  # Получение ID фото
            self.update_creation_date(photo_id, date_str)

        self.stackedDate.setCurrentWidget(self.watchDate)

    def update_creation_date(self, photo_id, date_str):
        if not self.db_connection.is_connected():
            self.db_connection.reconnect()
            # print("Соединение с БД восстановлено.")
        try:
            # Подготовка SQL-запроса для обновления creation_date
            update_query = """UPDATE photos 
                              SET creation_date = %s 
                              WHERE photoID = %s"""

            with self.db_connection.cursor() as cursor:
                cursor.execute(update_query, (date_str, photo_id))

            self.db_connection.commit()

        except mysql.connector.Error as err:
            print(f"Ошибка при обновлении базы данных: {err}")

    """методы редактирования описания"""
    def enable_editing_description(self, event):
        description = self.labelDescription.text()

        self.textEditDescription.setText(description)

        self.stackedDescription.setCurrentWidget(self.editDescription)

        self.textEditDescription.setFocus()

    def finish_editing_description(self):
        description = self.textEditDescription.toPlainText()
        selected_items = self.listWidget.selectedItems()
        self.labelDescription.setText(description)

        if selected_items:
            self.listWidget.selectedItems()[0].setData(self.ROLE_DESCRIPTION, description)
            photo_id = selected_items[0].data(self.ROLE_PHOTO_ID)  # Получение ID фото
            self.update_description(photo_id, description)

        self.stackedDescription.setCurrentWidget(self.watchDescription)

    def update_description(self, photo_id, description):
        if not self.db_connection.is_connected():
            self.db_connection.reconnect()
            # print("Соединение с БД восстановлено.")
        try:
            # Подготовка SQL-запроса для обновления creation_date
            update_query = """UPDATE photos 
                                     SET description = %s 
                                     WHERE photoID = %s"""

            with self.db_connection.cursor() as cursor:
                cursor.execute(update_query, (description, photo_id))

            self.db_connection.commit()

        except mysql.connector.Error as err:
            print(f"Ошибка при обновлении базы данных: {err}")

    """методы редактирования места"""
    def enable_editing_location(self, event):
        location = self.labelLocation.text()
        self.textEditLocation.setText(location)
        self.stackedLocation.setCurrentWidget(self.editLocation)
        self.textEditLocation.setFocus()

    def finish_editing_location(self):
        location = self.textEditLocation.toPlainText()
        selected_items = self.listWidget.selectedItems()
        self.labelLocation.setText(location)

        if selected_items:
            self.listWidget.selectedItems()[0].setData(self.ROLE_LOCATION, location)
            photo_id = selected_items[0].data(self.ROLE_PHOTO_ID)  # Получение ID фото
            self.update_location(photo_id, location)

        self.stackedLocation.setCurrentWidget(self.watchLocation)

    def update_location(self, photo_id, location_name):
        if not self.db_connection.is_connected():
            self.db_connection.reconnect()
            # print("Соединение с БД восстановлено.")

        try:
            with self.db_connection.cursor() as cursor:
                # Получить текущий locationID для photo_id
                current_location_query = """SELECT locationID FROM photos WHERE photoID = %s"""
                cursor.execute(current_location_query, (photo_id,))
                current_location = cursor.fetchone()

                # Проверить, существует ли location_name в таблице locations
                check_query = """SELECT locationID FROM locations WHERE location_name = %s"""
                cursor.execute(check_query, (location_name,))
                result = cursor.fetchone()

                if result:
                    # Если location_name есть, берем его locationID
                    location_id = result[0]
                else:
                    # Если location_name нет, добавляем его в таблицу locations
                    insert_query = """INSERT INTO locations (location_name) VALUES (%s)"""
                    cursor.execute(insert_query, (location_name,))
                    self.db_connection.commit()

                    # Получаем locationID для нового location_name
                    location_id = cursor.lastrowid

                # Обновляем locationID в таблице photos для указанного photo_id
                update_query = """UPDATE photos SET locationID = %s WHERE photoID = %s"""
                cursor.execute(update_query, (location_id, photo_id))

                # Проверить, нужно ли удалить предыдущее место
                if current_location:
                    old_location_id = current_location[0]
                    check_old_location_query = """SELECT COUNT(*) FROM photos WHERE locationID = %s"""
                    cursor.execute(check_old_location_query, (old_location_id,))
                    count = cursor.fetchone()[0]

                    if count == 0:
                        delete_old_location_query = """DELETE FROM locations WHERE locationID = %s"""
                        cursor.execute(delete_old_location_query, (old_location_id,))

            # Фиксируем изменения в базе данных
            self.db_connection.commit()

        except mysql.connector.Error as err:
            print(f"Ошибка при обновлении базы данных: {err}")

    """методы редактирования лиц"""
    def enable_editing_people(self, event):
        people_str = self.labelPeople.text()

        self.textEditPeople.setText(people_str)
        self.stackedPeople.setCurrentWidget(self.editPeople)
        self.textEditPeople.setFocus()

    def finish_editing_people(self):
        people_str = self.textEditPeople.toPlainText()
        selected_items = self.listWidget.selectedItems()
        self.labelPeople.setText(people_str)

        if selected_items:
            self.listWidget.selectedItems()[0].setData(self.ROLE_PEOPLE, people_str)
            photo_id = selected_items[0].data(self.ROLE_PHOTO_ID)  # Получение ID фото
            self.update_people(photo_id, people_str)

        self.stackedPeople.setCurrentWidget(self.watchPeople)
        self.add_faces_to_combobox()

    def update_people(self, photo_id, people_str):
        if not self.db_connection.is_connected():
            self.db_connection.reconnect()
            # print("Соединение с БД восстановлено.")

        try:
            with self.db_connection.cursor() as cursor:
                # Получить текущий список связей людей для photo_id
                current_people_query = """SELECT personID FROM photo_people WHERE photoID = %s"""
                cursor.execute(current_people_query, (photo_id,))
                current_people = set(row[0] for row in cursor.fetchall())

                # Разделить строку с новыми людьми на список
                new_people = set()
                for person_name in people_str.split(', '):
                    if not person_name.strip():
                        # Пропускаем пустые имена
                        continue

                    # Проверить, существует ли person_name в таблице people
                    check_query = """SELECT personID FROM people WHERE name = %s"""
                    cursor.execute(check_query, (person_name,))
                    result = cursor.fetchone()

                    if result:
                        # Если человек уже есть, берем его personID
                        person_id = result[0]
                    else:
                        # Если человека нет, добавляем его в таблицу people
                        insert_query = """INSERT INTO people (name) VALUES (%s)"""
                        cursor.execute(insert_query, (person_name,))
                        self.db_connection.commit()

                        # Получаем personID для нового человека
                        person_id = cursor.lastrowid

                    new_people.add(person_id)

                # Удалить связи с людьми, которые больше не указаны
                people_to_remove = current_people - new_people
                if people_to_remove:
                    delete_query = """DELETE FROM photo_people WHERE photoID = %s AND personID = %s"""
                    for person_id in people_to_remove:
                        cursor.execute(delete_query, (photo_id, person_id))

                # Добавить новые связи с людьми
                people_to_add = new_people - current_people
                if people_to_add:
                    insert_query = """INSERT INTO photo_people (photoID, personID) VALUES (%s, %s)"""
                    for person_id in people_to_add:
                        cursor.execute(insert_query, (photo_id, person_id))

                # Удалить записи о людях, если на них больше нет ссылок
                for person_id in people_to_remove:
                    check_person_query = """SELECT COUNT(*) FROM photo_people WHERE personID = %s"""
                    cursor.execute(check_person_query, (person_id,))
                    count = cursor.fetchone()[0]

                    if count == 0:
                        delete_person_query = """DELETE FROM people WHERE personID = %s"""
                        cursor.execute(delete_person_query, (person_id,))

            # Фиксируем изменения в базе данных
            self.db_connection.commit()

        except mysql.connector.Error as err:
            print(f"Ошибка при обновлении базы данных: {err}")

    """методы редактирования тегов"""
    def enable_editing_tags(self, event):
        tags_str = self.labelTags.text()

        self.textEditTags.setText(tags_str)
        self.stackedTags.setCurrentWidget(self.editTags)
        self.textEditTags.setFocus()

    def finish_editing_tags(self):
        tags_str = self.textEditTags.toPlainText()
        selected_items = self.listWidget.selectedItems()
        self.labelTags.setText(tags_str)

        if selected_items:
            self.listWidget.selectedItems()[0].setData(self.ROLE_TAGS, tags_str)
            photo_id = selected_items[0].data(self.ROLE_PHOTO_ID)  # Получение ID фото
            self.update_tags(photo_id, tags_str)

        self.stackedTags.setCurrentWidget(self.watchTags)

    def update_tags(self, photo_id, tags_str):
        if not self.db_connection.is_connected():
            self.db_connection.reconnect()
            # print("Соединение с БД восстановлено.")

        try:
            with self.db_connection.cursor() as cursor:
                # Получить текущий список связей людей для photo_id
                current_tags_query = """SELECT tagID FROM photo_tags WHERE photoID = %s"""
                cursor.execute(current_tags_query, (photo_id,))
                current_tags = set(row[0] for row in cursor.fetchall())

                # Разделить строку с новыми людьми на список
                new_tags = set()
                for tag_name in tags_str.split(', '):
                    if not tag_name.strip():
                        # Пропускаем пустые имена
                        continue

                    # Проверить, существует ли person_name в таблице people
                    check_query = """SELECT tagID FROM tags WHERE tag_name = %s"""
                    cursor.execute(check_query, (tag_name,))
                    result = cursor.fetchone()

                    if result:
                        # Если человек уже есть, берем его personID
                        tag_id = result[0]
                    else:
                        # Если человека нет, добавляем его в таблицу people
                        insert_query = """INSERT INTO tags (tag_name) VALUES (%s)"""
                        cursor.execute(insert_query, (tag_name,))
                        self.db_connection.commit()

                        # Получаем personID для нового человека
                        tag_id = cursor.lastrowid

                    new_tags.add(tag_id)

                # Удалить связи с людьми, которые больше не указаны
                tags_to_remove = current_tags - new_tags
                if tags_to_remove:
                    delete_query = """DELETE FROM photo_tags WHERE photoID = %s AND tagID = %s"""
                    for tag_id in tags_to_remove:
                        cursor.execute(delete_query, (photo_id, tag_id))

                # Добавить новые связи с тегами
                tags_to_add = new_tags - current_tags
                if tags_to_add:
                    insert_query = """INSERT INTO photo_tags (photoID, tagID) VALUES (%s, %s)"""
                    for tag_id in tags_to_add:
                        cursor.execute(insert_query, (photo_id, tag_id))

                # Удалить записи о тегах, если на них больше нет ссылок
                for tag_id in tags_to_remove:
                    check_tag_query = """SELECT COUNT(*) FROM photo_tags WHERE tagID = %s"""
                    cursor.execute(check_tag_query, (tag_id,))
                    count = cursor.fetchone()[0]

                    if count == 0:
                        delete_tag_query = """DELETE FROM tags WHERE tagID = %s"""
                        cursor.execute(delete_tag_query, (tag_id,))

            # Фиксируем изменения в базе данных
            self.db_connection.commit()

        except mysql.connector.Error as err:
            print(f"Ошибка при обновлении базы данных: {err}")

    # переопределение метода для завершения редактирования определённого поля
    def mousePressEvent(self, event):
        if self.stackedDate.currentWidget() == self.stackedDate.findChild(QWidget, "editDate"):
            self.finish_editing_date()
        if self.stackedDescription.currentWidget() == self.stackedDescription.findChild(QWidget, "editDescription"):
            self.finish_editing_description()
        if self.stackedLocation.currentWidget() == self.stackedLocation.findChild(QWidget, "editLocation"):
            self.finish_editing_location()
        if self.stackedPeople.currentWidget() == self.stackedPeople.findChild(QWidget, "editPeople"):
            self.finish_editing_people()
        if self.stackedTags.currentWidget() == self.stackedTags.findChild(QWidget, "editTags"):
            self.finish_editing_tags()

    """Методы отвечающие за работу кнопки Доваить в избранное"""
    def add_remove_favorite(self):
        if not self.db_connection.is_connected():
            self.db_connection.reconnect()
            # print("Соединение с БД восстановлено.")
        selected_items = self.listWidget.selectedItems()

        if selected_items:
            photo_id = selected_items[0].data(self.ROLE_PHOTO_ID)  # Получение ID фото
            is_favorite = selected_items[0].data(self.ROLE_IS_FAVORITE)

            if is_favorite:
                self.remove_from_favorite(photo_id)
                self.listWidget.selectedItems()[0].setData(self.ROLE_IS_FAVORITE, 0)
            else:
                self.add_to_favorite(photo_id)
                self.listWidget.selectedItems()[0].setData(self.ROLE_IS_FAVORITE, 1)

        # после добавления удаления проверка информации
        selected_items = self.listWidget.selectedItems()
        self.update_fav_button(selected_items)

        if self.album_displayed == 'favorite':
            self.load_favorite()

    def add_to_favorite(self, photo_id):
        try:
            with self.db_connection.cursor() as cursor:
                # Обновляем столбец isFavorite в таблице photos
                cursor.execute("UPDATE photos SET isFavorite = 1 WHERE photoID = %s", (photo_id,))
            self.db_connection.commit()
            # print(f"Фото {photo_id} добавлено в избранное.")
        except Exception as e:
            print(f"Ошибка при добавлении в избранное: {e}")

    def remove_from_favorite(self, photo_id):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("UPDATE photos SET isFavorite = 0 WHERE photoID = %s", (photo_id,))
            self.db_connection.commit()
            # print(f"Фото {photo_id} удалено из избранного.")
        except Exception as e:
            print(f"Ошибка при удалении из избранного: {e}")

    def reset_filters(self):
        # очистка комбобоксов
        for cb in self.comboboxes:
            cb.clear()
        self.add_faces_to_combobox()
        for cb in self.comboboxes:
            cb.setCurrentIndex(0)

        # сброс дат
        self.dateEdit.setDate(datetime.date(1800, 1, 1))
        self.dateEdit_2.setDate(datetime.date.today())

        # сбросить теги
        self.textEdit.clear()
        if self.filtered:
            self.load_all_images()

    def load_images(self, images_info):
        # предварительная очистка
        self.listWidget.clear()

        self.listWidget.setViewMode(QListWidget.IconMode)  # Режим значков
        self.listWidget.setIconSize(QtCore.QSize(100, 200))  # Размер значков
        self.listWidget.setResizeMode(QListWidget.Adjust)  # Автоматическая настройка

        # Отключаем возможность перетаскивания и сброса элементов
        self.listWidget.setDragEnabled(False)

        for info_tuple in images_info:
            photo_id = info_tuple[0]
            path = info_tuple[1]
            img_name = path.split('/')[-1]
            creation_date = info_tuple[2]
            location_name = info_tuple[3]
            people_names = info_tuple[4]
            tag_names = info_tuple[5]
            description = info_tuple[6]
            is_favorite = bool(info_tuple[7])

            preview_path = f"previews\\{photo_id}.jpg"
            # Загружаем изображение
            pixmap = QPixmap(preview_path)
            if pixmap.isNull():
                # сжатие изображения процентов на 70 (расширения)
                # сохранение его по адресу f"previews\\{photo_id}"
                # присвоение pixmap этого сжатого изображения

                img = PILImage.open(path)
                #
                # # Вычислить новый размер (сжать на 70%)
                # width, height = img.size
                # new_width = int(width * 0.08)
                # new_height = int(height * 0.08)
                # # if new_width < 400 or new_height < 400:
                # #     if new_width < new_height:
                # #         new_width = 400
                # #     if new_height < new_width:
                # #         new_height = 400
                #
                # # Изменить размер изображения
                # img_resized = img.resize((new_width, new_height), PILImage.Resampling.LANCZOS)
                # # Сохранить сжатое изображение
                # img_resized.save(preview_path)

                img.thumbnail((600, 600), PILImage.Resampling.LANCZOS)
                img.save(preview_path, format='JPEG', quality=85)

                pixmap = QPixmap(preview_path)
                if pixmap.isNull():
                    continue


            # Создаем элемент с иконкой
            item = QListWidgetItem(QIcon(pixmap), "")
            item.setData(self.ROLE_PIXMAP, pixmap)  # Сохраняем QPixmap в данных элемента
            item.setData(self.ROLE_IMAGE_NAME, img_name)
            item.setData(self.ROLE_PATH, path)
            item.setData(self.ROLE_DATE, creation_date)
            item.setData(self.ROLE_LOCATION, location_name)
            item.setData(self.ROLE_PEOPLE, people_names)
            item.setData(self.ROLE_TAGS, tag_names)
            item.setData(self.ROLE_DESCRIPTION, description)
            item.setData(self.ROLE_PHOTO_ID, photo_id)
            item.setData(self.ROLE_IS_FAVORITE, is_favorite)

            self.listWidget.addItem(item)

        self.buttonAddToFav.setText('')
        self.buttonAddToFav.setEnabled(False)

        # в стакедвиджетс только нужные оставить
        self.stackedDate.setCurrentWidget(self.watchDate)
        self.stackedDescription.setCurrentWidget(self.watchDescription)

    def load_all_images(self):
        if not self.db_connection.is_connected():
            self.db_connection.reconnect()
            # print("Соединение с БД восстановлено.")

        with self.db_connection.cursor() as cursor:
            cursor.execute("SELECT * FROM view_photo_info")
            images_info = cursor.fetchall()
        self.load_images(images_info)
        # print(images_info)
        self.filtered = False

        self.reset_filters()

        self.album_displayed = 'all'

    def add_faces_to_combobox(self):
        if not self.db_connection.is_connected():
            self.db_connection.reconnect()
            # print("Соединение с БД восстановлено.")
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT name FROM people")
                faces = cursor.fetchall()
            faces = [name[0] for name in faces]
            for combobox in self.comboboxes:
                # combobox.addItem(self.default_face)  # Добавляем первый элемент
                self.faces = [self.default_face] + faces
                combobox.addItems(self.faces)
                combobox.setCurrentIndex(0)  # Устанавливаем первый элемент по умолчанию

                # print(self.faces)
                # combobox.currentIndexChanged.connect(self.update_comboboxes)
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def load_favorite(self):
        if not self.db_connection.is_connected():
            self.db_connection.reconnect()
            # print("Соединение с БД восстановлено.")

        with self.db_connection.cursor() as cursor:
            cursor.execute("SELECT * FROM view_photo_info WHERE isFavorite = 1")
            images_info = cursor.fetchall()
        self.load_images(images_info)
        # print(images_info)
        self.filtered = False

        self.reset_filters()

        self.album_displayed = 'favorite'

    def update_preview_image(self, selected_items):
        # обновить превью
        pixmap = selected_items[0].data(Qt.UserRole)  # Получение изображения (QPixmap)
        if isinstance(pixmap, QPixmap):
            # Масштабируем изображение под размер label_4
            scaled_pixmap = pixmap.scaled(self.label_4.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_4.setPixmap(scaled_pixmap)  # Установка масштабированного изображения в label_4
            self.label_4.setAlignment(Qt.AlignCenter)

    def update_info_labels(self, selected_items):
        # Получаем данные из первого выделенного элемента
        selected_item = selected_items[0]

        # Достаём данные из элемента
        date = str(selected_item.data(self.ROLE_DATE))  # Дата создания
        location = selected_item.data(self.ROLE_LOCATION)  # Местоположение
        people = selected_item.data(self.ROLE_PEOPLE)  # Имена людей
        tags = selected_item.data(self.ROLE_TAGS)  # Теги
        description = selected_item.data(self.ROLE_DESCRIPTION)  # Описание

        # Обновляем текстовые поля
        self.labelDate.setText(date if date else "")
        self.labelLocation.setText(location if location else "")
        self.labelPeople.setText(people if people else "")
        self.labelTags.setText(tags if tags else "")
        self.labelDescription.setText(description if description else "")

    def update_fav_button(self, selected_items):
        # обновить текст кнопки
        is_favorite = selected_items[0].data(self.ROLE_IS_FAVORITE)
        if is_favorite:
            self.buttonAddToFav.setText('Убрать из избранного')

        else:
            self.buttonAddToFav.setText('Добавить в избранное')

    def update_labels(self):

        # Получение текущего выделенного элемента
        selected_items = self.listWidget.selectedItems()
        if selected_items:
            self.update_preview_image(selected_items)
            self.update_info_labels(selected_items)
            self.update_fav_button(selected_items)
            self.buttonAddToFav.setEnabled(True)
        else:
            self.label_4.clear()
            self.stackedDate.currentWidget().findChild(QLabel, "labelDate").clear()
            self.labelLocation.clear()
            self.labelPeople.clear()
            self.labelTags.clear()
            self.labelDescription.clear()
            self.buttonAddToFav.setEnabled(False)

    def filter_by_tags(self):
        if not self.db_connection.is_connected():
            self.db_connection.reconnect()
            # print("Соединение с БД восстановлено.")
        try:
            text = self.textEdit.toPlainText()
            tags = re.findall(r'#\w+', text)
            cleaned_tags = [tag[1:] for tag in tags]

            if not cleaned_tags:
                if self.filtered:
                    self.filtered = False
                    self.load_all_images()
                # print("No tags found.")
                return

            num_tags = len(cleaned_tags)
            query = f"""
                SELECT pt.photoID
                FROM photo_tags pt
                JOIN tags t ON pt.tagID = t.tagID
                WHERE t.tag_name IN ({', '.join(['%s'] * len(cleaned_tags))})
                GROUP BY pt.photoID
                HAVING COUNT(DISTINCT t.tagID) = %s;
            """

            # Используем локальный курсор
            with self.db_connection.cursor() as cursor:
                cursor.execute(query, cleaned_tags + [num_tags])
                result = cursor.fetchall()

            photo_ids = [row[0] for row in result]
            # print("photoID, соответствующие всем тегам:", photo_ids)

            if not photo_ids:
                # print("No matching photos found.")
                self.listWidget.clear()
                self.filtered = True
                return

            with self.db_connection.cursor() as cursor:
                # SQL-запрос для получения информации о фотографиях по photoID
                query_info = f"""
                            SELECT *
                            FROM view_photo_info
                            WHERE photoID IN ({', '.join(['%s'] * len(photo_ids))});
                        """

                # Выполняем второй запрос — получаем данные о фотографиях
                cursor.execute(query_info, photo_ids)
                results = cursor.fetchall()

            # print("Результат:", results)
            self.load_images(results)
            self.filtered = True

        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def filter_by_all(self):
        if not self.db_connection.is_connected():
            self.db_connection.reconnect()
            # print("Соединение с БД восстановлено.")

        try:
            # Получение тегов из текста
            text = self.textEdit.toPlainText()
            tags = re.findall(r'#\w+', text)
            cleaned_tags = [tag[1:] for tag in tags]

            # Получение дат из QDateEdit
            qdate1 = self.dateEdit.date()
            qdate2 = self.dateEdit_2.date()
            datetime1 = datetime.datetime(qdate1.year(), qdate1.month(), qdate1.day(), 0, 0, 0)
            datetime2 = datetime.datetime(qdate2.year(), qdate2.month(), qdate2.day(), 23, 59, 59)
            datetime1_str = datetime1.strftime('%Y-%m-%d %H:%M:%S')
            datetime2_str = datetime2.strftime('%Y-%m-%d %H:%M:%S')

            # Получение лиц из комбобоксов
            faces = [combobox.currentText() for combobox in self.comboboxes
                     if combobox.currentText() != self.default_face]

            # Проверяем наличие фильтров
            filters_applied = any([cleaned_tags, faces, datetime1_str, datetime2_str])
            if not filters_applied:
                if self.filtered:
                    self.filtered = False
                    self.load_all_images()
                # print("No filters applied.")
                return

            # Формирование основной части SQL-запроса
            query_conditions = []
            query_params = []

            if cleaned_tags:
                query_conditions.append(f"t.tag_name IN ({', '.join(['%s'] * len(cleaned_tags))})")
                query_params.extend(cleaned_tags)
            if faces:
                query_conditions.append(f"""pp.photoID IN (
                SELECT
                pp_inner.photoID
                FROM
                photo_people
                pp_inner
                JOIN
                people
                p_inner
                ON
                pp_inner.personID = p_inner.personID
                WHERE
                p_inner.name
                IN({', '.join(['%s'] * len(faces))})
                GROUP
                BY
                pp_inner.photoID
                HAVING
                COUNT(DISTINCT
                p_inner.personID) = %s
                )""")
                query_params.extend(faces + [len(faces)])
            if datetime1_str and datetime2_str:
                query_conditions.append("creation_date BETWEEN %s AND %s")
                query_params.extend([datetime1_str, datetime2_str])

            if not query_conditions:
                # print("No filters applied.")
                return

            # SQL-запрос с учетом всех условий
            query = f"""
                SELECT DISTINCT vpi.photoID, vpi.file_path, vpi.creation_date, vpi.location_name, 
                                vpi.people_names, vpi.tag_names, vpi.description, vpi.isFavorite
                FROM view_photo_info vpi
                LEFT JOIN photo_tags pt ON vpi.photoID = pt.photoID
                LEFT JOIN tags t ON pt.tagID = t.tagID
                LEFT JOIN photo_people pp ON vpi.photoID = pp.photoID
                WHERE {' AND '.join(query_conditions)};
            """

            with self.db_connection.cursor() as cursor:
                cursor.execute(query, query_params)
                results = cursor.fetchall()

            if not results:
                # print("No matching photos found.")
                self.listWidget.clear()
                self.filtered = True
                return

            # print("Результат:", results)
            self.load_images(results)
            self.filtered = True

        except Exception as e:
            print(f"Произошла ошибка: {e}")


# Основной код для запуска приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
