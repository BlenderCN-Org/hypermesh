from mathutils import Vector
import numpy

# variable names: h   for hypersettings
#                 p,q for points in 4-space
#                 a,b for points in 3-space


# input is a HyperPreset object, and a Vector
def map4to3(h, p):
    if h.perspective:
        direction = p - Vector(h.viewcenter) - Vector(h.cameraoffset)
    else:
        direction = Vector(h.cameraoffset)
    m = numpy.matrix([Vector(h.xvec),
            Vector(h.yvec),
            Vector(h.zvec),
            direction])
    m = m.transpose()
    result = numpy.linalg.solve(m, p - Vector(h.viewcenter))
    result = result[:3]
    return Vector(result)

# input is a HyperPreset object, and a Vector
def map3to4(h, a):
    vc = Vector(h.viewcenter)
    xv = Vector(h.xvec)
    yv = Vector(h.yvec)
    zv = Vector(h.zvec)
    return vc + a.x * xv + a.y * yv + a.z * zv

# input is a HyperPreset object, the 3-dimensional position
# and the previous 4-dimensional position
# TODO: write this
def map4to4(h, a, p):
    a4 = map3to4(h, a)
    q = map3to4(h, map4to3(h, p))
    if h.perspective:
        cam = Vector(h.viewcenter) + Vector(h.cameraoffset)
        factor = (p - cam).length / (q - cam).length
    else:
        factor = 1.0
    return p + factor * (a4 - q)
