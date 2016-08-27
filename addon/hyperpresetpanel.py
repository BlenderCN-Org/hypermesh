import bpy

class HyperPresetPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "object"
    bl_label = "Hypermesh projection"

    @classmethod
    def poll(self, context):
        if context.active_object is None:
            return False
        ob = context.active_object
        if ob.type != 'MESH':
            return False
        return True

    def draw(self, context):
        me = context.active_object.data
        layout = self.layout
        row = layout.row()
        if not me.hypersettings.hyper:
            layout.operator("hyper.makehyper", text="Make hyper")
            return
        layout.template_list("preset_list", "notsurewhattoputhere", context.scene, "hyperpresets", me.hypersettings, "preset")

