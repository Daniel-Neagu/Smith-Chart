from PyQt5.QtWidgets import QLabel, QPushButton, QWidget
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QEvent
from PyQt5.QtWidgets import * 



#helper functions to set up widgets and their styles, so that you don't have to do it in the main file
# also so you can save time for similar buttons

#remind to create functiont that will try to obtain the size of the screen and adjust the size of everything accordin to that
#so that the buttons and labels, and text, and etc. will get bigger in proportion to the screen getting bigger


def create_style_dict():
    return {
        "text": "",
        "color": "",
        "background-color": "",
        "font-size": "",
        "font-family" : "",
        "font-weight" : "",
        "text-align" : "",
        "border-color" : "",
        "border-width" : "",
        "border-style" : "",
        "border-radius" : "",
        "padding" : "",
        "margin" : ""
    }
def create_label(default, hover):
    label = QLabel(default["text"])
    label.setStyleSheet(
            "QLabel" "{" 
                f"color: {default["color"]};"
                f"background-color: {default["background-color"]};"
                f"font-size: {default["font-size"]};"
                f"font-family: {default["font-family"]};"
                f"font-weight: {default["font-weight"]};"

                f"text-align: {default["text-align"]};"

                f"border-color: {default["border-color"]};"
                f"border-width: {default["border-width"]};"
                f"border-style: {default["border-style"]};"

                f"padding: {default["padding"]};"
                f"margin: {default["margin"]};"

            "}" 
            f"QLabel:hover {{color: {hover["color"]}}};"
            )
    
    label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    return label

def create_widget(default,hover,pressed):
    widget = QWidget()
    widget.setStyleSheet(
            "QWidget {"
                f"border-color: {default['border-color']};"
                f"border-width: 1px;"
                f"border-style: "";"
            "}"

    )
    return widget

def smithcahrt_widget_border(color='white'):
    default = create_style_dict()
    hover = create_style_dict()
    pressed = create_style_dict()
    default["border-color"] = color
    return create_widget(default,hover,pressed)


def create_button(default, hover,pressed):
    button = QPushButton(default["text"])
    button.setStyleSheet(
            "QPushButton {" 
                f"color: {default['color']};"
                f"background-color: {default['background-color']};"
                f"font-size: {default['font-size']};"
                f"font-family: {default['font-family']};"
                f"font-weight: {default['font-weight']};"

                f"text-align: {default['text-align']};"

                f"border-color: {default['border-color']};"
                f"border-width: {default['border-width']};"
                f"border-style: {default['border-style']};"

                f"padding: {default['padding']};"
                f"margin: {default['margin']};"

            "}" 
            "QPushButton:hover {"
                f"color: {hover['color']};"
                f"background-color: {hover['background-color']};"
                f"border-width: {hover['border-width']};"
                f"border-color: {hover['border-color']};"
                f"font-size: {hover['font-size']};"

            "}"
            "QPushButton:pressed {"
                f"color: {pressed['color']};"
                f"background-color: {pressed['background-color']};"
                f"border-width: {pressed['border-width']};"
                f"border-color: {pressed['border-color']};"
                f"border-style: {pressed['border-style']};"
                f"font-size: {pressed['font-size']};"

            "}"
    )
    return button

#fix this or add an event filter so that it defocuses everywhere bc now it only defocuses, if you 
#press enter from the signal or if u move the cursor on top of the plot or else idk
class losefocusqeditline(QLineEdit):
    lostFocus = pyqtSignal()
    def __init__(self):
        super().__init__()
        QApplication.instance().installEventFilter(self)
    """
    def focusOutEvent(self, a0):
        return super().focusOutEvent(a0)"""
    
    def eventFilter(self, obj, event):
        # Detect mouse button press events
        if event.type() == QEvent.MouseButtonPress:
            # Check if the click is outside this QLineEdit
            if not self.underMouse():
                self.lostFocus.emit()
                self.clearFocus()  # Clear focus from QLineEdit
        return super().eventFilter(obj, event)

