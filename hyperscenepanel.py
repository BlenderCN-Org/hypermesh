import bpy
import pickle

class HyperScenePanel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_label = "Hypermesh projections"

    @classmethod
    def poll(self, context):
        if "hyperprojections" in context.scene.keys():
            return True
        else:
            return False

    def draw(self, context):
        layout = self.layout
        presets = pickle.loads(context.scene["hyperprojections"])
        for p in presets:
            row = layout.row()
            row.label(p.name)