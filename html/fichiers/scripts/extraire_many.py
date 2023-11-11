from typing import Optional, List, Dict
import xml.etree.ElementTree as ET
import argparse
import re
from pathlib import Path
from datetime import date  # pour renvoyer dans le bon ordre chronologique
from tqdm import tqdm

from extraire_un import extraire_td, extraire_a
from datastructures import Corpus, Article, Token
from export_xml import write_xml
from export_json import write_json
from export_pickle import write_pickle

MONTHS = ["Jan",
          "Feb",
          "Mar",
          "Apr",
          "May",
          "Jun",
          "Jul",
          "Aug",
          "Sep",
          "Oct",
          "Nov",
          "Dec"]

DAYS = [f"{x:02}" for x in range(1, 32)]

# Définir le dictionnaire de correspondance entre les catégories et les noms de fichiers XML
categories_dict = {
    "une": "0,2-3208,1-0,0",
    "international": "0,2-3210,1-0,0",
    "europe": "0,2-3214,1-0,0",
    "societe": "0,2-3224,1-0,0",
    "idees": "0,2-3232,1-0,0",
    "economie": "0,2-3234,1-0,0",
    "actualite-medias": "0,2-3236,1-0,0",
    "sport": "0,2-3242,1-0,0",
    "planete": "0,2-3244,1-0,0",
    "culture": "0,2-3246,1-0,0",
    "livres": "0,2-3260,1-0,0",
    "cinema": "0,2-3476,1-0,0",
    "voyage": "0,2-3546,1-0,0",
    "technologies": "0,2-651865,1-0,0",
    "politique": "0,57-0,64-823353,0",
    "sciences": "env_sciences"
}
new_dict = {valeur: cle for cle, valeur in categories_dict.items()}


def categorie_of_filename(filename: str) -> Optional[str]:
    for nom, code in categories_dict.items():
        if code in filename:
            return nom
    return None


def convert_month(m: str) -> int:
    return MONTHS.index(m) + 1


def parcours_dossier(corpus_dir: Path, categories: Optional[List[str]] = None,
                     start_date: Optional[date] = None, end_date: Optional[date] = None):
    if categories is not None and len(categories) > 0:
        categories = [categories_dict[c.lower()] for c in categories]
    else:
        categories = categories_dict.values()

    for month_dir in corpus_dir.iterdir():
        if not month_dir.is_dir():
            continue
        m = convert_month(month_dir.name)
        for day_dir in month_dir.iterdir():
            if not day_dir.is_dir():
                continue
            d = date.fromisoformat(f"2022-{m:02}-{day_dir.name}")
            if (start_date is not None and d < start_date) or (end_date is not None and d > end_date):
                continue
            for hour_dir in day_dir.iterdir():
                if not hour_dir.is_dir():
                    continue
                if re.match(r"\d{2}-\d{2}-\d{2}", hour_dir.name):
                    for xml_file in hour_dir.iterdir():
                        if xml_file.name.endswith(".xml") and any([xml_file.name.startswith(c) for c in categories]):
                            # yield(xml_file.name, extraire_td(xml_file.as_posix()))
                            c = categorie_of_filename(xml_file.name)
                            yield xml_file, d.isoformat(), c


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", help="start date (iso format)", default="2022-01-01")
    parser.add_argument("-e", help="end date (iso format)",
                        default="2023-01-01")
    parser.add_argument(
        "-o", help="output file (stdout si non spécifié)", required=True)
    parser.add_argument(
        "-f", help="format de sortie (xml par défault)", choices = ['xml','json','pickle'], default="xml",required = True)
    parser.add_argument(
        "-p", help="parser à utiliser (spacy par défault)",choices = ['spacy','stanza','trankit'], required = True, default="spacy")
    parser.add_argument("corpus_dir", help="la racine du dossier")
    parser.add_argument("categories", nargs="*", help="catégories à retenir")
    args = parser.parse_args()
    corpus = Corpus(categories=args.categories, begin=args.s,
                    end=args.e, chemin=Path(args.corpus_dir), articles=[])
    for xml_file, d, c in tqdm(parcours_dossier(Path(args.corpus_dir), args.categories, date.fromisoformat(args.s), date.fromisoformat(args.e))):
        for article in extraire_a(xml_file, d, c):
            corpus.articles.append(article)
    if args.p == "spacy" or args.p == None:
        import analyse_sp as analyse
    elif args.p == "stanza":
        import analyse_st as analyse
    elif args.p == "trankit":
        import analyse_tk as analyse
    for a in tqdm(corpus.articles):
        parser = analyse.create_parser()
        analyse.analyse_article(parser, a)
    if args.o is None:
        for title, description in extraire_td(args.corpus_dir):
            print(title)
            print(description)
    if args.o is not None:
        if args.f == "xml":
            write_xml(corpus, args.o)
        elif args.f == "json":
            write_json(corpus, args.o)
        elif args.f == "pickle":
            write_pickle(corpus, args.o)
        else:
            print("format non supporté")


if __name__ == "__main__":
    main()

# exemple d'utilisation: python3 extraire_deux.py -s 2022-01-01 -e 2022-01-31 -o corpus.xml /home/.../corpus une international
