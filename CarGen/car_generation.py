import os
import math
from time import time
import random

import numpy as np

import bpy
import bmesh
import mathutils

from.cars_dimensions import get_dimensions


#Function to get extreme values in list of vertices following an axis
def get_min_max(verts, axis):
    minn = 50000
    maxx = -50000
    for v in verts:
        if v.co[axis] > maxx:
            maxx = v.co[axis]
        if v.co[axis] < minn:
            minn = v.co[axis]
    return minn, maxx


#Get a dict with all stored car values
def load_car_dimensions_file():
    return get_dimensions()

def set_saved_values(params):
    saved_car = params.saved_car_list
    cars_loaded_dimensions = load_car_dimensions_file()
    cur_car = cars_loaded_dimensions[saved_car]
    for prop in cur_car:
        params[prop] = cur_car[prop]

#Function to randomise all car parameters. 
#For now, it is a simple multiplication of the default value by a random number following normal distribution with mean=1, sigma=0.1
def set_random_values(params):
    #First, put back default values
    params.property_unset("car_length")
    params.property_unset("car_width")
    params.property_unset("car_height")
    
    params.property_unset("wheelbase")
    params.property_unset("front_wheel")
    params.property_unset("wheel_radius")
    params.property_unset("wheel_width")
    
    params.property_unset("grille_height")
    params.property_unset("hood_angle")
    params.property_unset("hood_length")
    params.property_unset("windshield_angle")
    params.property_unset("roof_length")
    params.property_unset("roof_angle")
    params.property_unset("rear_window_angle")
    params.property_unset("rear_window_height")
    params.property_unset("trunk_angle")
    
    #Calculate 15 random nubers
    rnd = np.random.normal(1, 0.10, 16)
    
    #Multiply default value by random number
    params.car_length = params.car_length * rnd[0]
    params.car_width  = params.car_width  * rnd[1]
    params.car_height = params.car_height * rnd[2]
    
    params.wheelbase    = params.wheelbase    * rnd[3]
    params.front_wheel  = params.front_wheel  * rnd[4]
    params.wheel_radius = params.wheel_radius * rnd[5]
    params.wheel_width  = params.wheel_width  * rnd[6]
    
    params.grille_height      = params.grille_height      * rnd[7] 
    params.hood_angle         = params.hood_angle         * rnd[8] 
    params.hood_length        = params.hood_length        * rnd[9] 
    params.windshield_angle   = params.windshield_angle   * rnd[10]
    params.roof_length        = params.roof_length        * rnd[11]
    params.roof_angle         = params.roof_angle         * rnd[12]
    params.rear_window_angle  = params.rear_window_angle  * rnd[13]
    params.rear_window_height = params.rear_window_height * rnd[14]
    params.trunk_angle        = params.trunk_angle        * rnd[15]
    

    
