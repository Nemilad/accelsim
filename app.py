import json
import re

from browser import document, bind, html, window, timer
from browser.html import TD, DIV, P, IMG
from browser.widgets.dialog import InfoDialog

settings = {
    'current_language': "Русский",
    'block_enabled': {
        'macro_fusion': True,
        'micro_fusion': True,
        'LSD': True,
        'zeroing_idioms': True,
        'move_elimination': True
    },
    'arch_parameters': {
        'simple_decoders': 4,
        'complex_decoders': 1,
        'uop_complex': 4
    },
    'macro_parameters': {
        'ADD': {'JA': True, 'JNA': True, 'JAE': True, 'JNAE': True,
                'JB': True, 'JNB': True, 'JBE': True, 'JNBE': True,
                'JC': True, 'JNC': True, 'JE': True, 'JNE': True,
                'JG': True, 'JNG': True, 'JGE': True, 'JNGE': True,
                'JL': True, 'JNL': True, 'JLE': True, 'JNLE': True,
                'JS': False, 'JNS': False, 'JO': False, 'JNO': False,
                'JP': False, 'JNP': False, 'JPO': False, 'JPE': False,
                'JZ': True, 'JNZ': True},
        'SUB': {'JA': True, 'JNA': True, 'JAE': True, 'JNAE': True,
                'JB': True, 'JNB': True, 'JBE': True, 'JNBE': True,
                'JC': True, 'JNC': True, 'JE': True, 'JNE': True,
                'JG': True, 'JNG': True, 'JGE': True, 'JNGE': True,
                'JL': True, 'JNL': True, 'JLE': True, 'JNLE': True,
                'JS': False, 'JNS': False, 'JO': False, 'JNO': False,
                'JP': False, 'JNP': False, 'JPO': False, 'JPE': False,
                'JZ': True, 'JNZ': True},
        'ADC': {'JA': False, 'JNA': False, 'JAE': False, 'JNAE': False,
                'JB': False, 'JNB': False, 'JBE': False, 'JNBE': False,
                'JC': False, 'JNC': False, 'JE': False, 'JNE': False,
                'JG': False, 'JNG': False, 'JGE': False, 'JNGE': False,
                'JL': False, 'JNL': False, 'JLE': False, 'JNLE': False,
                'JS': False, 'JNS': False, 'JO': False, 'JNO': False,
                'JP': False, 'JNP': False, 'JPO': False, 'JPE': False,
                'JZ': False, 'JNZ': False},
        'SBB': {'JA': False, 'JNA': False, 'JAE': False, 'JNAE': False,
                'JB': False, 'JNB': False, 'JBE': False, 'JNBE': False,
                'JC': False, 'JNC': False, 'JE': False, 'JNE': False,
                'JG': False, 'JNG': False, 'JGE': False, 'JNGE': False,
                'JL': False, 'JNL': False, 'JLE': False, 'JNLE': False,
                'JS': False, 'JNS': False, 'JO': False, 'JNO': False,
                'JP': False, 'JNP': False, 'JPO': False, 'JPE': False,
                'JZ': False, 'JNZ': False},
        'INC': {'JA': False, 'JNA': False, 'JAE': False, 'JNAE': False,
                'JB': False, 'JNB': False, 'JBE': False, 'JNBE': False,
                'JC': False, 'JNC': False, 'JE': True, 'JNE': True,
                'JG': True, 'JNG': True, 'JGE': True, 'JNGE': True,
                'JL': True, 'JNL': True, 'JLE': True, 'JNLE': True,
                'JS': False, 'JNS': False, 'JO': False, 'JNO': False,
                'JP': False, 'JNP': False, 'JPO': False, 'JPE': False,
                'JZ': True, 'JNZ': True},
        'DEC': {'JA': False, 'JNA': False, 'JAE': False, 'JNAE': False,
                'JB': False, 'JNB': False, 'JBE': False, 'JNBE': False,
                'JC': False, 'JNC': False, 'JE': True, 'JNE': True,
                'JG': True, 'JNG': True, 'JGE': True, 'JNGE': True,
                'JL': True, 'JNL': True, 'JLE': True, 'JNLE': True,
                'JS': False, 'JNS': False, 'JO': False, 'JNO': False,
                'JP': False, 'JNP': False, 'JPO': False, 'JPE': False,
                'JZ': True, 'JNZ': True},
        'CMP': {'JA': True, 'JNA': True, 'JAE': True, 'JNAE': True,
                'JB': True, 'JNB': True, 'JBE': True, 'JNBE': True,
                'JC': True, 'JNC': True, 'JE': True, 'JNE': True,
                'JG': True, 'JNG': True, 'JGE': True, 'JNGE': True,
                'JL': True, 'JNL': True, 'JLE': True, 'JNLE': True,
                'JS': False, 'JNS': False, 'JO': False, 'JNO': False,
                'JP': False, 'JNP': False, 'JPO': False, 'JPE': False,
                'JZ': True, 'JNZ': True},
        'TEST': {'JA': True, 'JNA': True, 'JAE': True, 'JNAE': True,
                 'JB': True, 'JNB': True, 'JBE': True, 'JNBE': True,
                 'JC': True, 'JNC': True, 'JE': True, 'JNE': True,
                 'JG': True, 'JNG': True, 'JGE': True, 'JNGE': True,
                 'JL': True, 'JNL': True, 'JLE': True, 'JNLE': True,
                 'JS': True, 'JNS': True, 'JO': True, 'JNO': True,
                 'JP': True, 'JNP': True, 'JPO': True, 'JPE': True,
                 'JZ': True, 'JNZ': True},
        'AND': {'JA': True, 'JNA': True, 'JAE': True, 'JNAE': True,
                'JB': True, 'JNB': True, 'JBE': True, 'JNBE': True,
                'JC': True, 'JNC': True, 'JE': True, 'JNE': True,
                'JG': True, 'JNG': True, 'JGE': True, 'JNGE': True,
                'JL': True, 'JNL': True, 'JLE': True, 'JNLE': True,
                'JS': True, 'JNS': True, 'JO': True, 'JNO': True,
                'JP': True, 'JNP': True, 'JPO': True, 'JPE': True,
                'JZ': True, 'JNZ': True},
        'OR': {'JA': False, 'JNA': False, 'JAE': False, 'JNAE': False,
               'JB': False, 'JNB': False, 'JBE': False, 'JNBE': False,
               'JC': False, 'JNC': False, 'JE': False, 'JNE': False,
               'JG': False, 'JNG': False, 'JGE': False, 'JNGE': False,
               'JL': False, 'JNL': False, 'JLE': False, 'JNLE': False,
               'JS': False, 'JNS': False, 'JO': False, 'JNO': False,
               'JP': False, 'JNP': False, 'JPO': False, 'JPE': False,
               'JZ': False, 'JNZ': False},
        'XOR': {'JA': False, 'JNA': False, 'JAE': False, 'JNAE': False,
                'JB': False, 'JNB': False, 'JBE': False, 'JNBE': False,
                'JC': False, 'JNC': False, 'JE': False, 'JNE': False,
                'JG': False, 'JNG': False, 'JGE': False, 'JNGE': False,
                'JL': False, 'JNL': False, 'JLE': False, 'JNLE': False,
                'JS': False, 'JNS': False, 'JO': False, 'JNO': False,
                'JP': False, 'JNP': False, 'JPO': False, 'JPE': False,
                'JZ': False, 'JNZ': False},
        'NOT': {'JA': False, 'JNA': False, 'JAE': False, 'JNAE': False,
                'JB': False, 'JNB': False, 'JBE': False, 'JNBE': False,
                'JC': False, 'JNC': False, 'JE': False, 'JNE': False,
                'JG': False, 'JNG': False, 'JGE': False, 'JNGE': False,
                'JL': False, 'JNL': False, 'JLE': False, 'JNLE': False,
                'JS': False, 'JNS': False, 'JO': False, 'JNO': False,
                'JP': False, 'JNP': False, 'JPO': False, 'JPE': False,
                'JZ': False, 'JNZ': False},
        'NEG': {'JA': False, 'JNA': False, 'JAE': False, 'JNAE': False,
                'JB': False, 'JNB': False, 'JBE': False, 'JNBE': False,
                'JC': False, 'JNC': False, 'JE': False, 'JNE': False,
                'JG': False, 'JNG': False, 'JGE': False, 'JNGE': False,
                'JL': False, 'JNL': False, 'JLE': False, 'JNLE': False,
                'JS': False, 'JNS': False, 'JO': False, 'JNO': False,
                'JP': False, 'JNP': False, 'JPO': False, 'JPE': False,
                'JZ': False, 'JNZ': False},
        'max_fusions': 2,
        'transition': True
    },
    'micro_parameters': {
        'read_modify': True,
        'address_write': True,
        'combined_enabled': True
    },
    'lsd_parameters': {
        'buffer_size': 64
    },
    'zeroing_parameters': {
        'XOR': True,
        'SUB': True
    },
    'move_parameters': {
        'MOV': True,
        'r64': True,
        'r32': True,
        'self_move': False
    },
}

