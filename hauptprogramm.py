#!/usr/bin/python python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

import canbusstatus   # Status und setzen der Baudrate
from CANBusbeschreibung_einlesen import CANBUS_Konfiguration
from can_lesen_anzeigen import Anzeigenelemente, CANBUS
from can_lesen_anzeigen import Can_lesen, Can_anzeigen, Stop_CAN_Threads

class Bildschirmverwalter(ScreenManager): pass
class Hauptbildschirm(Screen):

    def stop(self):
        Stop_CAN_Threads().stop()
        return True

    def canwerte1_lesen(self):

        global canbus_konfiguration
        self.redu_botschaften=CANBUS().botschaften_sortieren(canbus_konfiguration.id_nr[0:4])
        global can0_exist
        if can0_exist == True:
            Can_lesen().start(self.redu_botschaften)
        return True
    def canwerte1_anzeigen(self):
        global Bildschirmverwalter
        fenster_id="s1"
        global can0_exist
        if can0_exist == True:
            Can_anzeigen().start(self.redu_botschaften,Bildschirmverwalter,fenster_id)
            canbusstatus.can0_status_ok()
    pass
class Bildschirm1_Canwerte(Screen):
    def canwerte2_lesen(self):
        global canbus_konfiguration
        self.redu_botschaften=CANBUS().botschaften_sortieren(canbus_konfiguration.id_nr[4:8])
        global can0_exist
        if can0_exist == True:
            Can_lesen().start(self.redu_botschaften)
        return True
    def canwerte2_anzeigen(self):
        global Bildschirmverwalter
        fenster_id="s2"
        global can0_exist
        if can0_exist == True:
            Can_anzeigen().start(self.redu_botschaften,Bildschirmverwalter,fenster_id)
            canbusstatus.can0_status_ok()
    def stop(self):
        Stop_CAN_Threads().stop()
    pass
class Bildschirm2_Canwerte(Screen):
    # fuer den Knopf zurueck
    def canwerte1_lesen(self):
        global canbus_konfiguration
        self.redu_botschaften=CANBUS().botschaften_sortieren(canbus_konfiguration.id_nr[0:4])
        global can0_exist
        if can0_exist == True:
            Can_lesen().start(self.redu_botschaften)
        return True
    def canwerte1_anzeigen(self):
        global Bildschirmverwalter
        fenster_id="s1"
        global can0_exist
        if can0_exist == True:
            Can_anzeigen().start(self.redu_botschaften,Bildschirmverwalter,fenster_id)
            canbusstatus.can0_status_ok()
    pass

    def stop(self):
        Stop_CAN_Threads().stop()
    pass

class Bildschirm_Einzelwert(Screen):
    def on_touch_down(self, touch):
        global Bildschirmverwalter, can0_exist, canbus_konfiguration
        obj_Einzelwert=Bildschirmverwalter.ids.s100
        if self.collide_point( *touch.pos ):
            # Umschalten zur Einwertanzeige
            Bildschirmverwalter.transition = NoTransition()
            Bildschirmverwalter.current = obj_Einzelwert.altesFenster

            # stoppt alle Threads wenn auf die Gesamtanzeige zurueck gegangen wird
            Stop_CAN_Threads().stop()

            # Start der Threads fuer die Gesamtanzeige
            if can0_exist == True:

                if obj_Einzelwert.altesFenster=="bs1cw":
                    redu_botschaften=CANBUS().botschaften_sortieren(canbus_konfiguration.id_nr[0:4])
                    Can_lesen().start(redu_botschaften)
                    # Start Anzeige
                    fenster_id="s1"
                    Can_anzeigen().start(redu_botschaften,Bildschirmverwalter,fenster_id)

                if obj_Einzelwert.altesFenster=="bs2cw":
                    redu_botschaften=CANBUS().botschaften_sortieren(canbus_konfiguration.id_nr[4:8])
                    Can_lesen().start(redu_botschaften)
                    # Start Anzeige
                    fenster_id="s2"
                    Can_anzeigen().start(redu_botschaften,Bildschirmverwalter,fenster_id)
            return True
        else:
            #print("Outsside")
            super(CAN_Wert_Anzeige, self).on_touch_down(touch)
            pass
    pass
