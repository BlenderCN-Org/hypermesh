#!/usr/bin/env python

import unittest
import sys

import bpy
import bmesh
import hypermesh

class TestMakeHyperOperator(unittest.TestCase):
    def test_invocation(self):
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.hyper.makehyper()
        me = bpy.context.active_object.data
        self.assertTrue(me.hypersettings.hyper)
        bpy.ops.object.delete()

    def test_layers(self):
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.hyper.makehyper()
        bm = bmesh.new()
        me = bpy.context.active_object.data
        bm.from_mesh(me)
        bm.verts.layers.float['hyperw']
        bm.verts.layers.float['hyperx']
        bm.verts.layers.float['hypery']
        bm.verts.layers.float['hyperz']
        bpy.ops.object.delete()



if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestMakeHyperOperator)
    success = unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    if not success:
        raise Exception('test failed')

