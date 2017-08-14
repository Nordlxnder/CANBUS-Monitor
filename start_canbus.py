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
        print("Can0 Schnittstelle ist aktiviert")

    def botschaften_sortieren(self,canbus_konfiguration, fenster):
        '''
            Funtion:

                + sortieren nach Botschafts-IDs
                + Ermitteln von Werten mit der gleichen Botschaftens-ID
                + Erstellen eines Vektor sortiert nach den ID und allen
                  zugehörigen Werten zur jeder einzelnen ID
                  (z.B. ID 100 Wert 2 und wert 3, ID 101 Wert1 und Wert4)

        '''
        global seite
        seite=fenster
        #print("Seite:\t",seite)
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
        # [Botschaft_ID, nr , [Startbit, Faktor, Offset, Anzeigennummer] ]
        # z.B:
        # [100, 0, [2, 0.00152587890625, 0.0, 1], [4, 0.00152587890625, 0.0, 4]]
        #print("Reduzierte Botschaften:\t",redu_botschaften)

        pass
        self.Start_can_filter(redu_botschaften)

    def Start_can_filter(self,redu_botschaften):
        '''
         Anzahl der Botschafts IDs , -1 weil 0-2
         es wird fuer jede Botschaft ein Filter gesetzt und gestartet
         in Abhaenigkeit von der Anzahl der unteschiedlichen Boschaften
         wird die Anzahl der Sockets gestartet.

         Für jede Botschaft wird nur ein Socket gestartet. Mit Hilfe eines Socket kann der CAN BUS gelesen werden .
         Zusätzlich bietet er die Möglichkeit einen Filter zusetzen für eine Botschaft dies reuziert die Last bei
         der Weiterverarbeitung der Daten.

         Für jede Botschaft wird ein Socket gestartet. Damit nur eine Botschaft
         gelesen wird, wird der Socket mit einem Filter für diese
         Botschaft versehen.
        '''

        bot_anzahl = len(redu_botschaften) - 1
        #print("Anzahl Botschaften: \t",bot_anzahl)
        # Speicherzelle
        # can_messpkt=[0,1,2,3] bei 4 Botschaften
        global can_messpkt, stop_lesen
        can_messpkt = []
        stop_lesen = []
        for x in range(bot_anzahl + 1):
            can_messpkt.append(x)
            stop_lesen.append(x)
        print("CAN Speicher:\t",can_messpkt)
        f = 0
        while f <= (bot_anzahl):
            '''
            Jede Botschaft muss eine eigene Instance bekommen , sonst wird sie
            immer überschrieben und nur die letzte Botschaft abgefragt.
            Deshalb wird die Classe CANBUS_Botschaften eingeführt
            im nächsten Schritt
            '''

            # Uebergabe der der Filtereinstellungen fuer jede Botschaft
            CANBUS_Botschaften().start_canbus(redu_botschaften[f])
            f += 1

            # immer wenn eine Botschaft kommt wird der Wert ausgelesen
            # Endlosschleife
            # can_pkt = self.can_interface.recv(16)
        # Übergabe des Vektors Filter_IDs an die Klasse Anzeigen am Ende des Programms
        time.sleep(1.5)
        Anzeigen(redu_botschaften, bot_anzahl)

