class BoolList():
    def __init__(self):
        self.list: list = []
    
    def add_bool(self, value: bool):
        self.list.append(value)

    def get_list(self) -> list:
        return self.list