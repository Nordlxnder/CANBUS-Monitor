#!/usr/bin/python python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.core.window import Window
#from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
import canbusstatus




class Bildschirmverwalter(ScreenManager): pass
class Hauptbildschirm(Screen):pass
class Bildschirm1_Canwerte(Screen):pass
class Bildschirm2_Canwerte(Screen):pass
class Bildschirm_Einzelwert(Screen): pass
class Bildschirm_Konfiguration(Screen):pass




class Programm(App):
    title = 'CANbus'
    icon = 'canbus2.png'
    def build(self):
        # Überprüfung und Anzeige auf den Hauptbildschirm
        # ob eine Cankarte vorhaden ist
        Bildschirmverwalter = self.root
        global can0_exist
        label_hauptbildschirm = Bildschirmverwalter.ids.s1.ids.l1
        can0_exist = canbusstatus.can0_check(label_hauptbildschirm)

        # Hintergrundfarbe ist Weis
        Window.clearcolor = (0.1,0.3,0.8,1)


if __name__=="__main__":
    Programm().run()