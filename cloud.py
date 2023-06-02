import bpy 
import random 
import math

startSpan = 0
endSpan = 5

edgeSize = .5
centerSize = 2

bpy.ops.mesh.primitive_uv_sphere_add()
main_obj = bpy.context.active_object
main_obj.location[2] = 1


for i in range(100):  
    size = 2
    percent = 5/10
    
    
    bpy.ops.mesh.primitive_uv_sphere_add()
    loop_obj = bpy.context.active_object
    
    span = 10
    height = 5
    
    x_val = random.random() * span - (span/2)
    y_val = random.random() * span - (span/2)
    
    xy_avg = (abs(x_val) + abs(y_val))/2
    
    #y = ab^x (a is size, b percent, x is xy_avg)
    
    size = size * (percent ** xy_avg)
    
    z_val = size + ((random.random() * size) - (size/2))
    
    loop_obj.location[0] = x_val
    loop_obj.location[1] = y_val
    loop_obj.location[2] = z_val
    
    
    
    loop_obj.scale[0] = size
    loop_obj.scale[1] = size 
    loop_obj.scale[2] = size
    
    mod_bool = loop_obj.modifiers.new("boolean", 'BOOLEAN') 
    mod_bool.operation = 'UNION'
    mod_bool.object = main_obj
    
    bpy.ops.object.modifier_apply(modifier="boolean")
    
    loop_obj.select_set(False)
    main_obj.select_set(True)
    bpy.ops.object.delete()
    main_obj = loop_obj