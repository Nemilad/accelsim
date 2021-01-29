from browser import document, bind, console

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
