bl_info = {
    "name": "CarGen",
    "blender": (2, 80, 0),
    "category": "Object",
    "description": "Generate car shaped object",
    "author": "Flavien Pagerie",
    "version": (0, 0, 1),
}

import bpy

from . import gui


def register():
    bpy.utils.register_class(gui.CarCreation)
    bpy.utils.register_class(gui.CarPanel)
    
def unregister():
    bpy.utils.unregister_class(gui.CarPanel)
    bpy.utils.unregister_class(gui.CarCreation)

if __name__ == "__main__":
    register()
