from arm.logicnode.arm_nodes import *

class MouseCoordsNode(ArmLogicTreeNode):
    """Deprecated. Is recommended to use 'Get Cursor Location' and 'Get Mouse Movement' nodes instead."""
    bl_idname = 'LNMouseCoordsNode'
    bl_label = 'Mouse Coords (Depreciated)'
    bl_description = "Please use the \"Get Cursor Location\" and \"Get Mouse Movement\" nodes instead"
    bl_icon = 'ERROR'
    arm_version = 2

    def init(self, context):
        super(MouseCoordsNode, self).init(context)
        self.add_output('NodeSocketVector', 'Coords')
        self.add_output('NodeSocketVector', 'Movement')
        self.add_output('NodeSocketInt', 'Wheel')

    def get_replacement_node(self, node_tree: bpy.types.NodeTree):
        if self.arm_version not in (0, 1):
            raise LookupError()

        all_new_nodes = []
        if len(self.outputs[0].links) > 0:
            # "coords": use the cursor coordinates
            newmain = node_tree.nodes.new('LNGetCursorLocationNode')
            new_secondary = node_tree.nodes.new('LNVectorNode')
            node_tree.links.new(newmain.outputs[0], new_secondary.inputs[0])
            node_tree.links.new(newmain.outputs[1], new_secondary.inputs[1])
            for link in self.outputs[0].links:
                node_tree.links.new(new_secondary.outputs[0], link.to_socket)
            all_new_nodes += [newmain, new_secondary]

        if len(self.outputs[1].links) > 0 or len(self.outputs[2].links) > 0:
            # "movement": use the mouse movement
            # "wheel": use data from mouse movement as well
            newmain = node_tree.nodes.new('LNGetMouseMovementNode')
            all_new_nodes.append(newmain)
            if len(self.outputs[1].links) > 0:
                new_secondary = node_tree.nodes.new('LNVectorNode')
                all_new_nodes.append(new_secondary)
                node_tree.links.new(newmain.outputs[0], new_secondary.inputs[0])
                node_tree.links.new(newmain.outputs[1], new_secondary.inputs[1])
                for link in self.outputs[1].links:
                    node_tree.links.new(new_secondary.outputs[0], link.to_socket)

            for link in self.outputs[2].links:
                node_tree.links.new(newmain.outputs[2], link.to_socket)

        return all_new_nodes

add_node(MouseCoordsNode, category='input', section='mouse', is_obsolete=True)
