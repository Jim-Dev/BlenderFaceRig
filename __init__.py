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
    
targetPath = "D:\\"
fname = ""
ext=""
SK_PREFIX = "NEW_"
shapekeyExtension = ".shapekey"

def GetScene():
    return bpy.context.scene

def GetSelectedObject():
    return bpy.context.object

def MuteAllShapeKeys():
    for shapeKey in GetSelectedObject().data.shape_keys.key_blocks:
    # toggle (if true set it to false and vice versa)
        shapeKey.mute = not shapeKey.mute
        
def ResetAllShapeKeys():
    for shapeKey in GetSelectedObject().data.shape_keys.key_blocks:
    # toggle (if true set it to false and vice versa)
        shapeKey.value = 0
      
def GetShapeKeyCount():
    return len(GetSelectedObject().data.shape_keys.key_blocks)

def GetShapeKeyByIndex(shapekeyIndex):
    return GetSelectedObject().data.shape_keys.key_blocks[shapekeyIndex]
      
def GetBaseShapeKey():
    return GetShapeKeyByIndex(0)
  
def GetActiveShapeKey():
    return GetSelectedObject().active_shape_key

  
def GetActiveShapeKeyIndex():
  return GetSelectedObject().active_shape_key_index
  
def GetBaseShapeKeyVertexCount():
    return len(GetSelectedObject().data.shape_keys.key_blocks[0].data)

def GetShapeKeyVertexCount(skIndex):
    return len(GetSelectedObject().data.shape_keys.key_blocks[skIndex].data)

  
def GetDeformVertex(skIndex):
    BaseSK = GetBaseShapeKey()
    ActiveSK = GetActiveShapeKey()
    DefVertex = {}
    
    for i in range(GetShapeKeyVertexCount(GetSelectedObject().active_shape_key_index)):
        activeVertex = ActiveSK.data[i].co
        baseVertex = BaseSK.data[i].co
        if (activeVertex != baseVertex):
            DefVertex[i]=[activeVertex.x,activeVertex.y,activeVertex.z]
            #DefVertex[i]=activeVertex
            #DefVertex.append(activeVertex)
    return DefVertex

def SaveShapeKeyToFile(shapeKeyIndex):
  
    (fname,ext) = os.path.splitext(targetPath)
    #filepath = fname + shapekeyExtension
    
    tmpShapeKey = GetShapeKeyByIndex(shapeKeyIndex)
    fname = tmpShapeKey.name
    print (bpy.types.Scene.conf_path)
    filepath = os.path.join(GetScene().conf_path,fname+shapekeyExtension)# targetPath+fname + shapekeyExtension
    #filepath = fname + tmpShapeKey.name + shapekeyExtension
    tmpShapeKey.value = tmpShapeKey.slider_max

    DefVertex = GetDeformVertex(shapeKeyIndex)
        #JsonVertexDump = json.dumps(DefVertex, sort_keys=True,indent=4, separators=(',', ': '))
        
    ShapeKeyEntry = {}
    ShapeKeyEntry[tmpShapeKey.name]=DefVertex
    JsonVertexDump = json.dumps(ShapeKeyEntry, sort_keys=True,indent=4, separators=(',', ': '))

    with open(filepath, 'w', encoding='utf-8') as f:
      f.write(JsonVertexDump)
    f.closed
    GetActiveShapeKey().value = 0

    return True
    
class SaveVisibleShapeKeys_Button(bpy.types.Operator):
    """Button Set the pivot poit on collision objects"""
    bl_idname = "sk.save_allvisible"
    bl_label = "Save Visible Shape keys"    
            
    def execute (self, context):
        for i in range(GetShapeKeyCount()):
            if not (GetShapeKeyByIndex(i).mute):
                SaveShapeKeyToFile(i)
      

        

        return {'FINISHED'} 
    
    
    
class SaveShapeKey_Button(bpy.types.Operator):
    """Button Set the pivot poit on collision objects"""
    bl_idname = "sk.save"
    bl_label = "Save Shape key"    
            
    def execute (self, context):
      
        SaveShapeKeyToFile(GetActiveShapeKeyIndex())

        return {'FINISHED'} 
    
class LoadShapeKey_Button(bpy.types.Operator):
    """Button Set the pivot poit on collision objects"""
    bl_idname = "sk.load"
    bl_label = "Save Shape key"    
            
    def execute (self, context):
        (fname,ext) = os.path.splitext(targetPath)
        filepath = fname + shapekeyExtension

        
        with open(filepath, 'r', encoding='utf-8') as f:
            fileContent = f.read()
        f.closed


        deserializedContent = json.loads(fileContent)

        shapeKeyNames = deserializedContent.keys()
       
        ResetAllShapeKeys()
        
        
        for shapeKeyName in shapeKeyNames:
            print(shapeKeyName)
            if (shapeKeyName in GetSelectedObject().data.shape_keys.key_blocks.keys()):
                GetSelectedObject().shape_key_add(SK_PREFIX+shapeKeyName)
            else:
                GetSelectedObject().shape_key_add(shapeKeyName)
                
            vertexStructure = deserializedContent[shapeKeyName]
            vertexIndices = vertexStructure.keys()
            
            for vertexIndex in vertexIndices:
                print (vertexIndex)
                print(vertexStructure[str(vertexIndex)])
                print(vertexStructure[str(vertexIndex)][0])
                
                GetSelectedObject().data.shape_keys.key_blocks[shapeKeyName].data[int(vertexIndex)].co.x = vertexStructure[vertexIndex][0]
                GetSelectedObject().data.shape_keys.key_blocks[shapeKeyName].data[int(vertexIndex)].co.y = vertexStructure[vertexIndex][1]
                GetSelectedObject().data.shape_keys.key_blocks[shapeKeyName].data[int(vertexIndex)].co.z = vertexStructure[vertexIndex][2]
      
        
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
        row.label(text="Base Vertex count: " + str(GetBaseShapeKeyVertexCount()))
        row = layout.row()
        row.label(text="Active shape key is: " + obj.active_shape_key.name)
        row = layout.row()
        row.label(text="Active Vertex count: " + str(GetShapeKeyVertexCount(GetSelectedObject().active_shape_key_index)))
        row = layout.row()
        row.label(text="Active Vertex count: " + str(len(GetDeformVertex(GetSelectedObject().active_shape_key_index))))
        row = layout.row()
        row.operator("sk.save", text="Save Selected",icon='SAVE_COPY') 
        row.operator("sk.save_allvisible", text="Save Visible",icon='VISIBLE_IPO_ON')
        row = layout.row()
        row.operator("sk.load", text="Load ShapeKey",icon='LOAD_FACTORY')   
        
        box6 = layout.row().box()
        col= box6.column()
        row=box6.row(align=True)

        col.prop(context.scene, 'conf_path',text = "SK Path ")
    
classes = [
    SaveShapeKey_Button,
    SaveVisibleShapeKeys_Button,
    LoadShapeKey_Button,
    ShapeKeyInfo_Panel
    ]     
    
def register():

    #object = bpy.context.object
    #bpy.types.Scene.test_enum = bpy.props.EnumProperty(items=enum_menu_items)
    bpy.types.Scene.conf_path = bpy.props.StringProperty \
      (
      name = "Root Path",
      default = "",
      description = "Define the root path of the project",
      subtype = 'DIR_PATH'
      )
    for c in classes:        
        bpy.utils.register_class(c)
    
def unregister():
    
    #del bpy.types.Scene.test_enum
    del bpy.types.Scene.conf_path
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()