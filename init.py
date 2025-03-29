from person import Person


def init_persons() -> {}:
    person1 = Person("Иван", "Иванов", 30)
    person2 = Person("Петр", "Петров", 25)
    person3 = Person("Мария", "Сидорова", 40)
    person4 = Person("Елена", "Смирнова", 35)
    person5 = Person("Алексей", "Кузнецов", 28)

    return {
        1: person1,
        2: person2,
        3: person3,
        4: person4,
        5: person5
    }

def init_admin() -> Person:
    return Person("admin", "***", 30)
