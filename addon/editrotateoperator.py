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
from mathutils import Vector
from math import pi, sin, cos
from .hypermeshpreferences import debug_message

class EditRotateOperator(bpy.types.Operator):
    bl_idname = "hyper.editrotateoperator"
    bl_label = "Rotate in 4D"

    def execute(self, context):
        debug_message("Executing EditRotateOperator")

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            debug_message("Mousemove")
            self.execute(context)
        elif event.type == 'LEFTMOUSE':
            return {'FINISHED'}
        elif event.type in ('RIGHTMOUSE', 'ESC'):
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.valuex = event.mouse_x
        self.valuey = event.mouse_y
        debug_message(str(event))
        context.window_manager.modal_handler_add(self)
        debug_message(str(self.valuex) + " " + str(self.valuey))
        return {'RUNNING_MODAL'}
        