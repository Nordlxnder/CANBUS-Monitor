#!/usr/bin/python python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

import canbusstatus   # Status und setzen der Baudrate
from Anzeigen import Anzeigenelemente
from CANBusbeschreibung_einlesen import CANBUS_Konfiguration



class Bildschirmverwalter(ScreenManager): pass
class Hauptbildschirm(Screen):pass
class Bildschirm1_Canwerte(Screen):pass
class Bildschirm2_Canwerte(Screen):pass
class Bildschirm_Einzelwert(Screen): pass
class Bildschirm_Konfiguration(Screen):pass
class CAN_Wert_Anzeige(BoxLayout):pass



class Programm(App):
    title = 'CANbus'
    icon = 'canbus2.png'
    def build(self):
        # Überprüfung und Anzeige auf den Hauptbildschirm
        # ob eine Cankarte vorhaden ist
        Bildschirmverwalter = self.root

        global can0_exist
        label_hauptbildschirm = Bildschirmverwalter.ids.s0.ids.l1
        can0_exist = canbusstatus.can0_check(label_hauptbildschirm)

        # DBC Datei einlesen und der Variable canbus_konfiguration zuweisen
        dateiname = "CANBusbeschreibung.conf"
        '''
        <canbus_konfiguration> besitzt folgende Atributte
            .id_nr  beinhaltet [Id Startbit Faktor Offset Nummer der Anzeige]
                               [100, 1,  0.00152587890625, 0.0, 1]
            .name_einheit  beinhaltet Name, Einheit, Nummer der Anzeige
                                    ['pmax1', 'bar', 1]
        '''
        global canbus_konfiguration
        canbus_konfiguration = CANBUS_Konfiguration().Datei_einlesen(dateiname)
        #print(canbus_konfiguration.id_nr)
        #print(canbus_konfiguration.name_einheit)

        # erstellt eine Liste der Anzeigeelement für die weitere Verwendung
        liste_anzeigen = Anzeigenelemente().liste_erstellen(Bildschirmverwalter)

        # Aktualisierung der Anzeigen von Name und Einheit
        Anzeigenelemente().Anzeige_Name_Einheit_aktualisieren(liste_anzeigen, canbus_konfiguration.name_einheit)

        # Hintergrundfarbe ist Weis
        Window.clearcolor = (0.1,0.3,0.8,1)


if __name__=="__main__":
    Programm().run()