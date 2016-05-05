import bpy
import bmesh
from hypermesh.updatehyperpositions import clean_mesh
from hypermesh.projections import map4to3
from mathutils import Vector

def project_to_3d(me):
    h = bpy.context.scene.hyperpresets[me.hypersettings.preset]
    if me.is_editmode:
        bm = bmesh.from_edit_mesh(me)
    else:
        bm = bmesh.new()
        bm.from_mesh(me)
    layx = bm.verts.layers.float['hyperx']
    layy = bm.verts.layers.float['hypery']
    layz = bm.verts.layers.float['hyperz']
    layw = bm.verts.layers.float['hyperw']
    for v in bm.verts:
        p = Vector([v[layx], v[layy], v[layz], v[layw]])
        newco = map4to3(h, p)
        v.co = newco
    if me.is_editmode:
        bmesh.update_edit_mesh(me)
    else:
        bm.to_mesh(me)
    me.update()

def find_dirty_meshes_with_given_hyperpreset(pr):
    meshes = []
    for me in bpy.data.meshes:
        if not me.hypersettings.hyper:
            continue
        if not bpy.context.scene.hyperpresets[me.hypersettings.preset] == pr:
            continue
        try:
            if me["hyperdirty"]:
                dirty = True
            else:
                dirty = False
        except KeyError:
            dirty = False
        if dirty:
            meshes.append(me)
    return meshes

def get_perspective(self):
    try:
        return self["perspective"]
    except KeyError:
        self["perspective"] = False
        return self["perspective"]

def set_perspective(self, value):
    print('enter set_perspective')
    dirties = find_dirty_meshes_with_given_hyperpreset(self)
    for me in dirties:
        clean_mesh(me)
    self["perspective"] = value
    for me in bpy.data.meshes:
        if not me.hypersettings.hyper:
            continue
        if not bpy.context.scene.hyperpresets[me.hypersettings.preset] == self:
            continue
        print('projecting right after this')
        project_to_3d(me)
        me["hyperdirty"] = False #important
    print('exit set_perspective')

class HyperPreset(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="Name",
            description="Name of the projection",
            default="AwesomeProjection")
    perspective = bpy.props.BoolProperty(name="Perspective",
            description="Use perspective when mapping to 3-space",
            get=get_perspective,
            set=set_perspective)
    viewcenter = bpy.props.FloatVectorProperty(name="View center",
            size=4,
            description="The point in 4-space at the origin of the image plane",
            default=(0.0, 0.0, 0.0, 0.0))
    cameraoffset = bpy.props.FloatVectorProperty(name="Camera offset",
            size=4,
            description="Vector from the view center to the camera position",
            default=(-4.0,0.0,0.0,0.0))
    xvec = bpy.props.FloatVectorProperty(name="X vector",
            size=4,
            description="Vector in image plane such that (view center + X vector) is mapped to (1,0,0)",
            default=(0.0, 1.0, 0.0, 0.0))
    yvec = bpy.props.FloatVectorProperty(name="Y vector",
            size=4,
            description="Vector in image plane such that (view center + Y vector) is mapped to (0,1,0)",
            default=(0.0, 0.0, 1.0, 0.0))
    zvec = bpy.props.FloatVectorProperty(name="Z vector",
            size=4,
            description="Vector in image plane such that (view center + Z vector) is mapped to (0,0,1)",
            default=(0.0, 0.0, 0.0, 1.0))

# set a hyperpreset to a builtin preset
# what is meant by builtin? Well, anything that's given by this function...
def set_to_builtin_preset(hyperpreset, builtin = 'noW'):
    hyperpreset.perspective = False
    hyperpreset.viewcenter = (0.0, 0.0, 0.0, 0.0)
    w = (1.0, 0.0, 0.0, 0.0)
    x = (0.0, 1.0, 0.0, 0.0)
    y = (0.0, 0.0, 1.0, 0.0)
    z = (0.0, 0.0, 0.0, 1.0)
    if builtin == 'noX':
        hyperpreset.xvec = w
        hyperpreset.yvec = y
        hyperpreset.zvec = z
        hyperpreset.cameraoffset = tuple([5 * t for t in x])
        hyperpreset.name = "No X"
    elif builtin == 'noY':
        hyperpreset.xvec = w
        hyperpreset.yvec = x
        hyperpreset.zvec = z
        hyperpreset.cameraoffset = tuple([5 * t for t in y])
        hyperpreset.name = "No Y"
    elif builtin == 'noZ':
        hyperpreset.xvec = w
        hyperpreset.yvec = x
        hyperpreset.zvec = y
        hyperpreset.cameraoffset = tuple([5 * t for t in z])
        hyperpreset.name = "No Z"
    else:
        hyperpreset.xvec = x
        hyperpreset.yvec = y
        hyperpreset.zvec = z
        hyperpreset.cameraoffset = tuple([5 * t for t in w])
        hyperpreset.name = "No W"

def add_presets_to_scene(context):
    hps = context.scene.hyperpresets
    if len(hps) > 0:
        return
    hps.add()
    hps.add()
    hps.add()
    hps.add()
    set_to_builtin_preset(hps[0], 'noW')
    set_to_builtin_preset(hps[1], 'noX')
    set_to_builtin_preset(hps[2], 'noY')
    set_to_builtin_preset(hps[3], 'noZ')

