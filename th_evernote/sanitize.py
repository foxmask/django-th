# coding: utf-8
import re
from tidylib import tidy_document
from xml.dom.minidom import parseString


def sanitize(html):
    # with from __future__ import unicode_litterals
    # tidy_document does not want other options at all
    # such as div merge char-encoding and so on
    document, errors = tidy_document(
        html, options={"output-xhtml": 1, "force-output": 1})

    parsed_dom = parseString(document)
    document_element = parsed_dom.documentElement
    remove_prohibited_elements(document_element)
    remove_prohibited_attributes(document_element)
    body = document_element.getElementsByTagName("body")[0]
    body.tagName = "en-note"
    return body.toxml()


def remove_prohibited_elements(document_element):
    """
        To fit the Evernote DTD need, drop this tag name
    """
    prohibited_tag_names = [
        "applet", "base", "basefont", "bgsound", "blink", "button", "dir",
        "embed", "fieldset", "form", "frame", "frameset", "head", "iframe",
        "ilayer", "input", "isindex", "label", "layer", "legend", "link",
        "marquee", "menu", "meta", "noframes", "noscript", "object",
        "optgroup", "option", "param", "plaintext", "script", "select",
        "style", "textarea", "xml", 'wbr']
    for tag_name in prohibited_tag_names:
        remove_prohibited_element(tag_name, document_element)


def remove_prohibited_element(tag_name, document_element):
    """
        To fit the Evernote DTD need, drop this tag name
    """
    elements = document_element.getElementsByTagName(tag_name)
    for element in elements:
        p = element.parentNode
        p.removeChild(element)


def filter_term(att):
    if att.startswith("on") or \
       att.startswith("data-") or \
       att in ["id", "class", "accesskey", "data", "dynsrc", "tabindex",
               "frame", "rules", "width", "trbidi", "imageanchor"]:
        return True


def remove_child_prohibited_attr(element):

    list_on_children = element.childNodes
    for child in list_on_children:
        if child.nodeType == 1:
            remove_prohibited_attributes(child)


def remove_href_prohibited_attr(element):
    try:
        if element.hasAttribute("href"):
            t = element.toxml()
            if re.search('href="http', t) or re.search('href="https', t):
                pass
            else:
                element.removeAttribute("href")
    except:
        pass


def remove_attr_prohibited(element):
    to_be_removed_atts = [att for att in element.attributes.keys()
                          if filter_term(att.lower())]

    for attribute in to_be_removed_atts:
        element.removeAttribute(attribute)


def remove_prohibited_attributes(element):
    """
        To fit the Evernote DTD need, drop this attribute name
    """
    remove_attr_prohibited(element)
    remove_href_prohibited_attr(element)
    remove_child_prohibited_attr(element)
