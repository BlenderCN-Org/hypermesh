import bpy
import bmesh
from hypermesh.projections import map3to4

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
        print("Make hyper executing.")
        me = context.active_object.data
        me.hypersettings.hyper = True
        bm = bmesh.new()
        bm.from_mesh(me)
        layx = bm.verts.layers.float.new('hyperx')
        layy = bm.verts.layers.float.new('hypery')
        layz = bm.verts.layers.float.new('hyperz')
        layw = bm.verts.layers.float.new('hyperw')
        for v in bm.verts:
            point = map3to4(me.hypersettings, v.co)
            v[layx] = point.x
            v[layy] = point.y
            v[layz] = point.z
            v[layw] = point.w
            print(point)
        bm.to_mesh(me)
        return {'FINISHED'}
