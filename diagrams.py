import numpy as np
import matplotlib.pyplot as plt

def diagram_bar(ax, dataset, labels):
    # Первая диаграмма (столбчатая)
    ax.bar(labels, dataset, color='purple')
    ax.set_title('Количество фотографий в разных местах')
    ax.set_xticks(labels)


def diagram_graph(ax, dataset_list, labels):
    # Вторая диаграмма (графики), показывающая количество фотографий с каждым человеком по датам
    for dataset, label in dataset_list:
        ax.plot(labels, dataset, label=label)
    ax.set_title('Частота людей на фотографиях по годам')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Количество фотографий')
    ax.legend()

def diagram_pie(ax, dataset, labels):
    # Третья диаграмма (круговая) - популярные теги
    ax.pie(dataset, labels=labels, autopct=lambda p: f'{int(p/100. * sum(dataset))}', startangle=90)
    ax.set_title('Популярные теги на фотографиях')

    # Изменение размера круговой диаграммы
    ax.set_position([0.6, 0.1, 0.3, 0.3])  # Увеличиваем размер, изменяя координаты (left, bottom, width, height)


def show_diagrams(locations, photo_counts, people_data, sorted_years, tag_names, tag_counts):
    # Создаем первое окно для столбчатой диаграммы
    fig1 = plt.figure(figsize=(8, 6))
    ax1 = fig1.add_subplot(111)
    diagram_bar(ax1, photo_counts, locations)
    plt.show()

    # Создаем второе окно для линейных графиков
    fig2 = plt.figure(figsize=(8, 6))
    ax2 = fig2.add_subplot(111)

    # Формируем данные для графиков частоты людей на фотографиях по годам
    person_datasets = []
    for person_name, year_counts in people_data.items():
        dataset = [year_counts.get(year, 0) for year in sorted_years]
        person_datasets.append((dataset, person_name))

    diagram_graph(ax2, person_datasets, sorted_years)
    plt.show()

    # Создаем третье окно для круговой диаграммы, которое занимает всё окно
    fig3 = plt.figure(figsize=(8, 6))  # Размер окна для круговой диаграммы
    ax3 = fig3.add_subplot(111)

    # Рисуем круговую диаграмму с количеством упоминаний вместо процентов
    ax3.pie(tag_counts, labels=tag_names, autopct=lambda p: f'{int(p * sum(tag_counts) / 100)}', startangle=90)

    # Сделать оси равными, чтобы диаграмма была круглой
    ax3.axis('equal')  # Это важный шаг

    plt.show()



# Основная часть программы (мейн)
if __name__ == "__main__":
    # Данные для диаграмм
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.tan(x) / 10  # Меньшая амплитуда для y3
    y_list = [(y1, 'sin(x)'), (y2, 'cos(x)'), (y3, 'tan(x)')]

    # Пример данных для круговой диаграммы
    y3_pie = [15, 30, 45, 10]  # Пример данных для круговой диаграммы
    labels = ['A', 'B', 'C', 'D']

    # Вызов функции для отображения диаграмм
    show_diagrams(labels, y3_pie, y3_pie, labels, x, y_list)
