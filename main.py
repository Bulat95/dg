import init, frame, aicontroller

print("Инициализация жителей отеля")
personList = init.init_persons()
print("Инициализация админа отеля")
admin = init.init_admin()
print("Жильцы и администратор сгенерированы")
print("Выбран первый житель")
selected_person = personList[1]

print("отправка сообщения от жителя")
aicontroller.send_openrouter(selected_person.getinfo(), False)

print("Запуск оболочки")
frame.start_frame()




