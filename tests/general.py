#!/usr/bin/env python

import unittest
import sys

import bpy
import bmesh
import hypermesh

class TestHypermesh(unittest.TestCase):
    def test_enabled(self):
        self.assertIsNotNone(hypermesh.bl_info)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestHypermesh)
    success = unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    if not success:
        raise Exception('test failed')

