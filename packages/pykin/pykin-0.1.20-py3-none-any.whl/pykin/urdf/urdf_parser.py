import numpy as np
from xml.etree import ElementTree as ET
from collections import OrderedDict

from pykin.urdf.urdf_tree import URDFTree
from pykin.geometry.frame import Joint, Link, Frame
from pykin.kinematics.transform import Transform

JOINT_TYPE_MAP = {'revolute': 'revolute',
                  'fixed': 'fixed',
                  'prismatic': 'prismatic'}

LINK_TYPE_MAP = { 'cylinder' : 'cylinder',
                  'sphere'   : 'sphere',
                  'box'      : 'box',
                  'mesh'     : 'mesh'}

def _convert_transform(origin):
    if origin is None:
        return Transform()
    else:
        return Transform(rot=origin.rot, pos=origin.pos)

def _convert_string_to_narray(str_input):
    if str_input is not None:
        return np.array([float(data) for data in str_input.split()])

class URDFParser:
    def __init__(self, filepath=None):
        if filepath:
            self.parse(filepath)

    def parse(self, filepath):
        tree_xml = ET.parse(filepath)
        root = tree_xml.getroot()
        robot_name = root.attrib.get('name')

        tree = URDFTree(name=robot_name)

        for idx, link_tag in enumerate(root.findall('link')):
            link_frame = self._parse_link(link_tag, idx=idx)
            tree.links[link_frame.link.name] = link_frame.link

        for idx, joint_tag in enumerate(root.findall('joint')):
            joint_frame = self._parse_joint(joint_tag, idx=idx)
            tree.joints[joint_frame.joint.name] = joint_frame.joint

        root_name = next(iter(tree.links))
        tree.root = tree.links[root_name]

        root_frame = Frame(root_name + "_frame")
        root_frame.joint = Joint()
        root_frame.link = Link(root_name, offset=_convert_transform(root_frame.link.offset))
        root_frame.children = self._build_chain_recursive(tree.root, tree.links, tree.joints)

        tree.root = root_frame
        self.tree = tree
        return tree

    def _parse_link(self, link_tag, idx):
        attrib = link_tag.attrib
        link_name = attrib.get('name', 'link_' + str(idx))
        frame = Frame(link_name + '_frame',
                      link=Link(link_name, offset=Transform(), dtype=None, radius=0, length=0, size=np.zeros(3), color={}))

        # dtype, length, radius
        for collision_tag in link_tag.findall('collision'):
            for origin_tag in collision_tag.findall('origin'):
                frame.link.offset.pos = _convert_string_to_narray(origin_tag.attrib.get('xyz'))
                frame.link.offset.rot = _convert_string_to_narray(origin_tag.attrib.get('rpy'))
            for geometry_tag in collision_tag.findall('geometry'):
                for shape_type in ["cylinder", "sphere", "mesh"]:
                    for shapes in geometry_tag.findall(shape_type):
                        frame.link.dtype = shapes.tag
                        frame.link.length = shapes.attrib.get('length', 0)
                        frame.link.radius = shapes.attrib.get('radius', 0)
                        frame.link.mesh = shapes.attrib.get('filename', None)
                        
        for visual_tag in link_tag.findall('visual'):
            for origin_tag in visual_tag.findall('origin'):
                frame.link.offset.pos = _convert_string_to_narray(origin_tag.attrib.get('xyz'))
                frame.link.offset.rot = _convert_string_to_narray(origin_tag.attrib.get('rpy'))
            for geometry_tag in visual_tag.findall('geometry'):
                for shape_type in ["box", "mesh"]:
                    for shapes in geometry_tag.findall(shape_type):
                        if shape_type != "mesh":
                            frame.link.dtype = shapes.tag
                        frame.link.size = _convert_string_to_narray(shapes.attrib.get('size', None))
                        frame.link.mesh = shapes.attrib.get('filename', None)

            for material_tag in visual_tag.findall('material'):
                for colors in material_tag.findall('color'):
                    frame.link.color[material_tag.get('name')] = _convert_string_to_narray(
                        colors.attrib.get('rgba'))
        return frame

    def _parse_joint(self, joint_tag, idx):
        attrib = joint_tag.attrib
        joint_name = attrib.get('name', 'joint_' + str(idx))

        frame = Frame(joint_name + '_frame',
                      joint=Joint(name=joint_name, offset=Transform(), dtype=attrib['type'], limit=[None, None]))

        parent_tag = joint_tag.find('parent')
        frame.joint.parent = parent_tag.attrib['link']

        child_tag = joint_tag.find('child')
        frame.joint.child = child_tag.attrib['link']

        # origin
        origin_tag = joint_tag.find('origin')
        if origin_tag is not None:
            frame.joint.offset.pos = _convert_string_to_narray(origin_tag.attrib.get('xyz'))
            frame.joint.offset.rot = _convert_string_to_narray(origin_tag.attrib.get('rpy'))

        # axis
        axis_tag = joint_tag.find('axis')
        if axis_tag is not None:
            frame.joint.axis = _convert_string_to_narray(axis_tag.attrib.get('xyz'))

        # limit
        limit_tag = joint_tag.find('limit')
        if limit_tag is not None:
            if "lower" in limit_tag.attrib:
                frame.joint.limit[0] = float(limit_tag.attrib["lower"])
            if "upper" in limit_tag.attrib:
                frame.joint.limit[1] = float(limit_tag.attrib["upper"])
        
        return frame

    def _build_chain_recursive(self, root: Link, links: OrderedDict, joints: OrderedDict) -> list:
        children = []
        for joint in joints.values():

            if joint.parent == root.name:
                child_frame = Frame(joint.child + "_frame")
                child_frame.joint = Joint(joint.name, 
                                        offset=_convert_transform(joint.offset), 
                                        dtype=JOINT_TYPE_MAP[joint.dtype], 
                                        axis=joint.axis, 
                                        limit=joint.limit)

                chil_link = links[joint.child]
                child_frame.link = Link(chil_link.name, 
                                        offset=_convert_transform(chil_link.offset),
                                        dtype=LINK_TYPE_MAP.get(chil_link.dtype),
                                        radius=chil_link.radius,
                                        length=chil_link.length,
                                        size=chil_link.size,
                                        color=chil_link.color)

                child_frame.children = self._build_chain_recursive(child_frame.link, links, joints)
                children.append(child_frame)

        return children
