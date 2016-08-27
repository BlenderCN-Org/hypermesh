---
title: "Hypermesh: internals"
layout: default
---

# Internal workings of the hypermesh addon

The Blender hypermesh addon allows the manipulation of meshes in 4-dimensional Euclidean space.
This is achieved by using ordinary Blender tools to manipulate _projections_ of this 4-mesh
to 3-dimensional Euclidean space.

This document described the internal working of the hypermesh addon.
It is not intended for end users, but as a document to help in understanding the code.

{::options toc_levels="2..6" /}
* this is where the TOC will be
{:toc}

## Overview

When the hypermesh plugin is loaded, the following extra information is kept track of:

 - Every scene holds a list of projections from 4-space to 3-space.
 - Every mesh holds a `HyperSettings` object, which keeps track of
     * whether the mesh is a 4-mesh (_hypermesh_) or an ordinary mesh (unaffected by the addon),
     * which projection from the scene's list is currently in use for this mesh.

When a mesh is turned into a hypermesh (by the `MakeHyperOperator`),
or when a hypermesh is inserted directly,
the Bmesh data underlying it contains 4 extra layers of floating point vertex information.
These layers are called `hyperx`, `hypery`, `hyperz`, `hyperw`, and they contain the
coordinates of the vertex in 4-space.

Of course, the ordinary 3-coordinates are related to these 4 hypercoordinates by means
of the projection used.
To ensure that this relation is maintained at all times, the following actions have to be undertaken:

 - when a vertex is moved in 3-space (standard Blender edit mode),
   its coordinates in 4-space should be updated
 - when a vertex is moved in 4-space (entering straight into a box provided by the addon),
   its coordinates in 3-space should be updated
 - when the projection is changed,
   its coordinates in 3-space should be updated

It should be noted that this is **not** what the addon does.
For performance reasons, it doesn't update the 4-coordinates automatically
whenever the 3-coordinates change. Rather, it marks the 4-coordinates as needing
an update by setting the mesh's `hypermesh-dirty` property to `True`.
Then whenever the 4-coordinates are needed (for example, when the 3-coordinates need to be
updated based on their value, or when they need to be shown in the UI),
they are updated (and `hypermesh-dirty` is set to `False`).

These are the essential workings of the addon.


## File structure

### \_\_init\_\_.py

The starting point of the plugin.
It does the following things:

 - populates `bl_info`, which is read by Blender to provide information about the plugin,
 - (re)imports the other files
 - (un)registers the addon's classes (such as Operators, Properties) with Blender
 - defines and registers a callback handler for `scene_update_post`; this is used to detect when a
   mesh has been edited

When a mesh has been edited in such a way that its 4-coordinates are no longer valid,
the mesh's `hypermesh-dirty` property should be set to `True`.
To achieve this, the code that updates 4-coordinates sets the mesh's `hypermesh-justcleaned` property,
indicating that an update has happened but the 4-coordinates are not dirty.


### hypereditpanel.py

The UI panel that is visible when editing a mesh (edit mode in the 3D view).


### hyperpreset.py

A `HyperPreset` is a `PropertyGroup` that contains the information defining a projection from 4-space
to 3-space.
(It's a list of these that the scene keeps track of.)
It also contains code that handles projection changes (by updating all meshes that use this projection).
Finally, it contains code that defines several standard projections from 4-space to 3-space.
These are projections that are probably useful in manipulating 4-meshes.


### hyperpresetpanel.py

Panel that is shown when a mesh is selected to pick which projection to use.
Selecting a projection here sets the selected object's projection.


### hyperscenepanel.py

Panel that is shown in the scene's properties listing all the projections
that exist in the scene.
Allows editing of projections.


### hypersettings.py

A `HyperSettings` object is a `PropertyGroup` that is associated to each mesh,
indicating whether the mesh is a hypermesh, and which projection is in use.
Also contains code to update a mesh when a different projection is picked.


### inserthypercubeoperator.py

Operator that inserts a hypercube into the scene.


### makehyperoperator.py

Operator that turns an existing mesh into a hypermesh.


### projections.py

This file contains the mathematical transformations relating 3-space to 4-space.


### updatehyperpositions.py

Operator that updates the 4-dimensional positions of a mesh's vertices on demand.
Call this operator if you want to see the correct hypercoordinates of your selection
in edit mode.


## Where's the data?

The addon stores several pieces of data when in use (hypercoordinates, presets, ...).
The following provides an overview of all these pieces of data.


### Data associated to meshes

The following pieces of information are stored for meshes:

 - for every mesh, a `HyperSettings` object (called `me.hypersettings` where `me` is the mesh)
 - for every hypermesh, four extra layers of floating point information per vertex (`hyperx`,
   `hypery`, `hyperz`, `hyperw`); these can be accessed from the mesh's Bmesh data
 - for every hypermesh, booleans `me["hypermesh-dirty"]` and `me["hypermesh-justcleaned"]`
   for keeping track of whether hypercoordinates need to be updated (where `me` is the mesh)

About storage in the `.blend`:
as far as I can tell, no `HyperSettings` object is written to the `.blend` unless
it is set at some point in time. For non-hyper-meshes, the `HyperSettings` are never written
to (they stay at the default), so I don't think that these meshes take up extra space in the
`.blend` when the addon is enabled.


### Data associated to scenes

The following pieces of information are stored for scenes:

 - for each scene, a collection of `HyperPreset`s (called `sc.hyperpresets` where `sc` is the scene)
 - for each scene, an `IntProperty` called `sc.selectedpreset`; it indicates which preset is currently
   selected in the scene's properties; this property is not written to the `.blend`



