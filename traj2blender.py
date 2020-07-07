import bpy  
from mathutils import Vector
from mathutils import Quaternion
from math import sqrt
from math import pow

"""
Created by Joakim Bohlin, 2020-05-29

Make sure to import gltf and remove the default cube, and save the .blend file
to the same directory as the trajectory, before running this script.
"""


# Setup path to trajectory
trajPath = bpy.path.abspath("//trajectory.dat")

# Select DNA or RNA
type = 'DNA'

# Select distance between keyframe
# (anything above 1 will interpolate between trajectory steps)
keyframeDist = 1


def bbnsDist(type='DNA'):
    if type is 'DNA':
        return  0.8147053
    elif type is 'RNA':
        return 0.8246211
      
def calcBBPos(x, y, z, a1, a2, a3, type='DNA'):
    bb = Vector()
    if type is 'DNA':
        bb.x = x - (0.34 * a1.x + 0.3408 * a2.x)
        bb.y = y - (0.34 * a1.y + 0.3408 * a2.y)
        bb.z = z - (0.34 * a1.z + 0.3408 * a2.z)
    elif type is 'RNA':
        bb.x = x - (0.4 * a1.x + 0.2 * a3.x)
        bb.y = y - (0.4 * a1.y + 0.2 * a3.y)
        bb.z = z - (0.4 * a1.z + 0.2 * a3.z)
    return bb

bbLast = False
def updatePositions(l, e, type='DNA'):
    global bbLast
    #extract position
    x = float(l[0])
    y = float(l[1])
    z = float(l[2])

    # extract axis vector a1 (backbone vector) and a3 (stacking vector) 
    a1 = Vector((float(l[3]), float(l[4]), float(l[5])))
    a3 = Vector((float(l[6]), float(l[7]), float(l[8])))
    
    # according to base.py a2 is the cross of a1 and a3
    a2 = a1.cross(a3)
    
    # compute backbone position (assume DNA)
    bb = calcBBPos(x, y, z, a1, a2, a3, type)

    # compute nucleoside cm
    ns = Vector((x + 0.4 * a1.x, y + 0.4 * a1.y, z + 0.4 * a1.z))

    # compute nucleoside rotation
    baseRotation = Vector((0, 0, 1)).rotation_difference(a3)

    # compute connector position
    con = Vector(((bb.x + ns.x) / 2, (bb.y + ns.y) / 2, (bb.z + ns.z) / 2))

    # compute connector rotation
    rotationCon = Vector((0, 0, 1)).rotation_difference((con - ns))
    
    # compute connector length
    conLen = bbnsDist()
    if all(v == 0 for v in [a1.x, a1.y, a1.z, a3.z, a3.y, a3.z]):
        conLen = 0

    components = {v.name.split('_')[0]: v for v in e.children}

    # compute sugar-phosphate positions/rotations
    sp = Vector()
    if bbLast and components['bbconnector'].scale != Vector((0, 0, 0)):
        sp.x = (bb.x + bbLast.x) / 2
        sp.y = (bb.y + bbLast.y) / 2
        sp.z = (bb.z + bbLast.z) / 2
        spLen = sqrt(pow(bb.x - bbLast.x, 2) + pow(bb.y - bbLast.y, 2) + pow(bb.z - bbLast.z, 2))
    else:
        sp = bb
        spLen = 0

    spRotation = Vector((0, 0, 1)).rotation_difference((sp - bb).normalized())

    # Update values
    components['backbone'].location = bb
    components['nucleoside'].location = ns
    components['nucleoside'].rotation_quaternion = baseRotation
    components['connector'].location = con
    components['connector'].rotation_quaternion = rotationCon
    components['bbconnector'].location = sp
    components['bbconnector'].rotation_quaternion = spRotation
    components['connector'].scale = Vector((1, 1, conLen))
    if (spLen > 0):
        components['bbconnector'].scale = Vector((1, 1, spLen))
    
    # Insert new keyframes
    components['backbone'].keyframe_insert(data_path="location")
    for name in ['nucleoside', 'connector', 'bbconnector']:
        components[name].keyframe_insert(data_path="location")
        components[name].keyframe_insert(data_path="rotation_quaternion")
    components['connector'].keyframe_insert(data_path="scale")
    components['bbconnector'].keyframe_insert(data_path="scale")
    
    # keep track of last backbone for sugar-phosphate positioning
    bbLast = bb

def loadTrajectory(trajPath, type='DNA', keyframeDist='1'):
    C = bpy.context

    # useful shortcut
    scene = C.scene
    collection = C.collection

    system = scene.objects[0]
    strands = system.children

    elements = {int(e.name.split('_')[1]): e for strand in strands for e in strand.children}

    print("{} elements found.".format(len(elements)))

    frame = 0
    i = 0
    with open(trajPath) as fp:
        for line in fp:
            vals = line.split(' ')
            if vals[0] == 't':
                frame += keyframeDist
                i = 0
                print('Frame {} ({})'.format(frame, line.strip()))
            elif len(vals) == 15:
                e = elements[i]
                scene.frame_set(frame)
                updatePositions(vals, e, type)
                i += 1
    scene.frame_end = frame
    print('Trajectory loading finished')


# Launch script
loadTrajectory(trajPath, type, keyframeDist)