class Bildschirm_Konfiguration(Screen):pass
class Baudrate_aendern(Screen):
    def baudrate(self,baudrate):
        global Bildschirmverwalter, can0_exist
        if can0_exist == True:
            canbusstatus.can_set_baudrate(baudrate)
            canbusstatus.status_ausgabe(Bildschirmverwalter)
        else:
            canbusstatus.keine_can0_karte(Bildschirmverwalter)
    pass
class CAN_Wert_Anzeige(BoxLayout):
    def on_touch_down(self, touch):
        global Bildschirmverwalter
        obj_Einzelwert=Bildschirmverwalter.ids.s100
        if self.collide_point( *touch.pos ):

            # Auslesen des Textelementes der Anzeige auf die geklickt wurde
            # Zuweisung des Textlabel für das Textlabel der Einzelbildanzeige
            obj_Einzelwert.ids.n1.text =self.ids.n1.text
            obj_Einzelwert.ids.w1.text =self.ids.w1.text
            obj_Einzelwert.ids.w1.font_size= 100
            obj_Einzelwert.ids.e1.text =self.ids.e1.text
            obj_Einzelwert.ids.e1.text_ori =self.ids.e1.text_ori
            obj_Einzelwert.altesFenster=self.parent.parent.parent.name

            # Umschalten zur Einwertanzeige
            Bildschirmverwalter.transition = NoTransition()
            Bildschirmverwalter.current = 'bsew'

            # Stop aller Threads und Start des Threads für den angezeigten Wert
            Stop_CAN_Threads().stop()

            # formatieren fuer die Uebergabe
            global canbus_konfiguration
            if obj_Einzelwert.altesFenster=="bs1cw":
                a=canbus_konfiguration.id_nr[int(self.ref_nr)]
            if obj_Einzelwert.altesFenster=="bs2cw":
                a=canbus_konfiguration.id_nr[int(self.ref_nr)+4]

            redu_botschaften_kurz=[[a[0],0,a[1:5]]]

            global can0_exist
            if can0_exist == True:
                Can_lesen().start(redu_botschaften_kurz)
            # Anzeige aktualisieren
            fenster_id="s100"
            Can_anzeigen().start(redu_botschaften_kurz,Bildschirmverwalter,fenster_id)

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
        '''

        # 1 Überprüfung und Anzeige auf den Hauptbildschirm
        # ob eine Cankarte vorhaden ist
        global Bildschirmverwalter
        Bildschirmverwalter = self.root

        global can0_exist
        can0_exist = canbusstatus.can0_check(Bildschirmverwalter)
        # Anzeige des Statuses im Haupfenste
        if can0_exist == True:
            canbusstatus.status_ausgabe(Bildschirmverwalter)

        # DBC Datei einlesen und der Variable canbus_konfiguration zuweisen
        dateiname = "CANBusbeschreibung.conf"
        #dateiname="./Beispieldateien/canbus.conf"
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
        CANBUS_Konfiguration().uebersicht_can_botschaften(Bildschirmverwalter,
        canbus_konfiguration,dateiname)

        # 3 Aktualisierung der Anzeigen von Name und Einheit
        # erstellt eine Liste der Anzeigeelement für die weitere Verwendung
        liste_anzeigen = Anzeigenelemente().liste_erstellen(Bildschirmverwalter)
        Anzeigenelemente().Anzeige_Name_Einheit_aktualisieren(liste_anzeigen, canbus_konfiguration.name_einheit)

        # Hintergrundfarbe ist Weis
        Window.clearcolor = (0.1,0.3,0.8,1)  # Blau
        # groesse des Fenters festlegen
        #Window.size = (800, 480)
        #Window.fullscreen = True

if __name__=="__main__":
    Programm().run()