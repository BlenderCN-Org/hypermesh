import bpy
import bmesh
from mathutils import Vector
from hypermesh.projections import map4to3

def handler_hypersettings_changed(self, context):
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
            p = Vector([v[layx], v[layy], v[layz], v[layw]])
            newco = map4to3(me.hypersettings, p)
            v.co = newco
        bm.to_mesh(me)
        me.update()

def get_perspective(self):
    try:
        return self["perspective"]
    except:
        self["perspective"] = False
        return self["perspective"]

def set_perspective(self, value):
    self["perspective"] = value

class HyperSettings(bpy.types.PropertyGroup):
    hyper = bpy.props.BoolProperty(name="Hyper",
            description="Is this object a hyperobject?",
            default=False)
    hyperdirty = bpy.props.BoolProperty(name="Dirty",
            description="Are the 4-coordinates of the vertices dirty?",
            default = True,
            options={'HIDDEN'})
    perspective = bpy.props.BoolProperty(name="Perspective",
            description="Use perspective when mapping to 3-space",
            update = handler_hypersettings_changed,
            get = get_perspective,
            set = set_perspective)
    viewcenter = bpy.props.FloatVectorProperty(name="View center",
            size=4,
            description="The point in 4-space at the origin of the image plane",
            default=(0.0, 0.0, 0.0, 0.0),
            update = handler_hypersettings_changed)
    cameraoffset = bpy.props.FloatVectorProperty(name="Camera offset",
            size=4,
            description="Vector from the view center to the camera position",
            default=(-4.0,0.0,0.0,0.0),
            update = handler_hypersettings_changed)
    xvec = bpy.props.FloatVectorProperty(name="X vector",
            size=4,
            description="Vector in image plane such that (view center + X vector) is mapped to (1,0,0)",
            default=(0.0, 1.0, 0.0, 0.0),
            update = handler_hypersettings_changed)
    yvec = bpy.props.FloatVectorProperty(name="Y vector",
            size=4,
            description="Vector in image plane such that (view center + Y vector) is mapped to (0,1,0)",
            default=(0.0, 0.0, 1.0, 0.0),
            update = handler_hypersettings_changed)
    zvec = bpy.props.FloatVectorProperty(name="Z vector",
            size=4,
            description="Vector in image plane such that (view center + Z vector) is mapped to (0,0,1)",
            default=(0.0, 0.0, 0.0, 1.0),
            update = handler_hypersettings_changed)
