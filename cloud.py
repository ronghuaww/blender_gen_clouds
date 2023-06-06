import bpy 
import random 
import math


class MESH_sphere_clouds(bpy.types.Operator):
    """lots of spheres for some fluffy clouds"""
    bl_idname = "mesh.sphere_clouds"
    bl_label = "Sphere Clouds"
    bl_options = {'REGISTER', 'UNDO'}

    num_spheres_prev = 0

    num_spheres: bpy.props.IntProperty(
        name="Number of Spheres", 
        description="Number of Spheres",
        default=50,
        min=1
    )

    span_x_prev = 0

    span_x: bpy.props.FloatProperty(
        name="X", 
        description="Length of the Clouds in the X-direction", 
        default=10
    )

    span_y_prev = 0

    span_y: bpy.props.FloatProperty(
        name="Y", 
        description="Length of the Clouds in the Y-direction", 
        default=10
    )

    radius: bpy.props.IntProperty(
        name="Maximum Radius", 
        description="Maximum Radius of the Spheres",
        default=2, 
        min=2
    )

    decay_rad: bpy.props.FloatProperty(
        name="Radius Decay Factor", 
        description="Exponential Decay of the radius as it gets further from the center", 
        default= 1/2,
        min=0, max= 1
    )

    min_segment: bpy.props.IntProperty(
        name="Segment", 
        description="Minmum number of Segments for Each Sphere",
        default=3, 
        min=3
    )

    growth_seg: bpy.props.FloatProperty(
        name="Segment Growth Factor", 
        description="Exponential Growth in the number of segments as it gets further from the center", 
        default=3,
        min=1, max=16
    )

    midpoint_x: bpy.props.FloatProperty(
        name="Midpoint X-Coordinate", 
        description="X-Coordinate for where the radius is the highest",
        default=0
    )

    midpoint_y: bpy.props.FloatProperty(
        name="Midpoint Y-Corrdinate", 
        description="Y-Coordinate for where the radius is the highest",
        default=3
    )

    # @classmethod
    # def poll(cls, context): 
    #     return context.area.type == 'VIEW_3D'


    def execute (self, context): 
        min_radius = 0.2

        # # default circle where all the new ones are merge with
        # s = bpy.ops.mesh.primitive_uv_sphere_add(
        #     segments=3, 
        #     ring_count=3, 
        #     radius=min_radius)
        # main_obj = bpy.context.active_object
        # main_obj.location[2] = 1

        if (self.num_spheres != self.num_spheres_prev 
            or self.span_x != self.span_x_prev 
            or self.span_y != self.span_y_prev):
            
            self.num_spheres_prev = self.num_spheres 
            self.span_x_prev = self.span_x
            self.span_y_prev = self.span_y

            for i in range(self.num_spheres):     
                x_val = random.random() * self.span_x - (self.span_x/2)
                y_val = random.random() * self.span_y - (self.span_y/2)
                xy_avg = (abs(x_val + self.midpoint_x) + abs(y_val + self.midpoint_y))/2
                
                # y = ab^x (a is size, b percent, x is xy_avg)
                # (x is xy_avg; y is the size/radius)
                rad = self.radius
                rad = rad * (self.decay_rad ** xy_avg)

                # small rad are not generated 
                #absoultely killing my computer 
                if (rad > min_radius): 
                    z_val = rad + ((random.random() * (rad)) - (rad/2))

                    # y = ab^x (a is the min segment; b is percentage (from 1 to 1.5)
                    # (x is size; y gives us the respective segment)
                    seg_val = int(self.min_segment * (self.growth_seg ** rad))

                    bpy.ops.mesh.primitive_uv_sphere_add(
                        segments=seg_val, 
                        ring_count=seg_val, 
                        radius=rad)
                    loop_obj = bpy.context.active_object
                    
                    loop_obj.location[0] = x_val
                    loop_obj.location[1] = y_val
                    loop_obj.location[2] = z_val
                    
                    # mod_bool = loop_obj.modifiers.new("boolean", 'BOOLEAN') 
                    # mod_bool.operation = 'UNION'
                    # mod_bool.object = main_obj
                    
                    # bpy.ops.object.modifier_apply(modifier="boolean")
                    
                    # loop_obj.select_set(False)
                    # main_obj.select_set(True)
                    # bpy.ops.object.delete()
                    # main_obj = loop_obj

        return {'FINISHED'}
        
def register(): 
    bpy.utils.register_class(MESH_sphere_clouds)

def unregister():
    bpy.utils.unregister_class(MESH_sphere_clouds)

# why does this not work?? 
#if __name__ == '__main__':
#   register()

bpy.utils.register_class(MESH_sphere_clouds)
