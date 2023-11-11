import pickle
from typing import List
from datastructures import Corpus, Article, Token

def analyse_to_pickle(tokens: List[Token]) -> List[dict]:
    result = []
    for tok in tokens:
        token_dict = {
            'forme': tok.forme,
            'pos': tok.pos,
            'lemme': tok.lemme
        }
        result.append(token_dict)
    return result

def article_to_pickle(article: Article) -> dict:
    return {
        'date': article.date,
        'categorie': article.categorie,
        'titre': article.titre,
        'description': article.description,
        'analyse': analyse_to_pickle(article.analyse)
    }

def corpus_to_pickle(corpus: Corpus) -> dict:
    return {
        'begin': corpus.begin,
        'end': corpus.end,
        'categories': corpus.categories,
        'chemin': str(corpus.chemin),
        'articles': [article_to_pickle(article) for article in corpus.articles]
    }

def write_pickle(corpus: Corpus, destination: str):
    data = corpus_to_pickle(corpus)
    with open(destination, 'wb') as pickle_file:
        pickle.dump(data, pickle_file)
