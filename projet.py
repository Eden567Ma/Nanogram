
import matplotlib.pyplot as plt
import time


def t1(j, l, s, est_noire):
    
    """
    Détermine T(j, l) pour une séquence donnée s.
    
    Parameters
    ----------
    j : int
        Index actuel de la colonne
    l : int
        Index actuel du bloc
    s : List[int]
        Séquence des longueurs de blocs
    est_noire: bool
        Booléen indiquant si la cellule (i, j) est coloriée en noir

    Returns
    -------
    bool
        True si T(j, l) est vrai, False sinon
    """

    # Cas 1 : Pas de bloc (l = 0)
    if l == 0:
        return True

    # Cas 2a : j < s_l - 1
    if j < s[l - 1] - 1:
        return False

    # Cas 2b : j = s_l - 1
    if j == s[l - 1] - 1:
        return l == 1

    # Cas 2c : j > s_l - 1
    else:
        return t1(j - s[l - 1] - 1, l - 1, s, est_noire) and (est_noire or (j > 0 and t(j - 1, l, s, est_noire)))
    
    
def T1(j, l, s):
    
    """
    Réalise le premier appel de la fonction t1
    
    Parameters
    ----------
    j : int
        Index actuel de la colonne
    l : int
        Index actuel du bloc
    s : List[int]
        Séquence des longueurs de blocs

    Returns
    -------
    bool
        True si T(j, l) est vrai, False sinon
    """

    return t1(j, l, s, True)



def T2(j, l, s, ligne):
    
    """
    Calcule T(j, l) pour une séquence donnée s en tenant compte des cases déjà coloriées.

    Parameters
    ----------
    j : int
        Index actuel de la colonne
    l : int
        Index actuel du bloc
    s : List[int]
        Séquence des longueurs de blocs
    ligne: List[int]
        Liste correspondant à une ligne de la grille (0 : non coloriée, 1 : coloriée en blanc, 2 : coloriée en noir)

    Returns
    -------
    bool
        True si T(j, l) est vrai, False sinon
    """
    
    # Vérification si les cases respectent bien notre modèle (0, 1 ou 2 uniquement)
    if ligne[j] != 0 and ligne[j] != 1 and ligne[j] != 2:
        return False
    
    # Cas 1 : Pas de bloc (l = 0)
    if l == 0:
                
        for i in range(j+1) : 
            
            # Si on rencontre une case coloriée en noir
            if ligne[i] == 2: 
                return False
        
        return True

    # Cas 2a : j < s_l - 1
    if j < s[l - 1] - 1:
        return False

    # Cas 2b : j = s_l - 1
    if j == s[l - 1] - 1:

        if l != 1:
            return False
        
        for i in range(j+1) : 
            
            # Si on rencontre une case coloriée en blanc
            if ligne[i] == 1:
                return False
               
        
        return True
        
    # Cas 2c : j > s_l - 1
    else:
        
        # Si la case d'indice j est coloriée en blanc
        if ligne[j] == 1:
            return T2(j-1, l, s, ligne)
        
        # Si la case d'indice j est coloriée en noir
        if ligne[j] == 2:
            
            if ligne[j-s[l-1]] == 2:
                return False
            
            for i in range(j-s[l-1]+1, j):
                if ligne[i] == 1:
                    return False
            
            return T2(j-s[l-1]-1, l-1, s, ligne)
        
        # Hypothèse selon laquelle la case suivante est coloriée en blanc
        hyp_blanc = ligne[:j] + [1]
        ligne_blanc = T2(j, l, s, hyp_blanc)   

        # Hypothèse selon laquelle la case suivante est coloriée en noir
        hyp_noir = ligne[:j] + [2]
        ligne_noir = T2(j, l, s, hyp_noir)
        
        if not(ligne_blanc or ligne_noir):
            return False
        
        return True


def lire_fichier(fichier):
    
    """
    S'occupe de l'ouverture et de la lecture d'un fichier
    
    Parameters
    ----------
    fichier : str
        Nom du fichier
    """
    
    lignes = []
    colonnes = []
    
    deja_vu = False
    
    
    with open(fichier, 'r') as f:
            
        lines = f.readlines()
            
        for line in lines:
                
            l = line.replace("\n", "")
            
            if l == "#":
                deja_vu = True
                
            elif not(deja_vu):
                l = [int(i) for i in l.split()]
                lignes.append(l)
            else:
                l = [int(i) for i in l.split()]
                colonnes.append(l)
            
    f.close()

    return lignes, colonnes


