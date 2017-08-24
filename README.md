Funktion:

	Onlineanzeige von CAN Werten
	Es können 8 Canwerte a 4 auf einer Seite angezeigt werden
	jeder Wert kann durch antippen der Einzelanzeige auf volle 
	Bildschirmgröße gebracht werden

Voraussetzung:

	can0 Schnittstelle sollte vorhanden sein 
	-----------------------------------------------

	Der Benutzer sollte den Befehl "ip" ohne Rootrechte ausführen können
	Dies kann man mit dem Eintrag in der /etc/sudoers erreichen
	##
	## User privilege specification
	##
	root ALL=(ALL) ALL
	username ALL=(ALL) ALL
	usersname ALL=(ALL) NOPASSWD: /sbin/ip

Software:

	Archlinux
	Python 3
	Kivy 
	sudo

Hardware:

	Raspberry Pi3 mit Can-Erweiterung
	Banana Pi mit Can-Erweiterung
	Touch Display 800x480 (andere sollten auch möglich sein;)


Beispiel: 
	canbus.log passt zur canbus.conf
	
	mit can-utils kann die Logdatei auf einem 2ten Raspi 
	abgespielt werden zum Testen
	
	Canschnittstelle aktivieren mit:
		sudo ip link set can0 type can bitrate 500000
		sudo ifconfig can0 up
		sudo modprobe can-raw
		ip -details link show can0
	
	Im Verzeichnis der Logdatei dann
	
        	canplayer -l i -I canbus.log	
	
