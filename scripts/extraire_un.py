#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import feedparser
from datastructures import Article
from pathlib import Path

def extraire_td(rss_file):	
	# Créer un élément racine pour le fichier XML
	root = ET.Element("channel")
    
	# Analyse du fichier XML
	feed = feedparser.parse(rss_file)
	
	# Parcourir les éléments <item> du fichier RSS
	for entry in feed.entries:
		title = entry.title
		description = entry.description
		yield title, description

def extraire_a(rss_file,date,categorie):
	feed = feedparser.parse(rss_file)
	for entry in feed.entries:
		article = Article(entry.title,entry.description,date,categorie,[])
		yield article	


