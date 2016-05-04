bl_info = {
    "name": "Hypermesh",
    "description": "Adds tools for manipulating 4-dimensional meshes to Blender.",
    "author": "Daan Michiels",
    "version": (0, 1),
    "blender": (2, 75, 0),
    "category": "Mesh"
}

if "bpy" in locals():
    import importlib
    importlib.reload(hypermesh.projections)
    importlib.reload(hypermesh.hypersettings)
    importlib.reload(hypermesh.makehyperoperator)
    importlib.reload(hypermesh.alignprojectionoperator)
    importlib.reload(hypermesh.hyperobjectpanel)
    importlib.reload(hypermesh.hypereditpanel)
    importlib.reload(hypermesh.updatehyperpositions)
else:
    import hypermesh.projections
    import hypermesh.hypersettings
    import hypermesh.makehyperoperator
    import hypermesh.alignprojectionoperator
    import hypermesh.hyperobjectpanel
    import hypermesh.hypereditpanel
    import hypermesh.updatehyperpositions

from hypermesh.hypersettings import HyperSettings
from hypermesh.makehyperoperator import MakeHyperOperator
from hypermesh.alignprojectionoperator import AlignProjectionOperator
from hypermesh.hyperobjectpanel import HyperObjectPanel
from hypermesh.hypereditpanel import HyperEditPanel
from hypermesh.updatehyperpositions import UpdateHyperPositions

import bpy
import random

@bpy.app.handlers.persistent
def handle_scene_changed(scene):
    for me in bpy.data.meshes:
        if me.is_updated:
            print("Mesh changed ({}, {}, {}).".format(me.name, me.is_updated_data, random.random()))
            if not me.hypersettings.hyper:
                continue
            try:
                # we need this to avoid infinite recursion with the scene updates
                if not me["hyperdirty"]:
                    me["hyperdirty"] = True
            except KeyError:
                continue

def register():
    print("Registering!")
    bpy.utils.register_module(__name__)
    bpy.types.Mesh.hypersettings = bpy.props.PointerProperty(type=HyperSettings)
    bpy.app.handlers.scene_update_post.append(handle_scene_changed)

def unregister():
    bpy.app.handlers.scene_update_post.remove(handle_scene_changed)
    del bpy.types.Mesh.hypersettings
    bpy.utils.unregister_module(__name__)
    print("Unregistered!")

if __name__ == "__main__":
    register()
