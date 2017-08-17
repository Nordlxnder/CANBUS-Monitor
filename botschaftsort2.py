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

class can_bot_lesen(threading.Thread):
    '''
    Quelle:

        https://docs.python.org/3/library/threading.html

        jede Botschschaft benötigt einen eignen Socket
        deshalb wird in jedem Thread die Schnittstelle neu eingebunden

    '''

    def __init__ (self,id,stop, speicher_nr):
        threading.Thread.__init__(self,name=id)
        #threading.Thread.__init__(self,name="test")
        self.id = id
        self.stop=stop
        self.speicher_nr=speicher_nr

    def run(self):

        can_interface = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        # Name der Schnittstelle
        interface = "can0"
        can_interface.bind((interface,))

        # Filter setzen
        filter_mask=0x7FF
        can_interface.setsockopt(socket.SOL_CAN_RAW,
        socket.CAN_RAW_FILTER,
        struct.pack("II",self.id,filter_mask))

        # CAN lesen
        global stop, can_messpkt
        stop=self.stop
        while (not stop):
            can_messpkt[self.speicher_nr]=can_interface.recv(16)

class can_lesen():

    def start(self,redu_botschaften):

        # Vektor für die uebergaber der Werte von den Threads Canlesen
        # an Canwerte anzeigen
        global can_messpkt
        can_messpkt=[]
        for x in range (4):
            can_messpkt.append(9999)
        self.redu_botschaften=redu_botschaften
        stop= False

        for i in range(0 ,len(self.redu_botschaften)):
            #stop= False
            #[100, 0, [2, 0.00152587890625, 0.0, 1], [4, 0.00152587890625, 0.0, 4]]
            #[Botschaft_ID, Speicher_nr , [Startbit, Faktor, Offset, Anzeigennummer]]

            botschschafts_id=self.redu_botschaften[i][0]
            speicher_nr=self.redu_botschaften[i][1]
            current=can_bot_lesen(botschschafts_id, stop , speicher_nr)
            # der Deamon wird aktiviert damit beim Programm
            # schliessen alle threads beendet werden
            current.daemon = True
            current.start()


class can_werte_anzeigen(threading.Thread):
    '''
    Quelle:

        https://docs.python.org/3/library/threading.html
    '''

    def __init__ (self,redu_botschaften,stop):
        threading.Thread.__init__(self,name="Anzeige")
        #threading.Thread.__init__(self,name="test")
        self.redu_botschaften = redu_botschaften
        self.stop=stop


    def run(self):
        global stop, can_messpkt
        stop=self.stop
        FMT = "<IB3x2s2s2s2s"
        while (not stop):
            # Refresrate
            time.sleep(0.1)
            # Messpunkte lesen
            # Abfragen der Speicherzelle
            n=0

            while n <len(self.redu_botschaften):
                speicher=can_messpkt[self.redu_botschaften[n][1]]
                if str(speicher)==str(9999) :
                    #print("Es wird keine Botschaft gesendet")
                    pass
                else:
                    # Aufloesen der Daten in der Speicherzelle nach Werten und ID
                    can_id, length, w1, w2, w3, w4 = struct.unpack(FMT, speicher)
                    daten=[can_id,w1, w2, w3, w4]

                    # Anzahl der Werte in der Botschaft
                    anzahl=len(self.redu_botschaften[n])-1
                    #print("Redu:\t",self.redu_botschaften[n])
                    #print("Anzahl:\t",anzahl)
                    # i=2 weil ID und die Speicherzelle abgezogen werden
                    i=2
                    # Umrechnen der CANwerte in eine Dezimalzahl fuer die Anzeige
                    while i <= anzahl:
                        # hex_wert=startbit
                        hex_wert=self.redu_botschaften[n][i][0]
                        faktor=self.redu_botschaften[n][i][1]
                        offset=self.redu_botschaften[n][i][2]
                        anzeige_nr=self.redu_botschaften[n][i][3]
                        var=str(binascii.hexlify(daten[hex_wert]), 'ascii')

                        # Numerischen Wert ermittel aus den Integer Wert + Faktor + Offset
                        wert= int(var,16)*faktor+offset
                        # kuerzen auf 2 nachkommastellen
                        wert_kurz='{:.2f}'.format(wert)

                        #a = eval("root.ids.s" + str(seite) + ".ids.a" + str(i))
                        if self.fenster_id=="s1":
                            a = eval("self.Bildschirmverwalter.ids."+str(self.fenster_id)+".ids.a" + str(anzeige_nr))
                        if self.fenster_id=="s2":
                            a = eval("self.Bildschirmverwalter.ids."+str(self.fenster_id)+".ids.a" + str(anzeige_nr-4))
                        if self.fenster_id=="s100":
                            a = eval("self.Bildschirmverwalter.ids."+str(self.fenster_id) )
                        a.ids.w1.text=wert_kurz

                        i +=1
                n +=1
        pass
class can_anzeigen():

    def start(self,redu_botschaften,Bildschirmverwalter,fenster_id):
        # Aufrufe des Threads fuer die Anzeige
        stop= False
        thread_anzeigen=can_werte_anzeigen(redu_botschaften, stop)
        thread_anzeigen.daemon = True
        thread_anzeigen.start()
        thread_anzeigen.Bildschirmverwalter=Bildschirmverwalter
        thread_anzeigen.fenster_id=fenster_id

class Stop_CAN_Threads():
    def stop(self):
        #alle_threads=threading.enumerate()
        #print ("alle Threads:\t",alle_threads)

        global stop
        stop= True
        # stoppt alle Threads wenn auf die Gesamtanzeige zurueck gegangen wird
        # es geht erst weiter wenn die threads gestoppt sind
        #aktiv_threads=threading.active_count()
        #print("Threads vor dem Stop:\t",threading.enumerate())
        while aktiv_threads >7:
            aktiv_threads=threading.active_count()
            #print(aktiv_threads)
        #print("Threads nach dem Stopp:\t",threading.enumerate())
