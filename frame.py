import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Frame, Label
import random
import os
from PIL import Image, ImageTk
import time
import winsound  # Для звуков (Windows)

# Создаем папку для изображений
images_folder = "chat_images"
if not os.path.exists(images_folder):
    os.makedirs(images_folder)


# История сообщений
chat_history = []

def format_message(message):
    """Форматирование текста: *курсив* и **жирный**"""
    if message.startswith('*') and message.endswith('*') and len(message) > 1:
        return f"<i>{message[1:-1]}</i>"
    elif message.startswith('**') and message.endswith('**') and len(message) > 2:
        return f"<b>{message[2:-2]}</b>"
    return message

def send_message(event=None):
    """Отправка сообщения пользователем"""
    message = message_entry.get("1.0", "end-1c").strip()
    if message:
        chat_area.config(state=tk.NORMAL)
        formatted_message = format_message(message)
        chat_area.insert(tk.END, f"Вы: {formatted_message}\n\n")
        chat_area.see(tk.END)
        chat_area.config(state=tk.DISABLED)
        chat_history.append(("user", message))
        message_entry.delete("1.0", tk.END)
        message_entry.config(height=2)
        winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)  # Звук отправки
        root.after(1000, show_typing_indicator)
    if event:
        return "break"

def show_typing_indicator():
    """Показ индикатора 'Гость думает...'"""
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "Гость думает...\n")
    chat_area.see(tk.END)
    chat_area.config(state=tk.DISABLED)
    root.after(1000, respond_to_message)

def respond_to_message():
    """Ответ гостя с удалением индикатора"""
    chat_area.config(state=tk.NORMAL)
    chat_area.delete("end-2l", "end-1l")  # Удаляем "Гость думает..."
    formatted_response = format_message("response")
    chat_area.insert(tk.END, f"Гость: {formatted_response}\n\n")
    chat_area.see(tk.END)
    chat_area.config(state=tk.DISABLED)
    chat_history.append(("bot", "response"))
    winsound.PlaySound("SystemQuestion", winsound.SND_ASYNC)  # Звук ответа
    if random.random() > 0.5:
        show_random_image()

def clear_chat():
    """Очистка чата"""
    chat_area.config(state=tk.NORMAL)
    chat_area.delete("1.0", tk.END)
    chat_area.config(state=tk.DISABLED)
    chat_history.clear()

def show_random_image():
    """Показ случайного изображения"""
    try:
        image_files = [f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        if not image_files:
            chat_area.config(state=tk.NORMAL)
            chat_area.insert(tk.END, "Бот: Нет доступных изображений.\n\n")
            chat_area.config(state=tk.DISABLED)
            return
        image_path = os.path.join(images_folder, random.choice(image_files))
        image = Image.open(image_path)
        width, height = image.size
        max_size = 300
        if width > height:
            new_width, new_height = max_size, int(height * (max_size / width))
        else:
            new_height, new_width = max_size, int(width * (max_size / height))
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_image)
        image_label.config(image=tk_image)
        image_label.image = tk_image
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "Бот: Вот случайная картинка!\n\n")
        chat_area.config(state=tk.DISABLED)
    except Exception as e:
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, f"Бот: Ошибка с картинкой: {str(e)}\n\n")
        chat_area.config(state=tk.DISABLED)

# Основное окно
root = tk.Tk()
root.title("Чат с живым ботом")
root.geometry("800x600")
root.resizable(True, True)

# Главный фрейм
main_frame = Frame(root, bg="#f0f0f0")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Чат-фрейм
chat_frame = Frame(main_frame, bg="#f0f0f0")
chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Область чата с полупрозрачностью
chat_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=40, height=20, bg="white", fg="black", relief=tk.FLAT)
chat_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
chat_area.config(state=tk.DISABLED)
root.attributes("-alpha", 0.95)  # Полупрозрачность окна

# Поле ввода и кнопки
input_frame = Frame(chat_frame, bg="#f0f0f0")
input_frame.pack(fill=tk.X, padx=5, pady=5)
message_entry = tk.Text(input_frame, font=('Arial', 12), wrap=tk.WORD, height=2, relief=tk.FLAT)
message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=5)
message_entry.bind("<Shift-Return>", lambda e: None)
message_entry.bind("<Return>", send_message)

def resize_text_field(event=None):
    """Динамическое расширение поля ввода"""
    text = message_entry.get("1.0", "end-1c")
    num_lines = text.count('\n') + 1
    new_height = max(2, min(6, num_lines))
    message_entry.config(height=new_height)
    return "break"

message_entry.bind("<KeyRelease>", resize_text_field)

send_button = Button(input_frame, text="Отправить", command=send_message, bg="#4CAF50", fg="white", relief=tk.FLAT)
send_button.pack(side=tk.RIGHT, padx=5)
# clear_button = Button(input_frame, text="Очистить чат", command=clear_chat, bg="#F44336", fg="white", relief=tk.FLAT)
# clear_button.pack(side=tk.RIGHT, padx=5)

# Фрейм для изображения
image_frame = Frame(main_frame, width=300, bg="#f0f0f0")
image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
image_label = Label(image_frame, bg="#f0f0f0")
image_label.pack(fill=tk.BOTH, expand=True)
show_image_button = Button(image_frame, text="Показать картинку", command=show_random_image, bg="#2196F3", fg="white", relief=tk.FLAT)
show_image_button.pack(pady=10)

# Приветственное сообщение
chat_area.config(state=tk.NORMAL)
chat_area.insert(tk.END, f"Бот: {"greetings"}\n\n")
chat_area.config(state=tk.DISABLED)

# Запуск
def start_frame():
    root.mainloop()