#Function that take the default cube, subdivide all edge by a number taking the parameter "Number of mesh points"
#It then assign all vertices to parts of the car depending on their position.
def init_dict(bm, params):
    #First, add 1 in x and z so the cube is not centered
    for v in bm.verts:
        v.co.x += 1.0
        v.co.z += 1.0

    #Subdivide each edges by a factor of (4 + 5 * "Number of mesh points")
    #There are 5 major parts in the upper car : hood, windshield, roof, rear window, trunk
    #So first divide by 4 to have 5 parts, then divide each part by "Number of mesh points"
    res = bmesh.ops.subdivide_edges(bm,
            edges=bm.edges,
            use_grid_fill=True,
            cuts=4 + 5*params.nbr_mesh_pts)

    #Create a dict containing all vertices for all parts of the car
    #The '_u' notation is for parts under some others like 'roof_u' is for vertices of the doors and vertices of the under car that are bellow the roof
    car_dict = {}
    car_dict['under'] = []
    car_dict['grille'] = []
    car_dict['hood'] = []
    car_dict['windshield'] = []
    car_dict['roof'] = []
    car_dict['rear_window'] = []
    car_dict['trunk'] = []
    car_dict['back'] = []
    car_dict['left'] = []
    car_dict['right'] = []
    car_dict['hood_u'] = []
    car_dict['windshield_u'] = []
    car_dict['roof_u'] = []
    car_dict['rear_window_u'] = []
    car_dict['trunk_u'] = []
    
    #Assign each vertices to the part in which it belong
    #One vertice may be in multiple parts if it is on the limit between two parts for example
    for v in bm.verts:
        if v.co.z < 1.999:
            if v.co.z < 0.001:
                car_dict['under'].append(v)
            if v.co.x > 1.999:
                car_dict['grille'].append(v)
            elif v.co.x < 0.001:
                car_dict['back'].append(v)
            if v.co.y > 0.999:
                car_dict['left'].append(v)
            elif v.co.y < -0.999:
                car_dict['right'].append(v)
                
            if v.co.x > 1.999:
                if abs(v.co.y) > 0.999:
                    car_dict['hood_u'].append(v)
            elif v.co.x > 1.601:
                car_dict['hood_u'].append(v)
            elif v.co.x > 1.599:
                car_dict['hood_u'].append(v)
                car_dict['windshield_u'].append(v)
            elif v.co.x > 1.201:
                car_dict['windshield_u'].append(v)
            elif v.co.x > 1.199:
                car_dict['windshield_u'].append(v)
                car_dict['roof_u'].append(v)
            elif v.co.x > 0.801:
                car_dict['roof_u'].append(v)
            elif v.co.x > 0.799:
                car_dict['roof_u'].append(v)
                car_dict['rear_window_u'].append(v)
            elif v.co.x > 0.401:
                car_dict['rear_window_u'].append(v)
            elif v.co.x > 0.399:
                car_dict['rear_window_u'].append(v)
                car_dict['trunk_u'].append(v)
            elif v.co.x > 0.001:
                car_dict['trunk_u'].append(v)
            else:
                if abs(v.co.y) > 0.999:
                    car_dict['trunk_u'].append(v)

        else :
            if v.co.y > 0.999:
                car_dict['left'].append(v)
            elif v.co.y < -0.999:
                car_dict['right'].append(v)
            if v.co.x > 1.999:
                car_dict['grille'].append(v)
                car_dict['hood'].append(v)
            elif v.co.x > 1.601:
                car_dict['hood'].append(v)
            elif v.co.x > 1.599:
                car_dict['hood'].append(v)
                car_dict['windshield'].append(v)
            elif v.co.x > 1.201:
                car_dict['windshield'].append(v)
            elif v.co.x > 1.199:
                car_dict['windshield'].append(v)
                car_dict['roof'].append(v)
            elif v.co.x > 0.801:
                car_dict['roof'].append(v)
            elif v.co.x > 0.799:
                car_dict['roof'].append(v)
                car_dict['rear_window'].append(v)
            elif v.co.x > 0.401:
                car_dict['rear_window'].append(v)
            elif v.co.x > 0.399:
                car_dict['rear_window'].append(v)
                car_dict['trunk'].append(v)
            elif v.co.x > 0.001:
                car_dict['trunk'].append(v) 
            else:
                car_dict['trunk'].append(v)
                car_dict['back'].append(v)
            
    return bm, car_dict


#function to apply a position to x and z for all part of the car that are flat
def put_to_size(bm, car_dict, params):
    
    #Function to apply the position
    def apply_x_and_z(car_dict, current, previous, curr_x_max, curr_z_max, prev_x_max, prev_z_max):
        #Get the current x min and max position, x is in the length of the car
        minx, maxx = get_min_max([i for i in car_dict[current] if i not in car_dict[previous]], 0)
        maxx = maxx + (maxx - minx) / (params.nbr_mesh_pts)
        pos_x = []
        for v in car_dict[current]:
            #For each vertice in the part, if it is not in the previous part, put the z position
            if v not in car_dict[previous]:
                v.co.z = prev_z_max + (curr_z_max - prev_z_max) * (maxx - v.co.x) / (maxx - minx)
                pos_x.append(v.co.x)
        pos_x = list(set(pos_x))
        #Set z position of what is under each part
        for v in car_dict[current + '_u']:
            previous_u = previous + '_u' if previous != 'grille' else 'grille'
            if v not in car_dict[previous_u]:
                v.co.z = v.co.z * ((prev_z_max + (curr_z_max - prev_z_max) * (maxx - v.co.x) / (maxx - minx)) / 2.0)
        
        for v in car_dict[current + '_u'] + car_dict[current]:
            if any(abs(i - v.co.x) < 0.001 for i in pos_x):
                v.co.x = prev_x_max + (curr_x_max - prev_x_max) * (maxx - v.co.x) / (maxx - minx)

    #### Multiply x and y position of everything by length and width of the car
    for v in bm.verts:
        v.co.x = v.co.x * params.car_length / 2.0
        v.co.y = v.co.y * params.car_width / 2.0

    #### Then for each part from front to rear, set z position (height) of the vertices
    
    #height of grille
    for v in car_dict['grille']:
        v.co.z = v.co.z * params.grille_height / 2.0
    val_cal_x = params.car_length
    val_cal_z = params.grille_height

    #hood height
    val_cap_x = val_cal_x - params.hood_length
    val_cap_z = val_cal_z + params.hood_length * math.sin(params.hood_angle * math.pi / 180)
    apply_x_and_z(car_dict, 'hood', 'grille', val_cap_x, val_cap_z, val_cal_x, val_cal_z)
    
    #windshield height
    val_pb_x = val_cap_x - (params.car_height - val_cap_z) / math.tan(params.windshield_angle * math.pi / 180)
    val_pb_z = params.car_height - params.wheels_enter_percent * params.wheel_radius / 50 
    apply_x_and_z(car_dict, 'windshield', 'hood', val_pb_x, val_pb_z, val_cap_x, val_cap_z)

    #roof height
    val_tt_x = val_pb_x - params.roof_length
    val_tt_z = val_pb_z + params.roof_length * math.sin(params.roof_angle * math.pi / 180)
    apply_x_and_z(car_dict, 'roof', 'windshield', val_tt_x, val_tt_z, val_pb_x, val_pb_z)

    #rear window height
    val_la_x = val_tt_x + params.rear_window_height / math.tan(params.rear_window_angle * math.pi / 180)
    val_la_z = val_tt_z - params.rear_window_height #* math.sin(params.rear_window_angle * math.pi / 180)
    apply_x_and_z(car_dict, 'rear_window', 'roof', val_la_x, val_la_z, val_tt_x, val_tt_z)

    #trunk height
    val_cof_x = 0
    val_cof_z = val_la_z + (val_la_x - val_cof_x) * math.tan(params.trunk_angle * math.pi / 180)
    apply_x_and_z(car_dict, 'trunk', 'rear_window', val_cof_x, val_cof_z, val_la_x, val_la_z)
    
    #height of the back of the car
    for v in car_dict['back']:
        if v not in car_dict['trunk'] + car_dict['trunk_u']:
            v.co.z = v.co.z * val_cof_z / 2.0

    #Define a dict with x and z poition of the limit between each parts
    positions = {}
    positions['grille_hood_x'] = val_cal_x
    positions['grille_hood_z'] = val_cal_z
    
    positions['hood_windshield_x'] = val_cap_x
    positions['hood_windshield_z'] = val_cap_z
    
    positions['windshield_roof_x'] = val_pb_x
    positions['windshield_roof_z'] = val_pb_z
    
    positions['roof_rear_window_x'] = val_tt_x
    positions['roof_rear_window_z'] = val_tt_z
    
    positions['rear_window_trunk_x'] = val_la_x
    positions['rear_window_trunk_z'] = val_la_z
    
    positions['trunk_back_x'] = val_pb_x
    positions['trunk_back_z'] = val_pb_z
    
    return bm, car_dict, positions


