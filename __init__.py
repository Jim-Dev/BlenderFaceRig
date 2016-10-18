"""
**Project Name:**      Shape key bake

**Product Home Page:** https://github.com/Jim-Dev/BlenderFaceRig

**Code Home Page:**    https://github.com/Jim-Dev/BlenderFaceRig

**Authors:**           Jimmy Toledo

**Copyright(c):**      

**Licensing:**         AGPL3

    

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


Abstract
--------

"""

import bpy
import os
import json

#from ui_buttons import Save_ShapeKey_Button

bl_info = {
    "name": "Shape key bake",
    "author": "Jimmy Toledo",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }
    
targetPath = "D:\CustomTarget"
fname = ""
ext=""
SK_PREFIX = "NEW_"

def MuteAllShapeKeys():
    for shapeKey in bpy.context.object.data.shape_keys.key_blocks:
    # toggle (if true set it to false and vice versa)
        shapeKey.mute = not shapeKey.mute
        
def ResetAllShapeKeys():
    for shapeKey in bpy.context.object.data.shape_keys.key_blocks:
    # toggle (if true set it to false and vice versa)
        shapeKey.value = 0

def GetBaseShapeKey():
    return bpy.context.object.data.shape_keys.key_blocks[0]
def GetActiveShapeKey():
    return bpy.context.object.active_shape_key

def GetSKVertexCount(skIndex):
    return len(bpy.context.object.data.shape_keys.key_blocks[skIndex].data)

def GetDeformVertex(skIndex):
    BaseSK = GetBaseShapeKey()
    ActiveSK = GetActiveShapeKey()
    DefVertex = {}
    
    for i in range(GetSKVertexCount(bpy.context.object.active_shape_key_index)):
        activeVertex = ActiveSK.data[i].co
        baseVertex = BaseSK.data[i].co
        if (activeVertex != baseVertex):
            DefVertex[i]=[activeVertex.x,activeVertex.y,activeVertex.z]
            #DefVertex[i]=activeVertex
            #DefVertex.append(activeVertex)
    return DefVertex

def WriteToDisk(filepath,shapeKey):
    file = open(filepath, "w")
    #file.write('   \n')

    fl = []
    #for block in object.data.shape_keys.key_blocks:
    fl.append(shapeKey.name)
    dataID=0
    for data in shapeKey.data:        
        vertex = data.co
        fl.append(str(dataID) +" "+str(vertex.x)+" "+str(vertex.y)+" "+str(vertex.z))


    file.write("\n".join(fl))
    file.write('    ]\n}\n')
    file.close()
    
class SaveShapeKey_Button(bpy.types.Operator):
    """Button Set the pivot poit on collision objects"""
    bl_idname = "sk.save"
    bl_label = "Save Shape key"    
            
    def execute (self, context):
        (fname,ext) = os.path.splitext(targetPath)
        filepath = fname + ".target"

        GetActiveShapeKey().value = GetActiveShapeKey().slider_max

        DefVertex = GetDeformVertex(bpy.context.object.active_shape_key_index)
        #JsonVertexDump = json.dumps(DefVertex, sort_keys=True,indent=4, separators=(',', ': '))
        
        ShapeKeyEntry = {}
        ShapeKeyEntry[bpy.context.object.active_shape_key.name]=DefVertex
        JsonVertexDump = json.dumps(ShapeKeyEntry, sort_keys=True,indent=4, separators=(',', ': '))
        
        with open(filepath, 'w') as f:
            f.write(JsonVertexDump)
        f.closed
        GetActiveShapeKey().value = 0
        
        print(GetDeformVertex(bpy.context.object.active_shape_key_index))
        print("\n")


        return {'FINISHED'} 
    
