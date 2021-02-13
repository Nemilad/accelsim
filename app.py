from browser import document, bind, console, alert
import re

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
    for line in code:
        pass
    pass

@bind("button.start", "click")
def simulation(ev):
    code = document["inputarea"].value
    if code_check(code):
        pass
    else:
        pass

def macro_fusion(code):
    pass

def micro_fusion(code):
    pass

def LSD(code):
    pass

def zeroing_idiom(code):
    pass

def ones_idiom(code):
    pass

@bind("input.counter", "change")
def counter_validation(ev):
    if (ev.target.value == ''):
        alert("Введите целое значение в диапазоне от " + ev.target.min + " до " + ev.target.max)
        ev.target.value = ev.target.min
        macro_fusions_validation()
    else:
        if (re.match('[0-9]*[.,][0-9]*|\\s', ev.target.value)):
            alert("Введите целое значение в диапазоне от " + ev.target.min + " до " + ev.target.max)
            ev.target.value = ev.target.min
            macro_fusions_validation()
        else:
            if (int(ev.target.value) < int(ev.target.min) or int(ev.target.value) > int(ev.target.max)):
                alert("Введите целое значение в диапазоне от " + ev.target.min + " до " + ev.target.max)
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
