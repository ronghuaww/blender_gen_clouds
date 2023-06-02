import bpy 
import random 
import math

span = 10 
radius = 2
decay_rad = 5/10

min_segment = 4 
growth_seg = 3/2

s = bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=10, radius=0.1)
main_obj = bpy.context.active_object
main_obj.location[2] = 1


for i in range(100):  
    
    x_val = random.random() * span - (span/2)
    y_val = random.random() * span - (span/2)
    xy_avg = (abs(x_val) + abs(y_val))/2
    
    # y = ab^x (a is size, b percent, x is xy_avg)
    # (x is xy_avg; y is the size/radius)
    radius = radius * (decay_rad ** xy_avg)
    
    z_val = radius + ((random.random() * radius) - (radius/2))

    # y = ab^x (a is the min segment; b is percentage (from 1 to 1.5)
    # (x is size; y gives us the respective segment)

    seg_val = int(min_segment * (growth_seg ** radius))

    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg_val, ring_count=seg_val, radius=radius)
    loop_obj = bpy.context.active_object
    
    loop_obj.location[0] = x_val
    loop_obj.location[1] = y_val
    loop_obj.location[2] = z_val
    
    mod_bool = loop_obj.modifiers.new("boolean", 'BOOLEAN') 
    mod_bool.operation = 'UNION'
    mod_bool.object = main_obj
    
    bpy.ops.object.modifier_apply(modifier="boolean")
    
    loop_obj.select_set(False)
    main_obj.select_set(True)
    bpy.ops.object.delete()
    main_obj = loop_obj