class LoadShapeKey_Button(bpy.types.Operator):
    """Button Set the pivot poit on collision objects"""
    bl_idname = "sk.load"
    bl_label = "Save Shape key"    
            
    def execute (self, context):
        (fname,ext) = os.path.splitext(targetPath)
        filepath = fname + ".target"

        
        with open(filepath, 'r') as f:
            fileContent = f.read()
        f.closed


        deserializedContent = json.loads(fileContent)
        '''
        print ("JSON BEGIN!!!!")
        vertexIndices = deserializedContent.keys()
        for vertexIndex in vertexIndices:
            print (vertexIndex)
            print(deserializedContent[vertexIndex])
        print ("JSON END!!!!")
'''     
        shapeKeyNames = deserializedContent.keys()
        '''
        for shapeKeyName in shapeKeyNames:
            print(shapeKeyName)
            vertexStructure = deserializedContent[shapeKeyName]
            vertexIndices = vertexStructure.keys()
            
            #vertexIndices = shapeKeyName.values()
            for vertexIndex in vertexIndices:
                print (vertexIndex)
                print(vertexStructure[str(vertexIndex)])
        
        '''
        ResetAllShapeKeys()
        
        
        for shapeKeyName in shapeKeyNames:
            print(shapeKeyName)
            if (shapeKeyName in bpy.context.object.data.shape_keys.key_blocks.keys()):
                bpy.context.object.shape_key_add(SK_PREFIX+shapeKeyName)
            else:
                bpy.context.object.shape_key_add(shapeKeyName)
                
            vertexStructure = deserializedContent[shapeKeyName]
            vertexIndices = vertexStructure.keys()
            
            #vertexIndices = shapeKeyName.values()
            for vertexIndex in vertexIndices:
                print (vertexIndex)
                print(vertexStructure[str(vertexIndex)])
                print(vertexStructure[str(vertexIndex)][0])
                
                bpy.context.object.data.shape_keys.key_blocks[shapeKeyName].data[int(vertexIndex)].co.x = vertexStructure[vertexIndex][0]
                bpy.context.object.data.shape_keys.key_blocks[shapeKeyName].data[int(vertexIndex)].co.y = vertexStructure[vertexIndex][1]
                bpy.context.object.data.shape_keys.key_blocks[shapeKeyName].data[int(vertexIndex)].co.z = vertexStructure[vertexIndex][2]
       
        '''
        bpy.context.object.shape_key_add("NewProcSK")
        for vertexIndex in vertexIndices:
            print(deserializedContent[vertexIndex])
            bpy.context.object.data.shape_keys.key_blocks["NewProcSK"].data[int(vertexIndex)].co.x = deserializedContent[vertexIndex][0]
            bpy.context.object.data.shape_keys.key_blocks["NewProcSK"].data[int(vertexIndex)].co.y = deserializedContent[vertexIndex][1]
            bpy.context.object.data.shape_keys.key_blocks["NewProcSK"].data[int(vertexIndex)].co.z = deserializedContent[vertexIndex][2]
        print ("JSON END!!!!")
        '''
        
        return {'FINISHED'} 

    
    
class ShapeKeyInfo_Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Generic3"
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
        row.label(text="Base shape key is: " + GetBaseShapeKey().name)
        row = layout.row()
        row.label(text="Base Vertex count: " + str(len(GetBaseShapeKey().data)))
        row = layout.row()
        row.label(text="Active shape key is: " + obj.active_shape_key.name)
        row = layout.row()
        row.label(text="Active Vertex count: " + str(GetSKVertexCount(bpy.context.object.active_shape_key_index)))
        row = layout.row()
        row.label(text="Active Vertex count: " + str(len(GetDeformVertex(bpy.context.object.active_shape_key_index))))
        row = layout.row()
        row.operator("sk.save", text="Save ShapeKey",icon='INLINK')   
        row.operator("sk.load", text="Load ShapeKey",icon='INLINK')   
        
        box6 = layout.row().box()
        col= box6.column()
        row=box6.row(align=True)
        col.label(text='SK Name:') 
        row.prop(context.scene,'FBX_base_name', expand=True)                       
        col.prop(context.scene,'FBX_Export_Custom_Name',text = "Custom Name")
    
classes = [
    SaveShapeKey_Button,
    LoadShapeKey_Button,
    ShapeKeyInfo_Panel
    ]     
    
def register():

    #object = bpy.context.object
    #bpy.types.Scene.test_enum = bpy.props.EnumProperty(items=enum_menu_items)
    for c in classes:        
        bpy.utils.register_class(c)
    
def unregister():
    
    #del bpy.types.Scene.test_enum
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()