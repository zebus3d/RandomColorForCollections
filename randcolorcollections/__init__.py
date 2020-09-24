
import bpy
import random

bl_info = {
    "name": "Collections Color Random",
    "author": "Jorge Hernandez Melendez",
    "version": (0, 1),
    "blender": (2, 91, 0),
    "location": "",
    "description": "Random colors for all Collections",
    "warning": "",
    "wiki_url": "",
    "category": "Interface",
    }

from bpy.types import (Operator, Panel)


class RandomColorCollections(Operator):
    bl_idname = "randcol.collections"
    bl_label = "Random Color for Collections"
    bl_description = "Random colors for all Collections"

    def execute(self, context):
        # Blender 2.91.0 Alpha
        # Random color for all collections

        colors = []
        used_colors = []

        # recreamos un array con los colores hardcoded que trae blende
        # por ahora trae 8 colores
        for i in range(8):
            colors.append('COLOR_' + str(i+1).zfill(2))

        # obtenermos un color aleatoreo
        def get_rand_color():
            if len(used_colors) == 0:
                color = random.choice(colors)
                return color
            else:
                color = random.choice(colors)
                return color

        # obtener un elemento que sea de los menos repetidos de un array:
        def check_minimun(a):
            used = []
            c = 0
            result = {}
            for i in a:
                if i in used:
                    c += used.count(i)
                    result[str(i)] = c
                else:
                    used.append(i)
                    c = 1
                    result[str(i)] = c
            # return the key corresponding to the minimum value within a dictionary:
            #print(result)
            return min(result, key=result.get)

        for col in bpy.data.collections:
            if hasattr(col, 'color_tag'):
                color = get_rand_color()
                # si ya esta siendo usado
                # entonces buscamos un color que sea de los menos usados
                if color in used_colors:
                    color = check_minimun(used_colors)
                    col.color_tag = color
                    used_colors.append(color)
                else:
                    used_colors.append(color)
                    col.color_tag = color


        return {'FINISHED'}


class RC_PT_Collections(Panel):
    bl_label = "Random Color for Collections"
    bl_category = "Random Color Collections"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        flow = layout.grid_flow(align=True)
        col = flow.column()
        # col = layout.box()
        col.operator("randcol.collections", text="Random Colors for all Collections")

all_classes = [
    RandomColorCollections,
    RC_PT_Collections
]

def register():
    from bpy.utils import register_class

    for cls in all_classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(all_classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()

