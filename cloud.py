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
        description="Exponential Decay of the radius for each spheres", 
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
        description="Exponential Growth in the number of segments", 
        default=3,
        min=1, max=16
    )

    midpoint_x_prev = 0
    midpoint_x: bpy.props.FloatProperty(
        name="Midpoint X-Coordinate", 
        description="X-Coordinate for where the radius is the highest",
        default=0
    )
    midpoint_y_prev = 3
    midpoint_y: bpy.props.FloatProperty(
        name="Midpoint Y-Corrdinate", 
        description="Y-Coordinate for where the radius is the highest",
        default=3
    )

    x_list = []
    y_list = []
    z_list = []


    # @classmethod
    # def poll(cls, context): 
    #     return context.area.type == 'VIEW_3D'

    def execute (self, context): 

        # default circle where all the new ones are merge with
        s = bpy.ops.mesh.primitive_uv_sphere_add(
            segments=3, 
            ring_count=3, 
            radius=min_radius)
        main_obj = bpy.context.active_object
        main_obj.location[2] = 1

        for i in range(self.num_spheres):     
            x_val = random.random() * self.span_x - (self.span_x/2)
            y_val = random.random() * self.span_y - (self.span_y/2)
            xy_avg = (abs(x_val + self.midpoint_x) + abs(y_val + self.midpoint_y))/2
            
            # y = ab^x (a is size, b percent, x is xy_avg)
            # (x is xy_avg; y is the size/radius)
            rad = self.radius
            rad = rad * (self.decay_rad ** xy_avg)

        # small rad are not generated 
        # absoultely not letting it kill my computer 
        if (rad > min_radius): 

            if (gen_bool): 
                x_list.append(x_val)
                y_list.append(y_val)
                z_list.append(z_val)

            z_val = rad + ((z_val * (rad)) - (rad/2))

            # y = ab^x (a is the min segment; b is percentage)
            # (x is size; y gives us the respective segment)
            seg_val = int(min_segment * (growth_seg ** rad))

            bpy.ops.mesh.primitive_uv_sphere_add(
                segments=seg_val, 
                ring_count=seg_val, 
                radius=rad,
                location=(x_val, y_val, z_val))
        
def register(): 
    bpy.utils.register_class(MESH_sphere_clouds)

def unregister():
    bpy.utils.unregister_class(MESH_sphere_clouds)

# why does this not work?? 
#if __name__ == '__main__':
#   register()

bpy.utils.register_class(MESH_sphere_clouds)
