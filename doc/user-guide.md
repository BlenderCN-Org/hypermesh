# Hypermesh addon user guide

The Blender hypermesh addon allows the manipulation of meshes in 4-dimensional Euclidean space.
This is achieved by using ordinary Blender tools to manipulate _projections_ of this 4-mesh
to 3-dimensional Euclidean space.

This is the user guide for the addon.
It is intended for anybody who wants to _use_ the hypermesh addon.
If you want to understand (or work on) the code, please read this document and also the
file `internals.md`.

## Installation

There are two ways of installing the addon:

 - The recommended option is to download/clone the repository, and run the script `package.py`.
   This will zip up the contents of the `addon` folder into a file called `hypermesh.zip`
   (and do some useful renaming).
   You can then install the addon using Blender's `File -> User Preferences... -> Install from File...`.

 - Alternatively, you can manually copy the addon into the Blender addons folder.
   To find out where it is located on your system, [consult Blender's documentation](https://www.blender.org/manual/getting_started/installing/configuration/directories.html).
   Most likely, it is `[Blender config directory]/scripts/addons/`.

   Make sure the addon gets its own folder.
   The recommended name for the addon's folder is `hypermesh`,
   so that you get files `[Blender config directory]/scripts/addons/hypermesh/__init__.py`
   and so on.

Don't forget to also _enable_ the addon in the user settings.

To remove the addon, you can use the _Remove_ button in Blender's user preferences,
or just delete the directory that the addon was installed in (typically `[Blender config directory]/scripts/addons/hypermesh/`).


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
currently no plans to ever support hyperfaces.)

A hypermesh is visualized in the 3D view by _projecting_ it to 3-dimensional Euclidean
space (the same way that 3-dimensional objects in the viewport are visualized by projecting
onto a flat monitor for most users — so, really, the 4-meshes are projected to 3-space
and then to 2-space, and that's what you see).

The following picture illustrates such a projection.

![Projecting a point from 3-space to 2-space.](projection.png?raw=true)

The 3-dimensional space is projected to the 2-dimensional space represented by the semi-transparent plane.
At the center of this plane is a black dot known as the _view center_.
The camera position is the other black dot.
The picture shows the projection of the white dot to the plane.

 - If the projection is _perspective_, the projection of the white dot onto the plane is
   the red dot on the yellow line (the line connecting the camera and the point to be projected).
 - If the projection is _not perspective_, the projection of the white dot onto the plane is
   the red dot on the green line (the green line is parallel to the purple one connecting camera and
   view center).

What the addon does is the analogous operation from 4-space to 3-space.
The following parameters describe a projection:

 - `View center`: the origin of the 3-space that we are projecting to
   (the rightmost black dot in the picture)
 - `Camera offset`: the vector from the `viewcenter` to the camera's position
   (purple and pointing to the left in the picture)
 - `X vector`: the vector such that (view center + x vector) is projected to (1,0,0)
   (blue and pointing to the lower right in the picture)
 - `Y vector`: the vector such that (view center + y vector) is projected to (0,1,0)
   (orange and pointing up in the picture)
 - `Z vector`: the vector such that (view center + z vector) is projected to (0,0,1)
   (missing from the picture because there's a dimension missing)
 - `Perspective`: whether to project using perspective or not

In the picture above, the white point gets mapped to about (0.4, -0.2) in the perspective case,
and to about (0.8, -0.3) in the non-perspective case.


### Updating hyperposition after mesh edit

When the hyperposition of a vertex is changed, it is re-projected and the 3D view shows
the updated projection.
This is straightforward.
However, when the _projection_ of the vertex is manipulated, updating its hyperposition
is ambiguous: there are infinitely many points in 4-space that project to the given point.
To resolve this ambiguity, the addon does the following: _when a vertex is moved in 3-space,
the underlying point in 4-space moves **parallel** to the projection 3-space_.


## Using the addon

### Creating a hypermesh

By default, the addon does not affect any of Blender's mesh operations.
Only the meshes that are explicitly marked as _hypermeshes_ will be treated by the addon.

To turn an existing mesh into a hypermesh, use the `Make hyper` operator.

