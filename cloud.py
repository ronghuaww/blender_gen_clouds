import bpy 
import random 
import math

class MESH_OT_sphere_clouds(bpy.types.Operator):
    """lots of spheres for some fluffy clouds"""
    bl_idname = "mesh.sphere_clouds"
    bl_label = "Sphere Clouds"
    bl_options = {'REGISTER', 'UNDO'}

    num_spheres_prev = 0
    span_x_prev = 0
    span_y_prev = 0

    num_spheres: bpy.props.IntProperty(
        name="Number of Spheres", 
        description="Number of Spheres",
        default=100,
        min=1, soft_min=50,soft_max=150
    )

    span_x: bpy.props.FloatProperty(
        name="X", 
        description="Length of the Clouds in the X-direction", 
        default=10,
        min=0, soft_max=15
    )

    span_y: bpy.props.FloatProperty(
        name="Y", 
        description="Length of the Clouds in the Y-direction", 
        default=10,
        min=0, soft_max=15
    )

    radius: bpy.props.FloatProperty(
        name="Maximum Radius", 
        description="Maximum Radius of the Spheres",
        default=2, 
        min=2, soft_max=5
    )

    decay_rad: bpy.props.FloatProperty(
        name="Radius Decay Factor", 
        description="Exponential Decay of the radius for each spheres", 
        default= 1/2,
        min=0, max= 1
    )

    midpoint_x: bpy.props.FloatProperty(
        name="Midpoint X-Coordinate", 
        description="X-Coordinate for where the radius is the highest",
        default=0,
        soft_min=-15/2, soft_max=15/2
    )

    midpoint_y: bpy.props.FloatProperty(
        name="Midpoint Y-Corrdinate", 
        description="Y-Coordinate for where the radius is the highest",
        default=3,
        soft_min=-15/2, soft_max=15/2
    )

    xyz = []
    names = []


    # @classmethod
    # def poll(cls, context): 
    #     return context.area.type == 'VIEW_3D'

    # def draw(self, context):
    #     layout = self.layout
    #     # text 
    #     layout.label(text = "Sphere Cloudssss")
    #     # button 
    #     layout.operator('mesh.sphere_clouds', text='Sphere Clouds')

    def execute (self, context): 
        gen_bool = True

        if (self.num_spheres != self.num_spheres_prev 
            or self.span_x != self.span_x_prev 
            or self.span_y != self.span_y_prev):
            
            self.num_spheres_prev = self.num_spheres 
            self.span_x_prev = self.span_x
            self.span_y_prev = self.span_y

            self.xyz.clear()
            self.names.clear()
        
        else: 
            gen_bool = not gen_bool

        self.my_clouds_gen(self.num_spheres, self.span_x, self.span_y, 
                           self.midpoint_x, self.midpoint_y, self.radius, 
                           self.decay_rad, gen_bool, self.xyz, self.names)
        
        #how do i make this into a conditional button
        self.my_merge_n_bool(self.names)

        return {'FINISHED'}
    
    def my_clouds_gen(self, num_spheres, span_x, span_y, midpoint_x, midpoint_y, 
                      radius, decay_rad, gen_bool, xyz, names): 
        min_radius = 0.15
        total = num_spheres if gen_bool else len(xyz)

        for i in range(total): 
            x_val = random.random() * span_x - (span_x/2) 
            y_val = random.random() * span_y - (span_y/2) 
            z_val = random.random() 

            if (not gen_bool): 
                x_val, y_val, z_val = xyz[i][0], xyz[i][1], xyz[i][2]
                

            xy_avg = (abs(x_val + midpoint_x) + abs(y_val + midpoint_y))/2
            
            # y = ab^x (a is size, b percent, x is xy_avg)
            rad = radius * (decay_rad ** xy_avg)

            # small rad are not generated 
            if (rad > min_radius): 
                if (gen_bool): 
                    xyz.append([x_val, y_val, z_val])

                z_val = rad + ((z_val * (rad)) - (rad/2))

                # y = log(a)(x - b) + c
                # y = log(3)(x) + 2
                seg_val = int(math.log(rad, 3) + 3) 
                seg_val = seg_val if seg_val > 0 else 1

                bpy.ops.mesh.primitive_ico_sphere_add(
                    subdivisions=seg_val,
                    radius=rad,
                    location=(x_val, y_val, z_val))
                
                loop_obj = bpy.context.active_object
                names.append(loop_obj.name)
    
    def my_merge_n_bool(self, names): 
        # selects last obj created from the cloud_gen method
        last_obj = bpy.context.active_object

        for each_name in names[:-1]: 
            select_obj = bpy.data.objects[each_name]
            bpy.context.view_layer.objects.active = select_obj
            loop_obj = bpy.context.active_object
                
            # modifiers with selected obj 
            mod_bool = loop_obj.modifiers.new("boolean", 'BOOLEAN') 
            mod_bool.operation = 'UNION'
            mod_bool.object = last_obj
            bpy.ops.object.modifier_apply(modifier="boolean")

            del_prev = bpy.data.objects 
            del_prev.remove(del_prev[last_obj.name], do_unlink=True)

            last_obj = loop_obj
    

class VIEW3D_PT_sphere_clouds(bpy.types.Panel): 
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Clouds"
    bl_label = "Sphere Clouds"


    def draw(self, context):
        layout = self.layout
        # text 
        layout.label(text = "Sphere Clouds")
        # button 
        layout.operator('mesh.sphere_clouds', text='Sphere Clouds')

        # layout.column().prop(context.scene.cursor, "mesh.sphere_clouds", text="Location")
        # layout.column().prop(MESH_OT_sphere_clouds, "num_spheres", text="Location")
        
def register(): 
    bpy.utils.register_class(MESH_OT_sphere_clouds)
    bpy.utils.register_class(VIEW3D_PT_sphere_clouds)

def unregister():
    bpy.utils.unregister_class(MESH_OT_sphere_clouds)
    bpy.utils.unregister_class(VIEW3D_PT_sphere_clouds)

# why does this not work?? 
# if __name__ == '__main__':
#   register()

bpy.utils.register_class(MESH_OT_sphere_clouds)
bpy.utils.register_class(VIEW3D_PT_sphere_clouds)