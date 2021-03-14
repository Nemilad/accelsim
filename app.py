from browser import document, bind, console, alert, html, window
from browser.html import TABLE, TR, TH, TD, DIV
from browser.widgets.dialog import InfoDialog
import re, json

settings = {
    'current_language': "Русский",
    'block_enabled': {
        'macro_fusion': True,
        'micro_fusion': True,
        'LSD': True,
        'zeroing_idioms': True,
        'ones_idioms': True
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
        'buffer size': 16
    },
    'zeroing_parameters': {
        'XOR': True,
        'SUB': True
    },
    'ones_parameters': {
        'CMP': True
    },
}

cell_style = {
    "zeroing_idiom": {"background-color": "#ff00ff"},
    "ones_idiom": {"background-color": "#ff007b"},
    "macro_fusion": {"background-color": "#ffff00"},
    "macro_fusion_2": {"background-color": "#cccc00"},
    "simple_dec": {"background-color": "#7b7bff"},
    "simple_dec_micro": {"background-color": "#ff7bff"},
    "complex_dec": {"background-color": "#ff7b7b"},
    "read_modify": {"background-color": "#40ff00"},
    "address_write": {"background-color": "#0040ff"},
    "combined": {"background-color": "#00ffff"}
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
    "One idioms": "Один идиомы",
    "Source code": "Исходный код",
    "Code examples:": "Готовые примеры:",
    "Example 1": "Пример 1",
    "Example 2": "Пример 2",
    "Example 3": "Пример 3",
    "Input from file:": "Ввод из файла:",
    "Select file": "Выберите файл",
    "Architecture parameters": "Параметры архитектуры",
    "Number of simple decoders:": "Количество простых декодеров:",
    "Number of complex decoders:": "Количество сложных декодеров:",
    "Maximum number of micro operations": "Максимальное число микро операций",
    "for a complex decoder:": "для сложного декодера:",
    "Both types of fusions": "Два вида слияния",
    "in one instruction": "в одной инструкции",
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
    "Operations before fusion": "Операции до слияния",
    "Operations after fusion": "Операции после слияния"
}

current_radio_button = "ADD"


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

    for element in document["input_tab"].select("p.subtitle"):
        if element.text in translation_dict.keys():
            element.text = translation_dict[element.text]

    for element in document["input_tab"].select("p.code-samples-title"):
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


def load_example():
    pass


def load_file():
    pass


def code_check(code):
    return True


def update_settings():
    input_value = document.select("div.blocks")[0].select("input.checkbox")
    settings["block_enabled"]["macro_fusion"] = input_value[0].checked
    settings["block_enabled"]["micro_fusion"] = input_value[1].checked
    settings["block_enabled"]["zeroing_idioms"] = input_value[2].checked
    settings["block_enabled"]["ones_idioms"] = input_value[3].checked
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
    settings["macro_parameters"]["max_fusions"] = input_value[0].value
    input_value = document.select("div.macro-checkbox-wrapper")[0].select(".checkbox")
    settings["macro_parameters"]["transition"] = input_value[0].checked
    input_value = document.select("div.idiom-0-wrapper")[0].select(".checkbox-1")
    settings["zeroing_parameters"]["XOR"] = input_value[0].checked
    settings["zeroing_parameters"]["SUB"] = input_value[1].checked