class CANBUS_Botschaften():
    '''
    Funktionen
    ==========
    + Filter setzen
    + Canbus lesen
    + Wert schreiben in die Speicherzelle can_messpkt [0,1,...]

    can_filter_id = ID, Speicherzelle [Startbit, Faktor, Offset, Anzeigeobjekt]
    [101, 1 [2, 0.00152587890625, 0.0, <Anzeige2 object at 0xb0478618>], [3,...]
    die Id wird für die Filterung verwendet
    '''

    def start_canbus(self,can_filter_id):
        '''
            Abschnitt Filter setzen

            Beispiel fuer Filtersetzen

                  id    0x64 Botschaft
                mask    0x7FF

                  id = 0b000001100100
                mask = 0b011111111111

        can_filter_id
        [100, 0, [2, 0.00152587890625, 0.0, 1], [4, 0.00152587890625, 0.0, 4]]

        '''
        self.can_filter_id=can_filter_id[0]
        self.anzeige_startbit=can_filter_id
        self.speicherzelle_nr=can_filter_id[1]
        print("Botschaftsid:\t",self.can_filter_id)
        filter_mask=0x7FF
        global can_interface
        #can_interface.setsockopt(socket.SOL_CAN_RAW, socket.CAN_RAW_FILTER,struct.pack("II", filter_id, mask))
        can_interface.setsockopt(socket.SOL_CAN_RAW, socket.CAN_RAW_FILTER,struct.pack("II", self.can_filter_id,filter_mask))

        '''
            CANbus lesen Start des Abfrageprozesses als parallelen Prozess
        '''
        #print("Speicherzelle1:\t",self.speicherzelle_nr)
        global stop_lesen
        stop_lesen[self.speicherzelle_nr]=threading.Event()
        can_lesen = threading.Thread(target=self.__canbus_Botschaft_lesen__, args=(1, stop_lesen[self.speicherzelle_nr]))
        can_lesen.daemon = True
        can_lesen.start()

    def stop_can_lesen(self):
        #print ("Stoplesen: \t",stop_lesen)
        # Stoppt den Thread f�r die Anzeige
        stop_anzeige.set()
        # Stoppt die Threads f�r die CAN Botschaften
        s=0
        while s<len(stop_lesen):
            stop_lesen[s].set()
            s +=1
        #print ("Stoplesen: \t",stop_lesen)
        return True
    pass

    def __canbus_Botschaft_lesen__(self, arg1, stop_lesen):
        '''

        '''
        global can_messpkt
        #print("Speicherzelle2:\t",self.speicherzelle_nr)
        # .is_set() fragt das Flag ab ob das Ereignis gesetzt ist
        while (not stop_lesen.is_set()):
            # immer wenn eine Botschaft kommt wird der Wert ausgelesen
            # Endlosschleife
            #print("Speicherzelle3:\t",can_messpkt[self.speicherzelle_nr])
            #can_messpkt[0]= self.can_interface.recv(16)
            #can_messpkt[self.speicherzelle_nr]= self.can_interface.recv(16)
            can_messpkt[self.speicherzelle_nr]= can_interface.recv(16)

class Anzeigen():
    '''
    Funktionen
    ==========

    + vorgabe der Auffrischrate 2 Hz
    + Werte in der CAN_Botschaft ermitteln
    + Anzeige aktualisieren

    filter_ids = ID, Speicherzelle [Startbit, Faktor, Offset, Anzeigeobjekt]
    '''

    def __init__(self,filter_ids,bot_anzahl,*args, **kwargs):
        self.vec=filter_ids
        self.bot_anzahl=bot_anzahl
        # �bergabe Speicherzelle startbit Anzeigeobjekt
        # Start der Aktualisierung der Anzeige als eigner Thread  mit 2 Hz
        global stop_anzeige
        stop_anzeige=threading.Event()
        anzeigen_aktualisieren = threading.Thread(target=self.anzeige_auffrischen, args=(1,stop_anzeige))
        anzeigen_aktualisieren.daemon = True
        anzeigen_aktualisieren.start()
        #print(self.vec)


    def anzeige_auffrischen(self,arg2,stop_anzeige):
        global can_messpkt
        # 4 Werte a 16 bit Format
        FMT = "<IB3x2s2s2s2s"
        print("Messpunktvektor:\t",can_messpkt)
        while (not stop_anzeige.is_set()):
            # Refresrate
            time.sleep(0.5)
            # Schliefe Speicherzelle
            n=0
            #print("vec L�nge:\t",len(self.vec[n][1]))
            while n <= (self.bot_anzahl):
                # Abfragen der Speicherzelle
                speicher=can_messpkt[self.vec[n][1]]
                # check ob schon ein Wert in der Zelle ist
                if len(str(speicher))==1 :
                    #print("Es wird keine Botschaft gesendet")
                    pass
                else:
                    # Botschaft �bersetzen
                    can_id, length, w1, w2, w3, w4 = struct.unpack(FMT, speicher)
                    daten=[can_id,w1, w2, w3, w4]
                    anzahl=len(self.vec[n])-1
                    # i=2 weil ID und die Speicherzelle abgezogen werden
                    i=2
                    while i <= anzahl:
                        # hex_wert=startbit
                        hex_wert=self.vec[n][i][0]
                        faktor=self.vec[n][i][1]
                        offset=self.vec[n][i][2]
                        var=str(binascii.hexlify(daten[hex_wert]), 'ascii')
                        # Numerischen Wert ermittel aus den Integer Wert + Faktor + Offset
                        wert= int(var,16)*faktor+offset
                        # kuerzen auf 2 nachkommastellen
                        wert_kurz='{:.2f}'.format(wert)
                        # Anzeige aktualisieren
                        #self.vec[n][i][3].ids.w1.text=wert_kurz
                        canwertanzeige= eval( "seite.ids.a" + str(i) + ".ids.w1")
                        canwertanzeige.text=wert_kurz
                        i +=1
                #testanzeige= eval("root.ids.s" + str(seite) + ".ids.a" + str(i))
                #canwertanzeige= eval( "seite.ids.a" + str(1) + ".ids.w1.text")
                #print("Seite mit CAN Wert: \t",testanzeige)
                n +=1
