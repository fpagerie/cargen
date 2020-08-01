import os
import math
from time import time
import random

import numpy as np

import bpy
import bmesh
import mathutils

from .car_generation import load_car_dimensions_file
from . import car_generation as CG

class CarCreation(bpy.types.Operator):
    """Create a Car"""
    bl_idname = "object.create_car"
    bl_label = "Create Car"
    bl_options = {'REGISTER', 'UNDO'}
    
    #Define basics Car Dimensions
    bpy.types.Scene.car_length = bpy.props.FloatProperty(name="Car Length", default=4.65, min=0.50, max=6.00, step=1, precision=3)
    bpy.types.Scene.car_width = bpy.props.FloatProperty(name="Car Width", default=1.90, min=0.50, max=4.00, step=1, precision=3)
    bpy.types.Scene.car_height = bpy.props.FloatProperty(name="Car Height", default=1.26, min=0.50, max=3.00, step=1, precision=3)
    
    #Define wheels Dimensions
    bpy.types.Scene.apply_wheels = bpy.props.BoolProperty(name="Add Wheels ?", default=True)
    bpy.types.Scene.wheelbase = bpy.props.FloatProperty(name="Car wheelbase", default=3.25, min=0.50, max=5.00, step=1, precision=3)
    bpy.types.Scene.front_wheel = bpy.props.FloatProperty(name="Distance from front of car to front wheel", default=0.7, min=0.20, max=1.5, step=1, precision=3)
    bpy.types.Scene.wheel_radius = bpy.props.FloatProperty(name="Wheel + tire radius", default=0.33, min=0.15, max=1.00, step=1, precision=3)
    bpy.types.Scene.wheel_width = bpy.props.FloatProperty(name="Wheel width", default=0.22, min=0.10, max=0.40, step=1, precision=3)
    bpy.types.Scene.wheels_enter_percent = bpy.props.FloatProperty(name="Percentage of wheel under the car floor", default=25, min=0, max=100, step=2, precision=1)
    
    #Define all cars dimensions from the front to the rear
    bpy.types.Scene.grille_height = bpy.props.FloatProperty(name="Grille Height", default=0.6, min=0.1, max=3.0, step=1, precision=3)
    bpy.types.Scene.hood_angle = bpy.props.FloatProperty(name="Hood Angle", default=6, min=-10, max=90, step=2, precision=1)
    bpy.types.Scene.hood_length = bpy.props.FloatProperty(name="Hood Length", default=1.30, min=0.1, max=3.0, step=1, precision=3)
    bpy.types.Scene.windshield_angle = bpy.props.FloatProperty(name="WindShield Angle", default=25, min=0, max=90, step=2, precision=1)
    bpy.types.Scene.roof_length = bpy.props.FloatProperty(name="Roof Length", default=0.78, min=0.1, max=3.0, step=1, precision=3)
    bpy.types.Scene.roof_angle = bpy.props.FloatProperty(name="Roof Angle", default=0, min=-40, max=40, step=1, precision=3)
    bpy.types.Scene.rear_window_angle = bpy.props.FloatProperty(name="Rear Window Angle", default=-30, min=-90, max=0, step=2, precision=1)
    bpy.types.Scene.rear_window_height = bpy.props.FloatProperty(name="Rear Window Height", default=0.35, min=0, max=3.0, step=1, precision=3)
    bpy.types.Scene.trunk_angle = bpy.props.FloatProperty(name="Trunk Angle", default=-2, min=-60, max=20, step=2, precision=1)
    
    #Define the curves that will be applied so the car is not a simple box
    bpy.types.Scene.apply_curves = bpy.props.BoolProperty(name="Apply Curves ?", default=True)
    bpy.types.Scene.grille_curve = bpy.props.StringProperty(name="Grille Curve", default="- 0.01 * (4.75*y)**2 - 0.005 * (3*(z + 0.5))**2 - 0.01 * (0.65*z + 0.65)**10")
    bpy.types.Scene.hood_curve = bpy.props.StringProperty(name="Hood Curve", default="- 0.01 * (0.65*x + 0.65)**2 - 0.005 * (4.75*y)**2")
    bpy.types.Scene.roof_curve = bpy.props.StringProperty(name="Roof Curve", default="- 0.01 * (1.17*x)**2 - 0.0015 * (4.75*y)**2")
    bpy.types.Scene.trunk_curve = bpy.props.StringProperty(name="Trunk Curve", default="- 0.01 * (1.05*(x))**2 - 0.0015 * (4.75*y)**2")
    bpy.types.Scene.rear_curve = bpy.props.StringProperty(name="Rear Curve", default="0.01 * (3.25*y)**2 + 0.005 * (3*(z + 0.5))**2 + 0.02 * (0.65*z + 0.65)**12")
    bpy.types.Scene.side_curve = bpy.props.StringProperty(name="Side Curve", default="0.005 * (3.25*x)**2 + 0.002 * (5*(z + 0.5))**2 + 0.15 * max(z+0.33*x - 0.15, 0)")
    bpy.types.Scene.under_curve = bpy.props.StringProperty(name="Under Curve", default="0.01 * (0.65*x)**2 + 0.005 * (4.75*y)**2")
    
    #Numbers of mesh points. The more, the finer the mesh will be
    bpy.types.Scene.nbr_mesh_pts = bpy.props.IntProperty(name="Number of mesh points", default=3, min=1, max=10)
    #Randomise car dimensions or not
    bpy.types.Scene.random_car = bpy.props.BoolProperty(name="Create Random Car ?", default=False)
    
    #Set enum property with the name of all saved cars dimensions
    items = []
    cars_loaded_dimensions = CG.load_car_dimensions_file()
    for model in cars_loaded_dimensions:
        items.append((model, model, ""))
    bpy.types.Scene.saved_car_list = bpy.props.EnumProperty(items=items, name="Load from File : ", description="zrthrt", default=None, options={'ANIMATABLE'}, update=None, get=None, set=None)
    bpy.types.Scene.load_from_file = bpy.props.BoolProperty(name="Load from file ?", default=False)
    
    
    def execute(self, context):
        stt = time()
        #Check if Car object exist, delete if yes, create if not
        scene = context.scene
        obj = []
        for obje in scene.objects:
            if obje.name == 'Car':
                obj.append(obje)
            elif obje.name in ['wheel1', 'wheel2', 'wheel3', 'wheel4']:
                obj.append(obje)
        if len(obj) != 0:
            bpy.ops.object.delete({"selected_objects": obj})
        bpy.ops.mesh.primitive_cube_add()
        obj = scene.objects['Cube']
        obj.name = 'Car'
        
        me = obj.data
        # Get a BMesh representation
        bm = bmesh.new()   # create an empty BMesh
        bm.from_mesh(me)   # fill it in from a Mesh
        
        if scene.load_from_file:
            scene.random_car = False
            CG.set_saved_values(scene)
        
        #set values if random dimensions is true
        if scene.random_car:
            CG.set_random_values(scene)
        
        #init dictionary containing vertices of each major part of the car
        bm, car_dict = CG.init_dict(bm, scene)
        
        #Create dict with points position
        car_pos_dict = CG.create_dict_all_pos(car_dict, True, {})

        #put the cube to car size
        bm, car_dict, positions = CG.put_to_size(bm, car_dict, scene)
        
        #Update dict with points position
        car_pos_dict = CG.create_dict_all_pos(car_dict, False, car_pos_dict)
        
        #if put curves is true, we appply them
        if scene.apply_curves:
            bm, car_dict = CG.put_curves(bm, car_dict, scene, car_pos_dict, positions)
        
        #Put the mesh back to the object
        bm.to_mesh(me)
        bm.free()  # free and prevent further access
        
        if scene.apply_wheels:
            #Add wheels and merge with car
            CG.add_wheels(scene)
        
        print('The car is ready')
        print('Time to create the car : ' + str(time() - stt) + ' s')
        return {'FINISHED'}


class CarPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Car Creation Panel"
    bl_idname = "OBJECT_PT_cargen"
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CarGen'
    
    def draw(self, context):
        #The layout is basically all the properties one after the other
        layoutt = self.layout
        layout = layoutt.box()
        obj = context.object
        scene = context.scene
        row = layout.row()
        row.label(text="Mesh Parameters :")

        row = layout.row()
        row.prop(scene, "nbr_mesh_pts")
        
        row = layout.row()
        row.prop(scene, "load_from_file")
        if  scene.load_from_file:
            row = layout.row()
            row.prop(scene, "saved_car_list")
        else:
            row = layout.row()
            row.prop(scene, "random_car")
            if not scene.random_car:
                row = layout.row()
                row.label(text="General Car Parameters :")
                row = layout.row()
                row.prop(scene, "car_length")
                row = layout.row()
                row.prop(scene, "car_width")
                row = layout.row()
                row.prop(scene, "car_height")
                
                row = layout.row()
                row.prop(scene, "apply_wheels")
                if scene.apply_wheels:
                    row = layout.row()
                    row.label(text="Wheels Dimensions :")
                    row = layout.row()
                    row.prop(scene, "wheelbase")
                    row = layout.row()
                    row.prop(scene, "front_wheel")
                    row = layout.row()
                    row.prop(scene, "wheel_radius")
                    row = layout.row()
                    row.prop(scene, "wheel_width")
                    row = layout.row()
                    row.prop(scene, "wheels_enter_percent")
                
                row = layout.row()
                row.label(text="Car Dimensions :")
                row = layout.row()
                row.prop(scene, "grille_height")
                row = layout.row()
                row.prop(scene, "hood_angle")
                row = layout.row()
                row.prop(scene, "hood_length")
                row = layout.row()
                row.prop(scene, "windshield_angle")
                row = layout.row()
                row.prop(scene, "roof_length")
                row = layout.row()
                row.prop(scene, "roof_angle")
                row = layout.row()
                row.prop(scene, "rear_window_angle")
                row = layout.row()
                row.prop(scene, "rear_window_height")
                row = layout.row()
                row.prop(scene, "trunk_angle")
                
            row = layout.row()
            row.prop(scene, "apply_curves")
            
            if scene.apply_curves:
                row = layout.row()
                row.prop(scene, "grille_curve")
                row = layout.row()
                row.prop(scene, "hood_curve")
                row = layout.row()
                row.prop(scene, "roof_curve")
                row = layout.row()
                row.prop(scene, "trunk_curve")
                row = layout.row()
                row.prop(scene, "rear_curve")
                row = layout.row()
                row.prop(scene, "side_curve")
                row = layout.row()
                row.prop(scene, "under_curve")
                
        row = layout.row()
        layout.operator('object.create_car')
        
        
        
        