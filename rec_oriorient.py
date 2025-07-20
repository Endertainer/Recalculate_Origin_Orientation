import bpy
import bmesh
from bpy.types import Operator


#━━━━━━━━━━━━━━
#     Main     
#━━━━━━━━━━━━━━

class REC_OT_OriginOrientation(Operator):
    bl_idname = "object.recalculate_origin_orientation"
    bl_label = "Recalculate Origin Orientation"
    bl_description = "Recalculate origin orientation to the selected face normal"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # Check if any objects are selected
        if not context.selected_objects:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}

        # Get the active object
        obj = context.active_object

        # Make sure the active object is a mesh
        if obj.type != 'MESH':
            self.report({'ERROR'}, "Selected object is not a mesh")
            return {'CANCELLED'}

        # Check that we are in Edit Mode
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Must be in Edit Mode")
            return {'CANCELLED'}

        # Access the mesh data in edit mode using BMesh
        bm = bmesh.from_edit_mesh(obj.data)

        # Get selected faces
        selected_faces = [f for f in bm.faces if f.select]

        # Ensure exactly one face is selected
        if not selected_faces:
            self.report({'ERROR'}, "No face selected")
            return {'CANCELLED'}
        elif len(selected_faces) > 1:
            self.report({'ERROR'}, "Only one face must be selected")
            return {'CANCELLED'}

        # Get the VIEW_3D area to perform transform operations
        area_type = 'VIEW_3D'
        areas = [area for area in context.window.screen.areas if area.type == area_type]

        # Enable origin transformation mode
        context.scene.tool_settings.use_transform_data_origin = True

        # Override context to access proper area for the orientation tools
        with context.temp_override(area=areas[0]):
            # Create a new transform orientation from selected face
            bpy.ops.transform.create_orientation(use=True)

            # Switch to Object Mode
            bpy.ops.object.editmode_toggle()

            # Store the name of the newly created orientation
            transform_type = context.scene.transform_orientation_slots[0].type

            # Align object to face orientation
            bpy.ops.transform.transform(
                mode='ALIGN',
                orient_type='Face',
                orient_matrix_type=transform_type,
                mirror=False,
                use_proportional_edit=False,
                snap=False
            )

            # Clean up: delete the temporary orientation
            bpy.ops.transform.delete_orientation()
            bpy.ops.transform.select_orientation(orientation='GLOBAL')

            # Switch Back to Edit Mode
            bpy.ops.object.editmode_toggle()

            # Disable origin transformation mode
            bpy.context.scene.tool_settings.use_transform_data_origin = False

        return {'FINISHED'}


# Function to draw the operator in the context menu
def draw_context_menu(self, context):
    self.layout.separator()
    self.layout.operator(REC_OT_OriginOrientation.bl_idname)


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     Register & Unregister     
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Register the classes and append the context menu to Blender's UI
def register():
    bpy.utils.register_class(REC_OT_OriginOrientation)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_context_menu)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(draw_context_menu)

# Unregister the classes and remove the context menu from Blender's UI
def unregister():
    bpy.utils.unregister_class(REC_OT_OriginOrientation)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_context_menu)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(draw_context_menu)

if __name__ == "__main__":
    register()