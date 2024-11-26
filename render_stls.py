import bpy
import os
import math

# Paths
stl_folder = r"C:\Users\legol\OneDrive\Desktop\RenderProject\models"
output_folder = r"C:\Users\legol\OneDrive\Desktop\RenderProject\renders"
os.makedirs(output_folder, exist_ok=True)

# Fixed camera position
camera = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
bpy.context.scene.collection.objects.link(camera)
camera.location = (0, -100, 100)
camera.rotation_euler = (math.radians(45), 0, 0)  # Fixed angle
bpy.context.scene.camera = camera

# Load and render each STL
for stl_file in os.listdir(stl_folder):
    if stl_file.endswith(".stl"):
        stl_path = os.path.join(stl_folder, stl_file)
        bpy.ops.import_mesh.stl(filepath=stl_path)
        obj = bpy.context.selected_objects[0]

        # Center the object
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
        obj.location = (0, 0, 0)
        obj.scale = (1, 1, 1)

        # Rotate the object for different views
        object_angles = [
            (45, 0, 0),
            (0, 45, 0),
            (0, 0, 45),
            (45, 45, 0),
            (90, 0, 0),
            (180, 0, 0),    # Bottom-up
            (180, 45, 0),   # Bottom diagonal view
            (180, 0, 45),   # Bottom side angled
        ]

        for i, angle in enumerate(object_angles):
            obj.rotation_euler = [math.radians(a) for a in angle]
            output_file = os.path.join(output_folder, f"{os.path.splitext(stl_file)[0]}_view_{i}.png")
            bpy.context.scene.render.filepath = output_file
            bpy.ops.render.render(write_still=True)

        # Delete the object after rendering
        bpy.data.objects.remove(obj, do_unlink=True)

print("Rendering complete!")
