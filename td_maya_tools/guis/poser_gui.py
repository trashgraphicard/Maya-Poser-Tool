#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    trashgraphicard

:synopsis:
    The GUI for poser tools for Maya.

:description:
    A GUI that applies a set of pose to a predetermined rig on a button click

:applications:
    Maya

:see_also:

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports
import os
from maya import cmds
from PySide2 import QtGui, QtWidgets, QtCore

# Imports That You Wrote
from .maya_gui_utils import get_maya_window, VLine, HLine
from td_maya_tools import poser, xml_utils
#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class PoseLayout(QtWidgets.QHBoxLayout):
    """
    This is the small layout box that presents a pose and its apply button. A number of
    these will be created based on the amount of provided pose
    """

    def __init__(self, path_to_img=None, joint_dict=None):
        super().__init__()
        self.img_path = path_to_img
        self.joint_dict = joint_dict
        

    def build_layout(self):
        """
        Build the layout
        """
        # create the image
        pose_img = QtWidgets.QLabel()
        pose_img.setPixmap(QtGui.QPixmap(self.img_path))

        # crate the layout for the text and apply button
        vbox = QtWidgets.QVBoxLayout()

        # create the text from the imge file
        img_label = QtWidgets.QLabel()
        img_name = os.path.basename(self.img_path)
        img_name = os.path.splitext(img_name)[0]
        img_label.setText(img_name)

        # adjust text font
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        img_label.setFont(font)

        # create the apply button
        apply_btn = QtWidgets.QPushButton()
        apply_btn.setText('Apply')

        # add widgets to vbox
        vbox.addWidget(img_label)
        vbox.addWidget(apply_btn)

        # add widgets and layouts to self
        self.addWidget(pose_img)
        self.addLayout(vbox)

        # signal button click
        apply_btn.clicked.connect(self.apply_values)
    
    def apply_values(self):
        """
        Apply the input transform and rotate values to the selected joint in Maya
        """
        for joint, attrib_dict in self.joint_dict.items():
            tx = attrib_dict['translations']['tx']
            ty = attrib_dict['translations']['ty']
            tz = attrib_dict['translations']['tz']
            rx = attrib_dict['rotations']['rx']
            ry = attrib_dict['rotations']['ry']
            rz = attrib_dict['rotations']['rz']

            # wrap values into float or None if empty
            # set to None rather than 0 so that the functions in poser will ignore them
            tx = float(tx) if tx.strip() else None
            ty = float(ty) if ty.strip() else None
            tz = float(tz) if tz.strip() else None
            rx = float(rx) if rx.strip() else None
            ry = float(ry) if ry.strip() else None
            rz = float(rz) if rz.strip() else None

            # apply translations and rotations
            poser.position_joint(joint, tx, ty, tz)
            poser.rotate_joint(joint, rx, ry, rz)
        