#Function to create a dict containing the initial position and position ratio of each vertice. 
#There are maybe some useless info in this dict but it may be useful in the future
def create_dict_all_pos(car_dict, new, car_pos_dict):
    #List of all parts of the car
    list_parts = ['left', 'right', 'under', 'grille', 'back', 'hood', 'windshield', 'roof', 'rear_window', 'trunk', 'hood_u', 'windshield_u', 'roof_u', 'rear_window_u', 'trunk_u']
    for item in list_parts:
        if new:
            car_pos_dict[item] = {}
        #Get the min and max position of all points in the part
        minx, maxx = get_min_max(car_dict[item], 0)
        miny, maxy = get_min_max(car_dict[item], 1)
        minz, maxz = get_min_max(car_dict[item], 2)

        list_y = []
        for v in car_dict[item]:
        #For each vertice, set : 
        # - the x, y andz ratio between the position of the point and the maximum position in that part
        # - the initial position after putting it to the actual size of the car
            if new:
                car_pos_dict[item][v] = {}
                if maxx != minx:
                    car_pos_dict[item][v]['ratio_x'] = (maxx - v.co.x) / (maxx - minx)
                else:
                    car_pos_dict[item][v]['ratio_x'] = None
                if maxy != miny:
                    car_pos_dict[item][v]['ratio_y'] = (maxy - v.co.y) / (maxy - miny)
                else:
                    car_pos_dict[item][v]['ratio_y'] = None
                if maxz != minz:
                    car_pos_dict[item][v]['ratio_z'] = (maxz - v.co.z) / (maxz - minz)
                else:
                    car_pos_dict[item][v]['ratio_z'] = None
                if item[-2:] != '_u' and item not in ['grille', 'back', 'left', 'right']:
                    car_pos_dict[item][v]['ratio_z'] = car_pos_dict[item][v]['ratio_x']
            else:
                car_pos_dict[item][v]['pos_x_init'] = v.co.x
                car_pos_dict[item][v]['pos_y_init'] = v.co.y
                car_pos_dict[item][v]['pos_z_init'] = v.co.z
            list_y.append(v.co.y)
        
        #When then add some info about min and max values of the position in that part
        list_y = list(set(list_y))
        car_pos_dict[item]['list_y'] = sorted(list_y)
        car_pos_dict[item]['min_x_values'] = [minx for i in range(len(list_y))]
        car_pos_dict[item]['max_x_values'] = [maxx for i in range(len(list_y))]
        car_pos_dict[item]['min_z_values'] = [minz for i in range(len(list_y))]
        car_pos_dict[item]['max_z_values'] = [maxz for i in range(len(list_y))]

    return car_pos_dict


