from lib.Ebene import Ebene

def initialisePlayground(playgroundFile):
    print()


# main Methode
# ruft A stern Methode mit den Beispieldaten auf
def main():

    # initialise playground
    file = open("spielfeld_2.csv", "r")
    item = open("S22.txt", "r")
    ebene = Ebene(file, item)

    # hard coded version
    ebene.felder[5][2].marker = "Medaillon"
    ebene.felder[10][15].marker = "Medaillon"
    ebene.felder[7][15].marker = "Krone"
    item.close()
    file.close()


# main methode aufrufen wenn datei ausgeführt wird
if __name__ == '__main__':
    main()