"""Требуется написать объектно-ориентированную программу с графическим интерфейсом в соответствии со своим вариантом.
В программе должны быть реализованы минимум один класс, три атрибута, четыре метода (функции).
Ввод данных из файла с контролем правильности ввода.
Базы данных использовать нельзя. При необходимости сохранять информацию в виде файлов, разделяя значения запятыми или пробелами.
Для GUI использовать библиотеку tkinter.
Объекты – договоры на медицинское обслуживание
Функции:	сегментация полного списка договоров по видам услуг
визуализация предыдущей функции в форме круговой диаграммы
сегментация полного списка договоров по врачам
визуализация предыдущей функции в форме круговой диаграммы"""

from tkinter import *
import tkinter.filedialog as fd
from tkinter.messagebox import showinfo, showerror, askyesno
from tkinter import ttk
import matplotlib.pyplot as plt
import re
import os

firstRun = True

class Service:
    manager_counts = {}
    service_counts = {}

    def __init__(self, manager, service, price):
        self.manager = manager
        self.service = service
        self.price = price
        self.update_counts(manager, service)

#Обновление количества элементов
    def update_counts(self, manager, service):
        Service.manager_counts[manager] = Service.manager_counts.get(manager, 0) + 1
        Service.service_counts[service] = Service.service_counts.get(service, 0) + 1

#Количество элементов
    @classmethod
    def count_manager_instances(cls, manager):
        return cls.manager_counts.get(manager, 0)

    @classmethod
    def count_service_instances(cls, service):
        return cls.service_counts.get(service, 0)

#Уникальные элементы
    @classmethod
    def unique_managers(cls):
        return list(cls.manager_counts.keys())

    @classmethod
    def unique_services(cls):
        return list(cls.service_counts.keys())



#Чтение файла
def entery():
    global firstRun
    errorFlag = False

    #Если файл открывается повторно
    if not firstRun:
        if askyesno(title="Информация", message="При повторном открытии файла старые данный сотрутся"):
            for i in tree.get_children():
                tree.delete(i)
        else:
            return
    else:
        firstRun = False
    showinfo(title="Информация", message="Советуется использовать формат: '<Имя Врача>, <Сервис>, <Цена>'")


    filename = fd.askopenfilename(filetypes=[("Текстовый файл", "*.txt")])
    with open(filename) as f:
        try:

            #Если файл пуст
            if os.path.getsize(filename) == 0:
                showinfo(title="Ошибка", message="Выбранный файл пуст.")
                firstRun = True

            #Работа с файлом
            for line in f:
                line = line.split()
                if re.match(r'^\d+(\.\d+)?$', line[2]):
                    Service(line[0], line[1], line[2])
                    tree.insert("", END, values=(line[0], line[1], line[2]))
                else:
                    errorFlag = True
                    continue

            #Если обнаружился неверный формат данных
            if errorFlag:
                print(1)
                showinfo(title="Ошибка", message="Некоторые данные имеют неверный формат")

        except Exception:
            showerror(title="Ошибка", message="Ошибка!")

#Cегментация по видам услуг
def pieService():
    plt.close()
    labels = Service.unique_services()
    vals = []
    for i in labels:
        print(i)
        vals.append(Service.count_service_instances(str(i)))
    plt.pie(vals, labels=labels, autopct='%1.1f%%')
    plt.title("Cегментация по видам услуг")
    plt.show()

#Cегментация по врачам
def pieManager():
    plt.close()
    labels = Service.unique_managers()
    vals = []
    for i in labels:
        print(i)
        vals.append(Service.count_manager_instances(str(i)))
    plt.pie(vals, labels=labels, autopct='%1.1f%%')
    plt.title("Cегментация по врачам")
    plt.show()




#Окно
root = Tk()
root.geometry("600x300")
root.resizable(False, False)
root.title("Code Output")

#Кнопки
text1 = Label(root, text="Загрузите файл")
text1.grid(row=1, column=1)
enter_button = Button(root, text="Загрузить файл", command=entery)
enter_button.grid(row=2, column=1)
ServiceButton = Button(root, text="Cегментация по видам услуг", command=pieService)
ServiceButton.grid(row=3, column= 1)
ManagerButton = Button(root, text="Cегментация по врачам", command=pieManager)
ManagerButton.grid(row=4, column=1)

#Таблица
columns = ("manager", "service", "price")
tree = ttk.Treeview(columns=columns, show="headings")
tree.grid(row=5,column=1, sticky="nsew")
tree.heading("manager", text="Имя")
tree.heading("service", text="Услуга")
tree.heading("price", text="Цена")


root.mainloop()