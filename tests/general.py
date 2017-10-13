#!/usr/bin/env python

import unittest

import bpy
import bmesh
import hypermesh

class TestHypermesh(unittest.TestCase):
    def test_enabled(self):
        self.assertIsNotNone(hypermesh.bl_info)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestHypermesh)
    unittest.TextTestRunner(verbosity=2).run(suite)

