#!/usr/bin/env python

import bpy
import unittest
from hypermesh.projections import map4to3, map3to4
from mathutils import Vector


class TestProjections(unittest.TestCase):
    def test_map4to3(self):
        hp = bpy.context.scene.hyperpresets.add()

        hp.perspective = False
        hp.viewcenter = (0.0, 0.0, 0.0, 1.5)
        hp.xvec = (1.0, 2.0, 0.0, 0.0)
        hp.yvec = (0.0, 1.0, 3.0, 0.0)
        hp.zvec = (0.0, 0.0, 1.0, 0.0)
        hp.cameraoffset = (0.0, 0.0, 1.0, 4.0)
        hp.name = "hey-you're-reading-my-code!"
        projected = map4to3(hp, Vector([1.0, 3.0, 4.0, 1.5]))
        self.assertAlmostEqual(projected[0], 1.0)
        self.assertAlmostEqual(projected[1], 1.0)
        self.assertAlmostEqual(projected[2], 1.0)

        hp.perspective = False
        hp.viewcenter = (0.1, -0.2, 0.0, -0.3)
        hp.xvec = (1.0, 2.0, 0.0, 0.0)
        hp.yvec = (0.0, 1.0, 3.0, 0.0)
        hp.zvec = (0.0, 0.0, 1.0, 0.0)
        hp.cameraoffset = (0.0, 0.0, 1.0, 4.0)
        hp.name = "hey-you're-reading-my-code!"
        projected = map4to3(hp, Vector([1.1, 2.8, 3.0, -4.3]))
        self.assertAlmostEqual(projected[0], 1.0)
        self.assertAlmostEqual(projected[1], 1.0)
        self.assertAlmostEqual(projected[2], 1.0)

        hp.perspective = True
        hp.viewcenter = (0.1, -0.2, 0.0, -0.3)
        hp.xvec = (1.0, 2.0, 0.0, 0.0)
        hp.yvec = (0.0, 1.0, 3.0, 0.0)
        hp.zvec = (0.0, 0.0, 1.0, 0.0)
        hp.cameraoffset = (0.0, 0.0, 1.0, 4.0)
        hp.name = "hey-you're-reading-my-code!"
        projected = map4to3(hp, Vector([4.1, 8.8, 1.0, -4.3]))
        self.assertAlmostEqual(projected[0], 2.0)
        self.assertAlmostEqual(projected[1], 0.5)
        self.assertAlmostEqual(projected[2], -0.5)

    def test_map3to4(self):
        hp = bpy.context.scene.hyperpresets.add()

        hp.perspective = False
        hp.viewcenter = (-10.0, 0.2, 0.0, 5.1)
        hp.xvec = (1.0, 1.0, 0.2, 2.0)
        hp.yvec = (0.0, 1.0, 3.0, 0.0)
        hp.zvec = (-1.0, 0.0, 1.0, -1.0)
        hp.cameraoffset = (0.0, 0.0, 1.0, 4.0)
        hp.name = "hey-you're-reading-my-code!"
        result = map3to4(hp, Vector([1.0, -2.0, 3.0]))
        self.assertAlmostEqual(result[0], -12.0, places=6)
        self.assertAlmostEqual(result[1], -0.8, places=6)
        self.assertAlmostEqual(result[2], -2.8, places=6)
        self.assertAlmostEqual(result[3], 4.1, places=6)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestProjections)
    success = unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    if not success:
        raise Exception('test failed')
