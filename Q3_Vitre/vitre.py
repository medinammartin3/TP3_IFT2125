# Martin Medina (20235219)
# Étienne Mitchell-Bouchard (20243430)
import sys


# N : Force maximale
# k : Nombre de fenêtres disponibles
# Valeur de retour : le nombre minimal de tests qu'il faut faire
#                   en pire cas pour déterminer le seuil de solidité 
#                   d'une fenêtre
# Doit retourner la réponse comme un int.

def vitre(N, k):
    # i -> nombres de niveaux de forces à tester (1 <= i <= N)
    # j -> nombre de vitres restantes (1 <= j <= k)
    # tab[i][j] = le nombre minimal de tests qu’il faudrait faire en pire cas pour trouver s avec j vitres

    # Initialisation du tableau
    tab = [[float("inf") for _ in range(N)] for _ in range(k)]

    # Conditions d'initialisation
    for i in range(k):
        tab[i][0] = 0  # On a besoin de 0 tests si il y a 1 seul niveau de force pour tester (car 1 <= s <= N)
    for i in range(N):
        tab[0][i] = i  # On a besoin de i tests si il y a i niveaux de forces pour tester et 1 seule vitre

    # Cas de base
    if k == 0 or N == 0:
        return 0

    # Remplissage du tableau
    for i in range(1, k):
        for j in range(1, N):
            # On trouve le nombre de tests à réaliser pour chaque résistance possible
            for s in range(1, j+1):
                nb_tests = 1 + max(tab[i - 1][s - 1], tab[i][j - s]) # Formule de récurrence
                # À la fin on veut le pire des cas (nombre plus grand de tests à réaliser)
                if nb_tests < tab[i][j]:
                    tab[i][j] = nb_tests

    return tab[k-1][N-1]


# Fonction main, vous ne devriez pas avoir à modifier
def main(args):
    N = int(args[0])
    k = int(args[1])

    answer = vitre(N, k)
    print(answer)


if __name__ == '__main__':
    main(sys.argv[1:])
