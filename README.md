# traj2blender
Load an oxDNA trajectory into Blender as animation keyframes

 1. Export glTF file from [oxView](https://sulcgroup.github.io/oxdna-viewer/)
 2. Import glTF file into Blender 2.8, save blender file in the same directory as your trajectory
 3. Inside Blender, open the "Scripting" workspace, then select open the traj2blender.py as a text file. Make sure the path is pointing at your trajectory file.
 3. Run the python script (Alt p) (you can check the progress if you launched blender from a terminal)
 4. When finished, the trajectory is loaded as keyframes in blender and you can simply start rendering an animation.
 
 Check out https://www.youtube.com/watch?v=nkKSbeOm0N8 to learn how to position camera, set materials etc.