def color_rec(j, l, s, ligne):
    
    """
    Colore une ligne de manière récursive

    Parameters
    ----------
    j : int
        Index actuel de la colonne
    l : int
        Index actuel du bloc
    s : List[int]
        Séquence des longueurs de blocs
    ligne: List[int]
        Liste correspondant à une ligne de la grille (0 : non coloriée, 1 : coloriée en blanc, 2 : coloriée en noir)
    """

    if ligne[j] != 0 and ligne[j] != 1 and ligne[j] != 2:
        return False
    
    # Cas 1 : Pas de bloc (l = 0)
    if l == 0:
                
        for i in range(j+1) : 
            
            # Si on rencontre une case coloriée en noir
            if ligne[i] == 2: 
                return False
            
        for i in range(j+1) : 

            # Si on rencontre une case vide, on la colore en blanc
            if ligne[i] == 0: 
                ligne[i] = 1
        
        return True

    # Cas 2a : j < s_l - 1
    if j < s[l - 1] - 1:
        return False

    # Cas 2b : j = s_l - 1
    if j == s[l - 1] - 1:

        if l != 1:
            return False
        
        for i in range(j+1) : 
            
            # Si on rencontre une case coloriée en blanc
            if ligne[i] == 1:
                return False
        
        for i in range(j+1) : 

            # Si on rencontre une case vide, on la colore en noir
            if ligne[i] == 0: 
                ligne[i] = 2
               
        return True
        
    # Cas 2c : j > s_l - 1
    else:
        
        # Si la case d'indice j est coloriée en blanc
        if ligne[j] == 1:
            return color_rec(j-1, l, s, ligne)
        
        # Si la case d'indice j est coloriée en noir
        if ligne[j] == 2:
            
            if ligne[j-s[l-1]] == 2:
                return False
            
            for i in range(j-s[l-1]+1, j):
                if ligne[i] == 1:
                    return False
                
            if ligne[j - s[l-1]] == 0: 
                ligne[j - s[l-1]] = 1
            
            for i in range(j - s[l-1] + 1, j) : 
                
                # Si on rencontre une case vide, on la colore en noir
                if ligne[i] == 0:
                    ligne[i] = 2

            return color_rec(j-s[l-1]-1, l-1, s, ligne)
        
      
        hyp_blanc = ligne[:j] + [1]
        ligne_blanc = color_rec(j, l, s, hyp_blanc)   

        hyp_noir = ligne[:j] + [2]
        ligne_noir = color_rec(j, l, s, hyp_noir)
        
        if not(ligne_blanc or ligne_noir):
            return False
        elif not ligne_noir: 
            for i in range(j+1): 
                if ligne[i] != hyp_blanc[i]:
                    ligne[i] = hyp_blanc[i]
        elif not ligne_blanc: 
            for i in range(j+1): 
                if ligne[i] != hyp_noir[i]:
                    ligne[i] = hyp_noir[i]
        else : 
            for i in range(j): 
                if hyp_blanc[i] == hyp_noir[i] and ligne[i] != hyp_blanc[i]:
                    ligne[i] = hyp_blanc[i]
        
        return True

    
def color_lig(grille, ligne, fichier):
    
    """
    Colore une ligne

    Parameters
    ----------
    grille : List[List[int]]
        grille à colorier
    ligne : int
        indice de la ligne à traiter
    fichier : str
        Nom du fichier
    
    Returns
    -------
    bool
        si le coloriage est possible
    List[List[int]]
        grille coloriée
    set(int)
        colonnes de la liste coloriées
    """
    
    # Ensemble des colonnes ajoutées/modifiées
    nouveaux = set()
    
    lig = grille[ligne]
    lig2 = lig.copy()
    
    lignes, _ = lire_fichier(fichier)   
    s = lignes[ligne]
    
    # vérification si T(j,l) vrai
    if not(T2(len(lig)-1, len(s), s, lig)):
        return False, grille, nouveaux
    
    color_rec(len(lig)-1, len(s), s, lig)   
    
    grille[ligne] = lig
    nouveaux = {i for i in range(0, len(lig)) if lig[i] != lig2[i]}
    
    return (True, grille, nouveaux)


def color_col(grille, colonne, fichier):
    
    """
    Colore une colonne

    Parameters
    ----------
    grille : List[List[int]]
        grille à colorier
    colonne : int
        indice de la colonne à traiter
    fichier : str
        Nom du fichier
    
    Returns
    -------
    bool
        si le coloriage est possible
    List[List[int]]
        colonne coloriée
    set(int)
        listes de la colonne coloriées
    """
    
    # Ensemble des colonnes ajoutées/modifiées
    nouveaux = set()
    
    col = []
    for l in range (0, len(grille)):
        col.append(grille[l][colonne])
    col2 = col.copy()
    

    _, colonnes = lire_fichier(fichier)
    s = colonnes[colonne]
    
    # vérification si T(j,l) vrai
    if not(T2(len(col)-1, len(s), s, col)):
        return False, grille, nouveaux

    color_rec(len(col)-1, len(s), s, col)   
    
    nouveaux = {i for i in range(0, len(col)) if col[i] != col2[i]}
    
    for l in range (0, len(grille)):
        grille[l][colonne] = col[l]
    
    return (True, grille, nouveaux)


