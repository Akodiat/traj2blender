# traj2blender
Load an oxDNA trajectory into Blender as animation keyframes. The instanced version is much faster for large structures

## traj2InstancedBlender.py

   1. Inside Blender, open the "Scripting" workspace, then select open the traj2InstancedBlender.py as a text file. Make sure the path is pointing at your trajectory and topology files.
   2. Run the python script (Alt p) (you can check the progress if you launched blender from a terminal)
   3. When finished, the trajectory is loaded as keyframes in blender, with all the elements as points.
   4. Next, create a new object to represent each element, for example an icosphere.
   5. Open `Geometry Nodes` and setup the instancing:
      1. With your object selected, click new to create input and output nodes.
      2. Click `Add`, `Instances`, and add an `Instance on Points` node, connecting input to output
      3. Click `Add`, `Input`, and add an `Object Info` node, connecting the icosphere geometry to the instance
      4. If you need to scale the instances, click `Add`, `Input`, and add a `Value` node.
    

## traj2blender.py
Load an oxDNA trajectory into Blender as animation keyframes

   1. Export glTF file from [oxView](https://sulcgroup.github.io/oxdna-viewer/)
   2. Import glTF file into Blender 2.8, save blender file in the same directory as your trajectory
   3. Inside Blender, open the "Scripting" workspace, then select open the traj2blender.py as a text file. Make sure the path is pointing at your trajectory file.
   3. Run the python script (Alt p) (you can check the progress if you launched blender from a terminal)
   4. When finished, the trajectory is loaded as keyframes in blender and you can simply start rendering an animation.
 
 Check out https://www.youtube.com/watch?v=nkKSbeOm0N8 to learn how to position camera, set materials etc.
