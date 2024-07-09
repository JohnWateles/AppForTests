class Queue:
    def __init__(self):
        self.massive = list()

    def add(self, element):
        self.massive.insert(0, element)

    def pop(self):
        return self.massive.pop()

    def __iter__(self):
        return iter(self.massive)       # Обратный порядок не нужен, чтоб окна тестов открывались в нужном

    def __str__(self):
        return str(self.massive)


if __name__ == "__main__":
    ...
