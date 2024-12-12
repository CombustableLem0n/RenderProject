import bpy
import os
import math
from mathutils import Vector

# Clear all existing objects
print("Clearing all existing objects...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Paths
stl_folder = r"C:\Users\legol\OneDrive\Desktop\RenderProject\stl_collection"
output_folder = r"C:\Users\legol\OneDrive\Desktop\RenderProject\test_data"
names_file = r"C:\Users\legol\OneDrive\Desktop\RenderProject\whitelist_parts.txt"
os.makedirs(output_folder, exist_ok=True)

# Read names from the text file and store them in a set for quick lookup
print(f"Reading valid names from: {names_file}")
with open(names_file, 'r') as file:
    valid_names = set(name.strip().lower() for name in file.read().split(','))
print(f"Valid names loaded: {valid_names}")

# Setup camera
print("Setting up the camera...")
camera = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
bpy.context.scene.collection.objects.link(camera)
camera.location = (0, -10, 10)
camera.rotation_euler = (math.radians(45), 0, 0)
bpy.context.scene.camera = camera

# Add a Sun lamp
print("Adding a Sun lamp...")
lamp_data = bpy.data.lights.new(name="Sun_Light", type="SUN")
lamp = bpy.data.objects.new(name="Sun_Light", object_data=lamp_data)
bpy.context.scene.collection.objects.link(lamp)
lamp.location = (0, -50, 50)
lamp.rotation_euler = (math.radians(45), 0, 0)  # Angle to match the camera view

def scale_camera_to_object(obj, camera, padding_factor=1.5):
    print(f"Scaling camera for object: {obj.name}")
    bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    min_coord = Vector((min(v[i] for v in bbox) for i in range(3)))
    max_coord = Vector((max(v[i] for v in bbox) for i in range(3)))
    dimensions = max_coord - min_coord
    max_dim = max(dimensions)
    camera_distance = max_dim * padding_factor
    camera.location = (0, -camera_distance, camera_distance)

# Render and generate JSON
object_id = 1
for stl_file in os.listdir(stl_folder):
    if stl_file.endswith(".stl"):
        obj_name = os.path.splitext(stl_file)[0].strip().lower()
        print(f"Processing file: {stl_file} (normalized name: {obj_name})")

        if obj_name not in valid_names:
            print(f"Skipping {stl_file}: Not in valid names list.")
            continue

        print(f"Importing STL: {stl_file}")
        stl_path = os.path.join(stl_folder, stl_file)
        bpy.ops.import_mesh.stl(filepath=stl_path)
        obj = bpy.context.selected_objects[0]

        print(f"Centering object: {obj.name}")
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
        obj.location = (0, 0, 0)
        obj.scale = (1, 1, 1)

        scale_camera_to_object(obj, camera)

        obj_folder = os.path.join(output_folder, obj_name)
        os.makedirs(obj_folder, exist_ok=True)
        print(f"Output folder for {obj_name} created at: {obj_folder}")

        render_width = 800
        render_height = 600
        bpy.context.scene.render.resolution_x = render_width
        bpy.context.scene.render.resolution_y = render_height

        object_angles = [
            (240, 0, 0), (235, 0, 0), (245, 0, 0), (240, 5, 0), (240, -5, 0), (240, 10, 0), (240, -10, 0), (242, 0, 0), (238, 0, 0), (240, 15, 0), 
            (240, -15, 0), (245, 5, 0), (235, 5, 0), (245, -5, 0), (235, -5, 0), (243, 0, 0), (237, 0, 0), (240, 0, 5), (240, 0, -5), (240, 20, 0), 
            (240, -20, 0), (240, 10, 10), (240, 10, -10), (235, 15, 0), (245, 15, 0), (240, 15, 10), (240, 15, -10), (245, 10, 5), (235, 10, 5), 
            (245, 5, 10), (235, 5, 10), (245, 0, 10), (235, 0, 10), (245, 0, 15), (235, 0, 15), (240, 20, 5), (240, 20, -5), (245, 15, 5), (235, 15, -5), 
            (240, 25, 0), (240, 25, 5), (240, -10, 10), (240, -10, -10), (235, -15, 0), (245, -15, 0), (240, -15, 10), (240, -15, -10), (245, -10, 5), 
            (235, -10, 5), (245, -5, 10), (235, -5, 10), (245, 0, 10), (235, 0, 10), (245, 0, 15), (235, 0, 15), (240, -20, 5), (240, -20, -5), (245, -15, 5), 
            (235, -15, -5), (240, -25, 0), (240, -25, 5), (240, 30, 0), (240, -30, 0), (240, 30, 5), (240, -30, 5), (240, 30, -5), (240, -30, -5), 
            (240, 35, 0), (240, -35, 0), (240, 35, 5), (240, -35, 5), (240, 35, -5), (240, -35, -5), (240, 40, 0), (240, -40, 0), (240, 40, 5), (240, -40, 5), 
            (240, 40, -5), (240, -40, -5), (240, 45, 0), (240, -45, 0), (240, 45, 5), (240, -45, 5), (240, 45, -5), (240, -45, -5), (240, 50, 0), (240, -50, 0), 
            (240, 50, 5), (240, -50, 5), (240, 50, -5), (240, -50, -5),
            ]

        for i, angle in enumerate(object_angles):
            print(f"Rendering view {i} for {obj_name} with angle: {angle}")
            obj.rotation_euler = [math.radians(a) for a in angle]
            image_name = f"{obj_name}_view_{i}.png"
            image_path = os.path.join(obj_folder, image_name)
            bpy.context.scene.render.filepath = image_path
            bpy.ops.render.render(write_still=True)
            print(f"Image saved: {image_path}")

        print(f"Removing object: {obj.name}")
        bpy.data.objects.remove(obj, do_unlink=True)
        object_id += 1

print("Rendering complete for valid STL files!")
