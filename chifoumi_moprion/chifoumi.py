from random import *
from time import sleep 

choix_joueur = input('Pierre (p), Feuille (f) ou Ciseaux (c) ? \n')
choix_pc = randint(1, 3)

match choix_pc:
    case 1:
        choix_pc = "Pierre"
    case 2:
        choix_pc = "Feuille"
    case 3:
        choix_pc = "Ciseaux"

match choix_joueur:
    case "p":
        print("Vous avez choisi Pierre.")
        sleep(1)
        print("L'ordinateur a choisi", choix_pc)
    case "f":
        print("Vous avez choisi Feuille.")
        sleep(1)
        print("L'ordinateur a choisi", choix_pc)
    case "c":
        print("Vous avez choisi Ciseaux.")
        sleep(1)
        print("L'ordinateur a choisi", choix_pc)
    case "G":
        print("Vous avez choisi Guardia.")
        sleep(1)
        print("Code secret - Vous avez gagné") 

if (choix_joueur == 'p' and choix_pc == "Ciseaux") or (choix_joueur == 'f' and choix_pc == "Pierre") or (choix_joueur == 'c' and choix_pc == "Feuille"):
    print("Le joueur gagne !")
elif (choix_joueur == 'p' and choix_pc == "Feuille") or (choix_joueur == 'f' and choix_pc == "Ciseaux") or (choix_joueur == 'c' and choix_pc == "Pierre"):
    print("L'ordinateur gagne !")
elif (choix_joueur == 'p' and choix_pc == "Pierre") or (choix_joueur == 'f' and choix_pc == "Feuille") or (choix_joueur == 'c' and choix_pc == "Ciseaux"):
    print("Egalité !")
 