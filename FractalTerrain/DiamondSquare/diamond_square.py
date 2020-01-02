bl_info = {
    "name": "Diamond Square",
    "category": "Mesh",
}

import bpy
import bmesh

class DiamondSquare(bpy.types.Operator):
  """Diamond Square"""      # blender will use this as a tooltip for menu items and buttons.
  bl_idname = "object.diamond_square"        # unique identifier for buttons and menu items to reference.
  bl_label = "Create fractal terrain using diamond square method"         # display name in the interface.
  bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

  def execute(self, context):
    level0 = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)]
    levels = [level0]
    level_count = 3
    for i in range(level_count):
      levels[i] = []
    mesh = bpy.context.object.data
    bm = bmesh.new()

    # convert the current mesh to a bmesh (must be in edit mode)
    bpy.ops.object.mode_set(mode='EDIT')
    bm.from_mesh(mesh)
    bpy.ops.object.mode_set(mode='OBJECT')  # return to object mode

    for v in verts:
      bm.verts.new(v)  # add a new vert

    # make the bmesh the object's mesh
    bm.to_mesh(mesh)
    bm.free()  # always do this when finished

    return {'FINISHED'}            # this lets blender know the operator finished successfully.

def register():
  bpy.utils.register_class(DiamondSquare)


def unregister():
  bpy.utils.unregister_class(DiamondSquare)


# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
  register()