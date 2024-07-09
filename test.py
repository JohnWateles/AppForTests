import dearpygui.dearpygui as dpg
# from dearpygui import demo
from time import time

TIME = int()
PREVIOUS_CLICK = int()
IS_TABLE_PROCESSING = False
# _MAX_VALUE_IN_TABLE = int()


# функция которая записывает результаты теста в словарь результата шаблона
def result_recording(test_name, result, recording_dict):
    recording_dict[test_name] = result


class AbsTest:
    # Тест, который будут проходить
    def __init__(self, tag: str, test: str = None, pattern_tag: str = "", recording_dict: dict = None):
        self.pattern_tag = pattern_tag
        self.tag = tag          # tag - это название папки, которую нужно открыть
        self.test = test       # В планах - суть теста, его структура, таблица или опросник и тд
        self.recording_dict = recording_dict
        self.passed = False
        if self.test == "table_sh":
            self.in_process = False     # Только для таблиц?
            self.result = 0         # Время выполнения таблицы
            self._max_value_in_table = int()
        elif self.test == "questions":
            self.result = {}    # В планах - {номер вопроса: ответ}
            self.questions = []
            self.answer = 0
            self.stop_index = None

    def __repr__(self):
        return self.tag

    def __str__(self):
        return self.tag

    def skip_test(self):
        if self.test == "table_sh":
            global IS_TABLE_PROCESSING
            test_name = self.tag
            result_recording(test_name, self.result, self.recording_dict)
            self.in_process = False
            self.passed = True
            dpg.delete_item(f"w_{self.pattern_tag}_{self.tag}")
            dpg.delete_item(f"gr_task_text{self.pattern_tag}_{self.tag}")
            dpg.delete_item(f"w_task_text{self.pattern_tag}_{self.tag}")
            dpg.delete_item(f"gr_table_sh_values{self.pattern_tag}_{self.tag}")
            dpg.delete_item(f"w_table_sh_values{self.pattern_tag}_{self.tag}")
            IS_TABLE_PROCESSING = False
        elif self.test == "questions":
            result_recording(self.tag, self.result, self.recording_dict)
            self.passed = True
            dpg.delete_item(f"w_{self.pattern_tag}_{self.tag}")
            pass
        else:
            pass

    def process(self):
        # dpg.delete_item(f"test_{self.tag}")
        self.in_process = not self.in_process

    @staticmethod
    def _start_timer_table():     # Старт таймера
        global TIME, PREVIOUS_CLICK, IS_TABLE_PROCESSING
        if not IS_TABLE_PROCESSING:
            TIME = time()
            PREVIOUS_CLICK = 1
            IS_TABLE_PROCESSING = True

    def _stop_timer_table(self, sender, app_data):      # Остановка таймера и запись результата
        global TIME, PREVIOUS_CLICK, IS_TABLE_PROCESSING
        if PREVIOUS_CLICK == self._max_value_in_table - 1:
            TIME = time() - TIME
            test_name = f"{sender[:-6]}".split("|||")[1]
            self.result = TIME
            TIME = int()
            result_recording(test_name, self.result, self.recording_dict)
            self.in_process = False
            self.passed = True
            dpg.delete_item(f"w_{self.pattern_tag}_{self.tag}")
            dpg.delete_item(f"gr_task_text{self.pattern_tag}_{self.tag}")
            dpg.delete_item(f"w_task_text{self.pattern_tag}_{self.tag}")
            dpg.delete_item(f"gr_table_sh_values{self.pattern_tag}_{self.tag}")
            dpg.delete_item(f"w_table_sh_values{self.pattern_tag}_{self.tag}")
            IS_TABLE_PROCESSING = False

    @staticmethod
    def _previous_click(sender):
        global PREVIOUS_CLICK
        if str(PREVIOUS_CLICK + 1) == dpg.get_item_label(sender):
            PREVIOUS_CLICK += 1

    def start(self, parent_window="primary_window", recording_dict=None):
        self.in_process = True
        global TIME
        from init_fonts import big_default_font, arial
        if self.test == "table_sh":
            # Добавить новый файл с текстом задания
            task_text = f"Текст задания\n{self.pattern_tag}, {self.tag}"
            with open(f"tests/{self.tag}/table_values.txt") as table_data:
                size = tuple(map(int, table_data.readline().split()))
                table = [[0 for _ in range(size[1])] for _ in range(size[0])]
                __values = tuple(map(int, table_data.readline().split()))
                __index = 0
                for i in range(size[0]):
                    for j in range(size[1]):
                        table[i][j] = __values[__index]
                        self._max_value_in_table = max(self._max_value_in_table, table[i][j])
                        __index += 1

            height = dpg.get_viewport_height() - 1
            width = dpg.get_viewport_width() - 1
            __button_size = 60

            with dpg.window(height=height, width=width, no_title_bar=True,
                            no_move=True, no_resize=True, pos=(0, 0), tag=f"w_{self.pattern_tag}_{self.tag}"):

                __table_width = size[0] * __button_size + (size[0] * 1.5 + 2) * 5
                __table_width2 = size[0] * __button_size + (size[0] * 1.5 + 2) * 5
                __table_height = size[1] * __button_size + (size[1] - 1) * 5
                __table_position = ((width - __table_width2) / 2, (height - __table_height) / 2)

                __task_width = 400
                __task_height = 100
                __task_position = ((width - __task_width) / 2, (height - __task_height) / 2 - 250)

                # with dpg.group(tag=f"gr_task_text{self.pattern_tag}_{self.tag}"):
                with dpg.child_window(width=__task_width, height=__task_height, pos=__task_position,
                                      tag=f"w_task_text{self.pattern_tag}_{self.tag}",
                                      no_scrollbar=True, no_scroll_with_mouse=True):
                    """no_scrollbar=True,
                                no_move=True, no_close=True, no_scroll_with_mouse=True, no_resize=True,
                                no_collapse=True, no_title_bar=True, """
                    _task_text = dpg.add_text(task_text)
                    dpg.bind_item_font(_task_text, arial)

                # with dpg.group(tag=f"gr_table_sh_values{self.pattern_tag}_{self.tag}"):
                with dpg.child_window(width=__table_width, height=__table_height + 15, pos=__table_position,
                                      tag=f"w_table_sh_values{self.pattern_tag}_{self.tag}",
                                      no_scrollbar=True, no_scroll_with_mouse=True):

                    with dpg.table(header_row=False):
                        for i in range(size[0]):
                            dpg.add_table_column(width_fixed=True)
                            with dpg.table_row():
                                for j in range(size[1]):
                                    if table[i][j] == 1:
                                        btn = dpg.add_button(label=f"{table[i][j]}", width=__button_size,
                                                             height=__button_size,
                                                             tag=f"{self.pattern_tag}|||{self.tag}_btn{i}{j}",
                                                             callback=self._start_timer_table)
                                    elif table[i][j] == self._max_value_in_table:
                                        btn = dpg.add_button(label=f"{table[i][j]}", width=__button_size,
                                                             height=__button_size,
                                                             tag=f"{self.pattern_tag}|||{self.tag}_btn{i}{j}",
                                                             callback=self._stop_timer_table)
                                    else:
                                        btn = dpg.add_button(label=f"{table[i][j]}", width=__button_size,
                                                             height=__button_size,
                                                             tag=f"{self.pattern_tag}|||{self.tag}_btn{i}{j}",
                                                             callback=self._previous_click)
                                    dpg.bind_item_font(btn, big_default_font)
                dpg.add_button(label="Skip", callback=self.skip_test)

        elif self.test == "questions":
            with open(f"tests/{self.tag}/questions.txt", "r", encoding="UTF-8") as questions_data:
                self.questions = [question.rstrip("\n") for question in questions_data.readlines()]
            self.stop_index = len(self.questions)
            height = dpg.get_viewport_height() - 1
            width = dpg.get_viewport_width() - 1
            with dpg.window(height=height, width=width, no_title_bar=True,
                            no_move=True, no_resize=True, pos=(0, 0), tag=f"w_{self.pattern_tag}_{self.tag}"):
                height_child_w = 500
                width_child_w = 600
                with dpg.child_window(height=height_child_w, width=width_child_w,
                                      pos=((width - width_child_w) // 2, (height - height_child_w) // 2),
                                      tag=f"c_w_{self.pattern_tag}_{self.tag}"):
                    text = dpg.add_text(f"{self.questions[self.answer]}", wrap=0)
                    btn = dpg.add_button(label="Начать", width=130, height=50, pos=((width_child_w - 130) // 2,
                                                                                    (height_child_w - 50) // 2
                                                                                    + int(height_child_w * 0.4)),
                                         callback=self.start_questions)
                    dpg.bind_item_font(text, arial)
                    dpg.bind_item_font(btn, arial)
                dpg.add_button(label="Skip", callback=self.skip_test)
        else:
            self.passed = True

    def _push_yes(self):
        self.result[f"{self.answer}"] = 1
        self.start_questions()

    def _push_no(self):
        self.result[f"{self.answer}"] = 0
        self.start_questions()

    def start_questions(self):
        from init_fonts import arial
        self.answer += 1
        if self.answer == self.stop_index:
            result_recording(self.tag, self.result, self.recording_dict)
            self.passed = True
            dpg.delete_item(f"w_{self.pattern_tag}_{self.tag}")
        else:
            dpg.delete_item(f"c_w_{self.pattern_tag}_{self.tag}")
            height = dpg.get_viewport_height() - 1
            width = dpg.get_viewport_width() - 1
            height_child_w = 600
            width_child_w = 900
            with dpg.child_window(height=height_child_w, width=width_child_w,
                                  pos=((width - width_child_w) // 2, (height - height_child_w) // 2),
                                  tag=f"c_w_{self.pattern_tag}_{self.tag}",
                                  parent=f"w_{self.pattern_tag}_{self.tag}"):
                text = dpg.add_text(f"{self.questions[self.answer]}", wrap=0)
                btn1 = dpg.add_button(label="Да", width=130, height=50,
                                      pos=((width_child_w - 130) // 2 - 150,
                                           (height_child_w - 50) // 2 + int(height_child_w * 0.4)),
                                      callback=self._push_yes)
                btn2 = dpg.add_button(label="Нет", width=130, height=50,
                                      pos=((width_child_w - 130) // 2 + 150,
                                           (height_child_w - 50) // 2 + int(height_child_w * 0.4)),
                                      callback=self._push_no)

                dpg.bind_item_font(text, arial)
                dpg.bind_item_font(btn1, arial)
                dpg.bind_item_font(btn2, arial)
                pass


if __name__ == "__main__":
    ...
