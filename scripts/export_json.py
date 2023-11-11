import json
from typing import List
from datastructures import Corpus, Article, Token

def analyse_to_json(tokens: List[Token]) -> List[dict]:
    result = []
    for tok in tokens:
        token_dict = {
            'forme': tok.forme,
            'pos': tok.pos,
            'lemme': tok.lemme
        }
        result.append(token_dict)
    return result

def article_to_json(article: Article) -> dict:
    return {
        'date': article.date,
        'categorie': article.categorie,
        'titre': article.titre,
        'description': article.description,
        'analyse': analyse_to_json(article.analyse)
    }

def corpus_to_json(corpus: Corpus) -> dict:
    return {
        'begin': corpus.begin,
        'end': corpus.end,
        'categories': corpus.categories,
        'chemin': str(corpus.chemin),
        'articles': [article_to_json(article) for article in corpus.articles]
    }

def write_json(corpus: Corpus, destination: str):
    data = corpus_to_json(corpus)
    with open(destination, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

