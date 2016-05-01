import bpy
import bmesh
from hypermesh.projections import map4to4
from mathutils import Vector

class UpdateHyperPositions(bpy.types.Operator):
    bl_idname = "hyper.update4"
    bl_label = "Update hyperpositions"

    @classmethod
    def poll(cls, context):
        if context.active_object is None:
            return False
        if context.active_object.type != 'MESH':
            return False
        me = context.active_object.data
        if not me.hypersettings.hyper:
            return False
        return True

    def execute(self, context):
        print("Updating 4-dim. positions.")
        me = context.active_object.data
        if context.mode != 'EDIT_MESH':
            bm = bmesh.new()
            bm.from_mesh(me)
        else:
            bm = bmesh.from_edit_mesh(me)
        layx = bm.verts.layers.float['hyperx']
        layy = bm.verts.layers.float['hypery']
        layz = bm.verts.layers.float['hyperz']
        layw = bm.verts.layers.float['hyperw']
        for v in bm.verts:
            old = Vector([v[layx], v[layy], v[layz], v[layw]])
            newco = map4to4(me.hypersettings, v.co, old)
            v[layx] = newco.x
            v[layy] = newco.y
            v[layz] = newco.z
            v[layw] = newco.w
        print(bm)
        print(me)
        print(bm.is_wrapped)
        if context.mode != 'EDIT_MESH':
            bm.to_mesh(me)
        else:
            bmesh.update_edit_mesh(me)
        return {'FINISHED'}