def coloration(grille, fichier):
    
    """
    Colore une grille

    Parameters
    ----------
    grille : List[List[int]]
        grille vide à colorier
    fichier : str
        Nom du fichier
    
    Returns
    -------
    int
        si le coloriage s'est bien déroulé
    List[List[int]]
        grille coloriée
    """
    
    # Duplication de la grille
    a = grille.copy()
    v = grille.copy()
    
    lignes_a_voir = {i for i in range(0, len(a))}
    colonnes_a_voir = {i for i in range(0, len(a[0]))}
    
    while(lignes_a_voir != set() or colonnes_a_voir != set()):

        new_lignes_a_voir = set(lignes_a_voir)
        
        for i in lignes_a_voir:

            ok, a, nouveaux = color_lig(a, i, fichier)
            
            if not(ok):
                return (0, v)
            
            colonnes_a_voir |= set(nouveaux)

            new_lignes_a_voir -= {i}
        
        lignes_a_voir = set(new_lignes_a_voir)
        
        new_colonnes_a_voir = set(colonnes_a_voir)
        
        for j in colonnes_a_voir:
            
            ok, a, nouveaux = color_col(a, j, fichier)
            
            if not(ok):
                return (0, v)
            
            lignes_a_voir |= set(nouveaux)

            new_colonnes_a_voir -= {j}
    
        colonnes_a_voir = set(new_colonnes_a_voir)
    
    for ligne in a:
        for colonne in ligne:
            if colonne == 0:
                return (-1, a)
    
    return (1, a)


def coloration_fichier(fichier):
    
    """
    Colore la grille contenue dans un fichier et renvoie la grille coloriée si c'est possible

    Parameters
    ----------
    fichier : str
        Nom du fichier
    
    Returns
    -------
    List[List[int]]
        grille coloriée
    """
    
    lig, col = lire_fichier(fichier)
    grille = [[0 for _ in range(0, len(col))] for _ in range(0, len(lig))]
    
    verdict, a = coloration(grille, fichier)
    
    if verdict == -1:
        print("On ne peut pas conclure")
        return False
    
    if verdict == 0:
        print("La coloration n'est pas possible")
        return False
    
    return a


def disp_terminal(grille):
    
    """
    Réalise un affichage basique de la grille dans le terminal
    
    Parameters
    ----------
    grille : List[List[int]]
        grille à afficher
    """
    
    for ligne in grille:
        ligne_str = " ".join(" " if valeur == 1 else "■" for valeur in ligne)
        print("|", ligne_str, "|")


def disp_sequence_ligne(s):
    
    seq = ""
    for ss in s:
        seq += str(ss) + " "
    
    return seq


def disp_sequence_colonne(s):
    
    seq = ""
    for ss in s:
        seq += str(ss) + "\n"
    
    return seq


def disp_graphique(grille, lig, col, taille = 0.5):
    
    lignes = len(grille)
    colonnes = len(grille[0])
    
    # Créer une nouvelle figure
    plt.figure(figsize=(colonnes * taille, lignes * taille))

    # Parcourir la grille et dessiner les carrés en noir ou blanc
    for i in range(lignes):
        for j in range(colonnes):
            if grille[i][j] == 2:
                couleur = 'black'
            else:
                couleur = 'white'
            plt.fill_between([j, j + 1], lignes - i - 1, lignes - i, color=couleur)

    # Ajouter des labels pour les colonnes
    for j in range(colonnes):
        plt.text(j + 0.5, lignes + 0.5, disp_sequence_colonne(col[j]), ha='center', va='bottom')

    # Ajouter des labels pour les lignes
    for i in range(lignes):
        plt.text(-0.5, lignes - i - 0.5, disp_sequence_ligne(lig[i]), ha='right', va='center')

    # Masquer les axes et les ticks
    plt.axis('off')

    # Afficher la figure
    plt.show()
    
    
def coloration_fichier_affichage(fichier, taille = 0.5):
    
    """
    Colore la grille contenue dans un fichier et affiche la grille si c'est possible

    Parameters
    ----------
    fichier : str
        Nom du fichier
    
    Returns
    -------
    List[List[int]]
        grille coloriée
    """
    
    lig, col = lire_fichier(fichier)
    
    a = coloration_fichier(fichier)
    
    if a:
        disp_graphique(a, lig, col, taille)
