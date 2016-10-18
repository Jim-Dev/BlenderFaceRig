# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Shape Key Extras",
    "description": "",
    "author": "poor",
    "version": (0, 0, 1),
    "blender": (2, 74, 0),
    "location": "Properties > Object Data > Shape Keys",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"
}

import bpy
import random

from bpy.props import (IntProperty,
                       BoolProperty,
                       FloatProperty,
                       StringProperty,
                       PointerProperty)

from bpy.types import (Operator,
                       PropertyGroup)

# -------------------------------------------------------------------
# helper    
# -------------------------------------------------------------------

def name_startswith_exclude(char_sequence, name):
    if char_sequence:
        char_list = [i.strip() for i in char_sequence.split(",")]
        if name.startswith(tuple(char_list)):
            return True
        else: 
            return False
    else: 
        return False

# -------------------------------------------------------------------
# properties    
# -------------------------------------------------------------------

class ShapeKeyExtrasSettings(PropertyGroup):

    value = FloatProperty(
        name = "Value",
        description = "Set static value",
        default = 0,
        #min = 0,
        #max =1
        )
    random_min = FloatProperty(
        name = "Min",
        description = "Set minimum random value",
        default = 0,
        #min = 0,
        #max =1
        )
    random_max = FloatProperty(
        name = "Max",
        description = "Set maximum random value",
        default = 1,
        #min = 0,
        #max =1
        )
    apply_enabled = BoolProperty (
        name = "Apply values for enabled Keys only",
        description = "Apply values for enabled Keys only",
        default = True 
        )
    exclude = StringProperty (
        name = "Exclude",
        description = "Exclude by first character",
        default = "#, =, *"
        )

# -------------------------------------------------------------------
# operators    
# -------------------------------------------------------------------

class EnableAllButton (Operator):
    bl_idname = "shapekeyextras.enable_all"
    bl_label = "Enable All"
    bl_description = "Enable all Shape Keys"

    def execute(self, context):       
        for shapekey in context.object.data.shape_keys.key_blocks:
            shapekey.mute = False

        self.report({'INFO'}, "All enabled")     
        return {'FINISHED'}


class DisableAllButton (Operator):
    bl_idname = "shapekeyextras.disable_all"
    bl_label = "Disable All"
    bl_description = "Disable all Shape Keys"

    def execute(self, context):       
        for shapekey in context.object.data.shape_keys.key_blocks:
            shapekey.mute = True

        self.report({'INFO'}, "All Shape Keys disabled")        
        return {'FINISHED'}

class ToggleAllButton (Operator):
    bl_idname = "shapekeyextras.toggle"
    bl_label = "Toggle Mute"
    bl_description = "Toggle Mute of all Shape Keys"

    def execute(self, context):        
        for shapekey in context.object.data.shape_keys.key_blocks:
            shapekey.mute = not shapekey.mute

        self.report({'INFO'}, "Enabled Shape Keys disabled and Disabled Shape Keys enabled")          
        return {'FINISHED'}

class RandomizeValueButton (Operator):
    bl_idname = "shapekeyextras.randomize"
    bl_label = "Randomize"
    bl_description = "Randomize all Shape Key Values"

    def execute(self, context):
        scn = context.scene
        ske = scn.shape_key_extras

        if ske.apply_enabled is True:       
            for shapekey in context.object.data.shape_keys.key_blocks:
                exclude_char = name_startswith_exclude(ske.exclude, shapekey.name)
                if shapekey.name is not 'Basis' and exclude_char is not True:
                    if shapekey.mute is False:
                        shapekey.value = random.uniform(ske.random_min, ske.random_max)
        else:
            for shapekey in context.object.data.shape_keys.key_blocks:
                exclude_char = name_startswith_exclude(ske.exclude, shapekey.name)
                if shapekey.name is not 'Basis' and exclude_char is not True:
                    shapekey.value = random.uniform(ske.random_min, ske.random_max)

        self.report({'INFO'}, "Values for Shape Keys generated")
        return {'FINISHED'}

class ApplyValueButton (Operator):
    bl_idname = "shapekeyextras.apply"
    bl_label = "Apply"
    bl_description = "Apply a static Value to all Shape Keys"

    def execute(self, context):
        scn = context.scene
        ske = scn.shape_key_extras

        if ske.apply_enabled is True:       
            for shapekey in context.object.data.shape_keys.key_blocks:
                exclude_char = name_startswith_exclude(ske.exclude, shapekey.name)
                if shapekey.name is not 'Basis' and exclude_char is not True:              
                    if shapekey.mute is False:
                        shapekey.value = ske.value
        else:
            for shapekey in context.object.data.shape_keys.key_blocks:
                exclude_char = name_startswith_exclude(ske.exclude, shapekey.name)
                if shapekey.name is not 'Basis' and exclude_char is not True:
                    shapekey.value = ske.value

        self.report({'INFO'}, "Value assigned to Shape Keys")        
        return {'FINISHED'}


# -------------------------------------------------------------------
# ui    
# -------------------------------------------------------------------

def draw_shapekey_extras(self, context):

    scn = context.scene
    layout = self.layout
    ske = scn.shape_key_extras

    layout.separator()

    row = layout.row()
    col = layout.column(align=True)
    row.label("Mute State:")
    rowsub = col.row(align=True)
    rowsub.operator("shapekeyextras.enable_all", icon="RESTRICT_VIEW_OFF")
    rowsub.operator("shapekeyextras.disable_all", icon="RESTRICT_VIEW_ON")
    col.operator("shapekeyextras.toggle", icon="FILE_REFRESH")

    row = layout.row()
    row.label("Set Shape Key Values:")
    col = layout.column(align=True)
    rowsub = col.row(align=True)
    rowsub.prop(ske, "random_min")
    rowsub.prop(ske, "random_max")
    col.operator("shapekeyextras.randomize")
    col.prop(ske, "value")
    col.operator("shapekeyextras.apply")
    col = layout.column(align=True)
    col.prop(ske, "exclude")
    col = layout.column(align=True)
    col.prop(ske, "apply_enabled")


# -------------------------------------------------------------------
# register    
# -------------------------------------------------------------------

def register():
    bpy.utils.register_module(__name__)
    bpy.types.DATA_PT_shape_keys.append(draw_shapekey_extras)
    bpy.types.Scene.shape_key_extras = PointerProperty(type=ShapeKeyExtrasSettings)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.DATA_PT_shape_keys.remove(draw_frame_rate_menu)
    del bpy.types.Scene.shape_key_extras

if __name__ == "__main__":
    register()