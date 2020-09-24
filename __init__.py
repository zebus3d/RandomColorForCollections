
import bpy
import random
from bpy.types import (Operator, Panel)
from itertools import cycle

bl_info = {
    "name": "Collections Color Random",
    "author": "Jorge Hernandez Melendez",
    "version": (0, 2),
    "blender": (2, 91, 0),
    "location": "",
    "description": "Random colors for all Collections",
    "warning": "",
    "wiki_url": "",
    "category": "Interface",
}


class RandomColorCollections(Operator):
    bl_idname = "randcol.collections"
    bl_label = "Random Color for Collections"
    bl_description = "Random colors for all Collections"

    def execute(self, context):
        # Blender 2.91.0 Alpha
        # Random color for all collections

        colors = []
        used_colors = []
        hardcoded_bcolors = 8

        # recreamos un array con los colores hardcoded que trae blende
        # por ahora trae 8 colores
        for i in range(hardcoded_bcolors):
            colors.append('COLOR_' + str(i + 1).zfill(2))

        if bpy.types.WindowManager.random_color_collections_toggle % 2 == 0:
            pool = cycle(colors)
            bpy.types.WindowManager.random_color_collections_toggle = 1
        else:
            pool = cycle(colors[::-1])
            bpy.types.WindowManager.random_color_collections_toggle = 0

        for col in bpy.data.collections:
            color = next(pool)
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
        col.operator(
            "randcol.collections",
            text="Random Colors for all Collections"
        )


all_classes = [
    RandomColorCollections,
    RC_PT_Collections
]


def register():
    from bpy.utils import register_class

    for cls in all_classes:
        register_class(cls)

    bpy.types.WindowManager.random_color_collections_toggle = 0


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(all_classes):
        unregister_class(cls)

    del bpy.types.WindowManager.random_color_collections_toggle


if __name__ == "__main__":
    register()
