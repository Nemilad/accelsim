from browser import document, bind, console, alert, html
from browser.html import TABLE, TR, TH, TD
import re

settings = {
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

    },
    'micro_parameters': {
        'read_modify': True,
        'address_write': True,
        'combined_enabled': True
    },
    'LSD_parameters': {
        'buffer size': 16
    },
    'Zeroing_parameters': {
        'XOR': True,
        'SUB': True
    },
    'Ones_parameters': {
        
    },
}

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

def load_example():
    pass

def load_file():
    pass

def code_check(code):
    return True

@bind("button.start", "click")
def simulation(ev):
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
                    'uop_after': ''
            }
            if line.split()[0][-1] == ':':
                mark_list.append({'mark': line.split()[0][:-1], 'pos': num})
                if len(line.split()) == 4:
                    template['op'] = line.split()[1]
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
                    template['op1'] = line.split()[1]
                    template['op2'] = line.split()[2]
                elif len(line.split()) == 2:
                    template['op'] = line.split()[0]
                    template['op1'] = line.split()[1]
                else:
                    template['op'] = line.split()[0]
            code_table.append(template.copy())
            template.clear()

        if settings["block_enabled"]["micro_fusion"]:
            micro_fusion(code_table)
        if settings["block_enabled"]["zeroing_idioms"]:
            zeroing_idioms(code_table)
        if settings["block_enabled"]["ones_idioms"]:
            ones_idioms(code_table)
        if settings["block_enabled"]["LSD"]:
            LSD(code_table, mark_list)
        if settings["block_enabled"]["macro_fusion"]:
            macro_fusion(code_table)

        fill_tables(code_table)

    else:
        pass

def macro_fusion(code_table):
    pass

def micro_fusion(code_table):
    pass

def LSD(code_table, mark_list):
    pass

def zeroing_idioms(code_table):
    pass

def ones_idioms(code_table):
    pass

def clear_tables():
    for row in document["micro_table"].select('tbody')[0].select('tr')[1:]:
        row.remove()
    for row in document["macro_table"].select('tbody')[0].select('tr')[1:]:
        row.remove()
    for row in document["macro_table_2"].select('tbody')[0].select('tr')[1:]:
        row.remove()

def fill_tables(code_table):
    clear_tables()
    for i, line in enumerate(code_table):
        document["micro_table"].select('tbody')[0] <= html.TR()
        document["macro_table"].select('tbody')[0] <= html.TR()
        document["macro_table_2"].select('tbody')[0] <= html.TR()

        u_row = document["micro_table"].select('tbody')[0].select('tr')[i + 1]
        u_row <= TD(f"{i+1}", Class="td")
        u_row <= TD(line["op"], Class="td")
        u_row <= TD(line["op1"], Class="td")
        u_row <= TD(line["op2"], Class="td")
        u_row <= TD(line["uop_read"], Class="td")
        u_row <= TD(line["uop_modify"], Class="td")
        u_row <= TD(line["uop_address"], Class="td")
        u_row <= TD(line["uop_write"], Class="td")
        u_row <= TD(line["uop_before"], Class="td")
        u_row <= TD(line["uop_after"], Class="td")

        m_row = document["macro_table"].select('tbody')[0].select('tr')[i + 1]
        m_row <= TD(f"{i+1}", Class="td")
        m_row <= TD(line["op"], Class="td")
        m_row <= TD(line["op1"], Class="td")
        m_row <= TD(line["op2"], Class="td")
        m_row <= TD(line["dec_type"], Class="td")
        m_row <= TD(line["dec_cycle"], Class="td")

        m2_row = document["macro_table_2"].select('tbody')[0].select('tr')[i + 1]
        m2_row <= TD(f"{i+1}", Class="td")
        m2_row <= TD(line["op"], Class="td")
        m2_row <= TD(line["op1"], Class="td")
        m2_row <= TD(line["op2"], Class="td")
        m2_row <= TD(line["dec_type_2"], Class="td")
        m2_row <= TD(line["dec_cycle_2"], Class="td")
    pass

@bind("input.counter", "change")
def counter_validation(ev):
    if (ev.target.value == ''):
        alert("Введите целое значение в диапазоне от " + ev.target.min + " до " + ev.target.max)
        if ev.target.value > ev.target.min:
            ev.target.value = ev.target.max
        else:
            ev.target.value = ev.target.min
        macro_fusions_validation()
    else:
        if (re.match('[0-9]*[.,][0-9]*|\\s', ev.target.value)):
            alert("Введите целое значение в диапазоне от " + ev.target.min + " до " + ev.target.max)
            if ev.target.value > ev.target.min:
                ev.target.value = ev.target.max
            else:
                ev.target.value = ev.target.min
            macro_fusions_validation()
        else:
            if (int(ev.target.value) < int(ev.target.min) or int(ev.target.value) > int(ev.target.max)):
                alert("Введите целое значение в диапазоне от " + ev.target.min + " до " + ev.target.max)
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

def macro_fusions_validation():
    if (int(document["input_fusions"].value) > int(document["input_decoders"].value)):
        alert("Количество макро слияний в такт не может быть больше, чем количество простых декодеров")
        document["input_fusions"].value = document["input_decoders"].value
