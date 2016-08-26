import bpy
import bmesh
from .projections import map3to4
from .hyperpreset import add_presets_to_scene
from mathutils import Vector

class MakeHyperOperator(bpy.types.Operator):
    bl_idname = "hyper.makehyper"
    bl_label = "Make hyper"

    @classmethod
    def poll(cls, context):
        if context.active_object is None:
            return False
        if context.active_object.type != 'MESH':
            return False
        me = context.active_object.data
        if me.hypersettings.hyper:
            return False
        return True

    def execute(self, context):
        me = context.active_object.data
        me.hypersettings.hyper = True
        me["hyperdirty"] = True
        me["justcleaned"] = False
        bm = bmesh.new()
        bm.from_mesh(me)
        bm.verts.layers.float.new('hyperx')
        bm.verts.layers.float.new('hypery')
        bm.verts.layers.float.new('hyperz')
        bm.verts.layers.float.new('hyperw')
        bm.to_mesh(me)
        add_presets_to_scene(context)
        return {'FINISHED'}