#Function to equilibrate the mesh which means to have elements that
# - are all about the same size 
# - are in the right place considering the position of the neighbouring parts
#This function is really CPU intensive, it is the one that make the car creation slow when there is a lot of vertices
#But I don't really know how to optimize it.
def equilibrate_mesh(car_dict, car_pos_dict, to_equilibrate, min_max_val, axis, axis_u, sec_axis):
    #car_dict is a dict that contains the list of  vertice of each part
    #car_pos_dict is a dict that contains each vertice of each part and the ratio of position between this vertice and the min/max of that part
    #to_equilibrate is the name of the part that will be equilibrated
    #min_max_val is a dict containing the new min/max values to apply the the part
    #axis, axe_u, sec_axis are 3 axis on which we will work
    
    #We have 3 possibilities, equilibrate the mesh of the part or the under part ("part_u") or both. 
    #The value of 'axis' and 'axis_u' is here to tell which to equilibrate. 
    #None means to not equilibrate, 0, 1 or 2 is the axis on which to equilibrate
    
    #The function is divided in two because we don't treat a part like an under part.
    
    #The value of sec_axis tell us which axis to take as reference to equilibrate
    if sec_axis == 0:
        sec_axe = 'x'
    elif sec_axis == 1:
        sec_axe = 'y'
    else:
        sec_axe = 'z'
    
    if axis is not None:
        #First convert 0, 1, 2 notation to x, y, z
        if axis == 0:
            axe = 'x'
        elif axis == 1:
            axe = 'y'
        else:
            axe = 'z'
        #Then for each vertice in the part, we equilibrate
        for v in car_pos_dict[to_equilibrate]:
            try: #The try/except is here because there are not only vertices in the dict but also min/max values
                ratio = car_pos_dict[to_equilibrate][v]['ratio_' + axe] #Get position ratio
                #We then calcuate the new min and max values of that part for a given value of sec_axis
                if not any(abs(i - v.co[sec_axis]) < 0.001 for i in min_max_val['min' + sec_axe]):
                    order = np.argsort(min_max_val['min' + sec_axe])
                    xp = np.array(min_max_val['min' + sec_axe])[order]
                    fp = np.array(min_max_val['min' + axe])[order]
                    cur_min = np.interp(v.co[sec_axis], xp, fp)
                else:
                    ind = [j for j, x in enumerate([abs(i - v.co[sec_axis]) < 0.001 for i in min_max_val['min' + sec_axe]]) if x][0]
                    cur_min = min_max_val['min' + axe][ind]
                #Same for the max value
                if not any(abs(i - v.co[sec_axis]) < 0.001 for i in min_max_val['max' + sec_axe]):
                    order = np.argsort(min_max_val['max' + sec_axe])
                    xp = np.array(min_max_val['max' + sec_axe])[order]
                    fp = np.array(min_max_val['max' + axe])[order]
                    cur_max = np.interp(v.co[sec_axis], xp, fp)
                else:
                    ind = [j for j, x in enumerate([abs(i - v.co[sec_axis]) < 0.001 for i in min_max_val['max' + sec_axe]]) if x][0]
                    cur_max = min_max_val['max' + axe][ind]
                #Finally we apply the new value to the vertice
                v.co[axis] = ratio * cur_min + (1 - ratio) * cur_max
            except:
                pass
    
    #This half of the function is almost the same as the first one except some minor change 
    #like there is no under grille so we have to make an exception
    if axis_u is not None:
        if axis_u == 0:
            axe_u = 'x'
        elif axis_u == 1:
            axe_u = 'y'
        else:
            axe_u = 'z'
        for v in car_pos_dict[to_equilibrate + '_u']:
            if (to_equilibrate in ['grille', 'back']) or (v not in car_dict['grille'] + car_dict['back']):
                try:
                    ratio_u = car_pos_dict[to_equilibrate + '_u'][v]['ratio_' + axe_u]
                    if not any(abs(i - v.co[sec_axis]) < 0.001 for i in min_max_val['min' + sec_axe]):
                        order = np.argsort(min_max_val['min' + sec_axe])
                        xp = np.array(min_max_val['min' + sec_axe])[order]
                        fp = np.array(min_max_val['min' + axe_u])[order]
                        cur_min_u = np.interp(v.co[sec_axis], xp, fp)
                    else:
                        ind = [j for j, x in enumerate([abs(i - v.co[sec_axis]) < 0.001 for i in min_max_val['min' + sec_axe]]) if x][0]
                        cur_min_u = min_max_val['min' + axe_u][ind]
                    if not any(abs(i - v.co[sec_axis]) < 0.001 for i in min_max_val['max' + sec_axe]):
                        order = np.argsort(min_max_val['max' + sec_axe])
                        xp = np.array(min_max_val['max' + sec_axe])[order]
                        fp = np.array(min_max_val['max' + axe_u])[order]
                        cur_max_u = np.interp(v.co[sec_axis], xp, fp)
                    else:
                        ind = [j for j, x in enumerate([abs(i - v.co[sec_axis]) < 0.001 for i in min_max_val['max' + sec_axe]]) if x][0]
                        cur_max_u = min_max_val['max' + axe_u][ind]
                    v.co[axis_u] = ratio_u * cur_min_u + (1 - ratio_u) * cur_max_u
                except:
                    pass
    return car_dict, car_pos_dict


