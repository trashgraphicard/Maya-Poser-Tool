#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#
"""
:author:
    trashgraphicard

:synopsis:
    Perform some operations on joints in Maya.

:description:
    This module include functions that perform simple operations on joints in Maya
    Contains the following functions:
        create_joints
        position_joint
        rotate_joint
        verify_joint

:applications:
    Maya
"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports
import maya.cmds as cmds

# Imports That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

def create_joints(joint_list=[]):
    """
    Create joints with the provided list of names. Each joint will be paretned to the one
    that came before it in the list.

    :param joint_list: a list of names for the joints
    :type: list

    :return: A list of names of joints that were created
    :type: list
    """
    if not joint_list:
        cmds.warning("You must provide names for the joints!")
    else:
        joint_names = []
        for joint in joint_list:
            if isinstance(joint, str):
                joint_names.append(cmds.joint(name=joint))
        return joint_names
    

def position_joint(joint=None, tx=None, ty=None, tz=None):
    """
    move a joint to the absolute position x, y and z

    :param joint: The joint node that you want to move
    :type: str

    :param tx: Absolute distance along x axis
    :type: float

    :param ty: Absolute distance along y axis
    :type: float

    :param tz: Absolute distance along z axis
    :type: float

    :return: The success of the operation
    :type: bool
    """
    if not verify_joint(joint):
        return None
    # using "!= None" so that the value of 0 evalutes to True
    if tx != None:
        cmds.move(tx, joint, moveX=True, absolute=True)
    if ty != None:
        cmds.move(ty, joint, moveY=True, absolute=True)
    if tz != None:
        cmds.move(tz, joint, moveZ=True, absolute=True)
    return True


def rotate_joint(joint=None, rx=None, ry=None, rz=None):
    """
    rotate a joint to the absolute degree x, y, and z

    :param joint: The joint node that you want to rotate
    :type: str

    :param rx: Absolute degree around x axis
    :type: float

    :param ry: Absolute degree around y axis
    :type: float

    :param rz: Absolute degree around z axis
    :type: float

    :return: The success of the operation
    :type: bool
    """
    if not verify_joint(joint):
        return None
    # using "!= None" so that the value of 0 evaluate to True
    if rx != None:
        cmds.rotate(rx, joint, rotateX=True, absolute=True)
    if ry != None:
        cmds.rotate(ry, joint, rotateY=True, absolute=True)
    if rz != None:
        cmds.rotate(rz, joint, rotateZ=True, absolute=True)
    return True


def verify_joint(node=None):
    """
    Verify if the input node is a joint or not

    :param node: The node you want to verify
    :type: str

    :return: The status of the verification
    :type: bool
    """
    if not cmds.objExists(node):
        cmds.warning(f"The node {node} does not exist!")
        return None
    elif cmds.nodeType(node) != "joint":
        cmds.warning(f"{node} is not a joint!")
        return None
    return True

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