cell_style = {
    "zeroing_idiom": {"background-color": "#ff00ff"},
    "move_elimination": {"background-color": "#F0421F"},
    "macro_fusion": {"background-color": "#ffff00"},
    "macro_fusion_2": {"background-color": "#cccc00"},
    "simple_dec": {"background-color": "#7b7bff"},
    "simple_dec_micro": {"background-color": "#ff7bff"},
    "complex_dec": {"background-color": "#ff7b7b"},
    "read_modify": {"background-color": "#40ff00"},
    "address_write": {"background-color": "#0040ff"},
    "combined": {"background-color": "#00ffff"},
    "lsd": {"background-color": "#ffc800"},
    "lsd_2": {"background-color": "#ff7b00"},
    "lsd_3": {"background-color": "#008000"},
    "lsd_4": {"background-color": "#00a000"}
}

russian_dict = {
    "Input": "Входные данные",
    "Options": "Параметры",
    "Decode table": "Таблица декодирования",
    "Micro operations table": "Таблица микро операций",
    "Start simulation": "Запуск симуляции",
    "Language": "Язык",
    "Units": "Блоки",
    "Macro fusion": "Макро слияние",
    "Micro fusion": "Микро слияние",
    "Zeroing idioms": "Нуль идиомы",
    "Source code": "Исходный код",
    "Code examples:": "Готовые примеры:",
    "Input from file:": "Ввод из файла:",
    "Select file": "Выберите файл",
    "Architecture parameters": "Параметры архитектуры",
    "Number of simple decoders:": "Количество простых декодеров:",
    "Number of complex decoders:": "Количество сложных декодеров:",
    "Maximum number of micro operations": "Максимальное число микро операций",
    "for a complex decoder:": "для сложного декодера:",
    "Both types of fusions": "Два вида слияния",
    "in one instruction": "в одной инструкции",
    "Registers 64 bit": "Регистры 64 бит",
    "Registers 32 bit": "Регистры 32 бит",
    "Moving": "Перемещение",
    "register into itself": "регистра в себя",
    "Micro operation": "Размер буфера",
    "buffer size:": "микро операций:",
    "Operations pairs for fusion": "Сливаемые пары операций",
    "First operation": "Первая операция",
    "Second operation": "Вторая операция",
    "Number of fusions per cycle:": "Количество слияний в такт:",
    "Transfer the first instruction to the next cycle": "Перенос первой инструкции на следующий такт",
    "when it reaches the last decoder": "при попадании на последний декодер",
    "With macro fusion": "С макро слиянием",
    "Without macro fusion": "Без макро слияния",
    "Instruction": "Инструкция",
    "Operand 1": "Операнд 1",
    "Operand 2": "Операнд 2",
    "Decoder": "Декодер",
    "Cycle": "Такт",
    "Result": "Результат",
    "Operations READ": "Операции READ",
    "Operations MODIFY": "Операции MODIFY",
    "Operations ADDRESS": "Операции ADDRESS",
    "Operations WRITE": "Операции WRITE",
    "Operations before": "Операций до",
    "Operations after": "Операций после"
}

current_radio_button = "ADD"
examples = {}


