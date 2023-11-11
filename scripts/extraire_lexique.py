from pathlib import Path
from typing import List, Dict
import argparse
import sys
import glob
import os

parser = argparse.ArgumentParser(description = 'lire le corpus du dossier')
parser.add_argument('path', nargs='+', type=str, required = True, help='nom du dossier du chemin que vous souhaitez lire')
args = parser.parse_args()


def lecture_par_liste():
    # Cela renvoie une liste contenant les noms de tous les fichiers avec l'extension .txt dans le dossier en argument.
    liste_fichiers = glob.glob(sys.argv[1]  + "/*.txt")
    return liste_fichiers

def lire_corpus():
    resultat = []
    for fichier in liste_fichiers:
        texte = fichier.read_text("utf-8")
        resultat.append(texte)
    return resultat

def term_freq(corpus: List[str]) -> Dict[str,int]:
    resultat = {}
    for doc in corpus:
        for word in doc.split():
            if word in resultat:
                resultat[word] += 1
            else:
                resultat[word] = 1
    return resultat

def nb_doc(corpus: List[str]) -> Dict[str, int]:
    resultat={}

    for doc in corpus:
        texte = set(corpus.split())

        for mot in corpus:
            if mot in resultat:
                resultat[mot] += 1
            else:
                resultat[mot] = 1
    return resultat

def main():
    corpus = lecture_par_liste(lire_corpus())
    print("doc freq")
    for k, v in nb_doc(corpus).items():
        print(f"{k}: {v}")
    print("term freq")
    for k, v in term_freq(corpus).items():
        print(f"{k}: {v}")

def afficher(fichiers):
    lexique = []
    for fichier in fichiers:
        with open(fichier, 'r') as f:
            for ligne in f:
                mots = ligne.strip().split()
                for mot in mots:
                    if mot not in lexique:
                        lexique.append(mot)
    return lexique


def list_files(répertoire):
    répertoire = Path("./Corpus")
    for nom_file in os.listdir(répertoire):
        if os.path.isfile(os.path.join(répertoire, nom_file)):
            print(nom_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lister les files dans un répertoire')
    parser.add_argument('répertoire', metavar='dir', type=str, help='le répertoire pour la liste de files est')
    args = parser.parse_args()

    list_files(args.répertoire)
    main(args.path)
    
    parser2 = argparse.ArgumentParser()
    parser2.add_argument('fichiers', nargs='+', type=str, help='les fichiers à lire')
    args2 = parser2.parse_args()
    lexique = afficher(args2.fichiers)
    for mot in lexique:
        sys.stdout.write(mot)




