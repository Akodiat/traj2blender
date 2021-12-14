import bpy
import numpy as np
from mathutils import Vector
import sys
bpy.app.debug = True

# Select topology and trajectory paths
topPath = bpy.path.abspath("/home/joakim/Downloads/robot_sim/T_0.01/init.top")
trajPath = bpy.path.abspath("/home/joakim/Downloads/robot_sim/T_0.01/trajectory.dat")

# Select distance between keyframe
# (anything above 1 will interpolate between trajectory steps)
keyframeDist = 10

def insert_keyframe(fcurves, frame, values):
    for fcu, val in zip(fcurves, values):
        fcu.keyframe_points.insert(frame, val, options={'FAST'})

def loadTrajectory(trajPath, topPath, keyframeDist='1'):
    C = bpy.context

    # useful shortcut
    scene = C.scene
    collection = C.collection
    
    with open(topPath) as f:
        nElements = int(f.readline().split(' ')[0])
        #nElements = len([line for line in fp]) - 1

    print("{} elements found".format(nElements))

    verts = [Vector() for p in range(nElements)]

    # add object to blender
    obj_name = bpy.path.display_name(trajPath)
    mesh_data = bpy.data.meshes.new(obj_name + "_data")
    obj = bpy.data.objects.new(obj_name, mesh_data)
    bpy.context.scene.collection.objects.link(obj)
    mesh_data.from_pydata(verts, [], [])
    
    
    action = bpy.data.actions.new("TrajectoryAnimation")
    obj.data.animation_data_create()
    obj.data.animation_data.action = action
    data_path = "vertices[%d].co"
    
    frames = []
    samples = [[] for i in range(nElements)]

    frame = 0
    i = 0
    with open(trajPath) as f:
        for line in f:
            vals = line.split(' ')
            if vals[0] == 't':
                frame += keyframeDist
                frames.append(frame)
                i = 0
                print('Frame {} ({})'.format(frame, line.strip()))
            elif len(vals) == 15:
                samples[i].append(Vector((float(vals[0]), float(vals[1]), float(vals[2]))))
                frames
                i += 1
                
    print('Finished reading data')
    for i, values in enumerate(samples):
        if (i%100==0):
            print('{:.3f}% of keyframes created'.format(100*i/nElements), end='\r', flush=True)
        v = obj.data.vertices[i]
        fcurves = [action.fcurves.new(data_path % v.index, index =  i) for i in range(3)]
        co_rest = v.co

        for t, value in zip(frames, values):
            co_kf = co_rest + value
            insert_keyframe(fcurves, t, co_kf) 

    scene.frame_end = frame
    print('Trajectory loading finished')

loadTrajectory(trajPath, topPath, keyframeDist)