r"""
LDA Model
=========

Introduces Gensim's LDA model and demonstrates its use on the NIPS corpus.

"""

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import argparse
import sys
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models import Phrases
from gensim.corpora import Dictionary


def charge_xml(xmlfile,upos):
    import xml.etree.ElementTree as ET 
    with open(xmlfile, 'r') as f:
        xml = ET.parse(f)
        docs = []
        for article in xml.findall("//analyse"):
            doc = []
            for token in article.findall("./token"):
                if token.attrib['pos'] in upos:
                    form = token.attrib['forme']
                    lemme = token.attrib['lemme']
                    pos = token.attrib['pos']
                    doc.append(f"{form}/{lemme}/{pos}")
            if len(doc) > 0:
                docs.append(doc)
    return docs


def charge_json(jsonfile,upos):
    import json
    with open(jsonfile, 'r') as f:
        data = json.load(f)
        docs = []
        for article in data['articles']:
            doc = []
            for token in article['analyse']:
                if token.attrib['pos'] in upos:
                    form = token.attrib['forme']
                    lemme = token.attrib['lemme']
                    pos = token.attrib['pos']
                    doc.append(f"{form}/{lemme}/{pos}")
            if len(doc) > 0:
                docs.append(doc)
    return docs


def charge_pickle(picklefile,upos):
    import pickle
    with open(picklefile, 'rb') as f:
        data = pickle.load(f)
        docs = []
        for article in data['articles']:
            doc = []
            for token in article['analyse']:
                if token.attrib['pos'] in upos:
                    form = token.attrib['forme']
                    lemme = token.attrib['lemme']
                    pos = token.attrib['pos']
                    doc.append(f"{form}/{lemme}/{pos}")
            if len(doc) > 0:
                docs.append(doc)
    return docs

# Add bigrams and trigrams to docs (only ones that appear 20 times or more).

def add_bigrams(docs, min_count=20):
    bigram = Phrases(docs, min_count=20)
    for idx in range(len(docs)):
        for token in bigram[docs[idx]]:
            if '_' in token:
                # Token is a bigram, add to document.
                docs[idx].append(token)
    return docs

from gensim.models import LdaModel

def train_lda_model(docs, num_topics=10, chunksize=2000, passes=20, iterations=400, eval_every=None,no_below=50,no_above=0.6):
    # fixer les paramètres du modèle

    # Create a dictionary representation of the documents
    dictionary = Dictionary(docs)

    # Filter out words that occur less than 20 documents, or more than 50% of the documents
    dictionary.filter_extremes(no_below=no_below, no_above=no_above)

    # Bag-of-words representation of the documents
    corpus = [dictionary.doc2bow(doc) for doc in docs]
    print('Number of unique tokens: %d' % len(dictionary),sys.stderr)
    print('Number of documents: %d' % len(corpus))


    # Make an index to word dictionary.
    temp = dictionary[0]  # This is only to "load" the dictionary.
    id2word = dictionary.id2token

    model = LdaModel(
        corpus=corpus,
        id2word=id2word,
        chunksize=chunksize,
        alpha='auto',
        eta='auto',
        iterations=iterations,
        num_topics=num_topics,
        passes=passes,
        eval_every=eval_every
    )

    return corpus, dictionary, model

def print_coherence(model,corpus):

    top_topics = model.top_topics(corpus)

    # Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
    avg_topic_coherence = sum([t[1] for t in top_topics]) / model.num_topics
    print('Average topic coherence: %.4f.' % avg_topic_coherence)
    from pprint import pprint
    pprint(top_topics)
    

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

def visualize_lda_model(model, corpus,dictionary, output_filename='lda_visualization.html'):
    vis_data = gensimvis.prepare(model, corpus, dictionary)
    with open(output_filename, 'w') as fout:
        pyLDAvis.save_html(vis_data, fout)

# Example usage:
#visualize_lda_model(trained_model, corpus, dictionary, output_filename='sortie.html')

def main():
    parser = argparse.ArgumentParser(description='Modèle LDA')
    parser.add_argument('-i', type=str, required=True, help='Chemin du fichier d\'entrée (format XML, JSON ou pickle)')
    parser.add_argument('-f', type=str, choices=['xml', 'json', 'pickle'], required=True, help='Format du fichier d\'entrée (xml, json ou pickle)')
    parser.add_argument('-o', type=str, default = None, help='Chemin du fichier de sortie pour la visualisation (format HTML)')
    parser.add_argument('-c', action='store_true',default = False, help='Afficher la cohérence des sujets')
    parser.add_argument('--no_below', type=int, default=50, help='Nombre minimum de documents dans lesquels un mot doit apparaître pour être conservé (par défaut=20)')
    parser.add_argument('--no_above', type=float, default=0.6, help='Pourcentage maximum de documents dans lesquels un mot peut apparaître pour être conservé (par défaut=0.5)')
    parser.add_argument('--num_topics', type=int, default=10, help='Nombre de sujets pour le modèle LDA (par défaut=10)')
    parser.add_argument('--chunksize', type=int, default=2000, help='Taille des lots pour l\'entraînement du modèle LDA (par défaut=2000)')
    parser.add_argument('--passes', type=int, default=20, help='Nombre de passes pour l\'entraînement du modèle LDA (par défaut=20)')
    parser.add_argument('--iterations', type=int, default=400, help='Nombre d\'itérations pour l\'entraînement du modèle LDA (par défaut=400)')
    parser.add_argument('POS',nargs= '*', help='parties du discours à retenir')
    args = parser.parse_args()

    # Charger les documents depuis le fichier
    if args.f == 'xml':
        docs = charge_xml(args.i,args.POS)
    elif args.f == 'json':
        docs = charge_json(args.i,args.POS)
    elif args.f == 'pickle':
        docs = charge_pickle(args.i,args.POS)
    else:
        raise ValueError('Format d\'entrée inconnu')

    # Prétraiter les documents
    docs = add_bigrams(docs)

    # Entraîner le modèle LDA
    corpus,dic,lda_model = train_lda_model(docs, num_topics=args.num_topics, chunksize=args.chunksize, passes=args.passes, iterations=args.iterations,no_below=args.no_below,no_above=args.no_above)

    if args.o is not None:
        # Visualiser le modèle LDA
        visualize_lda_model(lda_model, corpus, dic, output_filename=args.o)
    if args.c is True:
        print_coherence(lda_model,corpus)

if __name__ == '__main__':
    main()

# exemple d'utilisation: python3 LDA_model.py -i ../data/2022-01-01.xml -f xml -o sortie.html -c True --num_topics 10 --chunksize 2000 --passes 20 --iterations 400 --no_below 50 --no_above 0.6 ADJ NOUN VERB PROPN
