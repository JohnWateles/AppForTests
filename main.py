import dearpygui.dearpygui as dpg
from pattern import TestPattern
from test import AbsTest
import json
import os
from excel_work import create_excel_table, print_excel_file

dpg.create_context()
dpg.create_viewport(title="Title", clear_color=(50, 50, 50, 255))

TESTS_NAMES = tuple(os.listdir("tests"))  # Названия всех тестов (пока что это папки)
ALL_PATTERNS = list()  # Список из всех доступных шаблонов
SELECTED_PATTERN = None
__HELP_LIST = list()
START_TESTING = False   # Переменная, показывающая идёт ли сейчас тест (для dpg.is_dearpygui_running)
__PASSED_TESTS_NAMES = dict()   # Словарь вида {"Название теста на русском" : [Все пройденные тесты данного вида]}
CLOSE = False


# Повторная инициализация всех шаблонов из json файла
def init_patterns():
    global ALL_PATTERNS
    ALL_PATTERNS = list()
    with open("patterns.json") as file:
        for _pattern in json.load(file):
            for name_pattern, tests in _pattern.items():
                init_pattern = TestPattern(name_pattern)
                for test in tests:
                    if f"table_sh" in test.lower():
                        init_pattern.add_test(AbsTest(test, "table_sh", pattern_tag=init_pattern.tag,
                                                      recording_dict=init_pattern.results))
                    elif f"questions" in test.lower():
                        init_pattern.add_test(AbsTest(test, "questions", pattern_tag=init_pattern.tag,
                                                      recording_dict=init_pattern.results))
                    else:
                        init_pattern.add_test(AbsTest(test))
            ALL_PATTERNS.append(init_pattern)


def close_main_window():
    global CLOSE
    CLOSE = True


def start_all_tests():
    global START_TESTING
    START_TESTING = True


def start_testing():
    ...


def close_configure_tests():
    dpg.delete_item("configure_tests")


def close_w_end_all_tests():
    dpg.delete_item("w_end_all_tests")


# Сохраняет в SELECTED_PATTERN сохранённый шаблон, тесты которого будут исполняться
def save_selected_pattern(sender, pattern_name=dpg.get_value("choice_pattern")):
    _ = sender
    global SELECTED_PATTERN, ALL_PATTERNS
    for pattern in ALL_PATTERNS:
        if pattern.tag == pattern_name:
            SELECTED_PATTERN = pattern


# Создаёт новые кнопки выбора шаблона (после создания нового шаблона)
def create_buttons_choice_pattern():
    global ALL_PATTERNS
    dpg.delete_item("choice_pattern")
    radio_btn = dpg.add_radio_button([pattern.tag for pattern in ALL_PATTERNS], horizontal=True,
                                     callback=save_selected_pattern, tag="choice_pattern",
                                     parent="window_choice_pattern", default_value=ALL_PATTERNS[-1].tag)
    dpg.bind_item_font(radio_btn, big_default_font)
    save_selected_pattern(None, pattern_name=dpg.get_value("choice_pattern"))


# Открытие json, запись имени шаблона и списка тестов, обновление окна выбора шаблона, обнуление ненужных значений
def create_new_pattern():
    global __HELP_LIST, ALL_PATTERNS
    key = dpg.get_value("name_new_pattern")
    if (key != "") and (key not in ALL_PATTERNS) and (__HELP_LIST != list()):
        new_pattern = {key: __HELP_LIST}
        with open("patterns.json") as file:
            data = json.load(file)
        data.append(new_pattern)
        with open("patterns.json", "w") as file:
            json.dump(data, file, indent=2)

        dpg.set_value("name_new_pattern", "")
        for test_name in __HELP_LIST:
            dpg.set_value(test_name, False)
        __HELP_LIST = list()
        init_patterns()
        create_buttons_choice_pattern()


# __HELP_LIST - упорядоченный список тестов, которые добавятся в новый шаблон
# функция добавляет названия тестов в нужном порядке
def clicking(sender, app_data):
    global __HELP_LIST
    if app_data:
        __HELP_LIST.append(sender)
    else:
        __HELP_LIST.remove(sender)


