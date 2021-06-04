import os
import datetime
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem
from PyQt5 import QtGui, QtCore
from latas import *
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from Final3 import *
import numpy as np

myAPI = "6Y2UK5ORG1Z4BLWL"
anterior=1
import requests

class Ui_Dialog(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self, *args, **kwargs):
        QtWidgets.QApplication.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.datos= []
        #--------------------------------------
        self.label.setFont(QtGui.QFont('SansSerif', 10))
        self.label.setText("Reciclador")           
        self.Acelerometro.clicked.connect(lambda:  self.pantallaAce("Acelerometro"))
        self.Inductivo.clicked.connect(lambda:  self.pantallaInd("Sensor Inductivo"))
        self.Ultrasonico.clicked.connect(lambda:  self.pantallaUltra("Sensor Ultrasonico"))
       

    def pantallaAce(self,texto):   
        self.label.setFont(QtGui.QFont('SansSerif', 10))
        self.label.setText(texto)
        now = QDate.currentDate()
        tiempo = QTime.currentTime()
        gy=Acelerometro()
        self.inicio(str(gy),now.toString(Qt.ISODate),tiempo.toString(Qt.DefaultLocaleLongDate),1)
        self.agregar()
        self.web(0,0,gy)



    def pantallaInd(self,texto):
        self.label.setFont(QtGui.QFont('SansSerif', 10))
        self.label.setText(texto)
        now = QDate.currentDate()
        tiempo = QTime.currentTime()
        induc=Inductivo()
        if induc==0:
            self.inicio("Metal",now.toString(Qt.ISODate),tiempo.toString(Qt.DefaultLocaleLongDate),2)
            self.agregar()
            self.web(0,induc,0)
            return 0
        elif induc==1:  
            self.inicio("No metal",now.toString(Qt.ISODate),tiempo.toString(Qt.DefaultLocaleLongDate),2)
            self.agregar()
            self.web(0,induc,0)
            return 1
        else:
            self.inicio("No hay nada",now.toString(Qt.ISODate),tiempo.toString(Qt.DefaultLocaleLongDate),2)
            self.agregar()
            self.web(0,induc,0)
   
    def pantallaUltra(self,texto):
        self.label.setFont(QtGui.QFont('SansSerif', 10))
        self.label.setText(texto)        
        now = QDate.currentDate()
        tiempo = QTime.currentTime()
        ultra=Ultrasonico()
        self.inicio(str(ultra),now.toString(Qt.ISODate),tiempo.toString(Qt.DefaultLocaleLongDate),3)
        self.agregar()
        self.web(ultra,0,0)
        
    def inicio(self,uno,dos,tres,control):
        global anterior
        
        if control==anterior:
            self.datos.append((uno,dos,tres))
        else:
            anterior=control
            self.datos=[]
            self.Tabla.clearContents()
            self.datos.append((uno,dos,tres))

    def agregar(self):
        fila =0
        for registro in self.datos:
            columna=0
            for elemento in registro:   
                celda= QTableWidgetItem(elemento)
                self.Tabla.setItem(fila,columna,celda)
                columna+=1
            fila+=1

    def web(self,u,i,a):
        enviar=requests.get("https://api.thingspeak.com/update?api_key=6Y2UK5ORG1Z4BLWL&field1="+ str(u)+"&field2="+ str(i)+"&field3="+ str(a))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ui = Ui_Dialog()
    ui.show()
    app.exec_()
    
