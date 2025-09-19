#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    trashgraphicard

:synopsis:
    Some tools that deal with xml file.

:description:
    Utilitary functions and classes that help working with xml files.
    Contains the following funtions:
        read_pose_xml
    Contains the following classes:
        Autovivification

:applications:
    Maya

:see_also:
    td_maaya_tools.guis.maya_gui_utils
"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports
from maya import cmds
import os
import xml.etree.ElementTree as et

# Imports That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

def read_pose_xml(path=None):
    """
    Read an xml file containing information on poses and their properties, and convert
    them into a dictionary
    The dictionary should look something like this:
        dict[pose][joint][translations/rotations][x/y/x value] = '<x/y/z value>'
    For example:
        dict[dance][Spine][rotations][ry] = 48.45

    :param path: Full path the the xml file
    :type: string

    :return: Dictionary converted from the xml file
    :type: dict
    """
    if not path:
        cmds.warning('You must provide a file path')
        return None
    if not os.path.isfile(path):
        cmds.warning(f'The file path, {path}, is not a file')
        return None
    
    pose_dict = Autovivification()
    xml_fh = et.parse(path)
    root = xml_fh.getroot()
    for xml_pose in root:
        pose = xml_pose.tag
        for xml_joint in xml_pose:
            joint = xml_joint.tag
            for xml_attr in xml_joint:
                attr_type = xml_attr.tag
                attr_value = xml_attr.attrib
                pose_dict[pose][joint][attr_type] = attr_value
    return pose_dict



#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class Autovivification(dict):
    """
    This is a Python implementation of Perl's autovivification feature.
    """
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
        
        