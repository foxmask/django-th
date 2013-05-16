# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# sanitize use from https://raw.github.com/mindprince/pinboardToEvernote/master/sanitize.py
# and modifiy with the adding of the 2nd line
from tidylib import *
from xml.dom.minidom import *


def sanitize(html):
    # with  from __future__ import unicode_litterals
    # tidy_document does not want other options at all such as div merge char-encoding
    # and so on
    document, errors = tidy_document(html, options={"output-xhtml": 1})

    parsedDOM = xml.dom.minidom.parseString(document)
    documentElement = parsedDOM.documentElement
    removeProhibitedElements(documentElement)
    removeProhibitedAttributes(documentElement)
    body = documentElement.getElementsByTagName("body")[0]
    body.tagName = "en-note"
    return body.toxml()


def removeProhibitedElements(documentElement):
    """
        To fit the Evernote DTD need, drop this tag name
    """
    prohibitedTagNames = [
        "applet", "base", "basefont", "bgsound", "blink", "button", "dir", "embed", "fieldset", "form", "frame", "frameset", "head", "iframe", "ilayer", "input", "isindex",
        "label", "layer", "legend", "link", "marquee", "menu", "meta", "noframes", "noscript", "object", "optgroup", "option", "param", "plaintext", "script", "select", "style", "textarea", "xml", ]
    for tagName in prohibitedTagNames:
        removeProhibitedElement(tagName, documentElement)


def removeProhibitedElement(tagName, documentElement):
    """
        To fit the Evernote DTD need, drop this tag name
    """
    elements = documentElement.getElementsByTagName(tagName)
    for element in elements:
        p = element.parentNode
        p.removeChild(element)


def removeProhibitedAttributes(element):
    """
        To fit the Evernote DTD need, drop this attribute name
    """
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
