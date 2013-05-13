# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# from https://raw.github.com/mindprince/pinboardToEvernote/master/sanitize.py
import re
from tidylib import *
from xml.dom.minidom import *


def sanitize(html):
    document, errors = tidy_document(html, options={
        "output-xhtml": 1,
        "char-encoding": "utf8",
        "drop-proprietary-attributes": 1, "merge-divs": 1, "clean": 1})
                                     # xml.dom.minidom is an XML parser, not an
                                     # HTML parser. Therefore, it doesn't know
                                     # any HTML entities (only those which are
                                     # common to both XML and HTML). So, if I
                                     # didn't give output-xhtml I got
                                     # xml.parsers.expat.ExpatError: undefined
                                     # entity.
    parsedDOM = xml.dom.minidom.parseString(document)
    documentElement = parsedDOM.documentElement
    removeProhibitedElements(documentElement)
    removeProhibitedAttributes(documentElement)
    body = documentElement.getElementsByTagName("body")[0]
    body.tagName = "en-note"
    return body.toxml()


def removeProhibitedElements(documentElement):
    prohibitedTagNames = [
        "applet", "base", "basefont", "bgsound", "blink", "button", "dir", "embed", "fieldset", "form", "frame", "frameset", "head", "iframe", "ilayer", "input", "isindex",
        "label", "layer", "legend", "link", "marquee", "menu", "meta", "noframes", "noscript", "object", "optgroup", "option", "param", "plaintext", "script", "select", "style", "textarea", "xml", ]
    for tagName in prohibitedTagNames:
        removeProhibitedElement(tagName, documentElement)


def removeProhibitedElement(tagName, documentElement):
    elements = documentElement.getElementsByTagName(tagName)
    for element in elements:
        p = element.parentNode
        p.removeChild(element)


def removeProhibitedAttributes(element):
    prohibitedAttributes = ["id", "class", "onclick", "ondblclick", "onload",
                            "accesskey", "data", "dynsrc", "tabindex", "onmouseover", "onmouseout", "onblur", ]
    # FIXME All on* attributes are prohibited. How to use a regular expression
    # as argument to removeAttribute?
    for attribute in prohibitedAttributes:
        try:
            element.removeAttribute(attribute)
        except xml.dom.NotFoundErr:
            pass
    try:
        if element.hasAttribute("href"):
            t = element.toxml()
            if re.search('href="http', t) or re.search('href="https', t):
                pass
            else:
                element.removeAttribute("href")
    except:
        pass

    listOfChildren = element.childNodes
    for child in listOfChildren:
        if child.nodeType == 1:
            removeProhibitedAttributes(child)