class framestack(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.dict_name_index = {}
        #self.dict_name_frame = {}

    def add(self,frame,text):
        #frame = QFrame()
        #self.dict_name_frame.setdefault(text,frame)
        if self.dict_name_index:
            last_value = list(self.dict_name_index.values())[-1]
            self.dict_name_index.setdefault(text, int(int(last_value)+1))
            #print(f"added {text},{last_value+1}")
        else:
            self.dict_name_index.setdefault(text,0)
            #print(f"added {self.framedict["title_frame"]}")
        self.addWidget(frame)

    def setframe(self,text):
        if self.dict_name_index:
            self.setCurrentIndex(self.dict_name_index[text])
        else:
            return

def create_qeditline(default, hover,placeholder,text,w,h):
    qlineedit = losefocusqeditline()
    qlineedit.setFixedSize(QSize(w,h))
    qlineedit.setMaxLength(100)

    #qlineedit.textEdited.connect(lambda: qlineedit.cursorBackward(False, steps=100))
    #qlineedit.cursorPositionChanged.connect(lambda: qlineedit.cursorBackward(False, steps=100))
    qlineedit.editingFinished.connect(lambda: (qlineedit.cursorBackward(False, steps=100),qlineedit.clearFocus()))
    qlineedit.lostFocus.connect(lambda: qlineedit.cursorBackward(False, steps=100))
    qlineedit.setPlaceholderText(text)
    qlineedit.setStyleSheet(
            "QLineEdit {" 
                f"color: {default['color']};"
                f"background-color: {default['background-color']};"
                f"font-size: {default['font-size']};"
                f"font-family: {default['font-family']};"
                f"font-weight: {default['font-weight']};"

                f"text-align: {default['text-align']};"

                f"border-color: {default['border-color']};"
                f"border-width: {default['border-width']};"
                f"border-style: {default['border-style']};"

                f"padding: {default['padding']};"
                f"margin: {default['margin']};"
                "qproperty-cursorPosition: 0;"

            "}" 
            "QLineEdit:hover {"
                f"color: {hover['color']};"
                f"background-color: {hover['background-color']};"

            "}"
            "QLineEdit::placeholder {"
                f"font-size: {placeholder['font-size']};"
                f"font-style: {placeholder['font-style']};"
                f"color: {placeholder['color']};"

            "}"
            )
    
    return qlineedit


def title_label1():
    default = create_style_dict()
    hover = create_style_dict()
    default["text"] = "Smith Chart"
    default["color"] = "lightgreen"
    default["background-color"] = "black"
    default["font-size"] = "20px"
    default["font-family"] = "Times new Roman"
    default["font-weight"] = "bold"
    default["text-align"] = "center"
    default["border-color"] = "white"
    default["border-width"] = "4px"
    default["border-style"] = "solid"
    default["padding"] = "3px"
    default["margin"] = "1px"
    hover["color"] = "lightgreen"
    return create_label(default, hover)

def impmatch_singleimp_title(text):
    default = create_style_dict()
    hover = create_style_dict()
    default["text"] = text
    default["color"] = "lightblue"
    default["background-color"] = "black"
    default["font-size"] = "20px"
    default["font-family"] = "Times new Roman"
    default["font-weight"] = "bold"
    default["text-align"] = "center"
    default["border-color"] = "white"
    default["border-width"] = "4px"
    default["border-style"] = "solid"
    default["padding"] = "3px"
    default["margin"] = "1px"
    return create_label(default, hover)

def smith_chart_variable_label(text):
    default = create_style_dict()
    hover = create_style_dict()
    default["text"] = text
    default["color"] = "lightblue"
    default["background-color"] = "black"
    default["font-size"] = "20px"
    default["font-family"] = "Times new Roman"
    default["font-weight"] = "bold"
    default["text-align"] = "center"
    default["border-color"] = "white"
    default["border-width"] = "3px"
    default["border-style"] = "solid"
    default["padding"] = "1px"
    default["margin"] = "1px"
    return create_label(default, hover)

def smith_chart_input_labels(text,width,height,font=18,dc="darkblue",dbc="darkgrey"):
    default = create_style_dict()
    hover = create_style_dict()
    default["text"] = text
    default["color"] = dc
    default["background-color"] = dbc
    default["font-size"] = f"{font}px"
    default["font-family"] = "Times new Roman"
    default["font-weight"] = "bold"
    default["text-align"] = "center"
    default["border-color"] = "white"
    default["border-width"] = "3px"
    default["border-style"] = "solid"
    default["padding"] = "1px"
    default["margin"] = "1px"

    label = create_label(default,hover)
    label.setFixedSize(width,height)
    return label

def title_button(text):
    default = create_style_dict()
    hover = create_style_dict()
    pressed = create_style_dict()
    default["text"] = text
    default["color"] = "lightgreen"
    default["background-color"] = "black"
    default["font-size"] = "20px"
    default["font-family"] = "Times new Roman"
    default["font-weight"] = "bold"
    default["text-align"] = "center"
    default["border-color"] = "white"
    default["border-width"] = "4px"
    default["border-style"] = "solid"
    default["padding"] = "3px"
    default["margin"] = "1px"
    hover["background-color"] = "rgba(100, 100, 250, 250)"
    hover["color"] = "lightgreen"
    return create_button(default, hover,pressed)

def smith_chart_button(text,dC="darkgreen",hC="lightgreen",pC="white",hBGC="black",dBGC="black",pBGC="black",pBdC="",pBdW="",hBdC="",hBdW="",pBdS="",pFS=""):
    default = create_style_dict()
    hover = create_style_dict()
    pressed = create_style_dict()
    default["text"] = text
    default["color"] = dC
    default["background-color"] = dBGC
    default["font-size"] = "20px"
    default["font-family"] = "Times new Roman"
    default["font-weight"] = "bold"
    default["text-align"] = "center"
    default["border-color"] = "white"
    default["border-width"] = "4px"
    default["border-style"] = "solid"
    default["padding"] = "3px"
    default["margin"] = "4px"
    hover["background-color"] = hBGC
    hover["color"] = hC
    hover["border-color"] = hBdC
    hover["border-width"] = hBdW
    pressed["background-color"] = pBGC
    pressed["color"] = pC
    pressed["border-color"] = pBdC
    pressed["border-width"] = pBdW
    pressed["border-style"] = pBdS
    pressed["font-size"] = pFS
    return create_button(default, hover,pressed)

def smith_chart_button_clunky(text):
    default = create_style_dict()
    hover = create_style_dict()
    pressed = create_style_dict()
    default["text"] = text
    default["color"] = "lightblue"
    default["background-color"] = "black"
    default["font-size"] = "20px"
    default["font-family"] = "Times new Roman"
    default["font-weight"] = "bold"
    default["text-align"] = "center"
    default["border-color"] = "white"
    default["border-width"] = "4px"
    default["border-style"] = "solid"
    default["padding"] = "3px"
    default["margin"] = "4px"
    hover["background-color"] = "lightblue"
    hover["color"] = "darkblue"
    pressed["background-color"] = "darkblue"
    pressed["color"] = "lightblue"
    pressed["border-width"] = "3px"
    return create_button(default, hover,pressed)

def smith_chart_button_boop(text):
    default = create_style_dict()
    hover = create_style_dict()
    pressed = create_style_dict()
    default["text"] = text
    default["color"] = "lightblue"
    default["background-color"] = "black"
    default["font-size"] = "20px"
    default["font-family"] = "Times new Roman"
    default["font-weight"] = "bold"
    default["text-align"] = "center"
    default["border-color"] = "white"
    default["border-width"] = "4px"
    default["border-style"] = "solid"
    default["padding"] = "3px"
    default["margin"] = "4px"
    hover["color"] = "lightblue"
    hover["background-color"] = "black"
    hover["font-size"] = "21px"
    hover["border-width"] = "3px"
    pressed["color"] = "white"
    pressed["background-color"] = "black"
    pressed["font-size"] = "20px"
    pressed["border-width"] = "4px"
    return create_button(default, hover,pressed)

def smith_chart_button_bold(text):
    default = create_style_dict()
    hover = create_style_dict()
    pressed = create_style_dict()
    default["text"] = text
    default["color"] = "lightblue"
    default["background-color"] = "black"
    default["font-size"] = "20px"
    default["font-family"] = "Times new Roman"
    default["font-weight"] = "bold"
    default["text-align"] = "center"
    default["border-color"] = "white"
    default["border-width"] = "4px"
    default["border-style"] = "solid"
    default["padding"] = "3px"
    default["margin"] = "4px"
    hover["color"] = "lightblue"
    hover["background-color"] = "black"
    pressed["color"] = "white"
    pressed["background-color"] = "black"
    return create_button(default, hover,pressed)

def smith_chart_button_inset(text):
    default = create_style_dict()
    hover = create_style_dict()
    pressed = create_style_dict()
    default["text"] = text
    default["color"] = "lightblue"
    default["background-color"] = "black"
    default["font-size"] = "20px"
    default["font-family"] = "Times new Roman"
    default["font-weight"] = "bold"
    default["text-align"] = "center"
    default["border-color"] = "white"
    default["border-width"] = "4px"
    default["border-style"] = "solid"
    default["padding"] = "3px"
    default["margin"] = "4px"
    hover["background-color"] = "black"
    hover["color"] = "lightblue"
    hover["border-color"] = "lightblue"
    pressed["background-color"] = "rgba(10,40,55,1)"
    pressed["color"] = "lightblue"
    pressed["border-width"] = "3px"
    pressed["border-color"] = "lightblue"
    return create_button(default, hover,pressed)

def smith_chart_button_cozy(text):
    default = create_style_dict()
    hover = create_style_dict()
    pressed = create_style_dict()
    default["text"] = text
    default["color"] = "lightblue"
    default["background-color"] = "black"
    default["font-size"] = "15px"
    default["font-family"] = "Times new Roman"
    default["font-weight"] = "bold"
    default["text-align"] = "center"
    default["border-color"] = "white"
    default["border-width"] = "4px"
    default["border-style"] = "solid"
    default["padding"] = "3px"
    default["margin"] = "4px"
    hover["background-color"] = "black"
    hover["color"] = "lightblue"
    hover["border-color"] = "lightblue"
    pressed["background-color"] = "black"
    pressed["color"] = "lightblue"
    pressed["border-width"] = "5px"
    pressed["border-color"] = "lightblue"
    pressed["font-size"] = "19px"
    return create_button(default, hover,pressed)

def smith_chart_button_cozy_size(text,width,height):
    button = smith_chart_button_cozy(text)
    button.setFixedSize(width,height)
    return button


def smith_chart_ImpQLineEdit(width,height,text="",dC="darkblue",hC="lightblue"):
    default = create_style_dict()
    hover = create_style_dict()
    placeholder = create_style_dict()
    default["color"] = dC
    default["background-color"] = "darkgrey"
    default["font-size"] = "15px"
    default["font-family"] = "Times new Roman"
    default["font-weight"] = "bold"
    default["text-align"] = "center"
    default["border-color"] = "white"
    default["border-width"] = "4px"
    default["border-style"] = "solid"
    default["padding"] = "1px"
    default["margin"] = "1px"
    hover["background-color"] = "grey"
    hover["color"] = hC
    placeholder["color"] = "darkblue"
    placeholder["font-style"] = "italic"
    placeholder["font-size"] = "15px"

    return create_qeditline(default, hover,placeholder,text,width,height)
    


    



