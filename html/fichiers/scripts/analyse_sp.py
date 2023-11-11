import spacy

from collections import namedtuple
from dataclasses import dataclass

from datastructures import Token, Article


def create_parser():
    return spacy.load("fr_core_news_md")


def analyse_article(parser, article: Article) -> Article:
    result = parser( (article.titre or "" ) + "\n" + (article.description or ""))
    output = []
    for token in result:
        output.append(Token(token.text, token.lemma_, token.pos_))
    article.analyse = output
    return article
