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
from .hyperpreset import ensure_scene_is_hyper

class InsertHyperCubeOperator(bpy.types.Operator):
    bl_idname = "hyper.inserthypercube"
    bl_label = "Insert hypercube"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        sc = bpy.context.scene
        ensure_scene_is_hyper(sc)

        me = bpy.data.meshes.new("Hypercube")
        me.hypersettings.hyper = True
        me["hypermesh-dirty"] = False
        me["hypermesh-justcleaned"] = True

        bm = bmesh.new()
        bm.from_mesh(me)
        layx = bm.verts.layers.float.new('hyperx')
        layy = bm.verts.layers.float.new('hypery')
        layz = bm.verts.layers.float.new('hyperz')
        layw = bm.verts.layers.float.new('hyperw')

        for i in range(16):
            v = bm.verts.new((0,0,0))
            v[layx] = ((i & 0x01) << 1) - 1;
            v[layy] = ((i & 0x02) << 0) - 1;
            v[layz] = ((i & 0x04) >> 1) - 1;
            v[layw] = ((i & 0x08) >> 2) - 1;

        bm.verts.ensure_lookup_table()

        for i in range(16):
            for j in [0x01, 0x02, 0x04, 0x08]:
                k = i | j
                if k != i:
                    bm.edges.new((bm.verts[i], bm.verts[k]))

        bm.to_mesh(me)

        ob = bpy.data.objects.new("Hypercube", me)
        sc.objects.link(ob)
        sc.objects.active = ob
        ob.select = True

        # triggers a projection to 3D
        me.hypersettings.preset = 0

        return {'FINISHED'}

