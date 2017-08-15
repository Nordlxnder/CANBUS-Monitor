#!/usr/bin/python python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
import time

import canbusstatus   # Status und setzen der Baudrate
from Anzeigen import Anzeigenelemente
from CANBusbeschreibung_einlesen import CANBUS_Konfiguration
from botschaftsort2 import CANBUS , can_bot_lesen, can_lesen, can_anzeigen

class Bildschirmverwalter(ScreenManager): pass
class Hauptbildschirm(Screen):
    def canwerte1_lesen(self):
        global canbus_konfiguration
        self.redu_botschaften=CANBUS().botschaften_sortieren(canbus_konfiguration.id_nr[0:4])
        global can0_exist
        if can0_exist == True:
            can_lesen().start(self.redu_botschaften)
        return True
    def canwerte1_anzeigen(self):
        can_anzeigen().start(self.redu_botschaften)


    def stop(self):
        can_lesen().stop()
    pass
class Bildschirm1_Canwerte(Screen):
    def stop(self):
        can_lesen().stop()
    pass
class Bildschirm2_Canwerte(Screen):pass
class Bildschirm_Einzelwert(Screen):
    def on_touch_down(self, touch):
        global Bildschirmverwalter
        obj_Einzelwert=Bildschirmverwalter.ids.s100
        if self.collide_point( *touch.pos ):
            # Umschalten zur Einwertanzeige
            Bildschirmverwalter.transition = NoTransition()
            Bildschirmverwalter.current = obj_Einzelwert.altesFenster
            return True
        else:
            #print("Outsside")
            super(CAN_Wert_Anzeige, self).on_touch_down(touch)
            pass
    pass
class Bildschirm_Konfiguration(Screen):pass
class CAN_Wert_Anzeige(BoxLayout):
    def on_touch_down(self, touch):
        global Bildschirmverwalter
        obj_Einzelwert=Bildschirmverwalter.ids.s100
        if self.collide_point( *touch.pos ):
            # root = objekt Bildverwalter oberste Ebene
            root=self.parent.parent.parent.parent
            root.letzter_Bildschirm_Name= self.parent.parent.parent.name
            # Auslesen des Textelementes der Anzeige auf die geklickt wurde
            # Zuweisung des Textlabel für das Textlabel der Einzelbildanzeige
            obj_Einzelwert.ids.n1.text =self.ids.n1.text
            obj_Einzelwert.ids.w1.text =self.ids.w1.text
            obj_Einzelwert.ids.e1.text =self.ids.e1.text
            obj_Einzelwert.altesFenster=self.parent.parent.parent.name

            # Umschalten zur Einwertanzeige
            Bildschirmverwalter.transition = NoTransition()
            Bildschirmverwalter.current = 'bsew'
            return True
        else:
            #print("Outsside")
            super(CAN_Wert_Anzeige, self).on_touch_down(touch)
            pass
    pass

class Programm(App):
    title = 'CANbus'
    icon = 'canbus2.png'
    def build(self):
        '''

        Initialisierung

           1 Prüfung ob eine CAN Karte vorhanden ist ,
             wenn ja dann wird 500kBaud eingestellt
             und bindet den CAN Socket an die Can0
             Schnittstelle

           2 Anzeige der einzelnen CAN Botschaften im
             Konfigurationsfenster

           3 Einlesen der CANBUS Beschreibungsdatei
             Anpassen der Anzeigeelemente mit entspechend
             der Beschreibungsdatei (Name und Einheit)

           4 bindet den Socket an can0

        '''

        # 1 Überprüfung und Anzeige auf den Hauptbildschirm
        # ob eine Cankarte vorhaden ist
        global Bildschirmverwalter
        Bildschirmverwalter = self.root

        global can0_exist
        label_hauptbildschirm = Bildschirmverwalter.ids.s0.ids.l1
        can0_exist = canbusstatus.can0_check(label_hauptbildschirm)

        # DBC Datei einlesen und der Variable canbus_konfiguration zuweisen
        #dateiname = "CANBusbeschreibung.conf"
        dateiname="canbus100.conf"
        '''
        <canbus_konfiguration> besitzt folgende Atributte
            .id_nr  beinhaltet [Id Startbit Faktor Offset Nummer der Anzeige]
                               [100, 1,  0.00152587890625, 0.0, 1]
            .name_einheit  beinhaltet Name, Einheit, Nummer der Anzeige
                                    ['pmax1', 'bar', 1]
        '''
        global canbus_konfiguration
        canbus_konfiguration = CANBUS_Konfiguration().Datei_einlesen(dateiname)

        # 2 Anzeige einer Übersicht der CANBUS Botschaften im Konfigurationsfenster
        CANBUS_Konfiguration().uebersicht_can_botschaften(Bildschirmverwalter,canbus_konfiguration)

        # 3 Aktualisierung der Anzeigen von Name und Einheit
        # erstellt eine Liste der Anzeigeelement für die weitere Verwendung
        liste_anzeigen = Anzeigenelemente().liste_erstellen(Bildschirmverwalter)
        Anzeigenelemente().Anzeige_Name_Einheit_aktualisieren(liste_anzeigen, canbus_konfiguration.name_einheit)

        # Hintergrundfarbe ist Weis
        Window.clearcolor = (0.1,0.3,0.8,1)

if __name__=="__main__":
    Programm().run()