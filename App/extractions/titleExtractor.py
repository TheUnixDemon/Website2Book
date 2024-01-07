import html
import re
import json

import requests
from bs4 import BeautifulSoup

import sys
sys.path.append("configs")
import handleConfig
sys.path.append("requests")
import handleRequest

def htmlTranslation(htmlChaptertitle: str) -> str: # changes html expressions into normal text
    chaptertitle = html.unescape(html.unescape(htmlChaptertitle))
    return chaptertitle

def extractTitle(serverConfig: json, page) -> str:
    chaptertitleConfig = serverConfig["request"]["pattern"]["chaptertitle"]
    chaptertitleKeys = ["class", "tag", "section"] # the order is required
    
    classPattern = None; tagPattern = None; sectionPattern = None # additional patterns for title extraction | tag is required
    soup = BeautifulSoup(page.content, "html.parser")
    for chaptertitleKey in chaptertitleKeys:
        if chaptertitleKey in chaptertitleConfig: # checks if the entry is written down
            value = chaptertitleConfig[chaptertitleKey]
            match chaptertitleKey:
                case "class":
                    classPattern = value
                case "tag": # "tag" is a requirement by verifyConfig
                    tagPattern = value
                case "section":
                    sectionPattern = value
                    
    if classPattern and tagPattern: # search after the tag and the class at the same time
        elements = soup.find_all(tagPattern, class_=classPattern)
        if sectionPattern:
            elementsSection = []
            for element in elements:
                entries = element.get(sectionPattern)
                elementsSection.append(str(entries))
            
    htmlChaptertitle = None # at this time it is in html expressions and must be translated
    
    if elementsSection:
        if len(elementsSection) == 1: # not allowed to be larger as one entry
            htmlChaptertitle = str(elementsSection[0])
            chaptertitle = htmlTranslation(htmlChaptertitle)
            
            return chaptertitle