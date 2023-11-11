from typing import List
from xml.etree import ElementTree as ET

from datastructures import Corpus, Article, Token



def analyse_to_xml(tokens: List[Token]) -> ET.Element:
    root = ET.Element("analyse")
    for tok in tokens:
        tok_element = ET.SubElement(root, "token")
        tok_element.attrib['forme'] = tok.forme 
        tok_element.attrib['pos'] = tok.pos 
        tok_element.attrib['lemme'] = tok.lemme 
    return root


def article_to_xml(article: Article) -> ET.Element:
    art = ET.Element("article")
    art.attrib['date'] = article.date
    art.attrib['categorie'] = article.categorie
    title = ET.SubElement(art, "title")
    description = ET.SubElement(art, "description")
    title.text = article.titre
    description.text = article.description
    art.append(analyse_to_xml(article.analyse))
    return art

def write_xml(corpus: Corpus, destination: str):
    root = ET.Element("corpus")
    root.attrib['begin'] = corpus.begin
    root.attrib['end'] = corpus.end
    categories = ET.SubElement(root, "categories")
    for c in corpus.categories:
        ET.SubElement(categories, "cat").text = c
    content = ET.SubElement(root, "content")
    for article in corpus.articles:
        art_xml = article_to_xml(article)
        content.append(art_xml)
    tree = ET.ElementTree(root)
    ET.indent(tree)
    tree.write(destination)



