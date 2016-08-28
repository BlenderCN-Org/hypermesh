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

import bpy
import bmesh
from .projections import map4to4
from mathutils import Vector

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

        h = context.scene.hyperpresets[me.hypersettings.preset]

        layx = bm.verts.layers.float['hyperx']
        layy = bm.verts.layers.float['hypery']
        layz = bm.verts.layers.float['hyperz']
        layw = bm.verts.layers.float['hyperw']

        meanx = 0
        meany = 0
        meanz = 0
        meanw = 0
        for v in verts:
            old = Vector([v[layx], v[layy], v[layz], v[layw]])
            newco = map4to4(h, v.co, old)
            v[layx] = newco.x
            v[layy] = newco.y
            v[layz] = newco.z
            v[layw] = newco.w
            meanx += newco.x
            meany += newco.y
            meanz += newco.z
            meanw += newco.w
        bmesh.update_edit_mesh(me)

        n = len(verts)
        meanx /= n
        meany /= n
        meanz /= n
        meanw /= n
        
        if n == 1:
            row.label("Vertex:")
        else:
            row.label("Mean:")
        row = layout.row()
        row.label("({0:.6g}, {1:.6g}, {2:.6g}, {3:.6g})".format(meanx, meany, meanz, meanw))