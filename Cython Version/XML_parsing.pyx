###cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True, optimize.use_switch=True
# encoding: utf-8
#
# PYGAME IS REQUIRED
import pygame
#
# try:
#     from pygame.mask import from_surface
#     from pygame.math import Vector2
# except ImportError:
#     raise ImportError("\n<Pygame> library is missing on your system."
#           "\nTry: \n   C:\\pip install pygame on a window command prompt.")
#
#
# try:
#    from Sprites cimport Sprite
# except ImportError:
#     raise ImportError("\nSprites.pyd missing!.Build the project first.")

# CYTHON IS REQUIRED

try:
    cimport cython
    from cpython.dict cimport PyDict_DelItem, PyDict_Clear, PyDict_GetItem, PyDict_SetItem, \
        PyDict_Values, PyDict_Keys, PyDict_Items, PyDict_SetItemString
    from cpython cimport PyObject, PyObject_HasAttr, PyObject_IsInstance
    from cpython.list cimport PyList_GetItem
except ImportError:
    raise ImportError("\n<cython> library is missing on your system."
          "\nTry: \n   C:\\pip install cython on a window command prompt.")

import xml.etree.ElementTree as XML_ET


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef list xml_remove_weapon(str filename, str name_):
    """
    THE XML FILE MUST HAVE A SPECIFIC FORMAT, TAGS AND ATTRIBUTES.
    REFER TO THE XML FILE 'WEAPON.XML' FOR MORE DETAILS
    LOAD AN XML FILE AND REMOVE A SPECIFIC WEAPON CLASS

    :param filename : string; XML file to load
    :param name_    : string; weapon name to remove
    :return         : list;
    """
    tree = XML_ET.parse(filename)
    root = tree.getroot()

    cdef:
        list m_list = []
        m_list_append = m_list.append
        m_list_pop = m_list.pop
        int c=0
        str attribute, value

    for child in root.iter('weapon'):
        m_list_append(child.items())

    for weapon in list(m_list):
        attribute, value = <object>PyList_GetItem(weapon, 0)
        if attribute == 'name' and value == name_:
            m_list_pop(c)
        c += 1

    return m_list


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef xml_get_weapon(str filename, str weapon_name_):
    """
    Return a unique weapon class
    The xml file must have a specific format, tags and attributes.
    Refer to the XML file 'Weapon.xml' for more details

    :param filename      : string; xml file to load
    :param weapon_name_ : list; weapon to extract
    :return: list or None
    """
    tree = XML_ET.parse(filename)
    root = tree.getroot()
    cdef:
        list weapon_list = []
        weapon_list_append = weapon_list.append
        str attribute, value

    for child in root.iter('weapon'):
        weapon_list_append(child.items())

    cdef bint found = False
    for weapon in weapon_list:
        attribute, attribute_value = <object>PyList_GetItem(weapon,0)
        if attribute == 'name' and attribute_value == weapon_name_:
            found = True
            break
    if found:
        return weapon

    return None