@bind("button.start", "click")
def simulation(ev):
    clear_tables()
    code_table = []
    mark_list = []
    code = document["inputarea"].value
    if code_check(code):
        for num, line in enumerate(code.splitlines()):
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
                'uop_type': ''
            }
            if line.split()[0][-1] == ':':
                mark_list.append({'mark': line.split()[0][:-1], 'pos': num})
                if len(line.split()) == 4:
                    template['op'] = line.split()[1]
                    if line.split()[2][-1] == ",":
                        template['op1'] = line.split()[2][:-1]
                    else:
                        template['op1'] = line.split()[2]
                    template['op2'] = line.split()[3]
                elif len(line.split()) == 3:
                    template['op'] = line.split()[1]
                    template['op1'] = line.split()[2]
                elif len(line.split()) == 2:
                    template['op'] = line.split()[1]
            else:
                if len(line.split()) == 3:
                    template['op'] = line.split()[0]
                    if line.split()[1][-1] == ",":
                        template['op1'] = line.split()[1][:-1]
                    else:
                        template['op1'] = line.split()[1]
                    template['op2'] = line.split()[2]
                elif len(line.split()) == 2:
                    template['op'] = line.split()[0]
                    template['op1'] = line.split()[1]
                else:
                    template['op'] = line.split()[0]
            code_table.append(template.copy())
            template.clear()

        update_settings()
        micro_table(code_table)
        if settings["block_enabled"]["micro_fusion"]:
            micro_fusion(code_table)
        if settings["block_enabled"]["zeroing_idioms"]:
            zeroing_idioms(code_table)
        if settings["block_enabled"]["ones_idioms"]:
            ones_idioms(code_table)
        if settings["block_enabled"]["LSD"]:
            LSD(code_table, mark_list)
        macro_table(code_table)
        if settings["block_enabled"]["macro_fusion"]:
            macro_fusion(code_table)
        fill_tables(code_table)
        code_table.clear()
        mark_list.clear()
    else:
        pass


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
            if fusions_in_cycle != max_fusions and \
                    get_op_type(line["op1"]) != "m" and \
                    line["op"].upper() in settings["macro_parameters"]:
                checking = True
            elif fusions_in_cycle != max_fusions and \
                    checking and \
                    line["op"].upper() in settings["macro_parameters"][code_table[line_num-1]["op"].upper()] and \
                    settings["macro_parameters"][code_table[line_num-1]["op"].upper()][line["op"].upper()]:
                if free_simple_dec < 1 and settings["macro_parameters"]["transition"]:
                    free_simple_dec = settings["arch_parameters"]["simple_decoders"]
                    free_complex_dec = settings["arch_parameters"]["complex_decoders"]
                    current_cycle += 1
                    fusions_in_cycle = 0
                if free_simple_dec > 1:
                    checking = False
                    if code_table[line_num - 1]["dec_type"] == "complex" and \
                            code_table[line_num - 1]["dec_cycle"] == current_cycle:
                        free_complex_dec += 1
                        free_simple_dec -= 1
                    elif code_table[line_num - 1]["dec_cycle"] != current_cycle:
                        free_simple_dec -= 1
                    fusions_in_cycle += 1
                    line["dec_cycle"] = current_cycle
                    line["uop_after"] = 1
                    line["uop_type"] = "macro_fusion"
                    line["dec_type"] = "simple"
                    code_table[line_num - 1]["dec_cycle"] = current_cycle
                    code_table[line_num - 1]["uop_after"] = ""
                    code_table[line_num - 1]["uop_type"] = "macro_fusion"
                else:
                    checking = False
            else:
                checking = False
            if line["uop_type"] != "macro_fusion":
                if settings["macro_parameters"]["transition"] and checking and free_simple_dec < 1:
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


def LSD(code_table, mark_list):
    pass


def zeroing_idioms(code_table):
    for line in code_table:
        if line["op"].upper() in settings["zeroing_parameters"] and \
                settings["zeroing_parameters"][line["op"].upper()] and \
                line["op1"] == line["op2"] and \
                (get_op_type(line["op1"]) + "," + get_op_type(line["op2"]) == "r32,r32" or
                 get_op_type(line["op1"]) + "," + get_op_type(line["op2"]) == "r64,r64"):
            line["uop_after"] = 0
            line["uop_type"] = "zeroing_idiom"


def ones_idioms(code_table):
    pass


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
    merge = 0
    merge2 = 0
    fusion_count = 0
    for i, line in enumerate(code_table):
        document["micro_table"].select('tbody')[0] <= html.TR()
        document["macro_table"].select('tbody')[0] <= html.TR()
        document["macro_table_2"].select('tbody')[0] <= html.TR()

        if line["uop_type"] == "macro_fusion":
            fusion_count += 1

        u_row = document["micro_table"].select('tbody')[0].select('tr')[i + 1]
        u_row <= TD(f"{i + 1}", Class="td")
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
        elif line["uop_type"] == "macro_fusion":
            if fusion_count % 2 != 0:
                if fusion_count % 4 == 1:
                    u_row <= TD(1, Class="td", Style=cell_style["macro_fusion"], rowspan=2)
                else:
                    u_row <= TD(1, Class="td", Style=cell_style["macro_fusion_2"], rowspan=2)
        else:
            u_row <= TD(line["uop_after"], Class="td")

        m_row = document["macro_table"].select('tbody')[0].select('tr')[i + 1]
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
            merge = sum(1 for test_line in code_table if test_line["dec_cycle"] == line["dec_cycle"])
            m_row <= TD(line["dec_cycle"], Class="td", rowspan=merge)
            merge -= 1
        else:
            merge -= 1

        m2_row = document["macro_table_2"].select('tbody')[0].select('tr')[i + 1]
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
            merge2 = sum(1 for test_line in code_table if test_line["dec_cycle_2"] == line["dec_cycle_2"])
            m2_row <= TD(line["dec_cycle_2"], Class="td", rowspan=merge2)
            merge2 -= 1
        else:
            merge2 -= 1
    print(code_table)


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
                macro_fusions_validation()


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
        alert("Количество макро слияний в такт не может быть больше, чем количество простых декодеров")
        document["input_fusions"].value = document["input_decoders"].value


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
        document["result_tab_button"].focus()
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
