#!/usr/bin/python python
# -*- coding: utf-8 -*-

class CANBUS_Konfiguration():

    def Datei_einlesen(self,dateiname):
        Datei=open(dateiname,'r')
        inhalt_der_datei=Datei.readlines()
        # Kopfdaten gehen bis Zeile 2
        i = 3                       # Startzeile
        bis_zeile=10
        botschaften=[]                 # Botschaftskonfiguration
        while i <= (bis_zeile):
            botschaften.append(inhalt_der_datei[i])
            i +=1
        Datei.close

        # reduzierung des Datensatzes , entfernen von sonderzeichen  und so weiter
        i=0
        konf=[]
        while i <= (bis_zeile-3):
            A=botschaften[i].split("|")
            #['100 ', ' 1  ', ' pmax1 ', ' - ', ' 0.00152587890625 ',
            #                    ' 0  ', ' 0 ', ' 100 ', ' bar ', '\n']
            konf.append([int(A[0]), int(A[1]), A[2].replace(" ",""), float(A[4]),
            float(A[5]), float(A[6]), float(A[7]), A[8].replace(" ","")])
            i +=1

        '''
        Bot_id = int(A[0])
        Startbit = int(A[1])
        Name = A[2].replace(" ","")
        Faktor = float(A[4])
        Offset = float(A[5])
        Min = float(A[6])
        Max = float(A[7])
        Einheit = A[8].replace(" ","")
        B=len(A)
        '''

        # ID Startbit Nummer der zugehörigen Anzeige
        # Nr. = Startbit  1=0-15 2=16-31 3=32-47 4=48-63

        n=1       # n=Nummer der Anzeige Startwert
        id_nr=[]
        name_einheit=[]
        while n <=(i):
            # der erste Wert im Vektor ist immer die Nummer der Anzeige
            # das Objekt Anzeige ist in w (w[n])  als Objekt

            id_nr.append([
                          konf[n-1][0],
                          konf[n-1][1],
                            konf[0][3],
                            konf[0][4],
                          n
                         ])
            name_einheit.append([konf[n-1][2],konf[n-1][7],n])
            n +=1
        '''
        self.id_nr  beinhaltet [Id Startbit Faktor Offset Nummer der Anzeige]
                               [100, 1,  0.00152587890625, 0.0, 1]
        self.name_einheit  beinhaltet Name, Einheit, Nummer der Anzeige
                                    ['pmax1', 'bar', 1]
        '''

        self.id_nr=id_nr
        self.name_einheit=name_einheit

        return (self)

    def uebersicht_can_botschaften(self,Bildschirmverwalter,canbus_konfiguration):
        '''Übersicht im Konfigurationsfenster der einzelnen CAN Botschaften'''
        # Überschrift Botschaft Startbit Faktor Offset
        Bildschirmverwalter.ids.s101.ids.a1.text = str("                    Botschaft   Startbit   Faktor      Offset")
        k = 1
        while k <= 8:
            k_bot = eval("Bildschirmverwalter.ids.s101.ids.a" + str(k + 1))
            bot = str(canbus_konfiguration.id_nr[k - 1][0])
            sb = str(canbus_konfiguration.id_nr[k - 1][1])
            fkt = '{:.8}'.format(str(canbus_konfiguration.id_nr[k - 1][2]))
            ofs = str(canbus_konfiguration.id_nr[k - 1][3])
            k_bot.text = "Anzeige  {}".format(
                k) + "     " + bot + "              " + sb + "       " + fkt + "      " + ofs
            k += 1