#This function create a dict for the equilibrate function
#It creates a list of all x, y and z values for a given axis at the limit between two parts.
#It does that two times, one for the min values and one for the max values.
def create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, type, val, order):
#type = list de longueur 2 : chaque valeur étant 'calc' ou 'get' : calc pour prendre les valeur a l'intersection de 2 zones, get pour prendre les valeurs min ou max stockées dans car_pos_dict
#val = list de longueur 2 : si calc, nom des deux zones, si get nom de la zone et 'min' ou 'max'
#order = list de longueur 2 : ['min', 'max'] ou ['max, 'min']
    min_max_val = {}
    for i in range(2):
        #The 'else' in this if/else may be useless now, I may drop it in the future
        #I think the 'else' is quicker so I let it here but it may make things more complicated
        if type[i] == 'calc':
            #We just make a list of the positions of vertices that are at the limit between two parts
            list_x = []
            list_y = []
            list_z = []
            for v in [value for value in car_dict[val[i][0]] if value in car_dict[val[i][1]]]:
                list_x.append(v.co.x)
                list_y.append(v.co.y)
                list_z.append(v.co.z)
        else:
            #We take the list that is stored in the 'car_pos_dict' dict
            list_x = car_pos_dict[val[i][0]][val[i][1] + '_x_values']
            list_y = car_pos_dict[val[i][0]]['list_y']
            list_z = car_pos_dict[val[i][0]][val[i][1] + '_z_values']
        
        #Add the lists to the new dict
        min_max_val[order[i] + 'x'] = list_x
        min_max_val[order[i] + 'y'] = list_y
        min_max_val[order[i] + 'z'] = list_z
    return min_max_val


