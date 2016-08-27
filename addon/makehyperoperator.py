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
from .projections import map3to4
from .hyperpreset import add_presets_to_scene
from mathutils import Vector

class MakeHyperOperator(bpy.types.Operator):
    bl_idname = "hyper.makehyper"
    bl_label = "Make hyper"

    @classmethod
    def poll(cls, context):
        if context.active_object is None:
            return False
        if context.active_object.type != 'MESH':
            return False
        me = context.active_object.data
        if me.hypersettings.hyper:
            return False
        return True

    def execute(self, context):
        me = context.active_object.data
        me.hypersettings.hyper = True
        me["hypermesh-dirty"] = True
        me["hypermesh-justcleaned"] = False
        bm = bmesh.new()
        bm.from_mesh(me)
        bm.verts.layers.float.new('hyperx')
        bm.verts.layers.float.new('hypery')
        bm.verts.layers.float.new('hyperz')
        bm.verts.layers.float.new('hyperw')
        bm.to_mesh(me)
        add_presets_to_scene(context)
        return {'FINISHED'}

