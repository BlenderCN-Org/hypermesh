import bpy
import bmesh
from hypermesh.projections import map3to4
from mathutils import Vector

class AlignProjectionOperator(bpy.types.Operator):
    bl_idname = "hyper.alignprojection"
    bl_label = "Align hyperprojection"
    bl_options = {'INTERNAL' }

    axes = bpy.props.EnumProperty(items=[
        ('no W', 'No W', 'Use (X,Y,Z)'),
        ('no X', 'No X', 'Use (W,Y,Z)'),
        ('no Y', 'No Y', 'Use (W,X,Z)'),
        ('no Z', 'No Z', 'Use (W,X,Y)'),
        ])

    @classmethod
    def poll(cls, context):
        if context.active_object is None:
            return False
        if context.active_object.type != 'MESH':
            return False
        me = context.active_object.data
        return me.hypersettings.hyper

    def execute(self, context):
        print("Aligning projection.")
        print(self.axes)

        me = context.active_object.data
        h = me.hypersettings
        d = Vector(h.cameraoffset).length

        w = (1.0, 0.0, 0.0, 0.0)
        x = (0.0, 1.0, 0.0, 0.0)
        y = (0.0, 0.0, 1.0, 0.0)
        z = (0.0, 0.0, 0.0, 1.0)

        h.perspective = False
        if self.axes == 'no W':
            h.xvec = x
            h.yvec = y
            h.zvec = z
            h.cameraoffset = tuple(d * t for t in w)
        elif self.axes == 'no X':
            h.xvec = w
            h.yvec = y
            h.zvec = z
            h.cameraoffset = tuple(d * t for t in x)
        elif self.axes == 'no Y':
            h.xvec = w
            h.yvec = x
            h.zvec = z
            h.cameraoffset = tuple(d * t for t in y)
        elif self.axes == 'no Z':
            h.xvec = w
            h.yvec = x
            h.zvec = y
            h.cameraoffset = tuple(d * t for t in z)
        return {'FINISHED'}