#This function is the one that transforms a boxy car into a car that have curves so basically make a 2020 car from a 70s car
#To do that, it :
# - applies the function to each part of the car, one after the other
# - equilibrate the mesh of the neighbouring parts
#It goes from the front to the rear then does the sides.
#this order is important because the finl shape of the car depends on the order.
def put_curves(bm, car_dict, params, car_pos_dict, positions):
    #Define the function that will be applied to all the vertices of the part
    def func_grille(x, y, z, positions):
        return x + eval(params.grille_curve)
    #Get min and max position to multiply by the corresponding factor
    miny, maxy = get_min_max(car_dict['grille'], 1)
    minz, maxz = get_min_max(car_dict['grille'], 2)
    for v in car_dict['grille']:
        #For each vertice, multiply the position and apply the function
        y = -1 + 2 * ((v.co.y - miny) / (maxy - miny))
        z = -1 + 2 * ((v.co.z - minz) / (maxz - minz))
        v.co.x = func_grille(v.co.x, y, z, positions)
    
    #equilibrate hood on x after moving grille
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'get'], [['grille', 'hood'], ['hood', 'min']], ['max', 'min'])
    equilibrate_mesh(car_dict, car_pos_dict, 'hood', min_max_val, 0, None, 1)
    
    #equilibrate hood_u on x after moving grille
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['windshield_u', 'hood_u'], ['hood_u', 'grille']], ['min', 'max'])
    equilibrate_mesh(car_dict, car_pos_dict, 'hood', min_max_val, None, 0, 2)
    
    def func_hood(x, y, z, positions):
        return z + eval(params.hood_curve)#- 0.01 * (x - positions['grille_hood_x'])**2 - 0.005 * (5*y)**2
    minx, maxx = get_min_max(car_dict['hood'], 0)
    miny, maxy = get_min_max(car_dict['hood'], 1)
    for v in car_dict['hood']:
        x = -1 + 2 * ((v.co.x - minx) / (maxx - minx))
        y = -1 + 2 * ((v.co.y - miny) / (maxy - miny))
        v.co.z = func_hood(x, y, v.co.z, positions)
    
    #equilibrate grille on z after moving hood
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'get'], [['grille', 'hood'], ['grille', 'min']], ['max', 'min'])
    equilibrate_mesh(car_dict, car_pos_dict, 'grille', min_max_val, 2, None, 1)

    #equilibrate hood_u on z after moving hood
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'get'], [['left', 'hood'], ['hood_u', 'min']], ['max', 'min'])
    min_max_val['maxz'] = [i / (4 + 5*params.nbr_mesh_pts) * (3 + 5*params.nbr_mesh_pts) for i in min_max_val['maxz']]
    equilibrate_mesh(car_dict, car_pos_dict, 'hood', min_max_val, None, 2, 0)
    
    
    #def func_windshield(x, y, z):
    #    return z - 0.0015 * (3*y)**2
    #for v in car_dict['windshield']:
    #    v.co.z = func_windshield(v.co.x, v.co.y, v.co.z)
    
    def func_roof(x, y, z, positions):
        return z + eval(params.roof_curve)# - 0.01 * (3*(x - ((positions['windshield_roof_x'] + positions['roof_rear_window_x']) / 2)))**2 - 0.0015 * (5*y)**2
    minx, maxx = get_min_max(car_dict['roof'], 0)
    miny, maxy = get_min_max(car_dict['roof'], 1)
    for v in car_dict['roof']:
        x = -1 + 2 * ((v.co.x - minx) / (maxx - minx))
        y = -1 + 2 * ((v.co.y - miny) / (maxy - miny))
        v.co.z = func_roof(x, y, v.co.z, positions)
    
    #equilibrate roof_u on z after moving roof
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'get'], [['left', 'roof'], ['roof_u', 'min']], ['max', 'min'])
    min_max_val['maxz'] = [i / (4 + 5*params.nbr_mesh_pts) * (3 + 5*params.nbr_mesh_pts) for i in min_max_val['maxz']]
    equilibrate_mesh(car_dict, car_pos_dict, 'roof', min_max_val, None, 2, 0)
        
    #equilibrate windshield on z after moving roof
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['hood', 'windshield'], ['roof', 'windshield']], ['max', 'min'])
    equilibrate_mesh(car_dict, car_pos_dict, 'windshield', min_max_val, 2, None, 1)
    
    #equilibrate windshield_u on z after moving roof
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'get'], [['left', 'windshield'], ['windshield_u', 'min']], ['max', 'min'])
    min_max_val['maxz'] = [i / (4 + 5*params.nbr_mesh_pts) * (3 + 5*params.nbr_mesh_pts) for i in min_max_val['maxz']]
    equilibrate_mesh(car_dict, car_pos_dict, 'windshield', min_max_val, None, 2, 0)
    
    def func_trunk(x, y, z, positions):
        return z + eval(params.trunk_curve)# - 0.01 * (3*(x - positions['rear_window_trunk_x'] / 2))**2 - 0.0015 * (5*y)**2
    minx, maxx = get_min_max(car_dict['trunk'], 0)
    miny, maxy = get_min_max(car_dict['trunk'], 1)
    for v in car_dict['trunk']:
        x = -1 + 2 * ((v.co.x - minx) / (maxx - minx))
        y = -1 + 2 * ((v.co.y - miny) / (maxy - miny))
        v.co.z = func_trunk(x, y, v.co.z, positions)
    
    #equilibrate rear_window on z after moving roof and trunk
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['roof', 'rear_window'], ['rear_window', 'trunk']], ['max', 'min'])
    equilibrate_mesh(car_dict, car_pos_dict, 'rear_window', min_max_val, 2, None, 1)
    
    #equilibrate rear_window_u on z after moving roof and trunk
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'get'], [['left', 'rear_window'], ['rear_window_u', 'min']], ['max', 'min'])
    min_max_val['maxz'] = [i / (4 + 5*params.nbr_mesh_pts) * (3 + 5*params.nbr_mesh_pts) for i in min_max_val['maxz']]
    equilibrate_mesh(car_dict, car_pos_dict, 'rear_window', min_max_val, None, 2, 0)
    
    #equilibrate trunk_u on z after moving trunk
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'get'], [['left', 'trunk'], ['trunk_u', 'min']], ['max', 'min'])
    min_max_val['maxz'] = [i / (4 + 5*params.nbr_mesh_pts) * (3 + 5*params.nbr_mesh_pts) for i in min_max_val['maxz']]
    equilibrate_mesh(car_dict, car_pos_dict, 'trunk', min_max_val, None, 2, 0)
    
    #equilibrate back on z after moving trunk
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'get'], [['back', 'trunk'], ['back', 'min']], ['max', 'min'])
    equilibrate_mesh(car_dict, car_pos_dict, 'back', min_max_val, 2, None, 1)
    
    def func_back(x, y, z, positions):
        return x + eval(params.rear_curve)# + 0.01 * (3*y)**2 + 0.005 * (7*z - 1.5)**2
    miny, maxy = get_min_max(car_dict['back'], 1)
    minz, maxz = get_min_max(car_dict['back'], 2)
    for v in car_dict['back']:
        y = -1 + 2 * ((v.co.y - miny) / (maxy - miny))
        z = -1 + 2 * ((v.co.z - minz) / (maxz - minz))
        v.co.x = func_back(v.co.x, y, z, positions)
    
    #equilibrate trunk on x after moving back
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'get'], [['back', 'trunk'], ['trunk', 'max']], ['min', 'max'])
    equilibrate_mesh(car_dict, car_pos_dict, 'trunk', min_max_val, 0, 0, 1)
    
    #equilibrate trunk_u on x after moving back
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['rear_window_u', 'trunk_u'], ['trunk_u', 'back']], ['max', 'min'])
    equilibrate_mesh(car_dict, car_pos_dict, 'trunk', min_max_val, None, 0, 2)
    
    def func_left_side(x, y, z, positions):
        return y - eval(params.side_curve)
    def func_right_side(x, y, z, positions):
        return y + eval(params.side_curve)
    minx = 0
    maxx = params.car_length
    minz = 0
    maxz = params.car_height
    for v in car_dict['left'] + car_dict['right']:
        x = -1 + 2 * ((v.co.x - minx) / (maxx - minx))
        z = -1 + 2 * ((v.co.z - minz) / (maxz - minz))
        if v.co.y > 0:
            v.co.y = func_left_side(x, v.co.y, z, positions)
        else:
            v.co.y = func_right_side(x, v.co.y, z, positions)
    
    #equilibrate everything on y after moving left and right
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['grille', 'left'], ['grille', 'right']], ['max', 'min'])
    equilibrate_mesh(car_dict, car_pos_dict, 'grille', min_max_val, 1, None, 2)
    
    #equilibrate everything on y after moving left and right
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['hood', 'left'], ['hood', 'right']], ['max', 'min'])
    equilibrate_mesh(car_dict, car_pos_dict, 'hood', min_max_val, 1, None, 0)
    
    #equilibrate everything on y after moving left and right
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['windshield', 'left'], ['windshield', 'right']], ['max', 'min'])
    equilibrate_mesh(car_dict, car_pos_dict, 'windshield', min_max_val, 1, None, 0)
    
    #equilibrate everything on y after moving left and right
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['roof', 'left'], ['roof', 'right']], ['max', 'min'])
    equilibrate_mesh(car_dict, car_pos_dict, 'roof', min_max_val, 1, None, 0)
    
    #equilibrate everything on y after moving left and right
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['rear_window', 'left'], ['rear_window', 'right']], ['max', 'min'])
    equilibrate_mesh(car_dict, car_pos_dict, 'rear_window', min_max_val, 1, None, 0)
    
    #equilibrate everything on y after moving left and right
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['trunk', 'left'], ['trunk', 'right']], ['max', 'min'])
    equilibrate_mesh(car_dict, car_pos_dict, 'trunk', min_max_val, 1, None, 0)
    
    #equilibrate everything on y after moving left and right
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['back', 'left'], ['back', 'right']], ['max', 'min'])
    equilibrate_mesh(car_dict, car_pos_dict, 'back', min_max_val, 1, None, 2)
    
    #equilibrate everything on y after moving left and right
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['under', 'left'], ['under', 'right']], ['max', 'min'])
    equilibrate_mesh(car_dict, car_pos_dict, 'under', min_max_val, 1, None, 0)
    
    def func_under(x, y, z, positions):
        return z + eval(params.under_curve)#- 0.01 * (x - positions['grille_hood_x'])**2 - 0.005 * (5*y)**2
    minx, maxx = get_min_max(car_dict['under'], 0)
    miny, maxy = get_min_max(car_dict['under'], 1)
    for v in car_dict['under']:
        x = -1 + 2 * ((v.co.x - minx) / (maxx - minx))
        y = -1 + 2 * ((v.co.y - miny) / (maxy - miny))
        v.co.z = func_under(x, y, v.co.z, positions)
    
    #equilibrate grille on z after moving under
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['under', 'grille'], ['hood', 'grille']], ['min', 'max'])
    equilibrate_mesh(car_dict, car_pos_dict, 'grille', min_max_val, 2, None, 1)
    
    #equilibrate back on z after moving under
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['under', 'back'], ['trunk', 'back']], ['min', 'max'])
    equilibrate_mesh(car_dict, car_pos_dict, 'back', min_max_val, 2, None, 1)
    
    #equilibrate left on z after moving under
    min_max_val = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['under', 'left'], ['left', 'hood']], ['min', 'max'])
    min_max_val2 = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['under', 'left'], ['left', 'windshield']], ['min', 'max'])
    min_max_val['maxx'].extend(min_max_val2['maxx'])
    min_max_val['maxy'].extend(min_max_val2['maxy'])
    min_max_val['maxz'].extend(min_max_val2['maxz'])
    min_max_val2 = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['under', 'left'], ['left', 'roof']], ['min', 'max'])
    min_max_val['maxx'].extend(min_max_val2['maxx'])
    min_max_val['maxy'].extend(min_max_val2['maxy'])
    min_max_val['maxz'].extend(min_max_val2['maxz'])
    min_max_val2 = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['under', 'left'], ['left', 'rear_window']], ['min', 'max'])
    min_max_val['maxx'].extend(min_max_val2['maxx'])
    min_max_val['maxy'].extend(min_max_val2['maxy'])
    min_max_val['maxz'].extend(min_max_val2['maxz'])
    min_max_val2 = create_dict_for_equilibrate_mesh(car_dict, car_pos_dict, ['calc', 'calc'], [['under', 'left'], ['left', 'trunk']], ['min', 'max'])
    min_max_val['maxx'].extend(min_max_val2['maxx'])
    min_max_val['maxy'].extend(min_max_val2['maxy'])
    min_max_val['maxz'].extend(min_max_val2['maxz'])
    equilibrate_mesh(car_dict, car_pos_dict, 'left', min_max_val, 2, None, 0)
    equilibrate_mesh(car_dict, car_pos_dict, 'right', min_max_val, 2, None, 0)
    return bm, car_dict


