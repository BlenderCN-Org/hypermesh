# Using the hypermesh addon

The Blender hypermesh addon allows the manipulation of meshes in 4-dimensional Euclidean space.
This is achieved by using ordinary Blender tools to manipulate _projections_ of this 4-mesh
to 3-dimensional Euclidean space.

This is the user guide for the addon.
It is intended for anybody who wants to _use_ the hypermesh addon.
If you want to understand (or work on) the code, please read this document and also the
file `internals.md`.


## Math

This section describes the mathematics underlying the addon.
It is recommended that you read this section to understand the exact behavior of the addon.
The mathematical concepts will be illustrated using pictures in one dimension lower
(so the pictures show how the analogous addon would work for manipulating 3-dimensional meshes
using software than handles 2-dimensional meshes).

### Projecting from 4-space to 3-space

The meshes that are handles by the addon are meshes living in 4-dimensional Euclidean space.
These meshes have

 - vertices: each vertex has a position given by 4 floating point numbers
 - edges: an edge connects two vertices
 - faces: a face spans several edges

This is just like an ordinary Blender mesh, except that vertices have 4 coordinates.
The addon does **not** handle hyperfaces, 3-dimensional faces of 4-dimensional meshes.
(Such hyperfaces would overlap after projection to 3-space. There are
currently no plans to every support hyperfaces.)

A hypermesh is visualized in the 3D view by _projecting_ it to 3-dimensional Euclidean
space (the same way that 3-dimensional objects in the viewport are visualized by projecting
onto a flat monitor for most users -- so, really, the 4-meshes are projected to 3-space
and then to 2-space, and that's what you see).

The following picture illustrates such a projection.

![Projecting a point from 3-space to 2-space.](projection.png?raw=true)


## Creating a hypermesh

By default, the addon does not affect any of Blender's mesh operations.
Only the meshes that are explicitly marked as _hypermeshes_ will be treated by the addon.

To turn an existing mesh into a hypermesh, use the `Make hyper` operator.

