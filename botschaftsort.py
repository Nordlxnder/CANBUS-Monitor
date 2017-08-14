#!/usr/bin/python python
# -*- coding: utf-8 -*-
"""
Beschreibung

Es wird eine List aus 4 Elementen mit folgender konfiguration übergeben
konfiguration=[Id, Startbit, Faktor, Offset, Anzeige nr.,Anzeigeobjekt]

Die Liste wird dann nach den IDs sortiert und werde alle IDs ermittelt für
einen Filter.

"""


import socket
import struct
import threading ,sys
import binascii
import time

class CANBUS():

    def can0_schnittstelle_aktivieren(self):
        '''
            Bindet den Socket an die can0 Schnittstelle
            Das Can Interface wird global gesetzt damit
            es spaeter beim aktivieren  der threads fuer
            die einzelnen Botschaften genutzt werden kann
        '''

        global can_interface
        can_interface = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        # Name der Schnittstelle
        interface = "can0"
        can_interface.bind((interface,))
        #print("Can0 Schnittstelle ist aktiviert")

    def botschaften_sortieren(self,canbus_konfiguration):
        '''
            Funtion:

                + sortieren nach Botschafts-IDs
                + Ermitteln von Werten mit der gleichen Botschaftens-ID
                + Erstellen eines Vektor sortiert nach den ID und allen
                  zugehörigen Werten zur jeder einzelnen ID
                  (z.B. ID 100 Wert 2 und wert 3, ID 101 Wert1 und Wert4)

        '''

        # hier wird der Wert definiert nach dem sortiert wird
        #  ID    Startbit  Faktor
        #   0     1         2
        # [100], [1]],

        # sortiert nach der Botschafts ID
        def sortieren(bot):
            # Die letzte Zahl im Vektor is die Anzeige z.B. 8
            #[102, 4, 0.00152587890625, 0.0, 8]
            return bot[0]
        bot_sortiert = sorted(canbus_konfiguration, key=sortieren)


        # Ermitteln von Werten mit der gleichen Botschaftens-ID
        redu_botschaften = []
        s = 0
        alter_wert = 0  # fuer den Vergleich
        index = 0  # Wert für die Anzahl der Werte in einer Botschaft max.4
        #  speicherzelle 0 1 ,2 oder 3 jeder Botschaft in der Variable can_messpkt (typ Liste)
        save_pkt = -1
        # Zaehlen der doppelten Werte
        while s <= (3):
            # vergleich zwischen aktuellem Wert und dem Vorgaenger
            if bot_sortiert[s][0] == alter_wert:
                # vector besteht aus der Botschafts ID  und dem Index. In diesem Zweig
                # wird der Index hoch gezaehlt wenn der Wert sich wiederholt
                # max 4 sind erlaubt . Index geht von 0-3 fuer 4
                index += 1
                vector.append([bot_sortiert[s][1],
                               bot_sortiert[s][2], bot_sortiert[s][3], bot_sortiert[s][4]])
            else:
                alter_wert = bot_sortiert[s][0]
                # index zurücksetzen
                index = 0
                save_pkt += 1
                vector = [bot_sortiert[s][0], save_pkt, [bot_sortiert[s][1],
                                                         bot_sortiert[s][2],
                                                         bot_sortiert[s][3],
                                                         bot_sortiert[s][4]]]
                redu_botschaften.append(vector)
            s += 1
        # Es entsteht ein Vektor
        # [Botschaft_ID, Speicher_nr , [Startbit, Faktor, Offset, Anzeigennummer] ]
        # z.B:
        # [100, 0, [2, 0.00152587890625, 0.0, 1], [4, 0.00152587890625, 0.0, 4]]
        #print("Reduzierte Botschaften:\t",redu_botschaften)
        return redu_botschaften


def canbus_Botschaft_lesen(id):
        # CAN lesen
        global stop
        stop=False
        while (not stop):
            messpunkt=can_interface.recv(16)
            print("Messpunkt:\t",id,messpunkt)
        print("stopp")


class can_bot_lesen(threading.Thread):
    '''
    Quelle:

        https://docs.python.org/3/library/threading.html
    '''

    def __init__ (self,id,stop):
        threading.Thread.__init__(self,name=id)
        self.id = id
        self.stop=stop
    def run(self):
        # Filter setzen
        filter_mask=0x7FF
        can_interface.setsockopt(socket.SOL_CAN_RAW,
            socket.CAN_RAW_FILTER,
            struct.pack("II",self.id,filter_mask))


        # CAN lesen
        global stop
        stop=self.stop
        while (not stop):
            messpunkt=can_interface.recv(16)
            print("Messpunkt:\t",self.id,messpunkt)

        print("stopp")

class stop_can_lesen():
    def stop(self):
        global stop
        stop= True
        print ("Stopgedrueckt:\t",stop)
#