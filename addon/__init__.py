# This file is part of Hypermesh.
#
# Hypermesh is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hypermesh is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hypermesh.  If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Hypermesh",
    "description": "Adds tools for manipulating 4-dimensional meshes to Blender.",
    "author": "Daan Michiels",
    "version": (0, 1),
    "blender": (2, 75, 0),
    "category": "Mesh"
}

if "bpy" in locals(): #we're reloading
    import importlib
    importlib.reload(projections)
    importlib.reload(hypersettings)
    importlib.reload(makehyperoperator)
    importlib.reload(hyperpresetpanel)
    importlib.reload(hypereditpanel)
    importlib.reload(hyperscenepanel)
    importlib.reload(updatehyperpositions)
    importlib.reload(hyperpreset)
else:
    from . import hypersettings
    from . import makehyperoperator
    from . import hyperpresetpanel
    from . import hypereditpanel
    from . import hyperscenepanel
    from . import updatehyperpositions
    from . import hyperpreset

from .hypersettings import HyperSettings
from .makehyperoperator import MakeHyperOperator
from .hyperpresetpanel import HyperPresetPanel
from .hypereditpanel import HyperEditPanel
from .hyperscenepanel import HyperScenePanel
from .updatehyperpositions import UpdateHyperPositions
from .hyperpreset import HyperPreset

import bpy
import random
import sys

@bpy.app.handlers.persistent
def handle_scene_changed(scene):
    for me in bpy.data.meshes:
        if me.is_updated:
            if not me.hypersettings.hyper:
                continue
            try:
                if me["hypermesh-justcleaned"]:
                    me["hypermesh-justcleaned"] = False
                else:
                    me["hypermesh-dirty"] = True
            except KeyError:
                continue

def register():
    print("Registering hypermesh addon... ", end="")
    sys.stdout.flush()
    bpy.utils.register_module(__name__)
    print("done.")

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
    print("Unregistered hypermesh addon.")

if __name__ == "__main__":
    register()
