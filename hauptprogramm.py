#!/usr/bin/python python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
import socket
import threading

import canbusstatus   # Status und setzen der Baudrate
from Anzeigen import Anzeigenelemente
from CANBusbeschreibung_einlesen import CANBUS_Konfiguration
#from start_canbus import CANBUS #, CANBUS_Botschaften
from botschaftsort import CANBUS , can_bot_lesen, stop_can_lesen

class Bildschirmverwalter(ScreenManager): pass
class Hauptbildschirm(Screen):
    def canwerte1(self):
        if can0_exist == True:
            global canbus_konfiguration
            redu_botschaften=CANBUS().botschaften_sortieren(canbus_konfiguration.id_nr[0:4])
            print("Reduzierte Botschaften:\t",redu_botschaften)
            for i in range(0 ,len(redu_botschaften)):
                print("Task:\t",i)
                stop= False
                #[100, 0, [2, 0.00152587890625, 0.0, 1], [4, 0.00152587890625, 0.0, 4]]
                #[Botschaft_ID, Speicher_nr , [Startbit, Faktor, Offset, Anzeigennummer]]
                current=can_bot_lesen(redu_botschaften[i][0],stop)
                # der Deamon wird aktiviert damit beim Programm
                # schliessen alle threads beendet werden
                current.daemon = True
                current.start()
        return True
    def stop(self):
        act_threads=threading.active_count()
        print ("aktive Threads:\t",act_threads)
        alle_threads=threading.enumerate()
        print ("alle Threads:\t",alle_threads)
        stop_can_lesen().stop()
        print("Stopp gedrueckt")
    pass
class Bildschirm1_Canwerte(Screen):
    def stop(self):
        act_threads=threading.active_count()
        print ("aktive Threads:\t",act_threads)
        alle_threads=threading.enumerate()
        print ("alle Threads:\t",alle_threads)
        stop_can_lesen().stop()
        print("Stopp gedrueckt")
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

           4 Start des CANBUSes

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
        dateiname="canbus.conf"
        #dateiname="CANBusbeschreibung.conf"
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

        # 4 CANBUS Start mit den ersten 4 Werten
        if can0_exist == True:
            #print("Vektor    :\t",canbus_konfiguration.id_nr[0:4])
            CANBUS().can0_schnittstelle_aktivieren()
        #    redu_botschaften=CANBUS().botschaften_sortieren(canbus_konfiguration.id_nr[0:4])
        #    print("Reduzierte Botschaften:\t",redu_botschaften)
        #    for i in range(0 ,len(redu_botschaften)):
        #        print("Task:\t",i)
        #        stop= False
        #        #[100, 0, [2, 0.00152587890625, 0.0, 1], [4, 0.00152587890625, 0.0, 4]]
        #        #[Botschaft_ID, Speicher_nr , [Startbit, Faktor, Offset, Anzeigennummer]]
        #        current=can_bot_lesen(redu_botschaften[i][0],stop)
        #        # der Deamon wird aktiviert damit beim Programm
        #        # schliessen alle threads beendet werden
        #        current.daemon = True
        #        current.start()


        # Hintergrundfarbe ist Weis
        Window.clearcolor = (0.1,0.3,0.8,1)

if __name__=="__main__":
    Programm().run()