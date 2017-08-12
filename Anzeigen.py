class Anzeige_Name_Einheit_aktualisieren():

    def __init__(self,liste_anzeigen,name_einheit,*args,**kwargs):

        '''
         Zuweisung der Namen und Einheit für Anzeige 1 bis 8
         liste_anzeigen enthält die Anzeige element von 1 bis 8
         name_einheit enthält die Elemente Name und einheit von 1 bis x
         die aus der DBC Datei gelesen wurden
        '''

        bis= len(name_einheit)-1
        i=0
        while i <= bis:
                liste_anzeigen[i].ids.n1.text=name_einheit[i][0]
                liste_anzeigen[i].ids.e1.text=" " +name_einheit[i][1]
                i +=1
        pass

class Liste_der_Anzeigen():
    '''
    Es wird eine Liste mit 8 Anzeigeobjkten erstellt

    '''
    def liste_erstellen(self,root,*args,**kwargs):
        i=1
        seite=1
        global liste_anzeigen
        liste_anzeigen=[]
        while seite <= 2:
            # es gibt 4 Anzeigen auf einer Seite
            bis = (seite *4)
            #print("Seite",seite)
            while i <= bis:
                # mit eval wird der String wieder als
                # Objekt behandelt <__main__.Anzeige1 object ...
                a=eval("root.ids.s"+str(seite) +".ids.a"+ str(i))
                liste_anzeigen += [a]
                i +=1
            seite +=1
        return liste_anzeigen
    pass