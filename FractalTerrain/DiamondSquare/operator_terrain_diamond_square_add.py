import bpy
import bmesh
import random

from bpy.props import (
        BoolProperty,
        BoolVectorProperty,
        FloatProperty,
        FloatVectorProperty,
        IntProperty,
        )


class AddTerrainDiamondSquare(bpy.types.Operator):
    """Add a simple box mesh"""
    bl_idname = "mesh.terrain_diamond_square_add"
    bl_label = "Add Terrain (Diamond Square)"
    bl_options = {'REGISTER', 'UNDO'}

    width = FloatProperty(
            name="Width",
            description="Terrain Width",
            min=0.01, max=100.0,
            default=1.0,
            )
    height = FloatProperty(
            name="Height",
            description="Terrain Height",
            min=0.01, max=100.0,
            default=1.0,
            )
    depth = FloatProperty(
            name="Depth",
            description="Terrain Depth",
            min=0.01, max=100.0,
            default=1.0,
            )
    orderLevel = IntProperty(
            name="Order",
            description="Terrain Order",
            min=1, max=16,
            default=5,
            )
    seamless = BoolProperty(
            name="Seamless",
            description="Seamless Edges",
            default=False,
            )
    layers = BoolVectorProperty(
            name="Layers",
            description="Object Layers",
            size=20,
            options={'HIDDEN', 'SKIP_SAVE'},
            )

    # generic transform props
    view_align = BoolProperty(
            name="Align to View",
            default=False,
            )
    location = FloatVectorProperty(
            name="Location",
            subtype='TRANSLATION',
            )
    rotation = FloatVectorProperty(
            name="Rotation",
            subtype='EULER',
            )

    def execute(self, context):
        #self.report({'INFO'}, self.orderLevel)
        order = self.orderLevel
        size = 2**order+1

        verts = []
        for j in range(size):
            for i in range(size):
                verts.append([i*1.0/size,j*1.0/size,0.0])

        faces = []
        for j in range(size-1):
            for i in range(size-1):
                faces.append((j*size+i, j*size+i+1, (j+1)*size+i+1, (j+1)*size+i))

        if not self.seamless:
            for j in range(2):
                for i in range(2):
                    verts[j*(size-1)*size+i*(size-1)][2] = random.random()-0.5
        for k in range(order):
            step = 2**(order-k)
            halfstep = 2**(order-k-1)
            n = 2**k
            factor = 1.0/(2*n)
            self.report({'INFO'}, 'Iteration {0}, step: {1}, halfstep: {2}, n: {3}, factor: {4}'.format(k, step, halfstep, n, factor))
            for j in range(n):
                for i in range(n):
                    #self.report({'INFO'}, '\tVertex ({0}, {1})'.format(i, j))
                    r = 0
                    for J in range(2):
                        for I in range(2):
                            r += verts[(j+J)*step*size+(i+I)*step][2]
                    #self.report({'INFO'}, '\tVertex ({0}, {1})'.format(i, j))
                    r /= 4
                    r += (random.random()-0.5) * factor
                    verts[(j*step+halfstep)*size+i*step+halfstep][2] = r
            l = 1
            if self.seamless:
                l = 0
            for j in range(n+l):
                for i in range(n):
                    r = 0
                    N = 2
                    r += verts[j*step*size+i*step][2]
                    r += verts[j*step*size+(i+1)*step][2]
                    if j > 0:
                        r += verts[(j*step-halfstep)*size+i*step+halfstep][2]
                        N+=1
                    if j < n:
                        r += verts[(j*step+halfstep)*size+i*step+halfstep][2]
                        N+=1
                    r /= N
                    r += (random.random()-0.5) * factor
                    verts[j*step*size+i*step+halfstep][2] = r
            if self.seamless:
                for i in range(n):
                    verts[n*step*size+i*step+halfstep][2] = verts[i*step+halfstep][2]
            for j in range(n):
                for i in range(n+l):
                    r = 0
                    N = 2
                    r += verts[j*step*size+i*step][2]
                    r += verts[(j+1)*step*size+i*step][2]
                    if i > 0:
                        r += verts[(j*step+halfstep)*size+i*step-halfstep][2]
                        N+=1
                    if i < n:
                        r += verts[(j*step+halfstep)*size+i*step+halfstep][2]
                        N+=1
                    r /= N
                    r += (random.random()-0.5) * factor
                    verts[(j*step+halfstep)*size+i*step][2] = r
            if self.seamless:
                for j in range(n):
                    verts[(j*step+halfstep)*size+n*step][2] = verts[(j*step+halfstep)*size][2]

        # apply size
        for i, v in enumerate(verts):
            verts[i] = v[0] * self.width, v[1] * self.depth, v[2] * self.height

        mesh = bpy.data.meshes.new("Terrain")

        bm = bmesh.new()

        for v_co in verts:
            bm.verts.new(v_co)

        bm.verts.ensure_lookup_table()
        for f_idx in faces:
            bm.faces.new([bm.verts[i] for i in f_idx])

        bm.to_mesh(mesh)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AddTerrainDiamondSquare.bl_idname, icon='MESH_CUBE')


def register():
    bpy.utils.register_class(AddTerrainDiamondSquare)
    bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AddTerrainDiamondSquare)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    #unregister()
    register()

    # test call
    #bpy.ops.mesh.terrain_diamond_square_add()
