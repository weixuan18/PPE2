import stanza

from collections import namedtuple
from dataclasses import dataclass

from datastructures import Token, Article

def create_parser():
    return stanza.Pipeline(lang='fr', processors='tokenize,mwt,pos,lemma')

def analyse_article(parser, article: Article) -> Article:
    result = parser( (article.titre or "" ) + "\n" + (article.description or ""))
    output = []
    for sent in result.sentences:
        for word in sent.words:
            output.append(Token(word.text, word.lemma, word.pos))
        article.analyse = output
        return article
