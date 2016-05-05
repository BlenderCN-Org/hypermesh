import bpy

class HyperObjectPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "object"
    bl_label = "Hypermesh"

    @classmethod
    def poll(self, context):
        if context.active_object is None:
            return False
        if context.mode != 'OBJECT':
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
        layout.template_list("preset_list", "notsurewhattoputhere", context.scene, "hyperpresets", context.scene, "currentpreset")
        row = layout.row()
        row.prop(me.hypersettings, "preset")
        #row = layout.row()
        #row.prop(me.hypersettings, "viewcenter")
        #row = layout.row()
        #row.prop(me.hypersettings, "cameraoffset")
        #row = layout.row()
        #row.prop(me.hypersettings, "xvec")
        #row = layout.row()
        #row.prop(me.hypersettings, "yvec")
        #row = layout.row()
        #row.prop(me.hypersettings, "zvec")
        #row = layout.row(align=True)
        #row.operator('hyper.alignprojection', text='No W').axes = 'no W'
        #row.operator('hyper.alignprojection', text='No X').axes = 'no X'
        #row.operator('hyper.alignprojection', text='No Y').axes = 'no Y'
        #row.operator('hyper.alignprojection', text='No Z').axes = 'no Z'