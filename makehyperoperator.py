import bpy
import bmesh
from hypermesh.projections import map3to4
from mathutils import Vector
import pickle

class HyperPreset():

    def __init__(self, builtin = 'noW'):
        self.perspective = False
        self.viewcenter = (0.0, 0.0, 0.0, 0.0)
        w = (1.0, 0.0, 0.0, 0.0)
        x = (0.0, 1.0, 0.0, 0.0)
        y = (0.0, 0.0, 1.0, 0.0)
        z = (0.0, 0.0, 0.0, 1.0)
        if builtin == 'noX':
            self.xvec = w
            self.yvec = y
            self.zvec = z
            self.cameraoffset = w
            self.name = "No X"
        elif builtin == 'noY':
            self.xvec = w
            self.yvec = x
            self.zvec = z
            self.cameraoffset = y
            self.name = "No Y"
        elif builtin == 'noZ':
            self.xvec = w
            self.yvec = x
            self.zvec = y
            self.cameraoffset = z
            self.name = "No Z"
        else:
            self.xvec = x
            self.yvec = y
            self.zvec = z
            self.cameraoffset = w
            self.name = "No W"

def add_presets_to_scene(context):
    if "hyperprojections" in context.scene.keys():
        return
    presets = [HyperPreset(builtin='noW'),
            HyperPreset(builtin='noX'),
            HyperPreset(builtin='noY'),
            HyperPreset(builtin='noZ')]
    context.scene["hyperprojections"] = pickle.dumps(presets)
    print(context.scene["hyperprojections"])

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

        add_presets_to_scene(context)

        me = context.active_object.data
        me.hypersettings.hyper = True
        me["hyperdirty"] = True
        bm = bmesh.new()
        bm.from_mesh(me)
        bm.verts.layers.float.new('hyperx')
        bm.verts.layers.float.new('hypery')
        bm.verts.layers.float.new('hyperz')
        bm.verts.layers.float.new('hyperw')
        bm.to_mesh(me)
        return {'FINISHED'}

