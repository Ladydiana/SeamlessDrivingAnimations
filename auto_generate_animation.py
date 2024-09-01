import subprocess
import os
import bpy 
import sys
import random
import colorsys

#Generating that auto-increment file name based on the names of the files in the directory
def get_incremented_filename(directory, base_name, extension):
    existing_files = [
        f for f in os.listdir(directory)
        if f.startswith(base_name) and f.endswith(extension)
    ]
    
    existing_numbers = []
    for f in existing_files:
        name, ext = os.path.splitext(f)
        try:
            number = int(name[len(base_name):])
            existing_numbers.append(number)
        except ValueError:
            pass
    
    next_number = max(existing_numbers, default=0) + 1
    return f"{base_name}{next_number}{extension}"
    
    
def _debug(material_name, hex_color):
    # Debug: Print available materials
    print("Available materials:")
    for mat in bpy.data.materials:
        print(mat.name)
    print("Hex color to change to: ")
    print(hex_color);
    
    # Debug: Print all objects and their materials
    print("\nObjects and their materials:")
    for obj in bpy.data.objects:
        if obj.type == 'MESH':  # Only process objects of type 'MESH'
            if obj.material_slots:
                print(f"Object: {obj.name}")
                for mat_slot in obj.material_slots:
                    if mat_slot.material:
                        print(f"  Material: {mat_slot.material.name}")
    
    # Debug: Print nodes in materials
    print("\nMaterial nodes:")
    for mat in bpy.data.materials:
        print(f"Material: {mat.name}")
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                print(f"  Node: {node.name} ({node.type})")


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    
    
def generate_random_color():
    #h,s,l = random.random(), 0.5 + random.random()/2.0, 2.0 #0.4 + random.random()/5.0
    #r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]
    #return tuple(int(256*i) for i in colorsys.hls_to_rgb(h,l,s))
    rand = lambda: random.randint(0, 255)
    return hex_to_rgb('#%02X%02X%02X' % (rand(), rand(), rand()))


# If material is Principled BSDF
def set_material_color(material_name, hex_color):
    material = bpy.data.materials.get(material_name)
    if material:
        material.use_nodes = True
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            rgb_color = hex_to_rgb(hex_color)
            bsdf.inputs['Base Color'].default_value = (*rgb_color, 1.0)  # Add alpha as 1.0
            

#If material is Emission            
def set_emission_color(material_name, hex_color):
    
    # Retrieve the material by name
    material = bpy.data.materials.get(material_name)
    if material:
        material.use_nodes = True
        # Get the "Emission" shader node
        emission_node = material.node_tree.nodes.get("Emission")
        if emission_node:
            #rgb_color = hex_to_rgb(hex_color)
            rgb_color = generate_random_color()
            # Set the emission color
            print(f"Setting the emission color to '{rgb_color}'.")
            emission_node.inputs['Color'].default_value = (*rgb_color, 1.0)
        else:
            print(f"Emission node not found in material '{material_name}'.")
    else:
        print(f"Material '{material_name}' not found.")
        
def main():

    # Set the path to the Blender executable
    blender_executable = "C:/Program Files/Blender Foundation/Blender 4.0/blender.exe"  

    # Set the path to the .blend file
    blend_file = "C:/Users/Jedi Knight/Documents/GitHub/SynthwaveAnimations/Auto_LoopDrivingWireframe_City.blend"  

    # Set the output directory and base name
    output_directory = "C:/Users/Jedi Knight/Documents/GitHub/SynthwaveAnimations/renders/auto"  
    base_name = "auto_rendered_animation_"      # Base name for the output file
    extension = ".mkv"                     # Output file extension

    # Accept hex color value as an argument
    hex_color = sys.argv[-1]

    # Set the material name that you want to change the color of
    material_name = "House"  

    # Set the output file name
    output_file = os.path.join(output_directory, get_incremented_filename(output_directory, base_name, extension))

    # !!!IMPORTANT!!! Ensure the blend file is loaded, otherwise it will try to so this on the default one.
    bpy.ops.wm.open_mainfile(filepath=blend_file)

    # Modify the .blend file to update the material color
    #set_material_color(material_name, hex_color)
    set_emission_color(material_name, hex_color)

    # !!!IMPORTANT!!! Save the blend file. Otherwise it will render with the default material, not the new one!!!
    bpy.ops.wm.save_mainfile(filepath=blend_file)

    # Set the rendering command
    render_command = [
        blender_executable, 
        "-b", blend_file,    # Run in background mode without UI
        "-o", output_file,   # Specify the output file
        "-a",                # Render the animation
        "--", hex_color,  # Pass the hex color as an argument
    ]

    # Run the command
    subprocess.run(render_command, check=True)

    print(f"Rendering completed: {output_file}")

if __name__ == '__main__':
  main()