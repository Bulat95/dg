class Person:
    def __init__(self, first_name, last_name, age):
        self.name = first_name
        self.surname = last_name
        self.age = age

    def update_field(self, field_name, value):
        if hasattr(self, field_name):
            setattr(self, field_name, value)
            return True
        return False

    def get_field(self, field_name) -> str:
        return getattr(self, field_name)

    def getinfo(self) -> str:
        info = ""
        for attribute_name in vars(self):
            attribute_value = getattr(self, attribute_name)
            info += f"{attribute_name}: {attribute_value}\n"
        return info