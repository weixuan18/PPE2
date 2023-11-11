import trankit

from collections import namedtuple
from dataclasses import dataclass

from datastructures import Token, Article


def create_parser():
    return trankit.Pipeline('french', gpu=False)


def analyse_article(parser, article: Article) -> Article:
    result = parser( (article.titre or "" ) + "\n" + (article.description or ""))
    output = []
    for sentence in result['sentences']:
        for token in sentence['tokens']:
            if 'expanded' not in token.keys():
                token['expanded'] = [token]
            for w in token['expanded']:
                output.append(Token(w['text'], w['lemma'], w['upos']))
    article.analyse = output
    return article
