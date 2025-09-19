import os
import xml.etree.ElementTree as et

def read_pose_xml(path=None):

    if not path:
        return None
    if not os.path.isfile(path):
        return None
    
    trans_dict = Autovivification()
    xml_fh = et.parse(path)
    root = xml_fh.getroot()
    for xml_pose in root:
        pose = xml_pose.tag
        for xml_joint in xml_pose:
            joint = xml_joint.tag
            for xml_attr in xml_joint:
                attr_name = xml_attr.tag
                attr_value = xml_attr.attrib
                trans_dict[pose][joint][attr_name] = attr_value

    print(trans_dict)

def get_files_of_type(search_dir=None, type=None):
    """
    Get all files of a certain extension from a directory, and return them in a list.

    :param search dir: Path to the directory / folder to search in
    :type: string

    :param type: The file extension to search for, without the dot.
    :type: string

    :return: A list containig all files (not full path) that match the condition
    :type: string
    """
    file_list = os.listdir(search_dir)
    ret_list = []
    for file in file_list:
        if file.endswith(f'.{type}'):
            ret_list.append(file)
    return ret_list

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
        
if __name__ == '__main__':
    ls = get_files_of_type('C:/Users/henry.hou/Desktop/Projects/3311MainDir/code/td_maya_tools/guis/images', 'png')
    #read_pose_xml('C:/Users/henry.hou/Desktop/Projects/3311MainDir/code/td_maya_tools/guis/images/poses.xml')