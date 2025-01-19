import sys
import PyQt5.QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtGui import QGuiApplication
import widgets
import numpy as np
import plotting
import calculations

minimumSizeWindowX = 900
minimumSizeWindowY = 700

sizeWindowX = minimumSizeWindowX
sizeWindowY = minimumSizeWindowY

class Color(QWidget):

    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #window dimensions and specifications
        self.setWindowTitle("Smith Chart YAY")
        self.resize(minimumSizeWindowX,minimumSizeWindowY)
        self.setMinimumHeight(minimumSizeWindowY)
        self.setMinimumWidth(minimumSizeWindowX)
        #self.setFixedSize(QSize(minimumSizeWindowX,minimumSizeWindowY))

        #obtains the screen for methods: getsizewindowX, getsizewindowY
        self.screen = QGuiApplication.primaryScreen()

        #sets up all the screens and initializes the frame variables, therefore don't use go_to_frame before this or in them

        #self.frames = QStackedWidget(self)
        self.frames = widgets.framestack()
        #self.framedict = {}
        self.setUpTitleScreen()
        self.setUpSmithChart()
        self.setUpLoadFrame()
        self.setUpHelpFrame()
        self.setUpTitleScreenButtons()
        self.setUpSmithChartButtons()

        #takes you to the title screen first
        self.setCentralWidget(self.frames)


    def addtowidgetstack(self,frame,text,stack,dict):
        if dict:
            last_value = list(dict.values())[-1]
            dict.setdefault(text, int(int(last_value)+1))
            #print(f"added {text},{last_value+1}")
        else:
            dict.setdefault(text,0)
            #print(f"added {self.framedict["title_frame"]}")
        stack.addWidget(frame)

    
    def setUpTitleScreen(self):
        self.title_frame = QFrame()
        self.frames.add(self.title_frame,"title_frame")
        #self.addtowidgetstack(self.title_frame,"title_frame",self.frames,self.framedict)
        
        self.title_frameV = QVBoxLayout(self.title_frame)
        self.title_frame.setStyleSheet("QFrame{background-color: black}")

        self.title_spacer1 = QSpacerItem(self.getSizeWindowX(),int(self.getSizeWindowY()/4),hPolicy=QSizePolicy.Fixed,vPolicy=QSizePolicy.Fixed)
        self.title_frameV.addItem(self.title_spacer1)

        self.title_label1 = widgets.title_label1()
        self.title_frameV.addWidget(self.title_label1, alignment=Qt.AlignHCenter | Qt.AlignTop)

        self.title_spacer2 = QSpacerItem(self.getSizeWindowX(),int(self.getSizeWindowY()/3),hPolicy=QSizePolicy.Fixed,vPolicy=QSizePolicy.Fixed)
        self.title_frameV.addItem(self.title_spacer2)

        self.title_newbutton = widgets.title_button("New")
        self.title_frameV.addWidget(self.title_newbutton,alignment=Qt.AlignHCenter | Qt.AlignTop)
        self.title_loadbutton = widgets.title_button("Load")
        self.title_frameV.addWidget(self.title_loadbutton,alignment=Qt.AlignHCenter | Qt.AlignTop)
        self.title_helpbutton = widgets.title_button("Help")
        self.title_frameV.addWidget(self.title_helpbutton,alignment=Qt.AlignHCenter | Qt.AlignTop)

        self.title_spacer3 = QSpacerItem(self.getSizeWindowX(),int(self.getSizeWindowY()/3),hPolicy=QSizePolicy.Fixed,vPolicy=QSizePolicy.Fixed)
        self.title_frameV.addItem(self.title_spacer3)
    
    def setUpTitleScreenButtons(self):
        #self.title_newbutton.clicked.connect(lambda: self.frames.setCurrentIndex(self.framedict["smith_chart_frame"]))
        #self.title_loadbutton.clicked.connect(lambda: self.frames.setCurrentIndex(self.framedict["load_frame"]))
        #self.title_helpbutton.clicked.connect(lambda: self.frames.setCurrentIndex(self.framedict["help_frame"]))
        
        self.title_newbutton.clicked.connect(lambda: self.frames.setframe("smith_chart_frame"))

    def setUpSmithChart(self):
        self.smith_chart_frame = QFrame()
        self.smith_chart_frame.setStyleSheet("QFrame{background-color: black;}")
        #self.addtowidgetstack(self.smith_chart_frame,"smith_chart_frame",self.frames,self.framedict)
        self.frames.add(self.smith_chart_frame,"smith_chart_frame")
        self.smithchart_mainlayer = QVBoxLayout(self.smith_chart_frame)

        #THE LAYER VH1 CONTROLS THE TOP MENU BAR AND BUTTONS
        self.smithchart_H1 = QHBoxLayout()
        self.smithchart_mainlayer.addLayout(self.smithchart_H1)
        self.smithchart_mainlayer.setSpacing(0)  # No space between widgets
        self.smithchart_mainlayer.setContentsMargins(5, 5, 5, 5)

        self.smithchart_tophelp_button = widgets.smith_chart_button_clunky("help")
        self.smithchart_H1.addWidget(self.smithchart_tophelp_button, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.smithchart_topfile_button = widgets.smith_chart_button_clunky("file")
        self.smithchart_H1.addWidget(self.smithchart_topfile_button, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.smithchart_topload_button = widgets.smith_chart_button_clunky("load")
        self.smithchart_H1.addWidget(self.smithchart_topload_button, alignment=Qt.AlignTop | Qt.AlignLeft)

        self.smithchart_H1_spacer1= QSpacerItem(10,30,hPolicy=QSizePolicy.Expanding,vPolicy=QSizePolicy.Fixed)
        self.smithchart_H1.addItem(self.smithchart_H1_spacer1)

        #THIS NEXT HORIZONTAL LAYER INCLUDES THREE VERTICAL SUBLAYERS, 1 FOR A MENU AND CONTROL OF VARIABLES, 1 FOR THE GRAPH, 1 FOR CHARTS/DIAGRAMS IF NEEDED
        self.smithchart_H2 = QHBoxLayout()
        self.smithchart_mainlayer.addLayout(self.smithchart_H2)

        self.smithchart_H2.setSpacing(0)  # No space between widgets
        self.smithchart_H2.setContentsMargins(0, 0, 0, 0)

        #THIS LAYER CONTRAINS MENU AND VARIABLE CONTROLS CONDITINOS WHATEVER
        self.smithchart_H2V1 = QVBoxLayout()
        self.smithchart_H2.addLayout(self.smithchart_H2V1)

        self.smithchart_H2V1.setSpacing(0)  # No space between widgets
        self.smithchart_H2V1.setContentsMargins(0, 0, 0, 0)

        
        self.smithchart_H2V1_spacer1 = QSpacerItem(10,40,hPolicy=QSizePolicy.Fixed,vPolicy=QSizePolicy.Fixed)
        self.smithchart_H2V1.addItem(self.smithchart_H2V1_spacer1)
        #header functions of smith chart menu #Impedence Matching | Compass Mode | Color Settings
        self.smithchart_H2V1headers = QHBoxLayout()
        self.smithchart_H2V1.addLayout(self.smithchart_H2V1headers)

        self.smithchart_H2V1headers_impmatch_button = widgets.smith_chart_button_cozy("Impedence \nMatching")
       # self.smithchart_H2V1headers_impmatch_button.setMaximumSize(80,50)
        self.smithchart_H2V1headers.addWidget(self.smithchart_H2V1headers_impmatch_button, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.smithchart_H2V1headers_compass_button= widgets.smith_chart_button_cozy("Compass \nMode")
        #self.smithchart_H2V1headers_compass_button.setMaximumSize(80,50)
        self.smithchart_H2V1headers.addWidget(self.smithchart_H2V1headers_compass_button, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.smithchart_H2V1headers_color_button = widgets.smith_chart_button_cozy("Color \nSettings")
        #self.smithchart_H2V1headers_color_button.setMaximumSize(80,50)
        self.smithchart_H2V1headers.addWidget(self.smithchart_H2V1headers_color_button, alignment=Qt.AlignTop | Qt.AlignLeft)

        #BUFFER BETWEEN HEADERS AND THE MAIN STACK
        self.smithchart_H2V1_spacer2 = QSpacerItem(10,10,hPolicy=QSizePolicy.Fixed,vPolicy=QSizePolicy.Fixed)
        self.smithchart_H2V1.addItem(self.smithchart_H2V1_spacer2)
        #specific stack dealing with all three header tabs Imp Match | Color Settings | Compass Mode

        self.smithchart_H2V1stack = widgets.framestack()
        self.smithchart_H2V1.addWidget(self.smithchart_H2V1stack)
        self.smithchart_H2V1stack.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        #self.smithchart_H2V1stack.setSpacing(0)  # No space between widgets
        self.smithchart_H2V1stack.setContentsMargins(0, 0, 0, 0)
        
        #this frame index in the H2V1stack deals with the impedence matching tab
        
        self.smithchart_impmatch_frame = QFrame()
        self.smithchart_impmatch_frame.setContentsMargins(0, 0, 0, 0)
        self.smithchart_H2V1stack.add(self.smithchart_impmatch_frame,"impmatch_frame")
        #self.addtowidgetstack(self.smithchart_impmatch_frame,"impmatch_frame",self.smithchart_H2V1stack,self.smithchart_H2V1dict)
        
        
        self.smithchart_impmatch_main = QVBoxLayout(self.smithchart_impmatch_frame) #main layout for the items in the frame
        self.smithchart_impmatch_main.setSpacing(0)  # No space between widgets
        self.smithchart_impmatch_main.setContentsMargins(5, 0, 0, 0)
        #this layout deals with the double,single,series,parallel buttons which will change the  H2V1_impmatch_stack
        #buffer space between the header tabs and the options buttons
        #self.smithchart_impmatch_options_spacer1 = QSpacerItem(self.smithchart_H2V1width,10,hPolicy=QSizePolicy.Fixed, vPolicy=QSizePolicy.Fixed)
        #self.smithchart_impmatch_options.addItem(self.smithchart_impmatch_options_spacer1)

        self.smithchart_impmatch_widget = QWidget()
        self.smithchart_impmatch_widget.setStyleSheet("border: 2px solid white;")
        self.smithchart_impmatch_widget.setMaximumSize(235, 500)

        self.smithchart_impmatch_widget.setContentsMargins(0, 0, 0, 0)
        #widgets.smithcahrt_widget_border("blue")
        self.smithchart_impmatch_main.addWidget(self.smithchart_impmatch_widget)

        #H layout to contain the buttons
        self.smithchart_impmatch_optionsH = QHBoxLayout()
        self.smithchart_impmatch_optionsH.setSpacing(0)  # No space between widgets
        self.smithchart_impmatch_optionsH.setContentsMargins(0, 0, 0, 0)
        self.smithchart_impmatch_widget.setLayout(self.smithchart_impmatch_optionsH)

        #contains the single or double buttons
        self.smithchart_impmatch_options_SD = QVBoxLayout()
        self.smithchart_impmatch_options_SD.setSpacing(0)  # No space between widgets
        self.smithchart_impmatch_options_SD.setContentsMargins(45, 0, 5, 0)
        self.smithchart_impmatch_optionsH.addLayout(self.smithchart_impmatch_options_SD,stretch=1)
        self.smithchart_single_button = widgets.smith_chart_button_cozy_size("Single",70,40)
        self.smithchart_impmatch_options_SD.addWidget(self.smithchart_single_button,alignment=Qt.AlignCenter)
        self.smithchart_double_button = widgets.smith_chart_button_cozy_size("Double",70,40)
        self.smithchart_impmatch_options_SD.addWidget(self.smithchart_double_button,alignment=Qt.AlignCenter)

        #buffer
        #self.smithchart_impmatch_optionsH_spacer = QSpacerItem(10,20,hPolicy=QSizePolicy.Expanding, vPolicy=QSizePolicy.Fixed)
        #self.smithchart_impmatch_optionsH.addItem(self.smithchart_impmatch_optionsH_spacer)

        #contains the parallel or series buttons
        self.smithchart_impmatch_options_SP = QVBoxLayout()
        self.smithchart_impmatch_options_SP.setSpacing(0)  # No space between widgets
        self.smithchart_impmatch_options_SP.setContentsMargins(5,0, 45, 0)
        self.smithchart_impmatch_optionsH.addLayout(self.smithchart_impmatch_options_SP,stretch=1)
        self.smithchart_parallel_button = widgets.smith_chart_button_cozy_size("Parallel",70,40)
        self.smithchart_impmatch_options_SP.addWidget(self.smithchart_parallel_button,alignment=Qt.AlignCenter)
        self.smithchart_series_button = widgets.smith_chart_button_cozy_size("Series",70,40)
        self.smithchart_impmatch_options_SP.addWidget(self.smithchart_series_button,alignment=Qt.AlignCenter)
        #buffer space between the options buttons and the controls/variables underneath
        self.smithchart_impmatch_options_spacer2 = QSpacerItem(10,10,hPolicy=QSizePolicy.Fixed, vPolicy=QSizePolicy.Fixed)
        self.smithchart_impmatch_main.addItem(self.smithchart_impmatch_options_spacer2)
        #BUFFER BETWEEN HEADERS AND THE MAIN STACK
        #self.smithchart_impmatch_spacer1 = QSpacerItem(100,40,hPolicy=QSizePolicy.Fixed,vPolicy=QSizePolicy.Fixed)
        #self.smithchart_impmatch_main.addItem(self.smithchart_impmatch_spacer1)

        #this stack specifically deals with the variables for diff imp match options
        
        self.smithchart_impmatch_stack = widgets.framestack()
        self.smithchart_impmatch_main.addWidget(self.smithchart_impmatch_stack)
        #self.smithchart_impmatch_stack.setSpacing(0)  # No space between widgets
        self.smithchart_impmatch_stack.setContentsMargins(0, 0, 0, 0)
        self.smithchart_impmatch_stack.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        #frame for single series impedence matching
        self.smithchart_single_series_frame = QFrame()
        self.smithchart_single_series_frame.setContentsMargins(0, 0, 0, 0)
        self.smithchart_impmatch_stack.add(self.smithchart_single_series_frame,"single_series_frame")

        self.smithchart_single_series_V = QVBoxLayout(self.smithchart_single_series_frame)
        self.smithchart_single_series_V.setSpacing(0)  # No space between widgets
        self.smithchart_single_series_V.setContentsMargins(0, 0, 0, 0)

        #WIDGET CONTAINING THE INPUTS
        self.smithchart_single_series_inputW = QWidget()
        self.smithchart_single_series_inputW.setStyleSheet("border: 2px solid white;")
        self.smithchart_single_series_V.addWidget(self.smithchart_single_series_inputW)
        self.smithchart_single_series_inputW.setFixedSize(235, 130)

        self.smithchart_single_series_inputV = QVBoxLayout()
        self.smithchart_single_series_inputV.setSpacing(0)  # No space between widgets
        self.smithchart_single_series_inputV.setContentsMargins(0, 0, 0, 5)
        self.smithchart_single_series_inputW.setLayout(self.smithchart_single_series_inputV)

        self.smithchart_single_series_inputH1 = QHBoxLayout()
        self.smithchart_single_series_inputH1.setSpacing(0)  # No space between widgets
        self.smithchart_single_series_inputH1.setContentsMargins(0, 0, 0, 0)
        self.smithchart_single_series_inputV.addLayout(self.smithchart_single_series_inputH1)

        self.smithchart_single_Series_inputlabel = widgets.smith_chart_variable_label("inputs")
        self.smithchart_single_series_inputH1.addWidget(self.smithchart_single_Series_inputlabel,alignment=Qt.AlignCenter)

        self.smithchart_single_series_inputH2 = QHBoxLayout()
        self.smithchart_single_series_inputH2.setSpacing(0)  # No space between widgets
        self.smithchart_single_series_inputH2.setContentsMargins(3, 0, 3, 0)
        self.smithchart_single_series_inputV.addLayout(self.smithchart_single_series_inputH2)

        self.smithchart_single_series_inputH2spacer1 = QSpacerItem(5,10,hPolicy=QSizePolicy.Expanding,vPolicy=QSizePolicy.Fixed)
        self.smithchart_single_series_inputH2.addItem(self.smithchart_single_series_inputH2spacer1)
        self.smithchart_single_series_reloadlabel = widgets.smith_chart_input_labels("R{<sub>ZL</sub>}",55,40)
        self.smithchart_single_series_inputH2.addWidget(self.smithchart_single_series_reloadlabel,alignment=Qt.AlignLeft)
        self.smithchart_single_series_reload = widgets.smith_chart_ImpQLineEdit(55,40,"Ohm")
        self.smithchart_single_series_inputH2.addWidget(self.smithchart_single_series_reload,alignment=Qt.AlignLeft)
        self.smithchart_single_series_imloadlabel = widgets.smith_chart_input_labels("I{<sub>ZL</sub>}",55,40)
        self.smithchart_single_series_inputH2.addWidget(self.smithchart_single_series_imloadlabel,alignment=Qt.AlignLeft)
        self.smithchart_single_series_imload = widgets.smith_chart_ImpQLineEdit(55,40,"jOhm")
        self.smithchart_single_series_inputH2.addWidget(self.smithchart_single_series_imload,alignment=Qt.AlignLeft)
        self.smithchart_single_series_inputH2spacer2 = QSpacerItem(5,10,hPolicy=QSizePolicy.Expanding,vPolicy=QSizePolicy.Fixed)
        self.smithchart_single_series_inputH2.addItem(self.smithchart_single_series_inputH2spacer2)

        self.smithchart_single_series_inputH3 = QHBoxLayout()
        self.smithchart_single_series_inputH3.setSpacing(0)  # No space between widgets
        self.smithchart_single_series_inputH3.setContentsMargins(3, 0, 3, 0)
        self.smithchart_single_series_inputV.addLayout(self.smithchart_single_series_inputH3)

        self.smithchart_single_series_inputH3spacer1 = QSpacerItem(10,10,hPolicy=QSizePolicy.Expanding,vPolicy=QSizePolicy.Fixed)
        self.smithchart_single_series_inputH3.addItem(self.smithchart_single_series_inputH3spacer1)
        self.smithchart_single_series_implabel = widgets.smith_chart_input_labels("Z<sub>0</sub>",35,40)
        self.smithchart_single_series_inputH3.addWidget(self.smithchart_single_series_implabel,alignment=Qt.AlignLeft)
        self.smithchart_single_series_imp = widgets.smith_chart_ImpQLineEdit(60,40,"enter...")
        self.smithchart_single_series_inputH3.addWidget(self.smithchart_single_series_imp,alignment=Qt.AlignLeft)
        self.smithchart_single_series_phaseconstlabel = widgets.smith_chart_input_labels("B",35,40)
        self.smithchart_single_series_inputH3.addWidget(self.smithchart_single_series_phaseconstlabel,alignment=Qt.AlignLeft)
        self.smithchart_single_series_phaseconst = widgets.smith_chart_ImpQLineEdit(60,40,"enter...")
        self.smithchart_single_series_inputH3.addWidget(self.smithchart_single_series_phaseconst,alignment=Qt.AlignLeft)
        self.smithchart_single_series_inputH3spacer2 = QSpacerItem(10,10,hPolicy=QSizePolicy.Expanding,vPolicy=QSizePolicy.Fixed)
        self.smithchart_single_series_inputH3.addItem(self.smithchart_single_series_inputH3spacer2)

        self.smithchart_single_series_spacer1 = QSpacerItem(10,10,hPolicy=QSizePolicy.Fixed,vPolicy=QSizePolicy.Fixed)
        self.smithchart_single_series_V.addItem(self.smithchart_single_series_spacer1)

        #WIDGET CONTAINING THE OUTPUTS
        self.smithchart_single_series_outputW = QWidget()
        self.smithchart_single_series_outputW.setStyleSheet("border: 2px solid white;")
        self.smithchart_single_series_V.addWidget(self.smithchart_single_series_outputW)
        #self.smithchart_single_series_outputW.setFixedSize(235, 200)

        self.smithchart_single_series_outputV = QVBoxLayout()
        self.smithchart_single_series_outputV.setSpacing(0)  # No space between widgets
        self.smithchart_single_series_outputV.setContentsMargins(0, 5, 0, 5)
        self.smithchart_single_series_outputW.setLayout(self.smithchart_single_series_outputV)

        self.smithchart_single_series_outputH1 = QHBoxLayout()
        self.smithchart_single_series_outputH1.setSpacing(0)  # No space between widgets
        self.smithchart_single_series_outputH1.setContentsMargins(0, 0, 0, 0)
        self.smithchart_single_series_outputV.addLayout(self.smithchart_single_series_outputH1)

        self.smithchart_single_Series_outputlabel = widgets.smith_chart_variable_label("outputs")
        self.smithchart_single_series_outputH1.addWidget(self.smithchart_single_Series_outputlabel,alignment=Qt.AlignCenter)

        self.smithchart_single_series_outputVspacer1 = QSpacerItem(10,10,hPolicy=QSizePolicy.Expanding,vPolicy=QSizePolicy.Fixed)
        self.smithchart_single_series_outputV.addItem(self.smithchart_single_series_outputVspacer1)

        self.smithchart_single_series_outputH1 = QHBoxLayout()
        self.smithchart_single_series_outputH1.setSpacing(0)  # No space between widgets
        self.smithchart_single_series_outputH1.setContentsMargins(3, 0, 3, 0)
        self.smithchart_single_series_outputV.addLayout(self.smithchart_single_series_outputH1)
        self.smithchart_single_series_loadnormlabel = widgets.smith_chart_input_labels("Z<sub>L(n)</sub> =",110,40,font=14)
        self.smithchart_single_series_outputH1.addWidget(self.smithchart_single_series_loadnormlabel,alignment=Qt.AlignCenter)
        self.smithchart_single_series_refcoefmaglabel = widgets.smith_chart_input_labels("|&#915;<sub>d</sub>| =",110,40,font=14)
        self.smithchart_single_series_outputH1.addWidget(self.smithchart_single_series_refcoefmaglabel,alignment=Qt.AlignCenter)

        """
        self.smithchart_single_series_outputH2 = QHBoxLayout()
        self.smithchart_single_series_outputH2.setSpacing(0)  # No space between widgets
        self.smithchart_single_series_outputH2.setContentsMargins(3, 0, 3, 0)
        self.smithchart_single_series_outputV.addLayout(self.smithchart_single_series_outputH2)
        self.smithchart_single_series_SWRlabel = widgets.smith_chart_input_labels("SWR",58,40)
        self.smithchart_single_series_outputH2.addWidget(self.smithchart_single_series_SWRlabel,alignment=Qt.AlignLeft)
        """
        self.smithchart_single_series_outputH3 = QHBoxLayout()
        self.smithchart_single_series_outputH3.setSpacing(0)  # No space between widgets
        self.smithchart_single_series_outputH3.setContentsMargins(3, 0, 3, 0)
        self.smithchart_single_series_outputV.addLayout(self.smithchart_single_series_outputH3)
        self.smithchart_single_series_loadatd1label = widgets.smith_chart_input_labels("Z<sub>d1</sub> =",110,40,font=14)
        self.smithchart_single_series_outputH3.addWidget(self.smithchart_single_series_loadatd1label,alignment=Qt.AlignCenter)
        self.smithchart_single_series_loadatd2label = widgets.smith_chart_input_labels("Z<sub>d2</sub> =",110,40,font=14)
        self.smithchart_single_series_outputH3.addWidget(self.smithchart_single_series_loadatd2label,alignment=Qt.AlignCenter)

        self.smithchart_single_series_outputH4 = QHBoxLayout()
        self.smithchart_single_series_outputH4.setSpacing(0)  # No space between widgets
        self.smithchart_single_series_outputH4.setContentsMargins(3, 0, 3, 0)
        self.smithchart_single_series_outputV.addLayout(self.smithchart_single_series_outputH4)
        self.smithchart_single_series_jb1label = widgets.smith_chart_input_labels("b<sub>1</sub> =",110,40,font=14)
        self.smithchart_single_series_outputH4.addWidget(self.smithchart_single_series_jb1label,alignment=Qt.AlignCenter)
        self.smithchart_single_series_jb2label = widgets.smith_chart_input_labels("b<sub>2</sub> =",110,40,font=14)
        self.smithchart_single_series_outputH4.addWidget(self.smithchart_single_series_jb2label,alignment=Qt.AlignCenter)
        #also should add the non-normalized versions

        self.smithchart_single_series_outputH5 = QHBoxLayout()
        self.smithchart_single_series_outputH5.setSpacing(0)  # No space between widgets
        self.smithchart_single_series_outputH5.setContentsMargins(3, 0, 3, 0)
        self.smithchart_single_series_outputV.addLayout(self.smithchart_single_series_outputH5)
        self.smithchart_single_series_d1label = widgets.smith_chart_input_labels("d<sub>1</sub> =",110,40,font=14)
        self.smithchart_single_series_outputH5.addWidget(self.smithchart_single_series_d1label,alignment=Qt.AlignCenter)
        self.smithchart_single_series_d2label = widgets.smith_chart_input_labels("d<sub>2</sub> =",110,40,font=14)
        self.smithchart_single_series_outputH5.addWidget(self.smithchart_single_series_d2label,alignment=Qt.AlignCenter)

        self.smithchart_single_series_outputH6 = QHBoxLayout()
        self.smithchart_single_series_outputH6.setSpacing(0)  # No space between widgets
        self.smithchart_single_series_outputH6.setContentsMargins(3, 0, 3, 0)
        self.smithchart_single_series_outputV.addLayout(self.smithchart_single_series_outputH6)
        self.smithchart_single_series_l1label = widgets.smith_chart_input_labels("l<sub>1</sub> =",110,40,font=14)
        self.smithchart_single_series_outputH6.addWidget(self.smithchart_single_series_l1label,alignment=Qt.AlignCenter)
        self.smithchart_single_series_l2label = widgets.smith_chart_input_labels("l<sub>2</sub> =",110,40,font=14)
        self.smithchart_single_series_outputH6.addWidget(self.smithchart_single_series_l2label,alignment=Qt.AlignCenter)


        self.smithchart_single_series_outputVspacer2 = QSpacerItem(10,10,hPolicy=QSizePolicy.Expanding,vPolicy=QSizePolicy.Fixed)
        self.smithchart_single_series_outputV.addItem(self.smithchart_single_series_outputVspacer2)

        
        #frame for single parallel impedence matching
        self.smithchart_single_parallel_frame = QFrame()
        self.smithchart_single_parallel_frame.setContentsMargins(0, 0, 0, 0)
        self.smithchart_impmatch_stack.add(self.smithchart_single_parallel_frame,"single_parallel_frame")

        self.smithchart_single_parallel_V = QVBoxLayout(self.smithchart_single_series_frame)
        self.smithchart_single_parallel_V.setSpacing(0)  # No space between widgets
        self.smithchart_single_parallel_V.setContentsMargins(5, 0, 0, 0)

        self.smithchart_single_parallel_main = QWidget()
        self.smithchart_single_parallel_main.setStyleSheet("border: 2px solid white;")
        self.smithchart_single_parallel_main.setFixedSize(235, 100)
        
        #frame for double series impedence matching
        self.smithchart_double_series_frame = QFrame()
        self.smithchart_double_series_frame.setContentsMargins(0, 0, 0, 0)
        self.smithchart_impmatch_stack.add(self.smithchart_double_series_frame,"double_series_frame")

        self.smithchart_double_series_V = QVBoxLayout(self.smithchart_single_series_frame)
        self.smithchart_double_series_V.setSpacing(0)  # No space between widgets
        self.smithchart_double_series_V.setContentsMargins(5, 0, 0, 0)

        self.smithchart_double_series_main = QWidget()
        self.smithchart_double_series_main.setStyleSheet("border: 2px solid white;")
        self.smithchart_double_series_main.setMaximumSize(235, 500)

        #frame for double parallel impedence matching
        self.smithchart_double_parallel_frame = QFrame()
        self.smithchart_double_parallel_frame.setContentsMargins(0, 0, 0, 0)
        self.smithchart_impmatch_stack.add(self.smithchart_double_parallel_frame,"double_parallel_frame")

        self.smithchart_double_parallel_V = QVBoxLayout(self.smithchart_single_series_frame)
        self.smithchart_double_parallel_V.setSpacing(0)  # No space between widgets
        self.smithchart_double_parallel_V.setContentsMargins(5, 0, 0, 0)

        self.smithchart_double_parallel_main = QWidget()
        self.smithchart_single_parallel_main.setStyleSheet("border: 2px solid white;")
        self.smithchart_single_parallel_main.setMaximumSize(235, 500)

        self.smithchart_impmatch_doubleparallel_main_spacer2 = QSpacerItem(20,10,hPolicy=QSizePolicy.Fixed, vPolicy=QSizePolicy.Expanding)
        self.smithchart_H2V1.addItem(self.smithchart_impmatch_doubleparallel_main_spacer2)
        
        #BACK BUTTON TO GO BACK TO MAIN MENU FROM EVERYTHING
        self.smithchart_backbutton = widgets.smith_chart_button_bold("BACK")
        self.smithchart_H2V1.addWidget(self.smithchart_backbutton,alignment=Qt.AlignTop | Qt.AlignLeft)


        #THIS LAYER CONTROLS THE GRAPH/SMITH CHART PLOT
        self.smithchart_H2V2 = QVBoxLayout()
        self.smithchart_H2.addLayout(self.smithchart_H2V2)

        self.smithchart_H2V2.setSpacing(0)  # No space between widgets
        self.smithchart_H2V2.setContentsMargins(0, 0, 0, 0)

        #need to set the width of the spacer items, and the width/height of the graph to a proportional amount to screen width
        #also need to set a maximum to the plot dimensions
        self.smithchart_H2V2_spacer1 = QSpacerItem(200,10, hPolicy=QSizePolicy.Expanding, vPolicy=QSizePolicy.Fixed)
        self.smithchart_H2V2.addSpacerItem(self.smithchart_H2V2_spacer1)
        
        self.plot_graph = pg.PlotWidget()
        self.plot_graph.setMinimumSize(600,600)
        self.plot_graph.setAspectLocked()
        self.plot_graph.setFocusPolicy(Qt.NoFocus)
        self.plot_graph.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        
        self.smithchart_H2V2.addWidget(self.plot_graph)
        plotting.blank_plot(self.plot_graph)
        #self.plot_graph.resize(int(self.getSizeWindowX()/3),int(self.getSizeWindowX()/3))

        self.smithchart_H2V2_spacer2 = QSpacerItem(200,10, hPolicy=QSizePolicy.Expanding, vPolicy=QSizePolicy.Fixed)
        self.smithchart_H2V2.addSpacerItem(self.smithchart_H2V2_spacer2)

        
        #THIS LAYER CONTROLS ANY DIAGRAMS OR CIRCUIT DRAWINGS or something, lowkey maybe don't need this bc not much space
        self.smithchart_H2V3 = QVBoxLayout()
        self.smithchart_H2.addLayout(self.smithchart_H2V3)

        self.smithchart_H2V3.setSpacing(0)  # No space between widgets
        self.smithchart_H2V3.setContentsMargins(0, 0, 0, 0)

        self.smithchart_H2V3_spacer1 = QSpacerItem(40,200, hPolicy=QSizePolicy.Fixed, vPolicy=QSizePolicy.Expanding)
        self.smithchart_H2V3.addSpacerItem(self.smithchart_H2V3_spacer1)


    def setUpSmithChartButtons(self):
        
        self.smithchart_backbutton.clicked.connect(lambda: self.frames.setframe("title_frame"))
        self.setUpSmithChartCalculationsSingleSeries()

    def setUpSmithChartCalculationsSingleSeries(self):
        #calculate values here

        self.smithchart_single_series_reload.editingFinished.connect(lambda: (self.smithchartSingleSeriesChanges()))
        self.smithchart_single_series_imload.editingFinished.connect(lambda: (self.smithchartSingleSeriesChanges()))
        self.smithchart_single_series_imp.editingFinished.connect(lambda: (self.smithchartSingleSeriesChanges()))
        self.smithchart_single_series_phaseconst.editingFinished.connect(lambda: (self.smithchartSingleSeriesChanges()))

    def smithchartSingleSeriesChanges(self):
        #clear the graph so we can add changes to it
        plotting.blank_plot(self.plot_graph)
        
        #things to rewrite
        #obtain impedence values
        reload = self.smithchart_single_series_reload
        imload = self.smithchart_single_series_imload
        chrimp = self.smithchart_single_series_imp
        B = self.smithchart_single_series_phaseconst

        #check if they're valid
        #only if both the load and characteristic impedances are real move on and calculate them
        if(calculations.checkForValidImpedence(reload,imload)&calculations.checkForValidImpedence(chrimp,chrimp)):
            
            loadimp = calculations.convertImpTextToFloat(reload,imload)
            charimp = calculations.convertImpTextToFloat(chrimp,chrimp)
            #get the RefCoeffMag
            RefCoefMag = calculations.getRefCoeffMag(loadimp[0],loadimp[1],charimp[0])
            #get the normalized load impedence
            reloadnorm = loadimp[0]/charimp[0]
            imloadnorm = loadimp[1]/charimp[0]
            #plot the real circle 
            plotting.plotCircleReal(1,"pink",6,Qt.SolidLine,self.plot_graph,1000)
            #plot the SWR Circle
            plotting.plotCircle(0,0,RefCoefMag,1000,"blue",6,self.plot_graph)  
            #calculates intersection of real circle with SWR circle
            intersection_points = calculations.getIntersections2Circles(0,0,RefCoefMag,0.5,0,0.5)
            #plot the intersections the SWR circle has with the real circle
            plotting.plotPoints(intersection_points[0],intersection_points[1],self.plot_graph,"orange")
            #plot the norm load impedence
            loadpoint = calculations.convertImpedenceToPoint(reloadnorm,imloadnorm)
            plotting.plotPoints([loadpoint[0]],[loadpoint[1]],self.plot_graph,"orange")
            
            #set the text for Z1, Z2, b1, b2, d1, d2, l1, l2, Zn, RefCoeffMag
            #RefCoefficient
            self.smithchart_single_series_refcoefmaglabel.setText(f"|&#915;<sub>d</sub>|= {round(RefCoefMag,3)}")
            #Norm Load Impedance Zn
            if(loadimp[1]<0):
                self.smithchart_single_series_loadnormlabel.setText(f"Z<sub>L(n)</sub>= {round(reloadnorm,3)}-j{np.abs(round(imloadnorm,3))}")
            else:
                self.smithchart_single_series_loadnormlabel.setText(f"Z<sub>L(n)</sub>= {round(reloadnorm,3)}+j{np.abs(round(imloadnorm,3))}")

            #Moved Load Impedences Z1,Z2 and b1,b2
            newimp1 = calculations.convertPointToImpedence(intersection_points[0][0],intersection_points[1][0])
            newimp2 = calculations.convertPointToImpedence(intersection_points[0][1],intersection_points[1][1])
            if(newimp1[1]<0):
                self.smithchart_single_series_loadatd1label.setText(f"Z<sub>1(n)</sub>= {round(newimp1[0],3)}-j{abs(round(newimp1[1],3))}")
                self.smithchart_single_series_jb1label.setText(f"b<sub>1</sub> = +j{abs(round(newimp1[1],3))}")
            else:
                self.smithchart_single_series_loadatd1label.setText(f"Z<sub>1(n)</sub>= {round(newimp1[0],3)}+j{abs(round(newimp1[1],3))}")
                self.smithchart_single_series_jb1label.setText(f"b<sub>1</sub> = -j{abs(round(newimp1[1],3))}")
            if(newimp2[1]<0):
                self.smithchart_single_series_loadatd2label.setText(f"Z<sub>2(n)</sub>= {round(newimp2[0],3)}-j{abs(round(newimp2[1],3))}")
                self.smithchart_single_series_jb2label.setText(f"b<sub>2</sub> = +j{abs(round(newimp2[1],3))}")
            else:
                self.smithchart_single_series_loadatd2label.setText(f"Z<sub>2(n)</sub>= {round(newimp2[0],3)}+j{abs(round(newimp2[1],3))}")
                self.smithchart_single_series_jb2label.setText(f"b<sub>2</sub> = -j{abs(round(newimp2[1],3))}")

            #d1,d2
            d1 = calculations.getDistBetweenImpValues(reloadnorm,imloadnorm,newimp1[0],newimp1[1],RefCoefMag)
            d2 = calculations.getDistBetweenImpValues(reloadnorm,imloadnorm,newimp2[0],newimp2[1],RefCoefMag)
            self.smithchart_single_series_d1label.setText(f"d<sub>1</sub> = {round(d1,3)}&#411;")
            self.smithchart_single_series_d2label.setText(f"d<sub>2</sub> = {round(d2,3)}&#411;")
            #plot a line from origin that shows the intersections with the wavelength
            plotting.plotWavelengthLine(1.15,intersection_points[0][0],intersection_points[1][0],self.plot_graph,"orange")
            plotting.plotWavelengthLine(1.15,intersection_points[0][1],intersection_points[1][1],self.plot_graph,"orange")
            plotting.plotWavelengthLine(1.15,loadpoint[0],loadpoint[1],self.plot_graph,"orange")        
            
            #l1,l2
            if(calculations.checkForValidImpedence(B,B)):
                Bnum = calculations.convertImpTextToFloat(B,B) #need to input B twice because this is normally used for converting impedences, though we can do both!
                l1 = calculations.getShortCircuitShuntLength(Bnum[0],charimp[0],newimp1[1]*-1)
                l2 = calculations.getShortCircuitShuntLength(Bnum[0],charimp[0],newimp2[1]*-1)
                self.smithchart_single_series_l1label.setText(f"l<sub>1</sub> = {round(l1,3)}")
                self.smithchart_single_series_l2label.setText(f"l<sub>2</sub> = {round(l2,3)}")
    
        
    #maybe i should just be using a Qstack widget for these... since ill have to do this for every single subwindow, which
    #does not feel like the move!

        
    def setUpLoadFrame(self):
        self.load_frame = QFrame()
        self.load_frame.setStyleSheet(
            "QFrame{"
                "background-color: lightgreen;"
            
            "}"
        )
        #self.addtowidgetstack(self.load_frame,"load_frame",self.frames,self.framedict)
        self.frames.add(self.load_frame,"load_frame")
    def setUpHelpFrame(self):
        self.help_frame = QFrame()
        self.frames.add(self.help_frame,"help_frame")
        # self.addtowidgetstack(self.help_frame,"help_frame",self.frames,self.framedict)
        self.help_frame.setStyleSheet(
            "QFrame{"
                "background-color: lightblue;"
            
            "}"
        )
    


    #remind to create a function in widgets.py so that the size of the text scales with the screen becoming bigger
    def getSizeWindowX(self):
        return self.screen.size().width()
    def getSizeWindowY(self):
        return self.screen.size().height()


        
    #plotting a graph
    """            self.plot_graph = pg.PlotWidget()
    self.setCentralWidget(self.plot_graph)
    self.plot_graph.setFixedSize(QSize(400, 400));        """
    #button = QPushButton("Press Me!")
    # Set the central widget of the Window.
    #self.setCentralWidget(button)
    #button.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec()
