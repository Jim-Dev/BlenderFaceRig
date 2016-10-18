#Set Collision Pivots button  
import bpy
  
class Save_ShapeKey_Button(bpy.types.Operator):
    """Button Set the pivot poit on collision objects"""
    bl_idname = "ue.setcollpivots_button"
    bl_label = "Set Collision Pivots"    
            
    def execute (self, context):
        
        #Create group
        
        
        '''    
        group = "CollisionPivotgroup"
        
        if group in bpy.data.groups:
            print ("Group already created,will be removed and created again")
            bpy.data.groups["CollisionPivotgroup"].user_clear()        
            bpy.data.groups.remove(bpy.data.groups["CollisionPivotgroup"])
            bpy.ops.group.create(name="CollisionPivotgroup")   
        else:
            bpy.ops.group.create(name="CollisionPivotgroup")        
        
        ActionGroup = bpy.data.groups["CollisionPivotgroup"]
        '''
        bpy.ops.object.select_all(action='DESELECT')
            
        #Group Operation
            
        for ob in ActionGroup.objects:
                                                           
            print (ob.name)              
            ob.select = True
            bpy.context.scene.objects.active = ob
            bpy.ops.view3d.snap_cursor_to_selected()
            FBX_SelectCollsionObjects (self,context)
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            ob.select = False
            bpy.ops.object.select_all(action='DESELECT')
            FBX_Make_Only_selectedObjLayer_visible (self,context)
            
        bpy.data.groups["CollisionPivotgroup"].user_clear()        
        bpy.data.groups.remove(bpy.data.groups["CollisionPivotgroup"])        
        
        return {'FINISHED'} 