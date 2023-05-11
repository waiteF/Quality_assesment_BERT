import chatgpt_prompt as api
import bert_quality_assesment as bert
import database as db
from langdetect import detect
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Додаток аналізу тексту")
        self.geometry("700x500")  # Задаем размер окна

        # Створення вкладок
        self.notebook = ttk.Notebook(self)
        self.add_text_tab = ttk.Frame(self.notebook)
        self.read_from_file = ttk.Frame(self.notebook)
        self.results_tab = ttk.Frame(self.notebook)
        self.analysis_data_tab = ttk.Frame(self.notebook)

        # Додавання вкладок до ноутбука
        self.notebook.add(self.add_text_tab, text="Додати текст")
        self.notebook.add(self.read_from_file, text="Зчитати з файлу")
        self.notebook.add(self.results_tab, text="Аналіз переводу")
        self.notebook.add(self.analysis_data_tab, text="База даних")
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Кнопка додавання тексту
        self.add_text_button = ttk.Button(self.add_text_tab, text="Аналізувати", command=self.add_text)
        self.add_text_button.grid(row=2, column=0, padx=10, pady=10)

        # Поля "Обзор" для зчитування даних з файлів

        self.file1_label = tk.Label(self.read_from_file, text="Файл 1:")
        self.file1_label.grid(row=0, column=0, pady=10)

        self.file1_path = tk.StringVar()
        self.file1_entry = tk.Entry(self.read_from_file, textvariable=self.file1_path, width=50)
        self.file1_entry.grid(row=0, column=1, pady=5)

        self.browse1_button = tk.Button(self.read_from_file, text="Обзор...", command=self.browse_file1)
        self.browse1_button.grid(row=0, column=2, pady=5)

        self.file2_label = tk.Label(self.read_from_file, text="Файл 2:")
        self.file2_label.grid(row=1, column=0, pady=10)

        self.file2_path = tk.StringVar()
        self.file2_entry = tk.Entry(self.read_from_file, textvariable=self.file2_path, width=50)
        self.file2_entry.grid(row=1, column=1, pady=5)

        self.browse2_button = tk.Button(self.read_from_file, text="Обзор...", command=self.browse_file2)
        self.browse2_button.grid(row=1, column=2, pady=5)

        self.read_button = tk.Button(self.read_from_file, text="Зчитати", command=self.read_files)
        self.read_button.grid(row=2, column=0, columnspan=3, pady=5)

        self.data_label = tk.Label(self.read_from_file, text="Результат:")
        self.data_label.grid(row=3, column=0, pady=10)

        self.data_text = tk.Text(self.read_from_file, height=10, width=50)
        self.data_text.grid(row=4, column=0, columnspan=3, pady=5)


        # Поля для введення тексту
        self.text_label1 = ttk.Label(self.add_text_tab, text="Основний текст")
        self.text_label1.grid(row=0, column=0, padx=10, pady=10)
        self.text_entry1 = tk.Text(self.add_text_tab, height=10, width=50)
        self.text_entry1.grid(row=0, column=1, padx=10, pady=10)

        self.text_label2 = ttk.Label(self.add_text_tab, text="Автоматизований переклад")
        self.text_label2.grid(row=1, column=0, padx=10, pady=10)
        self.text_entry2 = tk.Text(self.add_text_tab, height=10, width=50)
        self.text_entry2.grid(row=1, column=1, padx=10, pady=10)

        # Мітка для відображення результатів
        self.results_label = scrolledtext.ScrolledText(self.results_tab, wrap="word", width=60, height=10)
        self.results_label.pack(padx=10, pady=10)

        # Ввод PRIMARY KEY щоб отримати результат з бд
        self.text_key_db = ttk.Entry(self.analysis_data_tab)
        self.text_key_db.grid(row=0, column=0, padx=10, pady=10)

        self.button_db = ttk.Button(self.analysis_data_tab, text="Запит", command=self.get_data_db)
        self.button_db.grid(row=1, column=0, padx=10, pady=10)
        self.text_db_label = scrolledtext.ScrolledText(self.analysis_data_tab, wrap="word", width=60, height=10)
        self.text_db_label.grid(row=2, column=0, padx=10, pady=10)

    # обзор файла
    def browse_file1(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        self.file1_path.set(file_path)

    def browse_file2(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        self.file2_path.set(file_path)

    # зчитати дані
    def read_files(self):
        file1_path = self.file1_path.get()
        file2_path = self.file2_path.get()

        try:
            with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r') as file2:
                data1 = file1.read()
                data2 = file2.read()

                self.data_text.delete('1.0', tk.END)
                self.data_text.insert(tk.END, "Результат з файлу 1:\n\n")
                self.data_text.insert(tk.END, data1)
                self.data_text.insert(tk.END, "\n\nРезультат з файлу 2:\n\n")
                self.data_text.insert(tk.END, data2)
                self.add_text(data1, data2)
        except FileNotFoundError:
            tk.messagebox.showerror("Помилка", "Один або обидва файли не знайдені.")



    # отримати дані з бд
    def get_data_db(self):
        key = self.text_key_db.get()
        list = []
        list = db.get_data(key)
        print(list)
        # Очищаем содержимое scrolledtext перед вставкой новых данных
        self.text_db_label.delete("1.0", "end")

        for item in list:
            self.text_db_label.insert("end", str(item) + "\n")

    # визначення мови перекладу
    def detect_language(self, text):
        language = detect(text)
        if language in ['uk', 'en']:
            return language
        else:
            return None

    def add_text(self, native, automate_translate):
        native_text = ""
        automate_translate_text = ""
        if len(native.strip()) != 0 and len(automate_translate.strip()) != 0:
            native_text = native
            automate_translate_text = automate_translate
        else:
            # Получение введенного текста
            native_text = self.text_entry1.get("1.0", tk.END).strip()
            automate_translate_text = self.text_entry2.get("1.0", tk.END).strip()

        # Проверка текста
        language_form_one = self.detect_language(native_text)
        language_form_two = self.detect_language(automate_translate_text)

        # Очищаем содержимое scrolledtext перед вставкой новых данных
        self.text_db_label.delete("1.0", tk.END)

        if language_form_one is None or language_form_two is None:
            temp = "Ви використали ні української, ні англійської мови " + str(language_form_one) + " " + str(
                language_form_two)
            self.results_label.insert(tk.END, temp)
            return

        if language_form_one == language_form_two:
            temp = "Помилка, ви використали одну і ту саму мову: " + str(language_form_one)
            self.results_label.insert(tk.END, temp)
            return

        # Анализ текста
        professional_translate = ""

        if language_form_one == "uk":
            professional_translate = api.generate_text(
                "Make a translation of the text from Ukrainian to English, you only need a translation, "
                "without unnecessary text and explanations - " + native_text)

        if language_form_one == "en":
            professional_translate = api.generate_text(
                "Make a translation of the text from English to Ukrainian, you only need a translation, "
                "without unnecessary text and explanations - " + native_text)

        similarity_score = bert.execute_analysis(professional_translate, automate_translate_text)
        # Обновление метки с результатами
        temp = "Результати аналізу: " + str(
            similarity_score) + "\nПрофесійний переклад: " + professional_translate + "\nЗвичайний переклад: " + automate_translate_text
        self.results_label.insert(tk.END, temp)

        # Добавление данных в базу данных
        abbreviation = language_form_one + "/" + language_form_two
        db.database_call(native_text, automate_translate_text, professional_translate, similarity_score, abbreviation)


if __name__ == "__main__":
    app = App()
    app.mainloop()
