from browser import document, bind, console, alert, html
from browser.html import TABLE, TR, TH, TD
import re, json

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

cell_style = {
    "zeroing_idiom": {"background-color": "#ff00ff"},
    "ones_idiom": {"background-color": "#ff007b"},
    "macro_fusion": {"background-color": "#ffff00"},
    "read_modify": {"background-color": "#40ff00"},
    "address_write": {"background-color": "#0040ff"},
    "combined": {"background-color": "#00ffff"}
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

def update_settings():
    input_value = document.select("div.blocks")[0].select("input.checkbox")
    settings["block_enabled"]["macro_fusion"] = input_value[0].checked
    settings["block_enabled"]["micro_fusion"] = input_value[1].checked
    settings["block_enabled"]["zeroing_idioms"] = input_value[2].checked
    settings["block_enabled"]["ones_idioms"] = input_value[3].checked
    settings["block_enabled"]["LSD"] = input_value[4].checked
    input_value = document.select("div.cpu-column-3")[0].select(".counter")
    settings["arch_parameters"]["simple_decoders"] = input_value[0].value
    settings["arch_parameters"]["complex_decoders"] = input_value[1].value
    settings["arch_parameters"]["uop_complex"] = input_value[2].value
    input_value = document.select("div.micro-column-3")[0].select(".micro-checkbox")
    settings["micro_parameters"]["read_modify"] = input_value[0].checked
    settings["micro_parameters"]["address_write"] = input_value[1].checked
    settings["micro_parameters"]["combined_enabled"] = input_value[2].checked

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
                    'uop_after': '',
                    'uop_type': ''
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

        update_settings()
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
        print(code_table)
        fill_tables(code_table)

    else:
        pass

def macro_fusion(code_table):
    pass

def micro_fusion(code_table):
    with open('./decode.json') as f:
        decode_data = json.load(f)
    for line in code_table:
        op_decode_1 = \
            get_op_type(line["op1"]) + "," + get_op_type(line["op2"])
        op_decode_2 = \
            get_op_type(line["op1"]).rstrip('1234567890') + "," + get_op_type(line["op2"]).rstrip('1234567890')
        if line["op"] in decode_data and op_decode_1 in decode_data[line["op"]]:
            line["uop_before"] = sum(decode_data[line["op"]][op_decode_1])
            line["uop_after"] = sum(decode_data[line["op"]][op_decode_1])
            line["uop_read"] = decode_data[line["op"]][op_decode_1][0]
            line["uop_modify"] = decode_data[line["op"]][op_decode_1][1]
            line["uop_address"] = decode_data[line["op"]][op_decode_1][2]
            line["uop_write"] =decode_data[line["op"]][op_decode_1][3]
        elif line["op"] in decode_data and op_decode_2 in decode_data[line["op"]]:
            line["uop_before"] = sum(decode_data[line["op"]][op_decode_2])
            line["uop_after"] = sum(decode_data[line["op"]][op_decode_2])
            line["uop_read"] = decode_data[line["op"]][op_decode_2][0]
            line["uop_modify"] = decode_data[line["op"]][op_decode_2][1]
            line["uop_address"] = decode_data[line["op"]][op_decode_2][2]
            line["uop_write"] =decode_data[line["op"]][op_decode_2][3]
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
    pass

def ones_idioms(code_table):
    pass

def get_op_type(op):
    g_intRegex = re.compile(r"^([+-]?[1-9]\d*|0)$")
    if g_intRegex.match(str(op).strip()) is not None:
        return("i")
    elif op.upper() in ['RAX', 'RCX', 'RDX', 'RBX', 'RSP', 'RBP', 'RSI', 'RDI']:
        return("r64")
    elif op.upper() in ['EAX', 'ECX', 'EDX', 'EBX', 'ESP', 'EBP', 'ESI', 'EDI']:
        return("r32")
    elif op.upper() in ['AX', 'CX', 'DX', 'BX', 'SP', 'BP', 'SI', 'DI']:
        return("r16")
    elif op.upper() in ['AH', 'BH', 'CH', 'DH']:
        return("r8h")
    elif op.upper() in ['AL', 'BL', 'CL', 'DL', 'SPL', 'BPL', 'SIL', 'DIL']:
        return("r8l")
    elif '[' in op and ']' in op:
        return("m")
    else:
        return("")
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
        if line["uop_type"] == "combined":
            u_row <= TD(line["uop_after"], Class="td", Style=cell_style["combined"])
        elif line["uop_type"] == "address_write":
            u_row <= TD(line["uop_after"], Class="td", Style=cell_style["address_write"])
        elif line["uop_type"] == "read_modify":
            u_row <= TD(line["uop_after"], Class="td", Style=cell_style["read_modify"])
        else:
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

@bind("input.micro-checkbox", "change")
def micro_settings_validation(ev):
    if (document["micro-checkbox-1"].checked == False or document["micro-checkbox-2"].checked == False):
        document["micro-checkbox-3"].checked = False
        document["micro-checkbox-3"].setAttribute('disabled', 'disabled')
    else:
        document["micro-checkbox-3"].removeAttribute('disabled')
