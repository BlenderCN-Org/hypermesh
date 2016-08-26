import bpy
import bmesh
from mathutils import Vector
from .projections import map4to3
from .updatehyperpositions import clean_mesh
from .hyperpreset import project_to_3d

def find_dirty_meshes_with_given_hypersettings(h):
    meshes = []
    for me in bpy.data.meshes:
        if not me.hypersettings.hyper:
            continue
        if not me.hypersettings == h:
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

def get_preset(self):
    try:
        return self["preset"]
    except KeyError:
        self["preset"] = 0
        return self["preset"]

def set_preset(self, value):
    dirties = find_dirty_meshes_with_given_hypersettings(self)
    for me in dirties:
        clean_mesh(me)
    self["preset"] = value
    for me in bpy.data.meshes:
        if not me.hypersettings.hyper:
            continue
        if not me.hypersettings == self:
            continue
        me["hyperdirty"] = False
        me["justcleaned"] = True
        project_to_3d(me) #this will trigger handle_scene_changed

class HyperSettings(bpy.types.PropertyGroup):
    hyper = bpy.props.BoolProperty(name="Hyper",
            description="Is this object a hyperobject?",
            default=False)
    preset = bpy.props.IntProperty(name="Projection preset",
            description="Which projection from 4-space to 3-space to use",
            min=0,
            max=3,
            get=get_preset,
            set=set_preset)

