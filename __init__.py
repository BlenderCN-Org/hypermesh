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
    importlib.reload(hypermesh.hyperpresetpanel)
    importlib.reload(hypermesh.hypereditpanel)
    importlib.reload(hypermesh.hyperscenepanel)
    importlib.reload(hypermesh.updatehyperpositions)
    importlib.reload(hypermesh.hyperpreset)
else:
    import hypermesh.projections
    import hypermesh.hypersettings
    import hypermesh.makehyperoperator
    import hypermesh.hyperpresetpanel
    import hypermesh.hypereditpanel
    import hypermesh.hyperscenepanel
    import hypermesh.updatehyperpositions
    import hypermesh.hyperpreset

from hypermesh.hypersettings import HyperSettings
from hypermesh.makehyperoperator import MakeHyperOperator
from hypermesh.hyperpresetpanel import HyperPresetPanel
from hypermesh.hypereditpanel import HyperEditPanel
from hypermesh.hyperscenepanel import HyperScenePanel
from hypermesh.updatehyperpositions import UpdateHyperPositions
from hypermesh.hyperpreset import HyperPreset

import bpy
import random

@bpy.app.handlers.persistent
def handle_scene_changed(scene):
    for me in bpy.data.meshes:
        if me.is_updated:
            if not me.hypersettings.hyper:
                continue
            try:
                if me["justcleaned"]:
                    me["justcleaned"] = False
                else:
                    me["hyperdirty"] = True
            except KeyError:
                continue

def register():
    print("Registering!")
    bpy.utils.register_module(__name__)
    print("Module registered.")
    bpy.types.Mesh.hypersettings = bpy.props.PointerProperty(type=HyperSettings)
    bpy.types.Scene.hyperpresets = bpy.props.CollectionProperty(type=HyperPreset)
    bpy.types.Scene.selectedpreset = bpy.props.IntProperty(options={'HIDDEN', 'SKIP_SAVE'})
    bpy.app.handlers.scene_update_post.append(handle_scene_changed)

def unregister():
    bpy.app.handlers.scene_update_post.remove(handle_scene_changed)
    del bpy.types.Scene.selectedpreset
    del bpy.types.Scene.hyperpresets
    del bpy.types.Mesh.hypersettings
    bpy.utils.unregister_module(__name__)
    print("Unregistered!")

if __name__ == "__main__":
    register()
