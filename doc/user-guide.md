# Using the hypermesh addon

The Blender hypermesh addon allows the manipulation of meshes in 4-dimensional Euclidean space.
This is achieved by using ordinary Blender tools to manipulate _projections_ of this 4-mesh
to 3-dimensional Euclidean space.

This is the user guide for the addon.
It is intended for anybody who wants to _use_ the hypermesh addon.
If you want to understand (or work on) the code, please read this document and also the
file `internals.md`.


## Creating a hypermesh

By default, the addon does not affect any of Blender's mesh operations.
Only the meshes that are explicitly marked as _hypermeshes_ will be treated by the addon.

To turn an existing mesh into a hypermesh, use the `Make hyper` operator.