#This function add wheels to the car
#It may be interesting to raise the car in the end to account for the size of the wheels
def add_wheels(params):
    #### First we create the space in the car where the wheel will be so we create a slightly bigger wheel and substract that from the car
    
    #Add 4 cylinder, one for each wheel to create the place for the actual wheel
    bpy.ops.mesh.primitive_cylinder_add(radius=params.wheel_radius + 0.03, depth=params.wheel_width + 0.04, rotation=(1.570795, 0.0, 0.0), enter_editmode=False, location=(params.car_length - params.front_wheel, (params.car_width/2)-params.wheel_width/2, 2* params.wheel_radius * (0.5 - params.wheels_enter_percent / 100)))
    params.objects['Cylinder'].name = 'wheel1'
    bpy.ops.mesh.primitive_cylinder_add(radius=params.wheel_radius + 0.03, depth=params.wheel_width + 0.04, rotation=(1.570795, 0.0, 0.0), enter_editmode=False, location=(params.car_length - params.front_wheel, -(params.car_width/2)+params.wheel_width/2, 2* params.wheel_radius * (0.5 - params.wheels_enter_percent / 100)))
    params.objects['Cylinder'].name = 'wheel2'
    bpy.ops.mesh.primitive_cylinder_add(radius=params.wheel_radius + 0.03, depth=params.wheel_width + 0.04, rotation=(1.570795, 0.0, 0.0), enter_editmode=False, location=(params.car_length - params.front_wheel - params.wheelbase, (params.car_width/2)-params.wheel_width/2, 2* params.wheel_radius * (0.5 - params.wheels_enter_percent / 100)))
    params.objects['Cylinder'].name = 'wheel3'
    bpy.ops.mesh.primitive_cylinder_add(radius=params.wheel_radius + 0.03, depth=params.wheel_width + 0.04, rotation=(1.570795, 0.0, 0.0), enter_editmode=False, location=(params.car_length - params.front_wheel - params.wheelbase, -(params.car_width/2)+params.wheel_width/2, 2* params.wheel_radius * (0.5 - params.wheels_enter_percent / 100)))
    params.objects['Cylinder'].name = 'wheel4'
    
    #remove some place for the wheels
    car = bpy.data.objects["Car"]
    bpy.context.view_layer.objects.active = car
    for item in ['wheel1', 'wheel2', 'wheel3', 'wheel4']:
        bpy.ops.object.modifier_add(type='BOOLEAN')
        car.modifiers[0].object = params.objects[item]
        car.modifiers[0].operation = 'DIFFERENCE'
        bpy.context.view_layer.objects.active = car
        bpy.ops.object.modifier_apply(apply_as='DATA',modifier=car.modifiers[0].name)
        bpy.ops.object.delete({"selected_objects": [params.objects[item]]})

    #### Then we create the real wheels
    bpy.ops.mesh.primitive_cylinder_add(radius=params.wheel_radius, depth=params.wheel_width, rotation=(1.570795, 0.0, 0.0), enter_editmode=False, location=(params.car_length - params.front_wheel, (params.car_width/2)-params.wheel_width/2, 2* params.wheel_radius * (0.5 - params.wheels_enter_percent / 100)))
    params.objects['Cylinder'].name = 'wheel1'
    bpy.ops.mesh.primitive_cylinder_add(radius=params.wheel_radius, depth=params.wheel_width, rotation=(1.570795, 0.0, 0.0), enter_editmode=False, location=(params.car_length - params.front_wheel, -(params.car_width/2)+params.wheel_width/2, 2* params.wheel_radius * (0.5 - params.wheels_enter_percent / 100)))
    params.objects['Cylinder'].name = 'wheel2'
    bpy.ops.mesh.primitive_cylinder_add(radius=params.wheel_radius, depth=params.wheel_width, rotation=(1.570795, 0.0, 0.0), enter_editmode=False, location=(params.car_length - params.front_wheel - params.wheelbase, (params.car_width/2)-params.wheel_width/2, 2* params.wheel_radius * (0.5 - params.wheels_enter_percent / 100)))
    params.objects['Cylinder'].name = 'wheel3'
    bpy.ops.mesh.primitive_cylinder_add(radius=params.wheel_radius, depth=params.wheel_width, rotation=(1.570795, 0.0, 0.0), enter_editmode=False, location=(params.car_length - params.front_wheel - params.wheelbase, -(params.car_width/2)+params.wheel_width/2, 2* params.wheel_radius * (0.5 - params.wheels_enter_percent / 100)))
    params.objects['Cylinder'].name = 'wheel4'
    
    #### Finally we merge the wheels with the rest of the car
    for name in ['Car', 'wheel1', 'wheel2', 'wheel3', 'wheel4']:
        bpy.data.objects[name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects["Car"]
    bpy.ops.object.join()
