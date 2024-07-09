from queue import Queue
from test import AbsTest
from datetime import datetime


class TestPattern:
    def __init__(self, tag: str):
        self.tag = tag      # название шаблона (для удобства)
        self.queue_of_tests = Queue()
        self.results = dict()

    def add_test(self, test: AbsTest):
        self.queue_of_tests.add(test)

    def start_tests(self):
        for test in self.queue_of_tests:
            test.start(recording_dict=self.results)
        """with (open(file := f"results/{self.tag} {str(datetime.today()).replace(":", "-").replace(".", "-")}.txt", "a")
              as f):
            f.writelines(self.results)"""

    def __repr__(self):
        return f"({self.tag}: {self.queue_of_tests})"

    def __str__(self):
        return str(self.tag)


if __name__ == "__main__":
    ...
