import bpy

enum_menu_items = [
                ('OPT1','Option 1','',1),
                ('OPT2','Option 2','',2),
                ('OPT3','Option 3','',3),
                ('OPT4','Option 4','',4),
                ('OPT5','Option 5','',5),
                ]


class LayoutPanel(bpy.types.Panel):
    bl_label = "Demo layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "ShapeKey"

    def draw(self, context):
        layout = self.layout
        self.layout.operator("object.mode_set", text='Edit', icon='EDITMODE_HLT').mode='EDIT'

        layout.label("Some Operators")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.operator("object.mode_set", text="Button1", icon='OBJECT_DATAMODE').mode='OBJECT'
        row.operator("object.mode_set", text="Button2", icon='SCULPTMODE_HLT').mode='SCULPT'
        row.operator("object.mode_set", text="Button3", icon='TPAINT_HLT').mode='TEXTURE_PAINT'

        row = layout.row()
        box = row.box()

        row = box.row()
        row.label("Some menus", icon='LINENUMBERS_ON')

        #row = box.row()
        # add the custom menu defined above
        #box.menu(CustomMenu.bl_idname, 'My custom menu', icon='SCRIPTWIN')

        #row = box.row()
        # add a standard blender menu - the add menu
        #box.menu('INFO_MT_mesh_add', 'Add', icon='ZOOMIN')

        row = box.row()
        # add an enum property menu
        # this allows only certain values to be set for a property
        box.prop_menu_enum(context.scene, 'test_enum', text='enum property', icon='NLA')



class WriteShapeKey(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Hello World Panel"
    bl_idname = "READ_SHAPE_KEY"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "ShapeKey"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Hello world!", icon='WORLD_DATA')

        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        row = layout.row()
        row.prop(obj, "name")

        row = layout.row()
        row.operator("mesh.primitive_cube_add")


class ShapeK(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Hello World Panel"
    bl_idname = "SHAPE_KEY_GENERIC"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "ShapeKey"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Hello world!", icon='WORLD_DATA')

        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        row = layout.row()
        row.prop(obj, "name")

        row = layout.row()
       
        #row.operator("mesh.primitive_cube_add")
        

class ReadShapeKey(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Generic"
    bl_idname = "WRITE_SHAPE_KEY"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "ShapeKey"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        row = layout.row()
        row.label(text="Active object is: " + obj.active_shape_key.name)

        row = box.row()
        # add an enum property menu
        # this allows only certain values to be set for a property
        box.prop_menu_enum(context.scene, 'test_enum', text='enum property', icon='NLA')


def register():
    
    object = bpy.context.object
    
    bpy.types.Scene.test_enum = bpy.props.EnumProperty(items=enum_menu_items)
    bpy.types.Scene.sk_enum = bpy.props.EnumProperty(items=enum_menu_items)
    bpy.utils.register_class(WriteShapeKey)
    bpy.utils.register_class(ReadShapeKey)
    bpy.utils.register_class(LayoutPanel)
    bpy.utils.register_class(ShapeK)
def unregister():
    bpy.utils.unregister_class(WriteShapeKey)
    bpy.utils.unregister_class(ReadShapeKey)
    bpy.utils.unregister_class(LayoutPanel)
    bpy.utils.unregister_class(ShapeK)
    del bpy.types.Scene.test_enum
    del bpy.types.Scene.sk_enum

if __name__ == "__main__":
    register()
