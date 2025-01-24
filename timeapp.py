from PySide6.QtCore import Qt, QCoreApplication, QTimer
from PySide6.QtWidgets import (QMainWindow, QPushButton, 
                               QGraphicsDropShadowEffect, 
                               QListWidget, QLabel)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QIcon, QPixmap, QFont, QFontDatabase
from PySide6.QtCore import QPoint
import os
from datetime import datetime


def path_fixer(file:str, p="resources") -> str:
    """ Fix Paths for icons and dbs """
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    file_path: str = os.path.join(BASE_DIR, p, file)
    return file_path

QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

class Time(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(300, 200)
        self.setWindowTitle("Time")
        self.normalWin = True
        
        # Set window flags for a frameless window
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Enable drop shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 0)
        shadow.setColor(Qt.black)
        self.setGraphicsEffect(shadow)
        
        # Dates and Time
        self.current_time = datetime.now()
        self.current_dateDay = self.current_time.strftime("%d")
        self.current_dateMonth = self.current_time.strftime("%m")
        self.current_dateYear = self.current_time.strftime("%Y")
        self.h  = self.current_time.strftime("%H")
        self.m = self.current_time.strftime("%M")
        self.counter_s = int(self.current_time.strftime("%S"))
        
        self.days = ["Sunday", "Monday", "Tuesday", "Wenesday", "Thursday", "Friday", "Saturday"]
        self.defualt_day = 5
        self.defualt_date  = 20
        
        # Load UI
        loader = QUiLoader() 
        self.ui = loader.load(path_fixer("Time.ui"))  
        
        self.setCentralWidget(self.ui)
    
        
        # Menu Bar
        self.formart_btn:QPushButton = self.findChild(QPushButton, "formart_btn")
        self.formart_options:QListWidget = self.findChild(QListWidget, "formart_options")
        self.close_btn:QPushButton = self.findChild(QPushButton, "close_btn")
        self.minimise_btn:QPushButton = self.findChild(QPushButton, "minimise_btn") 
        
        self.formart_options.hide()
        self.close_btn.setIcon(self.iconsetter("close.png"))
        self.minimise_btn.setIcon(self.iconsetter("minimize-sign.png"))
        self.formart_btn.clicked.connect(slot=self.formart_func)
        
        self.hours:QLabel = self.findChild(QLabel, "hours")
        self.minutes:QLabel = self.findChild(QLabel, "minutes")
        self.seconds:QLabel = self.findChild(QLabel, "seconds")
        self.am_pm:QLabel = self.findChild(QLabel, "am_pm")
        self.date:QLabel = self.findChild(QLabel, "date")
        self.day:QLabel = self.findChild(QLabel, "day")
        
        self.t_indicator:QLabel = self.findChild(QLabel, "t_indicator")
        self.hour_label:QLabel = self.findChild(QLabel, "hour_label")
        self.minutes_label:QLabel = self.findChild(QLabel, "minutes_label")
        self.sec_label:QLabel = self.findChild(QLabel, "sec_label")
       
        self.design()
        self.setTime_()
        self.date_setter()
        self.am_pm_setter()
        self.menuBtn_handler()
        self.extract_day()
       
        self.formart_options.clicked.connect(self.formart_opt_func)
  
        self.timer_Handler_(1000, self.auto_changeNumbers)
        self.timer_Handler_(600, self.indicatorHandler)
    
    def extract_day(self):
        if self.h == "00":
            day_index = self.defualt_day + 1
            self.day.setText(f"{self.days[day_index]}")
        else:
            day_index = self.defualt_day
            self.day.setText(f"{self.days[day_index]}")
        
    def mousePressEvent(self, event):
        """Capture the position when the mouse is pressed."""
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        """Handle the movement to drag the window."""
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()
    
    def iconsetter(self, ico:str, widget=None):
        """ Manage All icons in app """
        icon_ = QIcon()
        icon_.addPixmap(QPixmap(path_fixer(ico)))
        try:
            widget.setIcon(icon_)
        except:
            return icon_
    
    def formart_func(self):
        if self.formart_options.isHidden():
            self.formart_options.show()
        else:
            self.formart_options.hide()
    
    def formart_opt_func(self):
        if not self.formart_options.isHidden():
            if self.formart_options.currentRow() == 0 and int(self.h) >= 12:
                self.h = int(self.h) - 12
                if self.h == 0:
                    self.hours.setText(f"0{str(self.h)}")
                else:
                    self.hours.setText(f"{str(self.h)}")
                self.formart_options.hide()
              
            elif self.formart_options.currentRow() == 1 and int(self.h) <= 12 :
                self.h = int(self.h) + 12
                if self.h == 24:
                    self.h = "00"
                self.hours.setText(str(self.h))
                self.formart_options.hide()
                 
    def menuBtn_handler(self):
        self.close_btn.clicked.connect(self.close)
        self.minimise_btn.clicked.connect(self.showMinimized)
                                              
    def timer_Handler_(self, msec:int, func):
        """ Handles all timing """
        timer = QTimer(self)
        timer.start(msec)
        timer.timeout.connect(func)
    
    def indicatorHandler(self):
        self.t_indicator.setVisible(not self.t_indicator.isVisible())
    
    def handle_designFont(self, wid, size:int=20):
        # Load the custom font from the resource system
        font_id = QFontDatabase.addApplicationFont(path_fixer("DigitalNumbers-Regular.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)
        custom_font = QFont(font_family, size)
        if wid != None:
            wid.setFont(custom_font)
        else:
            print("NoneType Found: ", wid)
            ...

    def design(self):
        self.handle_designFont(self.hours)
        self.handle_designFont(self.minutes)
        self.handle_designFont(self.seconds)
        self.handle_designFont(self.am_pm, 9)
        
        self.handle_designFont(self.date, 11)
        
        self.handle_designFont(self.t_indicator, 25)
        
        self.handle_designFont(self.hour_label, 12)
        self.handle_designFont(self.minutes_label, 12)
        self.handle_designFont(self.sec_label, 12)
     
    def add_zero(self, value, wid):
        """ Adding zero to numbers less than2 length"""     
        if len(str(value)) >= 2:
            wid.setText(f"{str(value)}")
        else:
            wid.setText(f"0{str(value)}")

    def auto_changeNumbers(self):            
        self.setSceonds_()
        self.date_setter()
        self.am_pm_setter()

    def setSceonds_(self):
        self.counter_s = self.counter_s + 1
        if self.counter_s == 60:
            self.setMinutes_()
            self.counter_s = 0
            self.add_zero(self.counter_s, self.seconds)
        else:
            self.add_zero(self.counter_s, self.seconds)
    
    def setMinutes_(self):
        self.m = int(self.m) + 1   
        if self.m == 60:
            self.setHour_()
            self.m = 0
            self.add_zero(self.m, self.minutes)
        else:
            self.add_zero(self.m, self.minutes)
    
    def setHour_(self):
        self.h = int(self.h)+1
        if self.h == 12 or self.h == 24:
            """ still need fixing 24 and 12 hours settings  and am pm"""
            self.h = 0
            self.add_zero(self.h, self.hours)
        else:
            self.add_zero(self.h, self.hours)
            
    def setTime_(self):        
        """ Default Time... """
        self.hours.setText(self.h)
        self.minutes.setText(str(self.m))
        self.seconds.setText(str(self.counter_s))
      
    def date_setter(self):
        if int(self.h) >= 24 or str(self.h) == "00" and self.am_pm == "AM":
            self.current_dateDay = int(self.current_dateDay) + 1
            self.date.setText(f"{self.current_dateDay} - {self.current_dateMonth} - {self.current_dateYear}")
        else:
            self.date.setText(f"{self.current_dateDay} - {self.current_dateMonth} - {self.current_dateYear}")
        
    def am_pm_setter(self):
        if self.current_time.strftime("%H") == "12":
            self.am_pm.setText("PM")
        if self.current_time.strftime("%H") == "00":
            self.am_pm.setText("AM")  
           
        
        
       
        