@bind("select.language", "change")
def translate(ev):
    if settings["current_language"] == "English":
        if ev.target.value == "Русский":
            translation_dict = russian_dict
    elif ev.target.value == "English":
        if settings["current_language"] == "Русский":
            translation_dict = {v: k for k, v in russian_dict.items()}
    else:
        translation_dict = {}

    for element in document.select("div.tabs")[0].select("button"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    if ev.target.value == "English":
        for element in document.select("div.global-settings")[0].select("span.language-span-ru"):
            if element.text in translation_dict.keys():
                element.text = translation_dict[element.text]
        element.class_name = "language-span-en"
        for element in document.select("div.global-settings")[0].select("div.globe-ru"):
            element.class_name = "globe-en"

    if ev.target.value == "Русский":
        for element in document.select("div.global-settings")[0].select("span.language-span-en"):
            if element.text in translation_dict.keys():
                element.text = translation_dict[element.text]
        element.class_name = "language-span-ru"
        for element in document.select("div.global-settings")[0].select("div.globe-en"):
            element.class_name = "globe-ru"

    for element in document.select("p.blocks-title")[0]:
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document.select("div.blocks")[0].select("span"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document.select("div.global-settings")[0].select("button"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document.select("div.global-settings")[0].select("button"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document["input_tab"].select("p.subtitle-4-2"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document["input_tab"].select("option"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document["input_tab"].select("span"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    if ev.target.value == "English":
        for element in document["input_tab"].select("span.file-input-ru"):
              element.class_name = "file-input-en"

    if ev.target.value == "Русский":
        for element in document["input_tab"].select("span.file-input-en"):
              element.class_name = "file-input-ru"

    for element in document["input_tab"].select("input.load-file"):
        if element.value in translation_dict.keys():
            element.value = translation_dict[element.value]

    for element in document["parameters_tab"].select("p.subtitle-1"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document["parameters_tab"].select("p.subtitle-6"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document["parameters_tab"].select("div.cpu-column-2")[0].select("p"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document["parameters_tab"].select("div.me-column-2")[0].select("p"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document["parameters_tab"].select("span"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    if ev.target.value == "English":
        for element in document["parameters_tab"].select("p.subtitle-5-ru"):
            if element.text in translation_dict.keys():
                element.text = translation_dict[element.text]
            element.class_name = "subtitle-5-en"

    if ev.target.value == "Русский":
        for element in document["parameters_tab"].select("p.subtitle-5-en"):
            if element.text in translation_dict.keys():
                element.text = translation_dict[element.text]
            element.class_name = "subtitle-5-ru"

    for element in document["parameters_tab"].select("p.subtitle-3"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document["parameters_tab"].select("div.vertical-align"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document["macro_tab"].select("p.subtitle-4"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document["macro_tab"].select("p.subtitle-4-2"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document["macro_tab"].select("th"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document["micro_tab"].select("p.subtitle-4-2"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document["micro_tab"].select("th"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    settings["current_language"] = ev.target.value
    load_examples()


@bind("button.tab", "click")
def switch_tab(ev):
    button = document[ev.target.id]
    tab = document[ev.target.id[:-7]]
    for x in document.select("div.tabcontent"):
        document[x.id].style.display = "none"
    for x in document.select("button.tab"):
        document[x.id].class_name = document[x.id].class_name.replace(" active", "")
    tab.style.display = "block"
    button.class_name += " active"


@bind(document.select("div.macro-first-operation")[0].select("input.checkbox"), "click")
def switch_macro(ev):
    global current_radio_button
    current_radio_button = ev.target.parent.text
    for box in document.select("div.macro-second-operation")[0].select("input.checkbox"):
        box.checked = settings["macro_parameters"][ev.target.parent.text][box.parent.text]


@bind(document.select("div.macro-second-operation")[0].select("input.checkbox"), "click")
def macro_update(ev):
    global current_radio_button
    if ev.target.checked and current_radio_button != "":
        settings["macro_parameters"][current_radio_button][ev.target.parent.text] = True
    elif not ev.target.checked and current_radio_button != "":
        settings["macro_parameters"][current_radio_button][ev.target.parent.text] = False


def load_examples():
    global examples
    for element in document.select('select.code-samples')[0]:
        element.remove()
    examples.clear()
    if settings["current_language"] == "English":
        with open('./examples_en.json') as f:
            examples = json.load(f)
    elif settings["current_language"] == "Русский":
        with open('./examples_ru.json') as f:
            examples = json.load(f)
    option = document.createElement("option")
    option.text = ""
    document.select('select.code-samples')[0].add(option)
    for example in examples.keys():
        option = document.createElement("option")
        option.text = example
        document.select('select.code-samples')[0].add(option)


@bind("select.code-samples", "change")
def load_example(ev):
    global examples
    if ev.target.value != "":
        document["inputarea"].value = examples[ev.target.value]


@bind("textarea", "click")
def reset_example(ev):
    document.select('select.code-samples')[0].selectedIndex = 0


def code_check(code):
    return True


def update_settings():
    input_value = document.select("div.blocks")[0].select("input.checkbox")
    settings["block_enabled"]["macro_fusion"] = input_value[0].checked
    settings["block_enabled"]["micro_fusion"] = input_value[1].checked
    settings["block_enabled"]["move_elimination"] = input_value[2].checked
    settings["block_enabled"]["zeroing_idioms"] = input_value[3].checked
    settings["block_enabled"]["LSD"] = input_value[4].checked
    input_value = document.select("div.cpu-column-3")[0].select(".counter")
    settings["arch_parameters"]["simple_decoders"] = int(input_value[0].value)
    settings["arch_parameters"]["complex_decoders"] = int(input_value[1].value)
    settings["arch_parameters"]["uop_complex"] = int(input_value[2].value)
    input_value = document.select("div.micro-column-3")[0].select(".micro-checkbox")
    settings["micro_parameters"]["read_modify"] = input_value[0].checked
    settings["micro_parameters"]["address_write"] = input_value[1].checked
    settings["micro_parameters"]["combined_enabled"] = input_value[2].checked
    input_value = document.select("div.macro-checkbox-wrapper")[0].select(".counter")
    settings["macro_parameters"]["max_fusions"] = int(input_value[0].value)
    input_value = document.select("div.macro-checkbox-wrapper")[0].select(".checkbox")
    settings["macro_parameters"]["transition"] = input_value[0].checked
    input_value = document.select("div.idiom-0-wrapper")[0].select(".checkbox-1")
    settings["zeroing_parameters"]["XOR"] = input_value[0].checked
    settings["zeroing_parameters"]["SUB"] = input_value[1].checked
    input_value = document.select("div.me-wrapper")[0].select(".checkbox-1")
    settings["move_parameters"]["r64"] = input_value[0].checked
    settings["move_parameters"]["r32"] = input_value[1].checked
    settings["move_parameters"]["self_move"] = input_value[2].checked
    input_value = document.select("div.lsd-wrapper")[0].select(".counter")
    settings["lsd_parameters"]["buffer_size"] = int(input_value[0].value)

@bind("button.start", "click")
def simulation(ev):
    clear_tables()
    code_table = []
    mark_list = {}
    code = document["inputarea"].value
    if code_check(code):
        line_num = -1
        for line in code.splitlines():
            template = {
                'op': '',
                'op1': '',
                'op2': '',
                'dec_type': '',
                'dec_cycle': '',
                'dec_type_2': '',
                'dec_cycle_2': '',
                'uop_read': '',
                'uop_modify': '',
                'uop_address': '',
                'uop_write': '',
                'uop_before': '',
                'uop_after': '',
                'uop_type': '',
                'loop_num': []
            }
            if line != "" and line[0] != ";" and line[0][0] != ";":
                line_num += 1
                mark = False
                for word_num, word in enumerate(line.split()):
                    if word == ";" or word[0] == ";":
                        break
                    if word_num == 0 and word[-1] == ':':
                        mark_list[word[:-1]] = line_num
                        mark = True
                    elif word_num == 0:
                        template['op'] = word
                    elif word_num == 1 and mark:
                        template['op'] = word
                    elif word_num == 1 and word[-1] != "," and "," in word:
                        template['op1'] = word.split(",")[0]
                        template['op2'] = word.split(",")[1]
                    elif word_num == 1 and word[-1] == ",":
                        template['op1'] = word[:-1]
                    elif word_num == 1:
                        template['op1'] = word
                    elif word_num == 2 and word[-1] != "," and mark and "," in word:
                        template['op1'] = word.split(",")[0]
                        template['op2'] = word.split(",")[1]
                    elif word_num == 2 and word[-1] == "," and mark:
                        template['op1'] = word[:-1]
                    elif word_num == 2 and mark:
                        template['op1'] = word
                    elif word_num == 2:
                        template['op2'] = word
                    elif word_num == 3 and mark:
                        template['op2'] = word
                if template['op'] != "":
                    code_table.append(template.copy())
                else:
                    line_num -= 1
            template.clear()

        update_settings()
        micro_table(code_table)
        if settings["block_enabled"]["micro_fusion"]:
            micro_fusion(code_table)
        if settings["block_enabled"]["zeroing_idioms"]:
            zeroing_idioms(code_table)
        if settings["block_enabled"]["move_elimination"]:
            move_elimination(code_table)
        loop_finder(code_table, mark_list)
        if settings["block_enabled"]["LSD"]:
            lsd(code_table)
        macro_table(code_table)
        if settings["block_enabled"]["macro_fusion"]:
            macro_fusion(code_table)
        fill_tables(code_table)
        code_table.clear()
        mark_list.clear()
        end_of_simulation_popup()
    else:
        pass


def end_of_simulation_popup():
    client_width = document.documentElement.clientWidth
    client_height = document.documentElement.clientHeight
    if (client_height >= 920):
        top = int(client_height / 2) + 310
        left = int(client_width / 2) + 458
    elif (client_height >= 810 and client_height < 920):
        top = int(client_height / 2) + 220
        left = int(client_width / 2) + 458
    elif (client_height < 810):
        top = int(client_height / 2) + 150
        left = int(client_width / 2) + 458

    if settings["current_language"] == "Русский":
        popup = InfoDialog("", "Симуляция завершена", top=top, left=left, default_css=False)
    else:
        popup = InfoDialog("", "Simulation completed", top=top, left=left, default_css=False)
    popup_title = document.select("div.brython-dialog-title")[0]
    popup_title.remove()
    main_popup = document.select("div.brython-dialog-main")[0]
    main_popup.class_name = "brython-dialog-main-1"
    body_popup = document.select("div.brython-dialog-panel")[0]
    body_popup.class_name = "brython-dialog-panel-1"
    inner_div = body_popup.childNodes[0]
    inner_div.class_name = "custom-dialog-message"
    timer.set_timeout(hide_popup, 3000)

def hide_popup():
    document.select("div.brython-dialog-main-1")[0].remove()

def macro_table(code_table):
    current_cycle = 1
    free_simple_dec = settings["arch_parameters"]["simple_decoders"]
    free_complex_dec = settings["arch_parameters"]["complex_decoders"]
    complex_max = settings["arch_parameters"]["uop_complex"]
    for line in code_table:
        redo = True
        while redo:
            if line["uop_before"] < 1:
                line["dec_cycle_2"] = current_cycle
                redo = False
            elif free_simple_dec > 0 and line["uop_after"] <= 1:
                free_simple_dec -= 1
                line["dec_type_2"] = "simple"
                line["dec_cycle_2"] = current_cycle
                redo = False
            elif free_simple_dec == 0 and free_complex_dec > 0 and line["uop_after"] <= 1:
                free_complex_dec -= 1
                line["dec_type_2"] = "complex"
                line["dec_cycle_2"] = current_cycle
                redo = False
            elif free_complex_dec > 0 and 1 < line["uop_after"] <= complex_max:
                free_complex_dec -= 1
                line["dec_type_2"] = "complex"
                line["dec_cycle_2"] = current_cycle
                redo = False
            elif free_complex_dec > 0 and complex_max < line["uop_after"] <= complex_max + free_simple_dec:
                free_complex_dec -= 1
                free_simple_dec -= line["uop_after"]-complex_max
                line["dec_type_2"] = "complex"
                line["dec_cycle_2"] = current_cycle
                redo = False
            elif free_complex_dec > 0 and \
                    line["uop_after"] > complex_max + settings["arch_parameters"]["simple_decoders"]:
                free_complex_dec = settings["arch_parameters"]["simple_decoders"]
                free_simple_dec = settings["arch_parameters"]["complex_decoders"]
                current_cycle += 1
                line["dec_type_2"] = "ERROR"
                line["dec_cycle_2"] = current_cycle
                redo = False
            else:
                free_simple_dec = settings["arch_parameters"]["simple_decoders"]
                free_complex_dec = settings["arch_parameters"]["complex_decoders"]
                current_cycle += 1
                redo = True


def macro_fusion(code_table):
    current_cycle = 1
    free_simple_dec = settings["arch_parameters"]["simple_decoders"]
    free_complex_dec = settings["arch_parameters"]["complex_decoders"]
    complex_max = settings["arch_parameters"]["uop_complex"]
    fusions_in_cycle = 0
    max_fusions = settings["macro_parameters"]["max_fusions"]
    checking = False
    for line_num, line in enumerate(code_table):
        redo = True
        while redo:
            if get_op_type(line["op1"]) != "m" and \
                    line["op"].upper() in settings["macro_parameters"] and \
                    True in settings["macro_parameters"][line["op"].upper()].values():
                checking = True
            elif fusions_in_cycle < max_fusions and \
                    checking and \
                    line["op"].upper() in settings["macro_parameters"][code_table[line_num-1]["op"].upper()] and \
                    settings["macro_parameters"][code_table[line_num-1]["op"].upper()][line["op"].upper()]:
                if free_simple_dec + free_complex_dec < 1 and settings["macro_parameters"]["transition"]:
                    free_simple_dec = settings["arch_parameters"]["simple_decoders"]
                    free_complex_dec = settings["arch_parameters"]["complex_decoders"]
                    current_cycle += 1
                    fusions_in_cycle = 0
                if free_simple_dec + free_complex_dec >= 1:
                    checking = False
                    if code_table[line_num - 1]["dec_type"] == "complex" and \
                            code_table[line_num - 1]["dec_cycle"] == current_cycle:
                        line["dec_type"] = "complex"
                    elif code_table[line_num - 1]["dec_type"] == "simple" and \
                            code_table[line_num - 1]["dec_cycle"] == current_cycle:
                        line["dec_type"] = "simple"
                    elif code_table[line_num - 1]["dec_cycle"] != current_cycle:
                        free_simple_dec -= 1
                        line["dec_type"] = "simple"
                    fusions_in_cycle += 1
                    line["dec_cycle"] = current_cycle
                    line["uop_after"] = 1
                    line["uop_type"] = "macro_fusion"
                    code_table[line_num - 1]["dec_cycle"] = current_cycle
                    code_table[line_num - 1]["uop_after"] = ""
                    code_table[line_num - 1]["uop_type"] = "macro_fusion"
                else:
                    checking = False
            else:
                checking = False
            if line["uop_type"] != "macro_fusion":
                if settings["macro_parameters"]["transition"] and checking and free_simple_dec + free_complex_dec <= 1:
                    free_simple_dec = settings["arch_parameters"]["simple_decoders"]
                    free_complex_dec = settings["arch_parameters"]["complex_decoders"]
                    current_cycle += 1
                    fusions_in_cycle = 0
                    redo = True
                elif line["uop_before"] < 1:
                    line["dec_cycle"] = current_cycle
                    redo = False
                elif free_simple_dec > 0 and line["uop_after"] <= 1:
                    free_simple_dec -= 1
                    line["dec_type"] = "simple"
                    line["dec_cycle"] = current_cycle
                    redo = False
                elif free_simple_dec == 0 and free_complex_dec > 0 and line["uop_after"] <= 1:
                    free_complex_dec -= 1
                    line["dec_type"] = "complex"
                    line["dec_cycle"] = current_cycle
                    redo = False
                elif free_complex_dec > 0 and 1 < line["uop_after"] <= complex_max:
                    free_complex_dec -= 1
                    line["dec_type"] = "complex"
                    line["dec_cycle"] = current_cycle
                    redo = False
                elif free_complex_dec > 0 and complex_max < line["uop_after"] <= complex_max + free_simple_dec:
                    free_complex_dec -= 1
                    free_simple_dec -= line["uop_after"]-complex_max
                    line["dec_type"] = "complex"
                    line["dec_cycle"] = current_cycle
                    redo = False
                elif free_complex_dec > 0 and \
                        line["uop_after"] > complex_max + settings["arch_parameters"]["simple_decoders"]:
                    free_complex_dec = settings["arch_parameters"]["simple_decoders"]
                    free_simple_dec = settings["arch_parameters"]["complex_decoders"]
                    current_cycle += 1
                    fusions_in_cycle = 0
                    line["dec_type"] = "ERROR"
                    line["dec_cycle"] = current_cycle
                    redo = False
                else:
                    free_simple_dec = settings["arch_parameters"]["simple_decoders"]
                    free_complex_dec = settings["arch_parameters"]["complex_decoders"]
                    current_cycle += 1
                    fusions_in_cycle = 0
                    redo = True
            else:
                redo = False


def micro_table(code_table):
    with open('./decode.json') as f:
        decode_data = json.load(f)
    for line in code_table:
        if get_op_type(line["op2"]) != "":
            op_decode_1 = \
                get_op_type(line["op1"]) + "," + get_op_type(line["op2"])
            op_decode_2 = \
                get_op_type(line["op1"]).rstrip('1234567890') + "," + get_op_type(line["op2"]).rstrip('1234567890')
        else:
            op_decode_1 = \
                get_op_type(line["op1"])
            op_decode_2 = \
                get_op_type(line["op1"]).rstrip('1234567890')
        if line["op"] in decode_data and op_decode_1 in decode_data[line["op"]]:
            line["uop_before"] = sum(decode_data[line["op"]][op_decode_1])
            line["uop_after"] = sum(decode_data[line["op"]][op_decode_1])
            line["uop_read"] = decode_data[line["op"]][op_decode_1][0]
            line["uop_modify"] = decode_data[line["op"]][op_decode_1][1]
            line["uop_address"] = decode_data[line["op"]][op_decode_1][2]
            line["uop_write"] = decode_data[line["op"]][op_decode_1][3]
        elif line["op"] in decode_data and op_decode_2 in decode_data[line["op"]]:
            line["uop_before"] = sum(decode_data[line["op"]][op_decode_2])
            line["uop_after"] = sum(decode_data[line["op"]][op_decode_2])
            line["uop_read"] = decode_data[line["op"]][op_decode_2][0]
            line["uop_modify"] = decode_data[line["op"]][op_decode_2][1]
            line["uop_address"] = decode_data[line["op"]][op_decode_2][2]
            line["uop_write"] = decode_data[line["op"]][op_decode_2][3]
        else:
            print(line["op"] + " " + line["op1"] + " " + line["op2"] + " not supported")


def micro_fusion(code_table):
    for line in code_table:
        if settings["micro_parameters"]["combined_enabled"] and \
                line["uop_read"] > 0 and \
                line["uop_modify"] > 0 and \
                line["uop_address"] > 0 and \
                line["uop_write"] > 0:
            line["uop_after"] -= 2
            line["uop_type"] = "combined"
        elif settings["micro_parameters"]["address_write"] and \
                line["uop_address"] > 0 and \
                line["uop_write"] > 0:
            line["uop_after"] -= 1
            line["uop_type"] = "address_write"
        elif settings["micro_parameters"]["read_modify"] and \
                line["uop_read"] > 0 and \
                line["uop_modify"] > 0:
            line["uop_after"] -= 1
            line["uop_type"] = "read_modify"


def loop_finder(code_table, mark_list):
    loop_count = 0
    for line_num, line in enumerate(code_table):
        if line["op"].upper() == "LOOP" and line["op1"] in mark_list:
            if line_num > mark_list[line["op1"]]:
                loop_count += 1
                for i in range(line_num, mark_list[line["op1"]] - 1, -1):
                    code_table[i]["loop_num"].append(loop_count)


def lsd(code_table):
    loops_count = {}
    for line_num, line in enumerate(code_table):
        if line["loop_num"]:
            for x in line["loop_num"]:
                if x not in loops_count and (line["op"].upper() != "LOOP" or x != line["loop_num"][0]):
                    loops_count[x] = line["uop_after"]
                elif x in loops_count and (line["op"].upper() != "LOOP" or x != line["loop_num"][0]):
                    loops_count[x] += line["uop_after"]
            if line["op"].upper() == "LOOP" and \
                    settings['lsd_parameters']['buffer_size'] >= loops_count[line["loop_num"][0]]:
                loop_num = line["loop_num"][0]
                for test_line in code_table[line_num::-1]:
                    if loop_num in test_line["loop_num"]:
                        test_line["loop_num"][test_line["loop_num"].index(loop_num)] = -loop_num
                    else:
                        break


def zeroing_idioms(code_table):
    for line in code_table:
        if line["op"].upper() in settings["zeroing_parameters"] and \
                settings["zeroing_parameters"][line["op"].upper()] and \
                line["op1"] == line["op2"] and \
                (get_op_type(line["op1"]) + "," + get_op_type(line["op2"]) == "r32,r32" or
                 get_op_type(line["op1"]) + "," + get_op_type(line["op2"]) == "r64,r64"):
            line["uop_after"] = 0
            line["uop_type"] = "zeroing_idiom"


def move_elimination(code_table):
    for line in code_table:
        if line["op"].upper() in settings["move_parameters"] and \
                settings["move_parameters"][line["op"].upper()] and \
                get_op_type(line["op1"]) in settings["move_parameters"] and \
                settings["move_parameters"][get_op_type(line["op1"])] and \
                get_op_type(line["op1"]) == get_op_type(line["op2"]) and \
                (settings["move_parameters"]['self_move'] or line["op1"] != line["op2"]):
            line["uop_after"] = 0
            line["uop_type"] = "move_elimination"


def get_op_type(op):
    g_intRegex = re.compile(r"^([+-]?[1-9]\d*|0)$")
    if op == "":
        return ""
    elif g_intRegex.match(str(op).strip()) is not None:
        return "i"
    elif op.upper() in ['RAX', 'RCX', 'RDX', 'RBX', 'RSP', 'RBP', 'RSI', 'RDI']:
        return "r64"
    elif op.upper() in ['EAX', 'ECX', 'EDX', 'EBX', 'ESP', 'EBP', 'ESI', 'EDI']:
        return "r32"
    elif op.upper() in ['AX', 'CX', 'DX', 'BX', 'SP', 'BP', 'SI', 'DI']:
        return "r16"
    elif op.upper() in ['AH', 'BH', 'CH', 'DH']:
        return "r8h"
    elif op.upper() in ['AL', 'BL', 'CL', 'DL', 'SPL', 'BPL', 'SIL', 'DIL']:
        return "r8l"
    elif '[' in op and ']' in op:
        return "m"
    else:
        return "mark"


def clear_tables():
    for row in document["micro_table"].select('tbody')[0].select('tr')[1:]:
        row.remove()
    for row in document["macro_table"].select('tbody')[0].select('tr')[1:]:
        row.remove()
    for row in document["macro_table_2"].select('tbody')[0].select('tr')[1:]:
        row.remove()


def fill_tables(code_table):
    current_line, merge, merge2, fusion_count, before_count, after_count = 0, 0, 0, 0, 0, 0
    loops_count = {}
    for i, line in enumerate(code_table):
        document["micro_table"].select('tbody')[0] <= html.TR()
        # micro table output
        if line["uop_type"] == "macro_fusion":
            fusion_count += 1
        u_row = document["micro_table"].select('tbody')[0].select('tr')[i + 1]
        if line["loop_num"]:
            for x in line["loop_num"]:
                if x not in loops_count and line["op"].upper() != "LOOP":
                    loops_count[x] = []
                    loops_count[x].append(line)
                elif x in loops_count:
                    loops_count[x].append(line)
            if line["loop_num"][0] % 2 != 0 and len(line["loop_num"]) < 2:
                u_row <= TD(f"{i + 1}", Class="td", Style=cell_style["lsd"])
            elif line["loop_num"][0] % 2 == 0 and len(line["loop_num"]) < 2:
                u_row <= TD(f"{i + 1}", Class="td", Style=cell_style["lsd_2"])
            elif line["loop_num"][0] % 2 != 0 and len(line["loop_num"]) > 1:
                u_row <= TD(f"{i + 1}", Class="td", Style=cell_style["lsd_3"])
            elif line["loop_num"][0] % 2 == 0 and len(line["loop_num"]) > 1:
                u_row <= TD(f"{i + 1}", Class="td", Style=cell_style["lsd_4"])
        else:
            u_row <= TD(f"{i + 1}", Class="td")
        if line["uop_type"] == "combined":
            u_row <= TD(line["op"], Class="td", Style=cell_style["combined"])
        elif line["uop_type"] == "address_write":
            u_row <= TD(line["op"], Class="td", Style=cell_style["address_write"])
        elif line["uop_type"] == "read_modify":
            u_row <= TD(line["op"], Class="td", Style=cell_style["read_modify"])
        elif line["uop_type"] == "zeroing_idiom":
            u_row <= TD(line["op"], Class="td", Style=cell_style["zeroing_idiom"])
        elif line["uop_type"] == "move_elimination":
            u_row <= TD(line["op"], Class="td", Style=cell_style["move_elimination"])
        elif line["uop_type"] == "macro_fusion":
            if fusion_count % 4 == 1 or fusion_count % 4 == 2:
                u_row <= TD(line["op"], Class="td", Style=cell_style["macro_fusion"])
            else:
                u_row <= TD(line["op"], Class="td", Style=cell_style["macro_fusion_2"])
        else:
            u_row <= TD(line["op"], Class="td")
        u_row <= TD(line["op1"], Class="td")
        u_row <= TD(line["op2"], Class="td")
        u_row <= TD(line["uop_read"], Class="td")
        u_row <= TD(line["uop_modify"], Class="td")
        u_row <= TD(line["uop_address"], Class="td")
        u_row <= TD(line["uop_write"], Class="td")
        u_row <= TD(line["uop_before"], Class="td")
        if line["uop_type"] == "combined":
            u_row <= TD(line["uop_after"], Class="td", Style=cell_style["combined"])
        elif line["uop_type"] == "address_write":
            u_row <= TD(line["uop_after"], Class="td", Style=cell_style["address_write"])
        elif line["uop_type"] == "read_modify":
            u_row <= TD(line["uop_after"], Class="td", Style=cell_style["read_modify"])
        elif line["uop_type"] == "zeroing_idiom":
            u_row <= TD(line["uop_after"], Class="td", Style=cell_style["zeroing_idiom"])
        elif line["uop_type"] == "move_elimination":
            u_row <= TD(line["uop_after"], Class="td", Style=cell_style["move_elimination"])
        elif line["uop_type"] == "macro_fusion":
            if fusion_count % 2 != 0:
                if fusion_count % 4 == 1:
                    u_row <= TD(1, Class="td", Style=cell_style["macro_fusion"], rowspan=2)
                else:
                    u_row <= TD(1, Class="td", Style=cell_style["macro_fusion_2"], rowspan=2)
        else:
            u_row <= TD(line["uop_after"], Class="td")
        if line["uop_before"] != "":
            before_count += line["uop_before"]
        if line["uop_after"] != "":
            after_count += line["uop_after"]
    if not settings["block_enabled"]["macro_fusion"]:
        macro_fusion(code_table)
    fusion_count = 0
    for i, line in enumerate(code_table):
        #document["micro_table"].select('tbody')[0] <= html.TR()
        document["macro_table"].select('tbody')[0] <= html.TR()
        document["macro_table_2"].select('tbody')[0] <= html.TR()
        current_line += 1
        if line["uop_type"] == "macro_fusion":
            fusion_count += 1
# first macro table output
        m_row = document["macro_table"].select('tbody')[0].select('tr')[current_line]
        if line["loop_num"]:
            if line["loop_num"][0] % 2 != 0 and len(line["loop_num"]) < 2:
                m_row <= TD(f"{i + 1}", Class="td", Style=cell_style["lsd"])
            elif line["loop_num"][0] % 2 == 0 and len(line["loop_num"]) < 2:
                m_row <= TD(f"{i + 1}", Class="td", Style=cell_style["lsd_2"])
            elif line["loop_num"][0] % 2 != 0 and len(line["loop_num"]) > 1:
                m_row <= TD(f"{i + 1}", Class="td", Style=cell_style["lsd_3"])
            elif line["loop_num"][0] % 2 == 0 and len(line["loop_num"]) > 1:
                m_row <= TD(f"{i + 1}", Class="td", Style=cell_style["lsd_4"])
        else:
            m_row <= TD(f"{i + 1}", Class="td")
        m_row <= TD(line["op"], Class="td")
        m_row <= TD(line["op1"], Class="td")
        m_row <= TD(line["op2"], Class="td")
        if line["uop_type"] == "macro_fusion":
            if fusion_count % 2 != 0:
                if fusion_count % 4 == 1:
                    m_row <= TD(line["dec_type"], Class="td", Style=cell_style["macro_fusion"], rowspan=2)
                else:
                    m_row <= TD(line["dec_type"], Class="td", Style=cell_style["macro_fusion_2"], rowspan=2)
        elif line["dec_type"] == "simple" and (line["uop_type"] == "combined" or
                                             line["uop_type"] == "read_modify" or
                                             line["uop_type"] == "address_write"):
            m_row <= TD(line["dec_type"], Class="td", Style=cell_style["simple_dec_micro"])
        elif line["dec_type"] == "complex":
            m_row <= TD(line["dec_type"], Class="td", Style=cell_style["complex_dec"])
        else:
            m_row <= TD(line["dec_type"], Class="td", Style=cell_style["simple_dec"])
        if merge == 0:
            for test_line in code_table[i:]:
                if test_line["dec_cycle"] == line["dec_cycle"] and test_line["op"].upper() != "LOOP":
                    merge += 1
                elif test_line["dec_cycle"] == line["dec_cycle"] and test_line["op"].upper() == "LOOP":
                    merge += 1
                    break
                elif test_line["dec_cycle"] != line["dec_cycle"] or test_line["op"].upper() == "LOOP":
                    break
            if merge > 0:
                m_row <= TD(line["dec_cycle"], Class="td", rowspan=merge)
                merge -= 1
            else:
                m_row <= TD(line["dec_cycle"], Class="td")
        else:
            merge -= 1
# second macro table output
        m2_row = document["macro_table_2"].select('tbody')[0].select('tr')[current_line]
        if line["loop_num"]:
            if line["loop_num"][0] % 2 != 0 and len(line["loop_num"]) < 2:
                m2_row <= TD(f"{i + 1}", Class="td", Style=cell_style["lsd"])
            elif line["loop_num"][0] % 2 == 0 and len(line["loop_num"]) < 2:
                m2_row <= TD(f"{i + 1}", Class="td", Style=cell_style["lsd_2"])
            elif line["loop_num"][0] % 2 != 0 and len(line["loop_num"]) > 1:
                m2_row <= TD(f"{i + 1}", Class="td", Style=cell_style["lsd_3"])
            elif line["loop_num"][0] % 2 == 0 and len(line["loop_num"]) > 1:
                m2_row <= TD(f"{i + 1}", Class="td", Style=cell_style["lsd_4"])
        else:
            m2_row <= TD(f"{i + 1}", Class="td")
        m2_row <= TD(line["op"], Class="td")
        m2_row <= TD(line["op1"], Class="td")
        m2_row <= TD(line["op2"], Class="td")
        if line["dec_type_2"] == "simple" and (line["uop_type"] == "combined" or
                                               line["uop_type"] == "read_modify" or
                                               line["uop_type"] == "address_write"):
            m2_row <= TD(line["dec_type_2"], Class="td", Style=cell_style["simple_dec_micro"])
        elif line["dec_type_2"] == "complex":
            m2_row <= TD(line["dec_type_2"], Class="td", Style=cell_style["complex_dec"])
        else:
            m2_row <= TD(line["dec_type_2"], Class="td", Style=cell_style["simple_dec"])
        if merge2 == 0:
            for test_line in code_table[i:]:
                if test_line["dec_cycle_2"] == line["dec_cycle_2"] and test_line["op"].upper() != "LOOP":
                    merge2 += 1
                elif test_line["dec_cycle_2"] == line["dec_cycle_2"] and test_line["op"].upper() == "LOOP":
                    merge2 += 1
                    break
                elif test_line["dec_cycle_2"] != line["dec_cycle_2"] or test_line["op"].upper() == "LOOP":
                    break
            if merge2 > 0:
                m2_row <= TD(line["dec_cycle_2"], Class="td", rowspan=merge2)
                merge2 -= 1
            else:
                m2_row <= TD(line["dec_cycle_2"], Class="td")
        else:
            merge2 -= 1

        if line["loop_num"] and line["op"].upper() == "LOOP" and line["loop_num"][0] > 0:
            if line["loop_num"][0] % 2 != 0 and len(line["loop_num"]) < 2:
                color = cell_style["lsd"]
            elif line["loop_num"][0] % 2 == 0 and len(line["loop_num"]) < 2:
                color = cell_style["lsd_2"]
            elif line["loop_num"][0] % 2 != 0 and len(line["loop_num"]) > 1:
                color = cell_style["lsd_3"]
            elif line["loop_num"][0] % 2 == 0 and len(line["loop_num"]) > 1:
                color = cell_style["lsd_4"]
            for copy_line in loops_count[line["loop_num"][0]][:-1]:
                document["macro_table"].select('tbody')[0] <= html.TR()
                document["macro_table_2"].select('tbody')[0] <= html.TR()
                current_line += 1
                m_row = document["macro_table"].select('tbody')[0].select('tr')[current_line]
                m2_row = document["macro_table_2"].select('tbody')[0].select('tr')[current_line]
                m_row <= TD("", Class="td", Style=color)
                m_row <= TD(copy_line["op"], Class="td", Style=color)
                m_row <= TD(copy_line["op1"], Class="td", Style=color)
                m_row <= TD(copy_line["op2"], Class="td", Style=color)
                m_row <= TD("", Class="td", Style=color)
                m_row <= TD("", Class="td", Style=color)
                m2_row <= TD("", Class="td", Style=color)
                m2_row <= TD(copy_line["op"], Class="td", Style=color)
                m2_row <= TD(copy_line["op1"], Class="td", Style=color)
                m2_row <= TD(copy_line["op2"], Class="td", Style=color)
                m2_row <= TD("", Class="td", Style=color)
                m2_row <= TD("", Class="td", Style=color)
        elif line["loop_num"] and line["op"].upper() == "LOOP" and line["loop_num"][0] < 0:
            if line["loop_num"][0] % 2 != 0 and len(line["loop_num"]) < 2:
                color = cell_style["lsd"]
            elif line["loop_num"][0] % 2 == 0 and len(line["loop_num"]) < 2:
                color = cell_style["lsd_2"]
            elif line["loop_num"][0] % 2 != 0 and len(line["loop_num"]) > 1:
                color = cell_style["lsd_3"]
            elif line["loop_num"][0] % 2 == 0 and len(line["loop_num"]) > 1:
                color = cell_style["lsd_4"]
            document["macro_table"].select('tbody')[0] <= html.TR()
            document["macro_table_2"].select('tbody')[0] <= html.TR()
            current_line += 1
            m_row = document["macro_table"].select('tbody')[0].select('tr')[current_line]
            m2_row = document["macro_table_2"].select('tbody')[0].select('tr')[current_line]
            m_row <= TD("Frontend sleep", Class="td", Style=color, colspan=6)
            m2_row <= TD("Frontend sleep", Class="td", Style=color, colspan=6)
# last line addition
    document["micro_table"].select('tbody')[0] <= html.TR()
    u_row = document["micro_table"].select('tbody')[0].select('tr')[len(code_table)+1]
    u_row <= TD("Total", Class="td", colspan=8)
    u_row <= TD(before_count, Class="td")
    u_row <= TD(after_count, Class="td")


@bind("input.counter", "change")
def counter_validation(ev):
    client_width = document.documentElement.clientWidth
    client_height = document.documentElement.clientHeight
    minimum = ev.target.min
    maximum = ev.target.max
    if ev.target.value == '':
        popup(minimum, maximum, client_width, client_height)
        if ev.target.value > ev.target.min:
            ev.target.value = ev.target.max
        else:
            ev.target.value = ev.target.min
        macro_fusions_validation()
    else:
        if re.match('[0-9]*[.,][0-9]*|\\s', ev.target.value):
            popup(minimum, maximum, client_width, client_height)
            if ev.target.value > ev.target.min:
                ev.target.value = ev.target.max
            else:
                ev.target.value = ev.target.min
            macro_fusions_validation()
        else:
            if int(ev.target.value) < int(ev.target.min) or int(ev.target.value) > int(ev.target.max):
                popup(minimum, maximum, client_width, client_height)
                if ev.target.value > ev.target.min:
                    ev.target.value = ev.target.max
                else:
                    ev.target.value = ev.target.min
                macro_fusions_validation()
            else:
                dummy = ev.target.value
                ev.target.value = ''
                ev.target.value = dummy
                macro_fusions_validation_with_popup(client_width, client_height)


def popup(minimum, maximum, client_width, client_height):
    top = int(client_height / 2) - 58
    left = int(client_width / 2) - 192
    popup = InfoDialog("Ошибка", "Введите целое значение в диапазоне от " + minimum + " до " + maximum, top=top, left=left, default_css=False, ok="Ок")
    close_button = document.select("span.brython-dialog-close")[0]
    close_button.remove()
    document <= DIV(Class="overlay")
    ok_button = document.select("button.brython-dialog-button")[0]
    ok_button.bind("click", delete_overlay)


def delete_overlay(ev):
    div = document.select("div.overlay")[0]
    div.remove()


def macro_fusions_validation():
    if int(document["input_fusions"].value) > int(document["input_decoders"].value):
        document["input_fusions"].value = document["input_decoders"].value


def macro_fusions_validation_with_popup(client_width, client_height):
    if int(document["input_fusions"].value) > int(document["input_decoders"].value):
        document["input_fusions"].value = document["input_decoders"].value
        top = int(client_height / 2) - 58
        left = int(client_width / 2) - 374
        popup = InfoDialog("Ошибка", "Количество макро слияний в такт не может быть больше, чем количество простых декодеров", top=top, left=left, default_css=False, ok="Ок")
        close_button = document.select("span.brython-dialog-close")[0]
        close_button.remove()
        document <= DIV(Class="overlay")
        ok_button = document.select("button.brython-dialog-button")[0]
        ok_button.bind("click", delete_overlay)


@bind("input.micro-checkbox", "change")
def micro_settings_validation(ev):
    if not document["micro-checkbox-1"].checked or not document["micro-checkbox-2"].checked:
        document["micro-checkbox-3"].checked = False
        document["micro-checkbox-3"].setAttribute('disabled', 'disabled')
    else:
        document["micro-checkbox-3"].removeAttribute('disabled')


@bind("textarea", "keydown")
def inputarea_tabulation(ev):
    input_area = document["inputarea"]
    if ev.keyCode == 9:
        document["micro_tab_button"].focus()
        value = input_area.value
        start = input_area.selectionStart
        end = input_area.selectionEnd

        input_area.value = value[0:start] + '\t' + value[end:len(value)]

        input_area.selectionStart = input_area.selectionEnd = start + 1


@bind("input.file", "change")
def load_file(ev):
    def onload(event):
        document["inputarea"].value = event.target.result

    # Get the selected file as a DOM File object
    file = document["file"].files[0]
    # Create a new DOM FileReader instance
    reader = window.FileReader.new()
    # Read the file content as text
    reader.readAsText(file)
    reader.bind("load", onload)


@bind("svg.bi-question-square", "click")
def show_info(ev):
    client_width = document.documentElement.clientWidth
    client_height = document.documentElement.clientHeight
    tab = document.select("button.active")[0]
    if (tab.id == "input_tab_button"):
        if settings["current_language"] == "Русский":
            top = int(client_height / 2) - 170
            left = int(client_width / 2) - 378
            popup = InfoDialog("Справочная информация", "", top=top, left=left, default_css=False, ok="Ок")
        else:
            top = int(client_height / 2) - 170
            left = int(client_width / 2) - 330
            popup = InfoDialog("Reference information", "", top=top, left=left, default_css=False, ok="Ok")
        close_button = document.select("span.brython-dialog-close")[0]
        close_button.remove()
        document <= DIV(Class="overlay")
        ok_button = document.select("button.brython-dialog-button")[0]
        ok_button.bind("click", delete_overlay)
        title = document.select("div.brython-dialog-title")[0]
        title.class_name = "brython-dialog-title-1"

        element = document.select("div.brython-dialog-panel")[0].childNodes[0]
        element <= P(Id="info-input-tab-1", Class="info-input-tab-1", align="justify")
        element <= P(Id="info-input-tab-2", Class="info-input-tab-2",  align="justify")
        element <= P(Id="info-input-tab-3", Class="info-input-tab-2", align="justify")
        element <= P(Id="info-input-tab-4", Class="info-input-tab-2", align="justify")
        if settings["current_language"] == "Русский":
            document["info-input-tab-1"].innerHTML = "Данная вкладка предназначена для ввода исходного кода, который будет использован для симуляции программой."
            document["info-input-tab-2"].innerHTML = "Ввод исходного кода можно осуществить напрямую в текстовое поле или произвести выгрузку исходного кода из выбранного текстового файла."
            document["info-input-tab-3"].innerHTML = "Также имеется возможность выбрать готовые примеры кода."
            document["info-input-tab-4"].innerHTML = "При использовании памяти в качестве операндов инструкций переменные памяти нужно заключать в квадратные скобки для их правильного распознавания программой (например, [addr1])."
        else:
            document["info-input-tab-1"].innerHTML = "This tab is for entering the source code that will be used for simulation by the program."
            document["info-input-tab-2"].innerHTML = "The source code can be entered directly into the text field, or the source code can be unloaded from the selected text file."
            document["info-input-tab-3"].innerHTML = "There is also a possibility to choose the ready code examples."
            document["info-input-tab-4"].innerHTML = "When using memory as operands of instructions, the memory variables must be enclosed in square brackets for the program to recognize them correctly. (for example, [addr1])."
            document["info-input-tab-1"].class_name = "info-input-tab-1-en"
            document["info-input-tab-2"].class_name = "info-input-tab-2-en"
            document["info-input-tab-3"].class_name = "info-input-tab-2-en"
            document["info-input-tab-4"].class_name = "info-input-tab-2-en"

    elif (tab.id == "parameters_tab_button"):
        if (client_height >= 920):
            top = int(client_height / 2) - 350
            left = int(client_width / 2) - 540
        elif (client_height >= 810 and client_height < 920):
            top = int(client_height / 2) - 310
            left = int(client_width / 2) - 540
        elif (client_height < 810):
            top = int(client_height / 2) - 270
            left = int(client_width / 2) - 540
        if settings["current_language"] == "Русский":
            popup = InfoDialog("Справочная информация", "", top=top, left=left, default_css=False, ok="Ок")
        else:
            popup = InfoDialog("Reference information", "", top=top, left=left, default_css=False, ok="Ok")
        close_button = document.select("span.brython-dialog-close")[0]
        close_button.remove()
        document <= DIV(Class="overlay")
        ok_button = document.select("button.brython-dialog-button")[0]
        ok_button.bind("click", delete_overlay)
        title = document.select("div.brython-dialog-title")[0]
        title.class_name = "brython-dialog-title-1"

        element = document.select("div.brython-dialog-panel")[0].childNodes[0]
        element <= DIV(Id="info-parameters-wrapper", Class="info-parameters-wrapper")
        wrapper = document.select("div.brython-dialog-panel")[0].childNodes[0].select("div.info-parameters-wrapper")[0]
        wrapper <= P(Id="info-parameters-tab-1", Class="info-parameters-tab-1", align="justify")
        wrapper <= P(Id="info-parameters-tab-2", Class="info-parameters-tab-4", align="justify")
        wrapper <= P(Id="info-parameters-tab-3", Class="info-parameters-tab-3", align="justify")
        wrapper <= P(Id="info-parameters-tab-4", Class="info-parameters-tab-3", align="justify")
        wrapper <= P(Id="info-parameters-tab-5", Class="info-parameters-tab-4", align="justify")
        wrapper <= P(Id="info-parameters-tab-6", Class="info-parameters-tab-3", align="justify")
        wrapper <= P(Id="info-parameters-tab-7", Class="info-parameters-tab-3", align="justify")
        wrapper <= P(Id="info-parameters-tab-8", Class="info-parameters-tab-4", align="justify")
        wrapper <= P(Id="info-parameters-tab-9", Class="info-parameters-tab-3", align="justify")
        wrapper <= P(Id="info-parameters-tab-10", Class="info-parameters-tab-3", align="justify")
        wrapper <= P(Id="info-parameters-tab-11", Class="info-parameters-tab-4", align="justify")
        wrapper <= P(Id="info-parameters-tab-12", Class="info-parameters-tab-3", align="justify")
        wrapper <= P(Id="info-parameters-tab-13", Class="info-parameters-tab-4", align="justify")
        wrapper <= P(Id="info-parameters-tab-14", Class="info-parameters-tab-3", align="justify")
        wrapper <= P(Id="info-parameters-tab-15", Class="info-parameters-tab-4", align="justify")
        wrapper <= P(Id="info-parameters-tab-16", Class="info-parameters-tab-3", align="justify")
        wrapper <= P(Id="info-parameters-tab-17", Class="info-parameters-tab-3", align="justify")
        wrapper <= P(Id="info-parameters-tab-18", Class="info-parameters-tab-3", align="justify")
        if settings["current_language"] == "Русский":
            document["info-parameters-tab-1"].innerHTML = "Данная вкладка предназначена для настройки параметров симуляции."
            document["info-parameters-tab-2"].innerHTML = "Раздел 'Параметры архитектуры':"
            document["info-parameters-tab-3"].innerHTML = "- определение количества простых и сложных декодеров симулируемого процессора;"
            document["info-parameters-tab-4"].innerHTML = "- определение максимального количества микро операций для сложного декодера, которое он сможет декодировать за 1 такт работы процессора (если данного количества микро операций не хватит для декодирования инструкции, то для декодирования каждой дополнительной микро операции будет использоваться простой декодер)."
            document["info-parameters-tab-5"].innerHTML = "Раздел 'Микро слияние':"
            document["info-parameters-tab-6"].innerHTML = "- выбор типов пар микро операций, которые будут подвержены микро слиянию;"
            document["info-parameters-tab-7"].innerHTML = "- регулирование возможности процессора совершать микро слияния нескольких типов пар микро операций в одной инструкции."
            document["info-parameters-tab-8"].innerHTML = "Раздел 'Move elimination':"
            document["info-parameters-tab-9"].innerHTML = "- определение разрядности регистров, для которых будет работать блок 'Move elimination';"
            document["info-parameters-tab-10"].innerHTML = "- регулирование возможности работы блока 'Move elimination' для случая перемещения данных из регистра в этот же самый регистр."
            document["info-parameters-tab-11"].innerHTML = "Раздел 'LSD':"
            document["info-parameters-tab-12"].innerHTML = "- определение размера буфера микро операций (инструкции, микро операции которых попадут в буфер LSD, не будут декодироваться повторно в процессе декодирования циклов)."
            document["info-parameters-tab-13"].innerHTML = "Раздел 'Нуль идиомы':"
            document["info-parameters-tab-14"].innerHTML = "- выбор инструкций, которые будут учитываться при определении нуль идиом."
            document["info-parameters-tab-15"].innerHTML = "Раздел 'Макро слияние':"
            document["info-parameters-tab-16"].innerHTML = "- выбор пар операций, которые будут подвержены макро слиянию (для каждой первой инструкции можно создать набор инструкций, с которыми будет происходить макро слияние при условии последовательного расположения первой и второй инструкции в программном коде.);"
            document["info-parameters-tab-17"].innerHTML = "- определение максимального числа макро слияний за 1 такт работы процессора;"
            document["info-parameters-tab-18"].innerHTML = "- регулирование функции переноса инструкции на следующий такт, которая потенциально может участвовать в макро слиянии и попала на последний простой декодер, с целью проверки возможности её слияния с последующей инструкцией."
        else:
            document["info-parameters-tab-1"].innerHTML = "This tab is for setting the simulation parameters."
            document["info-parameters-tab-2"].innerHTML = "Section 'Architecture parameters':"
            document["info-parameters-tab-3"].innerHTML = "- determining the number of simple and complex decoders of the simulated processor;"
            document["info-parameters-tab-4"].innerHTML = "- determining of the maximum number of micro operations for a complex decoder that it can decode in 1 cycle of the processor (if this number of micro operations is not enough to decode the instruction, then a simple decoder will be used to decode each additional micro operation)."
            document["info-parameters-tab-5"].innerHTML = "Section 'Micro fusion':"
            document["info-parameters-tab-6"].innerHTML = "- selection of the types of pairs of micro operations that will be subject to micro fusion;"
            document["info-parameters-tab-7"].innerHTML = "- regulation of the processor's ability to micro fusion several types of pairs of micro operations in one instruction."
            document["info-parameters-tab-8"].innerHTML = "Section 'Move elimination':"
            document["info-parameters-tab-9"].innerHTML = "- determining the bit width of the registers for which the 'Move elimination' block will work;"
            document["info-parameters-tab-10"].innerHTML = "- regulation of the ability of the 'Move elimination' block to work in the case of moving data from a register to the same register."
            document["info-parameters-tab-11"].innerHTML = "Section 'LSD':"
            document["info-parameters-tab-12"].innerHTML = "- determining the size of the buffer of micro operations (instructions whose micro-operations will get into the LSD buffer will not be decoded again during the loop decoding)."
            document["info-parameters-tab-13"].innerHTML = "Section 'Zeroing idioms':"
            document["info-parameters-tab-14"].innerHTML = "- selection of instructions that will be taken into account when defining zeroing idioms."
            document["info-parameters-tab-15"].innerHTML = "Section 'Macro fusion':"
            document["info-parameters-tab-16"].innerHTML = "- selection of pairs of operations that will be subject to macro fusion (for each first instruction, you can create a set of instructions with which a macro fusion will take place, provided that the first and second instructions are sequentially located in the program code.);"
            document["info-parameters-tab-17"].innerHTML = "- determining of the maximum number of macro fusions for 1 cycle of the processor;"
            document["info-parameters-tab-18"].innerHTML = "- regulation of the function of transferring an instruction to the next cycle, which can potentially participate in a macro merge and got to the last simple decoder, in order to check the possibility of its merging with a subsequent instruction."

    elif (tab.id == "macro_tab_button"):
        if settings["current_language"] == "Русский":
            top = int(client_height / 2) - 230
            left = int(client_width / 2) - 340
            popup = InfoDialog("Справочная информация", "", top=top, left=left, default_css=False, ok="Ок")
        else:
            top = int(client_height / 2) - 230
            left = int(client_width / 2) - 290
            popup = InfoDialog("Reference information", "", top=top, left=left, default_css=False, ok="Ok")
        close_button = document.select("span.brython-dialog-close")[0]
        close_button.remove()
        document <= DIV(Class="overlay")
        ok_button = document.select("button.brython-dialog-button")[0]
        ok_button.bind("click", delete_overlay)
        title = document.select("div.brython-dialog-title")[0]
        title.class_name = "brython-dialog-title-1"

        element = document.select("div.brython-dialog-panel")[0].childNodes[0]
        element <= P(Id="info-macro-tab-1", Class="info-macro-tab-1", align="justify")
        element <= P(Id="info-macro-tab-2", Class="info-macro-tab-2", align="justify")
        element <= IMG(Id="img-macro-1", src="static/blue.png", Class="img")
        element <= P(Id="info-macro-tab-3", Class="info-macro-tab-3", align="justify")
        element <= IMG(Id="img-macro-2", src="static/pale red.png", Class="img")
        element <= P(Id="info-macro-tab-4", Class="info-macro-tab-3", align="justify")
        element <= IMG(Id="img-macro-3", src="static/purple.png", Class="img")
        element <= P(Id="info-macro-tab-5", Class="info-macro-tab-3", align="justify")
        element <= IMG(Id="img-macro-4", src="static/yellow.png", Class="img")
        element <= IMG(Id="img-macro-5", src="static/dark yellow.png", Class="img-2")
        element <= P(Id="info-macro-tab-6", Class="info-macro-tab-4", align="justify")
        element <= IMG(Id="img-macro-6", src="static/orange.png", Class="img")
        element <= IMG(Id="img-macro-7", src="static/dark orange.png", Class="img-2")
        element <= P(Id="info-macro-tab-7", Class="info-macro-tab-4", align="justify")
        element <= IMG(Id="img-macro-8", src="static/green.png", Class="img")
        element <= IMG(Id="img-macro-9", src="static/dark green.png", Class="img-2")
        element <= P(Id="info-macro-tab-8", Class="info-macro-tab-4", align="justify")
        if settings["current_language"] == "Русский":
            document["info-macro-tab-1"].innerHTML = "Данная вкладка предназначена для отображения этапа декодирования инструкций процессором."
            document["info-macro-tab-2"].innerHTML = "В таблицах отображается два варианта симуляции процесса декодирования инструкций с включенным и выключенным макро слиянием."
            document["info-macro-tab-3"].innerHTML = "- данным цветом в таблице выделяются простые декодеры."
            document["info-macro-tab-4"].innerHTML = "- данным цветом в таблице выделяются сложные декодеры."
            document["info-macro-tab-5"].innerHTML = "- данным цветом в таблице выделяются инструкции, которые попали в простой декодер благодаря включенному блоку 'Микро слияние'."
            document["info-macro-tab-6"].innerHTML = "- данными цветами в таблице выделяются инструкции, которые подверглись макро слиянию."
            document["info-macro-tab-7"].innerHTML = "- данными цветами выделяются циклы."
            document["info-macro-tab-8"].innerHTML = "- данными цветами выделяются вложенные циклы."
        else:
            document["info-macro-tab-1"].innerHTML = "This tab is for displaying the stage of decoding instructions by the processor."
            document["info-macro-tab-2"].innerHTML = "The tables display two options for simulating the process of decoding instructions with enabled and disabled macro fusion."
            document["info-macro-tab-3"].innerHTML = "- this color in the table highlights simple decoders."
            document["info-macro-tab-4"].innerHTML = "- this color in the table highlights complex decoders."
            document["info-macro-tab-5"].innerHTML = "- this color in the table highlights instructions that got into a simple decoder because of the 'Micro fusion' block is on."
            document["info-macro-tab-6"].innerHTML = "- these colors in the table highlight instructions that were undergone a macro fusion."
            document["info-macro-tab-7"].innerHTML = "- these colors highlight loops."
            document["info-macro-tab-8"].innerHTML = "- these colors highlight nested loops."
            document["info-macro-tab-1"].class_name = "info-macro-tab-1-en"
            document["info-macro-tab-2"].class_name = "info-macro-tab-2-en"
            document["info-macro-tab-3"].class_name = "info-macro-tab-3-en"
            document["info-macro-tab-4"].class_name = "info-macro-tab-3-en"
            document["info-macro-tab-5"].class_name = "info-macro-tab-3-en"
            document["info-macro-tab-6"].class_name = "info-macro-tab-4-en"
            document["info-macro-tab-7"].class_name = "info-macro-tab-4-en"
            document["info-macro-tab-8"].class_name = "info-macro-tab-4-en"

    elif (tab.id == "micro_tab_button"):
        top = int(client_height / 2) - 180
        left = int(client_width / 2) - 480
        if settings["current_language"] == "Русский":
            popup = InfoDialog("Справочная информация", "", top=top, left=left, default_css=False, ok="Ок")
        else:
            left = left + 40
            popup = InfoDialog("Reference information", "", top=top, left=left, default_css=False, ok="Ok")
        close_button = document.select("span.brython-dialog-close")[0]
        close_button.remove()
        document <= DIV(Class="overlay")
        ok_button = document.select("button.brython-dialog-button")[0]
        ok_button.bind("click", delete_overlay)
        title = document.select("div.brython-dialog-title")[0]
        title.class_name = "brython-dialog-title-1"

        element = document.select("div.brython-dialog-panel")[0].childNodes[0]
        element <= P(Id="info-micro-tab-1", Class="info-micro-tab-1", align="justify")
        element <= P(Id="info-micro-tab-2", Class="info-micro-tab-2", align="justify")
        element <= IMG(Id="img-micro-1", src="static/light green.png", Class="img")
        element <= P(Id="info-micro-tab-3", Class="info-micro-tab-3", align="justify")
        element <= IMG(Id="img-micro-2", src="static/navy.png", Class="img")
        element <= P(Id="info-micro-tab-4", Class="info-micro-tab-3", align="justify")
        element <= IMG(Id="img-micro-3", src="static/turquoise.png", Class="img")
        element <= P(Id="info-micro-tab-5", Class="info-micro-tab-3", align="justify")
        element <= IMG(Id="img-micro-4", src="static/dark purple.png", Class="img")
        element <= P(Id="info-micro-tab-6", Class="info-micro-tab-3", align="justify")
        element <= IMG(Id="img-micro-5", src="static/red.png", Class="img")
        element <= P(Id="info-micro-tab-7", Class="info-micro-tab-3", align="justify")
        element <= IMG(Id="img-micro-6", src="static/yellow.png", Class="img")
        element <= IMG(Id="img-micro-7", src="static/dark yellow.png", Class="img-2")
        element <= P(Id="info-micro-tab-8", Class="info-micro-tab-4", align="justify")
        element <= IMG(Id="img-micro-8", src="static/orange.png", Class="img")
        element <= IMG(Id="img-micro-9", src="static/dark orange.png", Class="img-2")
        element <= P(Id="info-micro-tab-9", Class="info-micro-tab-4", align="justify")
        element <= IMG(Id="img-micro-10", src="static/green.png", Class="img")
        element <= IMG(Id="img-micro-11", src="static/dark green.png", Class="img-2")
        element <= P(Id="info-micro-tab-10", Class="info-micro-tab-4", align="justify")
        if settings["current_language"] == "Русский":
            document["info-micro-tab-1"].innerHTML = "Данная вкладка предназначена для отображения результата работы блоков процессора на микро уровне."
            document["info-micro-tab-2"].innerHTML = "В таблице отображаются список инструкций и результат их декодирования в виде количества полученных микро операций каждого типа и суммарного числа микро операций."
            document["info-micro-tab-3"].innerHTML = "- данным цветом выделяются инструкции, для которых было выполнено микро слияние типа 'read-modify'."
            document["info-micro-tab-4"].innerHTML = "- данным цветом выделяются инструкции, для которых было выполнено микро слияния типа 'address-write'."
            document["info-micro-tab-5"].innerHTML = "- данным цветом выделяются инструкции, для которых было выполнено оба типа микро слияния."
            document["info-micro-tab-6"].innerHTML = "- данным цветом выделяются нуль идиомы, распознанные процессором."
            document["info-micro-tab-7"].innerHTML = "- данным цветом выделяются инструкции, которые подверглись работе блока 'Move elimination'."
            document["info-micro-tab-8"].innerHTML = "- данными цветами в таблице выделяются инструкции, которые подверглись макро слиянию."
            document["info-micro-tab-9"].innerHTML = "- данными цветами выделяются циклы."
            document["info-micro-tab-10"].innerHTML = "- данными цветами выделяются вложенные циклы."
        else:
            document["info-micro-tab-1"].innerHTML = "This tab is for displaying the result of the work of the processor blocks at the micro level."
            document["info-micro-tab-2"].innerHTML = "The table displays a list of instructions and the result of their decoding in the form of the number of received micro operations of each type and the total number of micro operations."
            document["info-micro-tab-3"].innerHTML = "- this color highlights instructions for which a micro fusion of the 'read-modify' type was performed."
            document["info-micro-tab-4"].innerHTML = "- this color highlights instructions for which a micro fusion of the 'address-write' type was performed."
            document["info-micro-tab-5"].innerHTML = "- this color highlights instructions for which both types of micro fusion were performed."
            document["info-micro-tab-6"].innerHTML = "- this color highlights zeroing idioms identified by the processor."
            document["info-micro-tab-7"].innerHTML = "- this color highlights instructions that were undergone the 'Move elimination' block."
            document["info-micro-tab-8"].innerHTML = "- these colors in the table highlight instructions that were undergone a macro fusion."
            document["info-micro-tab-9"].innerHTML = "- these colors highlight loops."
            document["info-micro-tab-10"].innerHTML = "- these colors highlight nested loops."
            document["info-micro-tab-1"].class_name = "info-micro-tab-1-en"
            document["info-micro-tab-2"].class_name = "info-micro-tab-2-en"
            document["info-micro-tab-3"].class_name = "info-micro-tab-3-en"
            document["info-micro-tab-4"].class_name = "info-micro-tab-3-en"
            document["info-micro-tab-5"].class_name = "info-micro-tab-3-en"
            document["info-micro-tab-6"].class_name = "info-micro-tab-3-en"
            document["info-micro-tab-7"].class_name = "info-micro-tab-3-en"
            document["info-micro-tab-8"].class_name = "info-micro-tab-4-en"
            document["info-micro-tab-9"].class_name = "info-micro-tab-4-en"
            document["info-micro-tab-10"].class_name = "info-micro-tab-4-en"


def init():
    load_examples()


document.onload = init()
