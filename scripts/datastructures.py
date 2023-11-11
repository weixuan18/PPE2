from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Token:
    forme: str
    lemme: str
    pos: str   


@dataclass
class Article:
    titre: str
    description: str
    date: str = ""
    categorie: str = ""
    analyse: Optional[List[Token]] = None

@dataclass
class Corpus:
    categories: List[str]
    begin: str
    end: str
    chemin: Path
    articles: List[Article]


