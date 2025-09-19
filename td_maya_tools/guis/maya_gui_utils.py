#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    trashgraphicard

:synopsis:
    Utility functions for maya GUIs.

:description:
    Some utility functions that work on maya GUIs.
    Contains the following functions:
        get_may_window
    Contains the following classes:
        HLine
        VLine

:applications:
    Maya.

:see_also:
    
"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports
from PySide2 import QtWidgets
from PySide2.QtWidgets import QFrame
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

# Imports That You Wrote
#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

def get_maya_window():
    """
    This gets a pointer to the maya window.

    :return: A pointer to the maya window.
    :type: pointer
    """
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class HLine(QFrame):
    """
    A QFrame item that can be used as a horizontal partition line
    """
    def make_line(self):
        """
        Draw the line
        """
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class VLine(QFrame):
    """
    A QFrame item that can be used as a vertical partition line
    """
    def make_line(self):
        """
        Draw the line
        """
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)

