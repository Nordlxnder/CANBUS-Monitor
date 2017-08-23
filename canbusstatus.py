
import subprocess

'''
    Funktionen:

    can0_check prüft ob einen CAN Karte vorhanden ist und gibt die Meldung im Hauptfensteraus
'''

def can0_check(Bildschirmverwalter):
    ''' prüft ob can0 auf dem PC existiert'''

    try:
        ausgabe = subprocess.check_output('ip -details link show can0', shell=True)
        subprocess.call("sudo ip link set dev can0 down", shell=True)
        subprocess.call("sudo ip link set can0 type can bitrate 500000", shell=True)
        subprocess.call("sudo ip link set dev can0 up", shell=True)
        return True
    except:
        keine_can0_karte(Bildschirmverwalter)
        #meldung="\nEs gibt keine CAN Karte can0 auf dem PC"
        #Bildschirmverwalter.ids.s0.ids.l1.text = meldung
        return False

def can_read_baudrate():
    '''
    Liesst mit Hilfe eines Shell Befehls den Status der CAN Karte
    '''

    ausgabe = subprocess.check_output('ip -details link show can0', shell=True)
    # Auslesen der baudrate
    a = str(ausgabe).split("\\t  ", 1)
    status = a[0].split()[6]
    # fq_codel=fair queuing controlled delay
    if status == "fq_codel":
        baud = a[1].split()[1]
        c = len(baud)
        # der Wert hat 7 Zeichen bei 1000 KHz  und 6 beim Rest
        if c == 7:
            bis = 4
        else:
            bis = 3
        baudrate = str(baud[0:bis]) + " kHz"
        status = a[0].split()[21].split('-')[1]

    else:
        # Die CAN Karte ist noch nicht konfiguriert
        baudrate = "0 kHz"
        status = "Offline"

    return baudrate, status

def can_set_baudrate(baudrate):
    '''
    Setzt mit Hilfe eines Shellbefehls die Baudrate 1000, 500 oder 250 kHz
    '''
    subprocess.call("sudo ip link set dev can0 down", shell=True)
    if baudrate == "1000 kHz":
        subprocess.call("sudo ip link set can0 type can bitrate 1000000", shell=True)
    if baudrate == "500 kHz":
        subprocess.call("sudo ip link set can0 type can bitrate 500000", shell=True)
    if baudrate == "250 kHz":
        subprocess.call("sudo ip link set can0 type can bitrate 250000", shell=True)
    subprocess.call("sudo ip link set dev can0 up", shell=True)
    pass

def status_ausgabe(Bildschirmverwalter):
    status = can_read_baudrate()
    #label_hauptbildschrim.text="Eine Cankarte ist vorhanden"
    if status[1] == "PASSIVE":
        fehlermeldung="\nDie CAN Karte ist " + status[1] + \
        "\nbitte die Abschlusswiderstände prüfen!!!"

        # Hauptfenster
        Bildschirmverwalter.ids.s0.ids.l1.text=fehlermeldung
        # Fenster Baudrate setzen
        Bildschirmverwalter.ids.s102.ids.l1.text=fehlermeldung
        Bildschirmverwalter.ids.s102.ids.l1.color= 1,0,1,1     # Farbe
        Bildschirmverwalter.ids.s102.ids.l1.font_size= 30      # Schriftgroesse
    else:
        meldung="\nDie CAN Karte ist " + status[1] + "\nBaudrate: " + status[0]
        Bildschirmverwalter.ids.s0.ids.l1.text=meldung
        Bildschirmverwalter.ids.s102.ids.l1.text=meldung
        Bildschirmverwalter.ids.s102.ids.l1.color= 1,1,1,1
        Bildschirmverwalter.ids.s102.ids.l1.font_size= 20
    pass

def keine_can0_karte(Bildschirmverwalter):
    meldung = "\nEs gibt keine CAN Karte can0 auf dem PC"
    Bildschirmverwalter.ids.s0.ids.l1.text = meldung
    Bildschirmverwalter.ids.s102.ids.l1.text = meldung
    Bildschirmverwalter.ids.s102.ids.l1.color = 1, 0, 1, 1  # Farbe
    Bildschirmverwalter.ids.s102.ids.l1.font_size = 30  # Schriftgroesse

def can0_timeout():
    Bildschirmverwalter.ids.s1.ids.a1.text="timeout"
    pass