class PoserGUI(QtWidgets.QDialog):
    """
    This class asseembles the main GUI that will be displayed
    """

    def _init_(self):
        super().__init__(parent=get_maya_window())
        self.img_paths = None
        self.pose_names = None
        self.pose_dict = None
        self.xml_lw = None
        self.msg_label = None

    def init_gui(self):
        """
        Set up and display the GUI to the user.
        """
        # make a main layout
        main_hb = QtWidgets.QHBoxLayout(self)

        # List and sort all joints in the scene
        joint_list = cmds.ls(type='joint')
        if not joint_list:
            self.display_message(title='No Joints',
            message='There are no joints in the scene')
        joint_list.sort()

        # get path to image
        self.img_paths, self.pose_names = self.get_images()

        # get pose dictionary
        self.pose_dict = self.get_pose_dict()

        # create pose layout and add to main layout
        pose_layout_grid = self.build_pose_layout()
        main_hb.addLayout(pose_layout_grid)

        # create xml layout and add to main layout
        xml_layout = self.build_xml_list_layout()
        main_hb.addLayout(xml_layout)

        # Configure the window
        self.setGeometry(600, 600, 300, 200)
        self.setWindowTitle('Poser GUI')
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.show()

    def build_pose_layout(self):
        """
        Instanciate PoseLayout classes based on the number of valid pose, then create a
        layout containing those instances

        :return: A grid layout containing all pose layouts
        :type: QtWidgets.QGridLayout
        """
        pose_layout_grid = QtWidgets.QGridLayout()

        column = 0
        row = 0
        for image in self.img_paths:
            pose_name = os.path.splitext(os.path.basename(image))[0]
            # check if the poser is valid
            ### if the pose is not in the xml file don't add it !!!!! ###
            # This cause me so much pain as the autovivi will add the key automatically
            # Caused a series of bugs afterward took me 3 hours to debug
            if not pose_name in self.pose_dict:
                continue
            pose_layout = PoseLayout(image, self.pose_dict[pose_name])
            pose_layout.build_layout()
            # wrap the layout into a container to control its size
            container = QtWidgets.QWidget()
            container.setLayout(pose_layout)
            container.setMinimumWidth(160)
            container.setMaximumWidth(180)
            pose_layout_grid.addWidget(container, row, column)

            # row and column increments
            # leaving empty slots in between for partition lines
            # that will be added later
            column += 2
            if column > 4:
                row += 2
                column = 0

        # loop over the grid and add partition line at appropriate slots
        for row in range(pose_layout_grid.rowCount()):
            for col in range(pose_layout_grid.columnCount()):
                if row % 2 == 0 and col % 2 == 1:
                    vline = VLine()
                    vline.make_line()
                    pose_layout_grid.addWidget(vline, row, col)
                elif row % 2 == 1 and col % 2 == 0:
                    hline = HLine()
                    hline.make_line()
                    pose_layout_grid.addWidget(hline, row, col)

        return pose_layout_grid
    
    def build_xml_list_layout(self):
        """
        This is a list widget that displays all joints found in the image folder
        As well as highlighting ones that do not have matching data in the xml file.

        :return: A layout that include the list widget
        :type: QtWidget.QVBoxLayout
        """
        xml_layout = QtWidgets.QVBoxLayout()
        self.xml_lw = QtWidgets.QListWidget()

        for pose in self.pose_names:
            lw_item = QtWidgets.QListWidgetItem(pose)
            # change the color if a pose if not in the xml file
            if not pose in self.pose_dict:
                lw_item.setBackground(QtGui.QColor('#CC3333'))
            self.xml_lw.addItem(lw_item)

        self.msg_label = QtWidgets.QLabel('Click list widget item for more info')
        self.xml_lw.itemClicked.connect(self.list_item_clicked)
            
        xml_layout.addWidget(self.xml_lw)
        xml_layout.addWidget(self.msg_label)

        return xml_layout

    def list_item_clicked(self):
        """
        update the message label to indicate whether the pose is valid or not.

        :return: wheteher the pose is valid or not. True if valid, false otherwise
        :type: bool
        """
        current_item_text = self.xml_lw.currentItem().text()
        if not current_item_text in self.pose_dict:
            self.msg_label.setText(f'{current_item_text} is not a valid pose')
            return None
        self.msg_label.setText(f'{current_item_text} is a valid pose')
        return True


    @classmethod
    def get_pose_dict(cls):
        """
        Get the dictionary containing poses and their respective information

        :return: A dictionary containing information on poses
        :type: dict
        """
        img_dir = os.path.join(os.path.dirname(__file__), 'images')
        xml_files = cls.get_files_of_type(img_dir, 'xml')

        if not xml_files:
            cls.display_message('No XML', 'No xml file found in the images folder')
            return None
        pose_dict = xml_utils.read_pose_xml(os.path.join(img_dir, xml_files[0]))
        return pose_dict

    @classmethod
    def get_images(cls):
        """
        Get paths and names to all png files from the image folder

        :return: A tuple containing 2 items
                 1. A list of paths to all the png files and
                 2. A list of all names of the png files
        :type: tuple
        """
        img_dir = os.path.join(os.path.dirname(__file__), 'images')
        img_files = cls.get_files_of_type(img_dir, 'png')
        path_list = []
        pose_list = []

        for img in img_files:
            path_list.append(os.path.join(img_dir, img))
            pose_list.append(os.path.splitext(img)[0].strip())

        if not img_files:
            cls.display_message('No Images', 'No images found in the images folder!')
            return None
        return path_list, pose_list
    
    @classmethod
    def get_files_of_type(cls, search_dir=None, type=None):
        """
        Get all files of a certain extension from a directory, and return them in a list.

        :param search dir: Path to the directory / folder to search in
        :type: string

        :param type: The file extension to search for, without the dot.
        :type: string

        :return: A list containig all files (not full path) that match the condition
        :type: list
        """
        file_list = os.listdir(search_dir)
        ret_list = []
        for file in file_list:
            if file.endswith(f'.{type}'):
                ret_list.append(file)
        return ret_list

    @classmethod
    def display_message(cls, title=None, message=None):
        """
        Displays a window containing a message to the user.
        The window needs to be interacted before any action and continue.

        :param title: The title of the window.
        :type: str

        :param message: The message in the pop up.
        :type: str
        """
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()