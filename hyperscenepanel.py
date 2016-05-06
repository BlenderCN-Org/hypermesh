import bpy

class preset_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "name", text="", emboss=False)
        elif self.layout_type in {'GRID'}:
            # maybe we should make this something more compact
            layout.prop(item, "name", text="", emboss=False)

class HyperScenePanel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_label = "Hypermesh projections"

    @classmethod
    def poll(self, context):
        return True

    def draw(self, context):
        layout = self.layout
        sc = context.scene
        layout.template_list("preset_list", "notsurewhattoputhere", sc, "hyperpresets", sc, "selectedpreset", type="DEFAULT")
        if len(sc.hyperpresets) < 1:
            return

        pr = sc.hyperpresets[sc.selectedpreset]
        row = layout.row()
        row.prop(pr, "perspective")
        row = layout.row()
        row.prop(pr, "viewcenter")
        row = layout.row()
        row.prop(pr, "cameraoffset")
        row = layout.row()
        row.prop(pr, "xvec")
        row = layout.row()
        row.prop(pr, "yvec")
        row = layout.row()
        row.prop(pr, "zvec")