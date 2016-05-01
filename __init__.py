bl_info = {
    "name": "Hypermesh",
    "description": "Adds tools for manipulating 4-dimensional objects to Blender.",
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

#from hypermesh.projections import map4to3, map3to4
from hypermesh.hypersettings import HyperSettings
from hypermesh.makehyperoperator import MakeHyperOperator
from hypermesh.alignprojectionoperator import AlignProjectionOperator
from hypermesh.hyperobjectpanel import HyperObjectPanel
from hypermesh.hypereditpanel import HyperEditPanel
from hypermesh.updatehyperpositions import UpdateHyperPositions

import bpy

def register():
    print("Registering!")
    bpy.utils.register_module(__name__)
    bpy.types.Mesh.hypersettings = bpy.props.PointerProperty(type=HyperSettings)

def unregister():
    del bpy.types.Mesh.hypersettings
    bpy.utils.unregister_module(__name__)
    print("Unregistered!")

if __name__ == "__main__":
    register()
