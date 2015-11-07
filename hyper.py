bl_info = {
    "name": "Hypergeometry",
    "description": "Adds tools for manipulating 4-dimensional objects to Blender.",
    "author": "Daan Michiels",
    "version": (0, 1),
    "blender": (2, 75, 0),
    "category": "Object"
}

import bpy
import bmesh
import mathutils
import random
import numpy

def map4to3(hypersettings, p):
    if not hypersettings.perspective:
        print('orthographic not implemented')
        return mathutils.Vector([0,0,0])

    m = numpy.matrix([mathutils.Vector(hypersettings.xvec),
            mathutils.Vector(hypersettings.yvec),
            mathutils.Vector(hypersettings.zvec),
            p - mathutils.Vector(hypersettings.viewcenter) - mathutils.Vector(hypersettings.cameraoffset)])
    m = m.transpose()
    result = numpy.linalg.solve(m, mathutils.Vector(hypersettings.cameraoffset))
    result = result[:3]
    return mathutils.Vector(result)

# q: the position in 3-space
# old: the previous position n 4-space
#      we need this to ensure the new point will be
#      on the same image-parallel hyperplane as the old
#      point
def map3to4(hypersettings, q, old):
    cam = mathutils.Vector(hypersettings.viewcenter) + mathutils.Vector(hypersettings.cameraoffset)
    p = mathutils.Vector(hypersettings.viewcenter) + \
        q.x * mathutils.Vector(hypersettings.xvec) + \
        q.y * mathutils.Vector(hypersettings.yvec) + \
        q.z * mathutils.Vector(hypersettings.zvec)
    m = numpy.matrix([mathutils.Vector(hypersettings.xvec),
            mathutils.Vector(hypersettings.yvec),
            mathutils.Vector(hypersettings.zvec),
            cam - old])
    n = numpy.matrix([mathutils.Vector(hypersettings.xvec),
            mathutils.Vector(hypersettings.yvec),
            mathutils.Vector(hypersettings.zvec),
            cam - p])
    t = numpy.linalg.det(m) / numpy.linalg.det(n)
    return cam + mathutils.Vector(t*(p - cam))

def handler_hypersettings_changed(self, context):
    print('hypersettings changed')
    # we don't know which object had its hypersettings changed
    # and we cannot trust it to be the active one
    # since one could change it through code (!)
    for ob in context.scene.objects:
        if ob.type != 'MESH':
            continue
        if ob.data.hypersettings != self:
            continue
        me = ob.data
        bm = bmesh.new()
        bm.from_mesh(me)
        layx = bm.verts.layers.float['hyperx']
        layy = bm.verts.layers.float['hypery']
        layz = bm.verts.layers.float['hyperz']
        layw = bm.verts.layers.float['hyperw']
        for v in bm.verts:
            newco = map4to3(me.hypersettings, mathutils.Vector([v[layx], v[layy], v[layz], v[layw]]))
            v.co = newco
        bm.to_mesh(me)
        me.update()


def mapFrom3To4(hypersettings, p):
    vc = mathutils.Vector(hypersettings.viewcenter)
    xv = mathutils.Vector(hypersettings.xvec)
    yv = mathutils.Vector(hypersettings.yvec)
    zv = mathutils.Vector(hypersettings.zvec)
    return vc + p.x * xv + p.y * yv + p.z * zv

class HyperSettings(bpy.types.PropertyGroup):
    hyper = bpy.props.BoolProperty(name="Hyper",
            description="Is this object a hyperobject?",
            default=False)
    perspective = bpy.props.BoolProperty(name="Perspective",
            description="Use perspective when mapping to 3-space",
            default = False,
            update = handler_hypersettings_changed)
    viewcenter = bpy.props.FloatVectorProperty(name="View center",
            size=4,
            description="The point in 4-space at the origin of the image plane",
            default=(0.0, 0.0, 0.0, 0.0),
            update = handler_hypersettings_changed)
    cameraoffset = bpy.props.FloatVectorProperty(name="Camera offset",
            size=4,
            description="Vector from the view center to the camera position",
            default=(0.0,0.0,0.0,-4.0),
            update = handler_hypersettings_changed)
    xvec = bpy.props.FloatVectorProperty(name="X vector",
            size=4,
            description="Vector in image plane such that (view center + X vector) is mapped to (1,0,0)",
            default=(1.0, 0.0, 0.0, 0.0),
            update = handler_hypersettings_changed)
    yvec = bpy.props.FloatVectorProperty(name="Y vector",
            size=4,
            description="Vector in image plane such that (view center + Y vector) is mapped to (0,1,0)",
            default=(0.0, 1.0, 0.0, 0.0),
            update = handler_hypersettings_changed)
    zvec = bpy.props.FloatVectorProperty(name="Z vector",
            size=4,
            description="Vector in image plane such that (view center + Z vector) is mapped to (0,0,1)",
            default=(0.0, 0.0, 1.0, 0.0),
            update = handler_hypersettings_changed)

@bpy.app.handlers.persistent
def handler_scene_edited(scene):
    ob = scene.objects.active
    if not ob:
        return
    if not ob.is_updated:
        return
    if not ob.type == 'MESH':
        return
    me = ob.data
    if not me.hypersettings.hyper:
        return
    # We can't actually do this because we'll recurve infinitely
    print('hyperobject updated ' + str(random.random()) + ' -- copying from 3 to 4')

class HyperEditPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "object"
    bl_label = "Hypergeometry"

    @classmethod
    def poll(self, context):
        if context.mode != 'EDIT_MESH':
            return False
        ob = context.active_object
        if ob.type != 'MESH':
            return False
        me = ob.data
        return me.hypersettings.hyper

    def draw(self, context):
        me = context.active_object.data
        bm = bmesh.from_edit_mesh(me)
        verts = [v for v in bm.verts if v.select]
        layout = self.layout
        row = layout.row()
        if len(verts) == 0:
            row.label("Nothing selected")
            return

        layx = bm.verts.layers.float['hyperx']
        layy = bm.verts.layers.float['hypery']
        layz = bm.verts.layers.float['hyperz']
        layw = bm.verts.layers.float['hyperw']

        n = len(verts)
        medianx = sum([v[layx] for v in verts]) / n
        mediany = sum([v[layy] for v in verts]) / n
        medianz = sum([v[layz] for v in verts]) / n
        medianw = sum([v[layw] for v in verts]) / n
        if n == 1:
            row.label("Vertex:")
        else:
            row.label("Median:")
        row = layout.row()
        row.label("({0:.6g}, {1:.6g}, {2:.6g}, {3:.6g})".format(medianx, mediany, medianz, medianw))

class HyperObjectPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "object"
    bl_label = "Hypergeometry"

    @classmethod
    def poll(self, context):
        if context.mode != 'OBJECT':
            return False
        ob = context.active_object
        if not ob:
            return False
        if ob.type != 'MESH':
            return False
        me = ob.data
        return me.hypersettings.hyper

    def draw(self, context):
        me = context.active_object.data
        layout = self.layout
        row = layout.row()
        if not me.hypersettings.hyper:
            layout.operator("hyper.makehyper", text="Make hyper")
            return
        row.prop(me.hypersettings, "perspective")
        row = layout.row()
        row.prop(me.hypersettings, "viewcenter")
        row = layout.row()
        row.prop(me.hypersettings, "cameraoffset")
        row = layout.row()
        row.prop(me.hypersettings, "xvec")
        row = layout.row()
        row.prop(me.hypersettings, "yvec")
        row = layout.row()
        row.prop(me.hypersettings, "zvec")

# This doesn't work in edit mode yet
class Update4Information(bpy.types.Operator):
    bl_idname = "hyper.update4"
    bl_label = "Update 4-dim. positions"

    def execute(self, context):
        print("Updating 4-dim. positions.")
        if context.active_object.type != 'MESH':
            self.report({'ERROR_INVALID_INPUT'}, "Object must be a mesh.")
            return {'FINISHED'}
        me = context.active_object.data
        if not me.hypersettings.hyper:
            self.report({'ERROR_INVALID_INPUT'}, "Object must be hyper.")
            return {'FINISHED'}
        bm = bmesh.new()
        bm.from_mesh(me)
        layx = bm.verts.layers.float['hyperx']
        layy = bm.verts.layers.float['hypery']
        layz = bm.verts.layers.float['hyperz']
        layw = bm.verts.layers.float['hyperw']
        for v in bm.verts:
            old = mathutils.Vector([v[layx], v[layy], v[layz], v[layw]])
            newco = map3to4(me.hypersettings, v.co, old)
            v[layx] = newco.x
            v[layy] = newco.y
            v[layz] = newco.z
            v[layw] = newco.w
        print(bm)
        print(me)
        print(bm.is_wrapped)
        bm.to_mesh(me)
        return {'FINISHED'}

class MakeHyperOperator(bpy.types.Operator):
    bl_idname = "hyper.makehyper"
    bl_label = "Make hyper"

    def execute(self, context):
        print("Make hyper executing.")
        if context.active_object.type != 'MESH':
            self.report({'ERROR_INVALID_INPUT'}, "Object must be a mesh.")
            return {'FINISHED'}
        me = context.active_object.data
        me.hypersettings.hyper = True
        bm = bmesh.new()
        bm.from_mesh(me)
        layx = bm.verts.layers.float.new('hyperx')
        layy = bm.verts.layers.float.new('hypery')
        layz = bm.verts.layers.float.new('hyperz')
        layw = bm.verts.layers.float.new('hyperw')
        for v in bm.verts:
            point = mapFrom3To4(me.hypersettings, v.co)
            v[layx] = point.x
            v[layy] = point.y
            v[layz] = point.z
            v[layw] = point.w
        bm.to_mesh(me)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MakeHyperOperator)
    bpy.utils.register_class(Update4Information)
    bpy.utils.register_class(HyperSettings)
    bpy.types.Mesh.hypersettings = bpy.props.PointerProperty(type=HyperSettings)
    bpy.utils.register_class(HyperObjectPanel)
    bpy.utils.register_class(HyperEditPanel)
    bpy.app.handlers.scene_update_post.append(handler_scene_edited)

def unregister():
    bpy.app.handlers.scene_update_post.remove(handler_scene_edited)
    bpy.utils.unregister_class(HyperEditPanel)
    bpy.utils.unregister_class(HyperObjectPanel)
    bpy.utils.unregister_class(HyperSettings)
    bpy.utils.unregister_class(Update4Information)
    bpy.utils.unregister_class(MakeHyperOperator)
    
    # Is this line ok?
    del bpy.types.Mesh.hypersettings


