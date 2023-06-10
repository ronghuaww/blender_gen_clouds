import bpy 
import random 
import math

class properties_sphere_clouds(bpy.types.PropertyGroup):
    num_spheres: bpy.props.IntProperty(
        name="Count", 
        description="Number of Spheres",
        default=100,
        min=1, soft_min=50, soft_max=150
    )

    span_x: bpy.props.FloatProperty(
        name="X Span", 
        description="Length of the Clouds in the X-direction", 
        default=10,
        min=0, soft_max=15
    )

    span_y: bpy.props.FloatProperty(
        name="Y Span", 
        description="Length of the Clouds in the Y-direction", 
        default=10,
        min=0, soft_max=15
    )

    radius: bpy.props.FloatProperty(
        name="Radius", 
        description="Maximum Radius of the Spheres",
        default=2, 
        min=2, soft_max=5
    )

    decay_rad: bpy.props.FloatProperty(
        name="Decay Factor", 
        description="Exponential Decay of the radius for each spheres", 
        default= 1/2,
        min=0, max= 1
    )

    midpoint_x: bpy.props.FloatProperty(
        name="X Midpoint", 
        description="X-Coordinate for where the radius is the highest",
        default=0,
        soft_min=-15/2, soft_max=15/2
    )

    midpoint_y: bpy.props.FloatProperty(
        name="Y Midpoint", 
        description="Y-Coordinate for where the radius is the highest",
        default=3,
        soft_min=-15/2, soft_max=15/2
    )

class MESH_OT_sphere_clouds(bpy.types.Operator):
    """lots of spheres for some fluffy clouds"""
    bl_idname = "mesh.sphere_clouds"
    bl_label = "Sphere Clouds"
    bl_options = {'REGISTER', 'UNDO'}

    action: bpy.props.EnumProperty(
        name="functions", 
        description="Steps in buttons",
        items=[('CREATE_SPHERES', 'Create Spheres', 'establish cloud shape'),
               ('MERGE_UNION', 'Merge', 'merge all spheres into one mesh')]
    )
    
    num_spheres_prev = 0
    span_x_prev = 0
    span_y_prev = 0

    xyz = []
    names = []

    # viewed only in 3d viewport
    @classmethod
    def poll(cls, context): 
        return context.area.type == 'VIEW_3D'

    def draw(self, context):
        var = context.scene.clouds_var
        if self.action == 'CREATE_SPHERES':
            layout = self.layout
            # text 
            layout.label(text = "Sphere Cloudssss")
            # button 
            # layout.operator('mesh.sphere_clouds', text='Sphere Clouds')
            layout.column().prop(var, "num_spheres", text="Count")
            layout.column().prop(var, "span_x", text="X Span")
            layout.column().prop(var, "span_y", text="Y Span")
            layout.column().prop(var, "radius", text="Radius")
            layout.column().prop(var, "decay_rad", text="Decay Factor")
            layout.column().prop(var, "midpoint_x", text="X Midpoint")
            layout.column().prop(var, "midpoint_y", text="Y Midpoint")


    def execute (self, context): 
        var = context.scene.clouds_var

        if self.action == 'CREATE_SPHERES':
            self.create_spheres(var)
        if self.action == 'MERGE_UNION': 
            self.merge_n_bool(self.names, var)
            
        return {'FINISHED'}
    
    def create_spheres(self, var): 
        gen_bool = True

        if (var.num_spheres != self.num_spheres_prev 
            or var.span_x != self.span_x_prev 
            or var.span_y != self.span_y_prev):
            
            self.num_spheres_prev = var.num_spheres 
            self.span_x_prev, self.span_y_prev = var.span_x, var.span_y
            self.xyz.clear()

        else: 
            gen_bool = not gen_bool

        self.sub_sphere_gen(var.num_spheres, var.span_x, var.span_y, 
                            var.midpoint_x, var.midpoint_y, var.radius, 
                            var.decay_rad, gen_bool, self.xyz, self.names)
        
    def sub_sphere_gen(self, num_spheres, span_x, span_y, midpoint_x, 
                       midpoint_y, radius, decay_rad, gen_bool, xyz, names): 
        min_radius = 0.15
        total = num_spheres if gen_bool else len(xyz)
        names.clear()

        for i in range(total): 
            x_val = random.random() * span_x - (span_x/2) 
            y_val = random.random() * span_y - (span_y/2) 
            z_val = random.random() 

            if (not gen_bool): 
                x_val, y_val, z_val = xyz[i][0], xyz[i][1], xyz[i][2]

            xy_avg = (abs(x_val + midpoint_x) + abs(y_val + midpoint_y))/2
            
            # y = ab^x (a is size, b percent, x is xy_avg)
            rad = radius * (decay_rad ** xy_avg)

            # very small rad are not generated 
            if (rad > min_radius): 
                if (gen_bool): 
                    xyz.append([x_val, y_val, z_val])

                z_val = rad + ((z_val * (rad)) - (rad/2))

                # y = log(a)(x - b) + c || y = (log(3)(x) + 2)
                seg_val = int(math.log(rad, 3) + 3) 
                seg_val = seg_val if seg_val > 0 else 1

                bpy.ops.mesh.primitive_ico_sphere_add(
                    subdivisions=seg_val,
                    radius=rad,
                    location=(x_val, y_val, z_val))
                
                loop_obj = bpy.context.active_object
                names.append(loop_obj.name)
    
    def merge_n_bool(self, names): 
        if (len(names) < 1): 
            self.report({"ERROR_INVALID_INPUT"}, 
                        "Spheres needs to be generated first.")

        else: 
            select_obj = bpy.data.objects[names[0]]
            bpy.context.view_layer.objects.active = select_obj
            last_obj = bpy.context.active_object

            for each_name in names[1:]: 
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
            names.clear()
    

class VIEW3D_PT_sphere_clouds(bpy.types.Panel): 
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Clouds"
    bl_label = "Sphere Clouds"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        var = scene.clouds_var
        
        # text 
        layout.label(text = "Sphere Clouds")
        # button 
        ######################### add icons  UILayout.operator()
        layout.operator('mesh.sphere_clouds', text='Sphere Clouds').action = 'CREATE_SPHERES'
        # layout.operator('mesh.sphere_clouds', text="Merge n union").action = 'MERGE_UNION'

        sphere_input = layout.column()

        # sphere_input.prop(var, "num_spheres")
        # sphere_input.prop(var, "span_x")
        # sphere_input.prop(var, "span_y")
        # sphere_input.prop(var, "radius")
        # sphere_input.prop(var, "decay_rad")
        # sphere_input.prop(var, "midpoint_x")
        # sphere_input.prop(var, "midpoint_y")

        
def register(): 
    bpy.utils.register_class(MESH_OT_sphere_clouds)
    bpy.utils.register_class(VIEW3D_PT_sphere_clouds)
    bpy.utils.register_class(properties_sphere_clouds)
    
    bpy.types.Scene.clouds_var = bpy.props.PointerProperty(type=properties_sphere_clouds)

def unregister():
    bpy.utils.unregister_class(MESH_OT_sphere_clouds)
    bpy.utils.unregister_class(VIEW3D_PT_sphere_clouds)
    bpy.utils.register_class(properties_sphere_clouds)

    del bpy.types.Scene.clouds_var

# why does this not work?? 
# if __name__ == '__main__':
#   register()

register()