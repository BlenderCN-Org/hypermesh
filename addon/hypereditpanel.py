import bpy
import bmesh

class HyperEditPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "object"
    bl_label = "Hypercoordinates"

    @classmethod
    def poll(self, context):
        if context.active_object is None:
            return False
        if context.mode != 'EDIT_MESH':
            return False
        ob = context.active_object
        if ob.type != 'MESH':
            return False
        me = ob.data
        return me.hypersettings.hyper

    def draw(self, context):
        me = context.active_object.data
        bm = bmesh.from_edit_mesh(me)
        verts = [v for v in bm.verts if v.select]
        layout = self.layout
        row = layout.row()
        if len(verts) == 0:
            row.label("Nothing selected")
            return

        layx = bm.verts.layers.float['hyperx']
        layy = bm.verts.layers.float['hypery']
        layz = bm.verts.layers.float['hyperz']
        layw = bm.verts.layers.float['hyperw']

        n = len(verts)
        meanx = sum([v[layx] for v in verts]) / n
        meany = sum([v[layy] for v in verts]) / n
        meanz = sum([v[layz] for v in verts]) / n
        meanw = sum([v[layw] for v in verts]) / n
        if n == 1:
            row.label("Vertex:")
        else:
            row.label("Mean:")
        row = layout.row()
        row.label("({0:.6g}, {1:.6g}, {2:.6g}, {3:.6g})".format(meanx, meany, meanz, meanw))