# Окно конфигурации шаблонов
def configure_tests():
    global ALL_PATTERNS, TESTS_NAMES, SELECTED_PATTERN
    height = dpg.get_viewport_height() - 33
    width = dpg.get_viewport_width() - 14
    with dpg.window(tag="configure_tests", modal=True, height=height, width=width, no_title_bar=True, no_move=True,
                    no_resize=True):
        with dpg.group(tag="gr_test_settings"):
            with dpg.child_window(autosize_x=True, height=110, tag="window_choice_pattern"):
                # Выбор шаблона
                if SELECTED_PATTERN is None:
                    if len(ALL_PATTERNS) != 0:
                        radio_btn = dpg.add_radio_button([pattern.tag for pattern in ALL_PATTERNS], horizontal=True,
                                                         callback=save_selected_pattern, tag="choice_pattern",
                                                         default_value=ALL_PATTERNS[-1].tag)
                    else:
                        radio_btn = dpg.add_radio_button([pattern.tag for pattern in ALL_PATTERNS], horizontal=True,
                                                         callback=save_selected_pattern, tag="choice_pattern",
                                                         default_value="")
                else:
                    radio_btn = dpg.add_radio_button([pattern.tag for pattern in ALL_PATTERNS], horizontal=True,
                                                     callback=save_selected_pattern, tag="choice_pattern",
                                                     default_value=str(SELECTED_PATTERN))
                dpg.bind_item_font(radio_btn, big_default_font)
                save_selected_pattern(None, pattern_name=dpg.get_value("choice_pattern"))

        with dpg.group(tag="gr_create_new_pattern"):  # Создание своего шаблона
            with dpg.child_window(width=300, height=250):
                with dpg.group():
                    dpg.add_text(default_value="Create a new pattern", pos=(77, 0))  # Название окна
                with dpg.group(tag="gr_name_new_pattern", horizontal=True):
                    dpg.add_text(default_value="Pattern name")
                    dpg.add_input_text(tag="name_new_pattern", width=150)  # Ввод имени нового шаблона

                with dpg.group(tag="gr_tests_in_new_pattern"):
                    with dpg.table(header_row=False, tag="available_tests"):
                        dpg.add_table_column()
                        for test_name in TESTS_NAMES:
                            with dpg.table_row():  # Создание колонны из названий тестов
                                dpg.add_selectable(label=f"{test_name}", width=100, tag=test_name, callback=clicking)
                dpg.add_button(label="Create pattern", tag="create_new_pattern", callback=create_new_pattern,
                               height=25, width=150)

        with dpg.group(tag="gr_close_btn", pos=(width // 2 - 65, height - 75)):
            dpg.add_button(tag="close_btn", label="Save and close",
                           callback=close_configure_tests, height=30, width=120)


def end_tests():
    with dpg.window(tag="end_tests", popup=True):
        text = dpg.add_text(f"Вы завершили выполнение тестов")
        dpg.bind_item_font(text, arial)
        dpg.add_button(label="Close window", callback=lambda: dpg.delete_item("end_tests"))


def close_answers_window():
    global __PASSED_TESTS_NAMES
    dpg.delete_item("w_all_results")
    __PASSED_TESTS_NAMES = dict()


def show_result_window():
    # Проблема в том, что программа будет работать только для любых таблиц Шульте и одного опросника ВСК
    # Чтобы добавить другие виды тестов, нужно будет доделывать программу
    height_w_results = dpg.get_viewport_height() - 1
    width_w_results = dpg.get_viewport_width() - 1
    for test_name, test_result in SELECTED_PATTERN.results.items():
        if "table_sh" in test_name:
            if "Таблица Шульте" not in __PASSED_TESTS_NAMES:
                __PASSED_TESTS_NAMES["Таблица Шульте"] = list()
                __PASSED_TESTS_NAMES["Таблица Шульте"].append((test_name, test_result))
            else:
                __PASSED_TESTS_NAMES["Таблица Шульте"].append((test_name, test_result))
        elif "questions" in test_name:
            if "Опросник ВСК" not in __PASSED_TESTS_NAMES:
                __PASSED_TESTS_NAMES["Опросник ВСК"] = list()
                __PASSED_TESTS_NAMES["Опросник ВСК"].append((test_name, test_result))
            else:
                __PASSED_TESTS_NAMES["Опросник ВСК"].append((test_name, test_result))
        else:
            """if "unnamed test" not in __PASSED_TESTS_NAMES:
                __PASSED_TESTS_NAMES["unnamed test"] = list()
                __PASSED_TESTS_NAMES["unnamed test"].append((test_name, test_result))
            else:
                __PASSED_TESTS_NAMES["unnamed test"].append((test_name, test_result))"""
            pass
    # print(__PASSED_TESTS_NAMES)
    if "Таблица Шульте" in __PASSED_TESTS_NAMES:
        count_tables = len(__PASSED_TESTS_NAMES["Таблица Шульте"])
        _average_time = round(sum(test_time for name, test_time in __PASSED_TESTS_NAMES["Таблица Шульте"]) /
                              count_tables, 2)      # "эффективность работы"(ЭР)
        __PASSED_TESTS_NAMES["Таблица Шульте"].append((f"Эффективность работы", _average_time))
        _workability = round(__PASSED_TESTS_NAMES["Таблица Шульте"][0][1] / _average_time, 2)\
            if _average_time != 0 else 0        # "врабатываемость"
        __PASSED_TESTS_NAMES["Таблица Шульте"].append((f"Врабатываемость", _workability))
        if count_tables >= 3:
            _stability = round(__PASSED_TESTS_NAMES["Таблица Шульте"][-2][1] / _average_time, 2)\
                if _average_time != 0 else 0  # "устойчивость"
        else:
            _stability = _workability
        __PASSED_TESTS_NAMES["Таблица Шульте"].append((f"Устойчивость", _stability))

    if "Опросник ВСК" in __PASSED_TESTS_NAMES:
        self_control = {"1": -1, "2": -1, "3": 1, "4": 1, "5": 0, "6": -1, "7": 1, "8": -1, "9": -1, "10": -1,
                        "11": -1, "12": -1, "13": 0, "14": 0, "15": -1, "16": 0, "17": -1, "18": -1, "19": -1,
                        "20": -1, "21": 0, "22": -1, "23": -1, "24": 1, "25": -1, "26": 0, "27": -1, "28": 0,
                        "29": 0, "30": 0}
        persistence = {"1": 0, "2": 1, "3": -1, "4": -1, "5": 1, "6": 0, "7": -1, "8": -1, "9": 0, "10": 0,
                       "11": 1, "12": -1, "13": 0, "14": -1, "15": -1, "16": 0, "17": 1, "18": 1, "19": -1,
                       "20": 1, "21": -1, "22": 0, "23": -1, "24": 1, "25": 0, "26": 1, "27": -1, "28": -1,
                       "29": -1, "30": -1}
        general_index = {"1": 0, "2": 1, "3": 1, "4": 1, "5": 1, "6": 0, "7": 1, "8": -1, "9": 1, "10": 0,
                         "11": 1, "12": -1, "13": 0, "14": 0, "15": -1, "16": 0, "17": 1, "18": 1, "19": -1,
                         "20": 1, "21": 0, "22": 0, "23": -1, "24": 1, "25": 1, "26": -1, "27": 1, "28": 0,
                         "29": 0, "30": 0}
        for _test in __PASSED_TESTS_NAMES["Опросник ВСК"]:
            if len(__PASSED_TESTS_NAMES["Опросник ВСК"]) == 1 and len(_test[1]) == 30:
                create_excel_table(*_test)
                count_self_control = int()
                count_persistence = int()
                count_general_index = int()
                for index in range(1, 31):
                    index = str(index)
                    if _test[1][index] == self_control[index]:
                        count_self_control += 1

                    if _test[1][index] == persistence[index]:
                        count_persistence += 1

                    if _test[1][index] == general_index[index]:
                        count_general_index += 1

                __PASSED_TESTS_NAMES["Опросник ВСК"].append((_test[0], {"Самообладание": count_self_control,
                                                                        "Настойчивость": count_persistence,
                                                                        "Общий индекс ВСК": count_general_index}))
    # print(__PASSED_TESTS_NAMES)
    with dpg.window(tag="w_all_results", height=height_w_results, width=width_w_results, no_title_bar=True,
                    no_move=True, no_resize=True, pos=(0, 0)):
        _count_c_w = len(__PASSED_TESTS_NAMES)
        if _count_c_w == 1:
            height_child_w = height_w_results - 500
        else:
            height_child_w = height_w_results // 2 - 200
        width_child_w = 800
        iteration = 0

        for name_test_type, test_name_and_results in __PASSED_TESTS_NAMES.items():
            # print(name_test_type, test_name_and_results)
            with dpg.child_window(width=width_child_w, height=height_child_w, tag=f"c_w_{name_test_type}_results",
                                  pos=((width_w_results - width_child_w) // 2,
                                       (height_w_results - height_child_w) // 2 - 200
                                       + height_child_w * iteration + 1)):

                text1 = dpg.add_text(name_test_type)
                dpg.bind_item_font(text1, arial)
                for test_name, test_result in test_name_and_results:
                    if isinstance(test_result, float):
                        text2 = dpg.add_text(f"{test_name}: {round(test_result, 2)}")
                        dpg.bind_item_font(text2, arial)
                    else:
                        text2 = dpg.add_text(f"{test_name}: {test_result}", wrap=0)
                        dpg.bind_item_font(text2, arial)
            iteration += 1
        dpg.add_button(label="Close", height=50, width=120, callback=close_answers_window,
                       pos=((width_w_results - 120) // 2, (height_w_results - 200)))


def close_w_printing_result():
    dpg.delete_item("w_printing_result")


def printing_results():
    height = dpg.get_viewport_height() - 33
    width = dpg.get_viewport_width() - 14
    with dpg.window(tag="w_printing_result", modal=True, height=height, width=width, no_title_bar=True, no_move=True,
                    no_resize=True):
        with dpg.child_window(width=300, height=93):
            with dpg.group(tag="gr_name_file", horizontal=True):
                dpg.add_text(default_value="Select file:")

                # найти все файлы для печати и выбрать последний добавленный файл
                available_files = tuple(os.listdir("results"))

                dpg.add_combo(available_files, default_value=available_files[-1] if len(available_files) > 0 else "",
                              tag="file_selection")
            dpg.add_button(label="Print selected file", tag="print_selected_file", callback=print_excel_file,
                           height=25, width=150)
            dpg.add_button(label="Close", tag="close_w_printing_result", callback=close_w_printing_result,
                           height=25, width=150)


# Инициализация шрифтов
from init_fonts import big_default_font, arial

# Настройка цвета для класса mvWindowAppItem
with dpg.theme() as default_theme:
    with dpg.theme_component(dpg.mvWindowAppItem):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (50, 50, 50))

# Основное окно
init_patterns()
with dpg.window(tag="primary_window") as primary_window:
    with dpg.window(tag="settings", autosize=True, no_move=True, no_resize=True,
                    no_close=True, no_collapse=True, no_title_bar=True, no_scrollbar=True,
                    pos=(0, 0), no_focus_on_appearing=False):
        with dpg.group(tag="group_settings"):
            settings = dpg.add_text("Settings", pos=(46, 6))
            dpg.bind_item_font(settings, big_default_font)

        with dpg.group(tag="group_buttons"):
            dpg.add_button(label='Start Testing', callback=start_all_tests, width=184, height=30)
            dpg.add_button(label="Configure Tests", callback=configure_tests, width=184, height=30)
            dpg.add_button(label="Print results", callback=printing_results, width=184, height=30)
            dpg.add_button(label="Exit", callback=close_main_window, width=184, height=30)

dpg.bind_item_theme(primary_window, default_theme)  # Изменение цвета primary_window

dpg.set_primary_window(window=primary_window, value=True)

dpg.setup_dearpygui()
dpg.show_viewport()
# dpg.toggle_viewport_fullscreen()

while dpg.is_dearpygui_running():
    if START_TESTING:
        START_TESTING = False
        if isinstance(SELECTED_PATTERN, TestPattern):
            SELECTED_PATTERN.start_tests()
        else:
            pass
    if isinstance(SELECTED_PATTERN, TestPattern):
        for test in SELECTED_PATTERN.queue_of_tests:
            if not test.passed:
                break
        else:
            show_result_window()    # Окно вывода результатов
            height_t = dpg.get_viewport_height() - 33
            width_t = dpg.get_viewport_width() - 14
            with dpg.window(tag="w_end_all_tests", modal=True, height=height_t, width=width_t, no_title_bar=True,
                            no_move=True, no_resize=True):
                with dpg.group(tag="gr_end_all_tests_close_btn", pos=(width_t // 2 - 100, height_t // 2 - 50)):
                    dpg.add_button(tag="w_end_all_tests_close_btn", label="Close and calculate result",
                                   callback=close_w_end_all_tests, height=50, width=200)
            # print(SELECTED_PATTERN.results)  # Все результаты шаблона, после полного его прохождения
            SELECTED_PATTERN = None
            init_patterns()
    if CLOSE:
        break
    dpg.render_dearpygui_frame()
dpg.destroy_context()
