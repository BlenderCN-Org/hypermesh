#!/usr/bin/env python

import unittest
import bpy
import bmesh


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
        # check whether we can access these
        bm.verts.layers.float['hyperw']
        bm.verts.layers.float['hyperx']
        bm.verts.layers.float['hypery']
        bm.verts.layers.float['hyperz']
        bpy.ops.object.delete()

    def test_preset(self):
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.hyper.makehyper(selected_preset=2)
        self.assertEqual(bpy.context.active_object.data.hypersettings.preset, 2)
        bpy.ops.object.delete()

    def test_creation_hyperpresets(self):
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.hyper.makehyper(selected_preset=1)
        self.assertGreater(len(bpy.context.scene.hyperpresets), 0)
        bpy.ops.object.delete()


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestMakeHyperOperator)
    success = unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    if not success:
        raise Exception('test failed')
