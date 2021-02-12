from browser import document, bind, console

settings = {
    'block_enabled': {
        'macro_fusion': True,
        'micro_fusion': True,
        'LSD': True,
        'Zeroing_Idioms': True,
        'Ones_Idioms': True
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
                    template['op'] = line.split()[1]
            code_table.append(template.copy())
            template.clear()
        print(code_table)
        print(mark_list)

    else:
        pass

def macro_fusion(code_table):
    pass

def micro_fusion(code_table):
    pass

def LSD(code_table, mark_list):
    pass

def zeroing_idiom(code_table):
    pass

def ones_idiom(code_table):
    pass
