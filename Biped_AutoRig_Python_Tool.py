# ---------------------------------------------------------------------------------------
# Biped Auto-Rig Tool – Definition Script
# Developed by Arrow Lyu
#
# ---------------------------------------------------------------------------------------
# This script contains the core rigging functions for creating a biped auto-rig system.
# Designed for humanoid or two-legged creature rigs in Autodesk Maya using Python.
# The functions defined here are modular and reusable in your auto-rig pipeline.
#
# The rig is based on Python modules and concepts learned from my professor Dennis Turner.
# Some module structures are quoted with permission and adapted for this use.
#
# Use this together with the run script: Biped_AutoRig_Creation.py
#
# How to Use:
# 1. Make sure your character is properly positioned and named in Maya.
# 2. Manually place the locators to match your character’s proportions.
# 3. Select which modules to add or remove.
# 4. Run the script and start painting weights.
#
# =======================
#
# Happy rigging!
# ---------------------------------------------------------------------------------------
# (c) 2025 by Arrow Lyu. All rights reserved. For portfolio and educational use only.
# ---------------------------------------------------------------------------------------



import sys; sys.dont_write_bytecode=True
import maya.cmds as cmds
import importlib
import maya.api.OpenMaya as om

import den_Utilities_v12 as denUt
importlib.reload(denUt)
print(denUt.__file__)


# ---------------------------------------------------------------------------------------
# Create Single Pivot Rig (Cog/root pivot group)

def jly_makeBasePiv(name='RigName', radius=1.0, dpTime = 0.01 ):
    
    # Make a big master pivot grp to hold other pivots
    RootPivGrp = denUt.den_makeGrp( nodeName=name+'_Piv_Grp', pos=(0,0,0) )
    # Lock selected grp xyz attributes, except visibility
    denUt.den_Lock(  1,1,1 , 1,1,1 , 1,1,1 , 0 )
    # Make a base rig pivot grp for base rig
    BasePivGrp = denUt.den_makeGrp( nodeName='BasePiv_Grp', pos=(0,0,0) )
    # Lock selected grp xyz attributes, except visibility
    denUt.den_Lock(  1,1,1 , 1,1,1 , 1,1,1 , 0 )
    # Parent base pivot grp under the master root pivot grp
    BasePivGrp = cmds.parent( BasePivGrp, RootPivGrp )[0]
    # Make a locator to be Cog pivot, 1 meter up from the ground
    denUt.den_makeLoc( nodeName='Cog_Piv', pos=(0, 100, 0), radius=radius )
    # Change display override color to color20(pink), do it on the Shape (not the object) so only the target gets the color
    denUt.den_ColorShape(20)
    # Lock all except translation
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    # Parent Cog under base rig pivot grp
    cmds.parent( 'Cog_Piv', BasePivGrp )
    # Use DiagPause to show the building process
    denUt.den_DiagPause( seconds=dpTime )
    # Return the big master pivot grp
    return RootPivGrp


# ---------------------------------------------------------------------------------------
# Create Base Rig (root rig group)

def jly_makeBaseRig(label='abcdef',ctrlRadius=50.0, dpTime = 0.01 ):
    # Make a big master rig grp to hold other rig parts
    RootRigGrp = denUt.den_makeGrp( nodeName=label+'_Rig_Grp', pos=(0,0,0) )
    # Lock all the attributes, except visibility
    denUt.den_Lock(  1,1,1 , 1,1,1 , 1,1,1 , 0 )    
    # Make a grp for the rig
    BaseRigGrp = denUt.den_makeGrp( nodeName='Base_Grp', pos=(0,0,0) )
    # Lock all the attributes, except visibility
    denUt.den_Lock(  1,1,1 , 1,1,1 , 1,1,1 , 0 )
    # Parent base rig grp under root rig grp
    BaseRigGrp = cmds.parent( BaseRigGrp, RootRigGrp )
    # Set 5 variables for every rig parts:
    BaseSpaceINs = [] # SpaceINs and SpaceOUTs are used to connect 2 body parts
    BaseSpaceOUTs = [] 
    BaseBindJoints = [] # BaseBindJoints hold names of all the Jx joints
    BaseCtrlsALL = [] # BaseCtrlsALL holds names of all the controls
    BaseGutsALL = [] 
    
    # Asking what's the translate value of cog pivot, and store in CogPos variable
    CogPos = cmds.xform( 'Cog_Piv', ws=True, q=True, t=True )
    
    # - Create 3 control circles:
    # Create world control
    WorldCtrl = cmds.circle( radius=ctrlRadius, normal=(0,1,0), name='World_Ctrl' )[0]
    # Color the ctrl
    denUt.den_ColorShape(11)
    # Parent ctrl under base rig grp
    WorldCtrl = cmds.parent( WorldCtrl, BaseRigGrp )
    # Take the selected ctrl, adds a zero null above it to zero its transform, auto compensates for hierachies and parenting
    WorldCtrl = denUt.den_AddZeroNull()
    # Lock scale attribute
    denUt.den_Lock(  0,0,0 , 0,0,0 , 1,1,1 , 0 )
    # Capture and reset *
    WorldCtrl = cmds.ls( WorldCtrl )
    # Add it to the list of BaseCtrlsAll, 'BaseCtrlsALL += WorldCtrl' means 'BaseCtrlsALL = WorldCtrl+BaseCtrlsALL'
    BaseCtrlsALL += WorldCtrl
    
    # Create world offset control
    WorldOffsetCtrl = cmds.circle( radius=ctrlRadius*0.9, normal=(0,1,0), name='WorldOffset_Ctrl' )[0]
    # Color the ctrl
    denUt.den_ColorShape(10)
    # Parent ctrl under base rig grp
    WorldOffsetCtrl = cmds.parent( WorldOffsetCtrl, WorldCtrl, relative=False )
    # Add 0 null
    WorldOffsetCtrl = denUt.den_AddZeroNull()
    # Lock scale attribute
    denUt.den_Lock(  0,0,0 , 0,0,0 , 1,1,1 , 0 )
    # Capture and reset *
    WorldOffsetCtrl = cmds.ls( WorldOffsetCtrl )
    # Add it to the list of BaseCtrlsAll
    BaseCtrlsALL += WorldOffsetCtrl
    
    # Create All control
    AllCtrl = denUt.den_MakeLabel( nodeName='All_Ctrl', pos=(0,0,0), radius=ctrlRadius*0.8, doT=False, label=label, doCircle=True )
    # Color the ctrl
    denUt.den_ColorShape(21)
    # Parent ctrl under base rig grp
    AllCtrl = cmds.parent( AllCtrl, WorldOffsetCtrl )
    # Add 0 null
    AllCtrl = denUt.den_AddZeroNull()
    # Capture and reset
    AllCtrl = cmds.ls( AllCtrl )  
    # Add it to the list of BaseCtrlsAll
    BaseCtrlsALL += AllCtrl
    
    # - Create cog control (ball)
    CogCtrl = denUt.den_MakeBall( nodeName='Cog_Ctrl', pos=(0,0,0), radius=ctrlRadius*0.5, doT=False )
    # Transform the cog ball ctrl
    cmds.xform( t=CogPos )
    # Color the ctrl
    denUt.den_ColorShape(21)
    # Parent cog ctrl under all ctrl grp
    CogCtrl = cmds.parent( CogCtrl, AllCtrl )
    # Add 0 null
    CogCtrl = denUt.den_AddZeroNull()
    # Capture and reset
    CogCtrl = cmds.ls( CogCtrl )
    # Add it to the list of BaseCtrlsAll
    BaseCtrlsALL += CogCtrl
    
    # - Add attributes to control visibility of rig parts 
    # Global Scale:
    # Add an attribute to control global scale
    cmds.addAttr( AllCtrl[0], longName='Global_Scale', attributeType='float', defaultValue=1.0 )
    # Make global scale attribute visible in channel box
    cmds.setAttr ( AllCtrl[0]+'.Global_Scale', lock=False, channelBox=True )
    # Connect global scale attribute to scaleXYZ
    cmds.connectAttr( AllCtrl[0]+'.Global_Scale', AllCtrl[0]+'.sx' )
    cmds.connectAttr( AllCtrl[0]+'.Global_Scale', AllCtrl[0]+'.sy' )
    cmds.connectAttr( AllCtrl[0]+'.Global_Scale', AllCtrl[0]+'.sz' )
    
    # Show or hide geo/ctrl/guts/drawStyle groups:
    # Add an attribute to control Render geo
    cmds.addAttr( AllCtrl[0], longName='Show_Render_Geo', attributeType='enum', enumName=' off ---: --- on' )
    # Make attribute visible in channel box
    cmds.setAttr ( AllCtrl[0]+'.Show_Render_Geo', lock=False, channelBox=True )
    # Add an attribute to control Proxy geo
    cmds.addAttr( AllCtrl[0], longName='Show_Proxy_Geo', attributeType='enum', enumName=' off ---: --- on' )
    cmds.setAttr ( AllCtrl[0]+'.Show_Proxy_Geo', 1, lock=False, channelBox=True )
    # Add an attribute to control Box geo
    cmds.addAttr( AllCtrl[0], longName='Show_Box_Geo', attributeType='enum', enumName=' off ---: --- on' )
    cmds.setAttr ( AllCtrl[0]+'.Show_Box_Geo', 1, lock=False, channelBox=True )
    # Add an attribute to control control group
    cmds.addAttr( AllCtrl[0], longName='Show_Controls', attributeType='enum', enumName=' off ---: --- on' )
    cmds.setAttr ( AllCtrl[0]+'.Show_Controls', 1, lock=False, channelBox=True )
    # Add an attribute to control guts
    cmds.addAttr( AllCtrl[0], longName='Show_Guts', attributeType='enum', enumName=' off ---: --- on' )
    cmds.setAttr ( AllCtrl[0]+'.Show_Guts', lock=False, channelBox=True )
    # Add an attribute to control draw style
    cmds.addAttr(  AllCtrl[0], longName='Bone_Draw_Style', attributeType='enum', enumName='Bone:Multi-child as Box:None' )
    cmds.setAttr (  AllCtrl[0]+'.Bone_Draw_Style', lock=False, channelBox=True )
    
    # Add 3 different custom color attributes to the AllCtrl (added in 'Extra Attributes')
    # Add overall attribute to control Center color
    cmds.addAttr(AllCtrl, ln="Center_Color", uac=True, at="float3")
    # Add attributes for R, G, B
    cmds.addAttr(AllCtrl, ln="Center_ColorR", at="float", parent="Center_Color")
    cmds.addAttr(AllCtrl, ln="Center_ColorG", at="float", parent="Center_Color")
    cmds.addAttr(AllCtrl, ln="Center_ColorB", at="float", parent="Center_Color")
    # Add overall attribute to control Left color
    cmds.addAttr(AllCtrl, ln="Left_Color", uac=True, at="float3")
    # Add attributes for R, G, B
    cmds.addAttr(AllCtrl, ln="Left_ColorR", at="float", parent="Left_Color")
    cmds.addAttr(AllCtrl, ln="Left_ColorG", at="float", parent="Left_Color")
    cmds.addAttr(AllCtrl, ln="Left_ColorB", at="float", parent="Left_Color")
    # Add overall attribute to control Right color
    cmds.addAttr(AllCtrl, ln="Right_Color", uac=True, at="float3")
    # Add attributes for R, G, B
    cmds.addAttr(AllCtrl, ln="Right_ColorR", at="float", parent="Right_Color")
    cmds.addAttr(AllCtrl, ln="Right_ColorG", at="float", parent="Right_Color")
    cmds.addAttr(AllCtrl, ln="Right_ColorB", at="float", parent="Right_Color")
    # Set colors Center:yellow, Left:blue, Right:red (use [0] to extract from the list)
    cmds.setAttr(AllCtrl[0] + ".Center_Color", 0.8, 0.8, 0.05, type="double3")
    cmds.setAttr(AllCtrl[0] + ".Left_Color", 0, 0.3, 0.95, type="double3")
    cmds.setAttr(AllCtrl[0] + ".Right_Color", 1, 0.03, 0.05, type="double3")
    
    # Connect control visibility to AllCtrl
    # for all string in the list, enumerate: each string goes into 's' variable, 'i' variable picks up the index of each string
    for i,s in enumerate(BaseCtrlsALL):
        # find all shapes and make it invisible, not objects
        shapes = cmds.listRelatives( s, shapes=True )
        print( shapes )
        for shape in shapes:
            # do all except no.2 (the AllCtrl, stays visible)
            if i != 2:
                cmds.connectAttr( AllCtrl[0]+'.Show_Controls', shape+'.visibility' )
    
    # Select AllCtrl
    cmds.select( AllCtrl[0] )
    # Lock the scale of AllCtrl
    denUt.den_Lock(  0,0,0 , 0,0,0 , 1,1,1 , 0 )
    
    # Add spaceOut
    # Create empty group for CogSpaceOUT
    CogSpaceOUT = denUt.den_makeGrp( nodeName='CogSpace_OUT', pos=(0,0,0) )
    # Parent under CogCtrl
    CogSpaceOUT = cmds.parent( CogSpaceOUT, CogCtrl )[0]
    # Create empty group for AllSpaceOUT
    AllSpaceOUT = denUt.den_makeGrp( nodeName='AllSpace_OUT', pos=(0,0,0) )
    # Parent under AllCtrl
    AllSpaceOUT = cmds.parent( AllSpaceOUT, AllCtrl )[0]
    # Add the created spaceOut to BaseSpaceOUTs list
    BaseSpaceOUTs += [CogSpaceOUT, AllSpaceOUT]
    
    # Return the top level root group node, SpaceINs, SpaceOUTs, BindJoints, CtrlsALL, GutsALL lists in order (same order for all body parts)
    return RootRigGrp, BaseSpaceINs, BaseSpaceOUTs, BaseBindJoints, BaseCtrlsALL, BaseGutsALL


# ---------------------------------------------------------------------------------------
# Create Torso Pivots

# Prefix: used for naming multuple sets of body parts, such as many pair of arms
def jly_makeBipedTorsoPivs( prefix='', radius=2.0, dpTime = 0.01 ):
    
    # Create a root torso pivot group to hold all torso pivots
    TorsoPivGrp = denUt.den_makeGrp( nodeName=prefix+'TorsoPiv_Grp', pos=(0,0,0) )
    # Lock all the attributes, except visibility
    denUt.den_Lock(  1,1,1 , 1,1,1 , 1,1,1 , 0 )
    
    # Create locator for Pelvis pivot
    PelvisPiv = denUt.den_makeLoc( nodeName=prefix+'Pelvis_Piv', pos=(0, 100, 0), radius=radius )
    # Color the locator, and add DiagPause for display rig building process
    denUt.den_ColorShape(20); denUt.den_DiagPause( seconds=dpTime )
    # Lock all the attributes, except translate
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Create locator for Spine01 pivot
    Spine01Piv = denUt.den_makeLoc( nodeName=prefix+'Spine01_Piv', pos=(0, 110, 0), radius=radius )
    denUt.den_ColorShape(20); denUt.den_DiagPause( seconds=dpTime )
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Create locator for Spine02 pivot
    Spine02Piv = denUt.den_makeLoc( nodeName=prefix+'Spine02_Piv', pos=(0, 120, 0), radius=radius )
    denUt.den_ColorShape(20); denUt.den_DiagPause( seconds=dpTime )
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Create locator for Chest pivot
    ChestPiv = denUt.den_makeLoc( nodeName=prefix+'Chest_Piv', pos=(0, 130, 0), radius=radius )
    denUt.den_ColorShape(20); denUt.den_DiagPause( seconds=dpTime )
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Create locator for Neck pivot
    Neck01Piv = denUt.den_makeLoc( nodeName=prefix+'Neck01_Piv', pos=(0, 140, 0), radius=radius )
    denUt.den_ColorShape(20); denUt.den_DiagPause( seconds=dpTime )
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Create locator for Head pivot
    HeadPiv = denUt.den_makeLoc( nodeName=prefix+'Head_Piv', pos=(0, 150, 0), radius=radius )
    denUt.den_ColorShape(20); denUt.den_DiagPause( seconds=dpTime )
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Create locator for HeadEnd pivot
    HeadEndPiv = denUt.den_makeLoc( nodeName=prefix+'HeadEnd_Piv', pos=(0, 160, 0), radius=radius/2 )
    denUt.den_ColorShape(20); denUt.den_DiagPause( seconds=dpTime )
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Create locator for Jaw pivot
    JawPiv = denUt.den_makeLoc( nodeName=prefix+'Jaw_Piv', pos=(0, 150, 5), radius=radius )
    denUt.den_ColorShape(20); denUt.den_DiagPause( seconds=dpTime )
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Create locator for JawEnd pivot
    JawEndPiv = denUt.den_makeLoc( nodeName=prefix+'JawEnd_Piv', pos=(0, 150, 10), radius=radius/2 )
    denUt.den_ColorShape(20); denUt.den_DiagPause( seconds=dpTime )
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Parent all created pivots under TorsoPivGrp
    cmds.parent( PelvisPiv,Spine01Piv,Spine02Piv,ChestPiv,Neck01Piv,HeadPiv,HeadEndPiv,JawPiv,JawEndPiv,TorsoPivGrp )
    # Put DP in the end of pivot creation to refresh orient
    denUt.den_DiagPause( seconds=dpTime )
    return TorsoPivGrp


# ---------------------------------------------------------------------------------------
# Create Torso Rig

# control radius: user can control ctrl size, list order - pelvis, chest, head, jaw
# displayLocalAxis: check joint orient if correct
def jly_makeBipedTorsoRig( prefix='', radius=3.0, ctrlRadius=(19.0,21.0,12.0,2.0), displayLocalAxis=False, dpTime = 0.01 ):
    
    # Make a big master Torso rig group,to hold other groups 
    TorsoRigGrp = denUt.den_makeGrp( nodeName=prefix+'Torso_Grp', pos=(0,0,0) )
    # Lock all the attributes, except visibility
    denUt.den_Lock(  1,1,1 , 1,1,1 , 1,1,1 , 0 )
    
    # Set 5 variables for every rig parts:
    TorsoSpaceINs = []
    TorsoSpaceOUTs = []
    TorsoBindJoints = []
    TorsoCtrlsALL = []
    TorsoGutsALL = []
    
    # Create SpaceIN for Tosor, to accept transforms from the Cog
    TorsoSpaceIN = denUt.den_makeGrp( nodeName=prefix+'Torso_SpaceIN', pos=(0,0,0) )
    # Parent it under the root rig group
    TorsoSpaceIN = cmds.parent( TorsoSpaceIN, TorsoRigGrp )
    # Add SpaceIN to the list variable
    TorsoSpaceINs += TorsoSpaceIN
    
    # Query all the pivots worldSpace position to build the rig, and store the result in a variable
    PelvisPos = cmds.xform( prefix+'Pelvis_Piv', ws=True, q=True, t=True )
    Spine01Pos = cmds.xform( prefix+'Spine01_Piv', ws=True, q=True, t=True )
    Spine02Pos = cmds.xform( prefix+'Spine02_Piv', ws=True, q=True, t=True )
    ChestPos = cmds.xform( prefix+'Chest_Piv', ws=True, q=True, t=True )
    Neck01Pos = cmds.xform( prefix+'Neck01_Piv', ws=True, q=True, t=True )
    HeadPos = cmds.xform( prefix+'Head_Piv', ws=True, q=True, t=True )
    HeadEndPos = cmds.xform( prefix+'HeadEnd_Piv', ws=True, q=True, t=True )
    JawPos = cmds.xform( prefix+'Jaw_Piv', ws=True, q=True, t=True )
    JawEndPos = cmds.xform( prefix+'JawEnd_Piv', ws=True, q=True, t=True )
    
    # - Draw a chain of joints, parent them under SpaceIN
    # Select SpaceIN
    cmds.select( TorsoSpaceIN )
    # Create joint at the specific position
    PelvisJoint = denUt.den_makeJoint( nodeName=prefix+'Pelvis_Jnt', pos=(PelvisPos), radius=radius, leaveSelected=True ); denUt.den_DiagPause( seconds=dpTime )
    Spine01Joint = denUt.den_makeJoint( nodeName=prefix+'Spine01_Jnt', pos=(Spine01Pos), radius=radius, leaveSelected=True ); denUt.den_DiagPause( seconds=dpTime )
    Spine02Joint = denUt.den_makeJoint( nodeName=prefix+'Spine02_Jnt', pos=(Spine02Pos), radius=radius, leaveSelected=True ); denUt.den_DiagPause( seconds=dpTime )
    ChestJoint = denUt.den_makeJoint( nodeName=prefix+'Chest_Jnt', pos=(ChestPos), radius=radius, leaveSelected=True ); denUt.den_DiagPause( seconds=dpTime )
    Neck01Joint = denUt.den_makeJoint( nodeName=prefix+'Neck01_Jnt', pos=(Neck01Pos), radius=radius, leaveSelected=True ); denUt.den_DiagPause( seconds=dpTime )
    HeadJoint = denUt.den_makeJoint( nodeName=prefix+'Head_Jnt', pos=(HeadPos), radius=radius, leaveSelected=True ); denUt.den_DiagPause( seconds=dpTime )
    HeadEndJoint = denUt.den_makeJoint( nodeName=prefix+'Head_end', pos=(HeadEndPos), radius=radius*0.4, leaveSelected=False ); denUt.den_DiagPause( seconds=dpTime )
    # Select HeadJoint, so when create JawJoint, the JawJoint will be parented under HeadJoint
    cmds.select(HeadJoint)
    JawJoint = denUt.den_makeJoint( nodeName=prefix+'Jaw_Jnt', pos=(JawPos), radius=radius, leaveSelected=True ); denUt.den_DiagPause( seconds=dpTime )
    JawEndJoint = denUt.den_makeJoint( nodeName=prefix+'Jaw_end', pos=(JawEndPos), radius=radius*0.4, leaveSelected=True ); denUt.den_DiagPause( seconds=dpTime )
    
    # Display local axis fot all joints, also can be made into a for loop *
    if ( displayLocalAxis ):
        cmds.setAttr( PelvisJoint+'.displayLocalAxis', 1 )
        cmds.setAttr( Spine01Joint+'.displayLocalAxis', 1 )
        cmds.setAttr( Spine02Joint+'.displayLocalAxis', 1 )
        cmds.setAttr( ChestJoint+'.displayLocalAxis', 1 )
        cmds.setAttr( Neck01Joint+'.displayLocalAxis', 1 )
        cmds.setAttr( HeadJoint+'.displayLocalAxis', 1 )
        cmds.setAttr( JawJoint+'.displayLocalAxis', 1 )
    
    
    # Orient all the joints to what we want
    # e: Edit mode, OJ:orient joint, zdown: orient Y stick toward the back
    cmds.joint( PelvisJoint, e=True, oj='xyz', secondaryAxisOrient='zdown', ch=True, zso=True )
    cmds.joint( JawJoint, e=True, oj='xyz', secondaryAxisOrient='zdown', ch=True, zso=True )
    
    # Add a single chain IK handles for body parts in between (joints Spine01, Spine02, Neck01)
    # The other parts (Pelvis, Cheat, Head) will be 100% driven directly by their own controls, so no need of IK
    # Select 2 objects
    cmds.select( Spine01Joint, Spine02Joint )
    # Create the IK handle between them
    Spine01Handle = denUt.den_AddIKHandle('ikSCsolver',False)
    cmds.select( Spine02Joint, ChestJoint )
    Spine02Handle = denUt.den_AddIKHandle('ikSCsolver',False)
    cmds.select( Neck01Joint, HeadJoint )
    Neck01Handle = denUt.den_AddIKHandle('ikSCsolver',False)
    
    # Create Pelvis control
    PelvisCtrl = denUt.den_MakeBall(nodeName=prefix+'Pelvis_Ctrl',pos=(0,0,0),radius=ctrlRadius[0],doT=False)
    # Move the control to line up with the pivot position
    cmds.xform( t=PelvisPos )
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    
    # Create Chest control
    ChestCtrl = denUt.den_MakeBall(nodeName=prefix+'Chest_Ctrl',pos=(0,0,0),radius=ctrlRadius[1],doT=False)
    # Move the control to line up with the pivot position
    cmds.xform( t=ChestPos )
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    
    # Create Head control
    HeadCtrl = denUt.den_MakeBall(nodeName=prefix+'Head_Ctrl',pos=(0,0,0),radius=ctrlRadius[2],doT=False)
    # Move the control to line up with the pivot position
    cmds.xform( t=HeadPos )
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    
    # Create Jaw control
    JawCtrl = denUt.den_MakeBall(nodeName=prefix+'Jaw_Ctrl',pos=(0,-6,10),radius=ctrlRadius[3],doT=True)
    # Move the control to line up with the pivot position
    cmds.xform( t=JawPos )
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    
    # Add the 4 controls to the TorsoALL control list *I cleaned up :)*
    TorsoCtrlsALL += [PelvisCtrl,ChestCtrl,HeadCtrl,JawCtrl]
    
    # ===============================================================================================
    # - Just In Case Control:
    # This for loop is here when character has more than one spine/neck joint
    # Make a list of all spine joints
    '''
    VertJoints = [Spine02Joint]
    print( VertJoints )
    # Make a list for all spine controls
    VertControls = []
    for jx in VertJoints:
        print( jx )
        # Name the control and replace _Jnt with _Ctrl
        CtrlName = jx.replace('_Jnt', '_Ctrl')
        print( CtrlName )
        # Create a spine control
        Ctrl = denUt.den_MakeBall(nodeName=CtrlName,pos=(0,2,0),radius=0.3,doT=True)
        # Color the control
        denUt.den_ColorShapeRGB(rgb=(1,0,1))
        # Parent under the joint
        Ctrl = cmds.parent( Ctrl, jx, relative=True )
        # Parent under Torso SpaceIN
        Ctrl = cmds.parent( Ctrl, TorsoSpaceIN )
        # Add 0 null
        Ctrl = denUt.den_AddZeroNull()
        # Lock scale attribute
        denUt.den_Lock(  0,0,0 , 0,0,0 , 1,1,1 , 0 )
        # Add the control to the list
        VertControls += Ctrl
        denUt.den_DiagPause( seconds=dpTime )
    
    # Add the controls to Torso controls list
    TorsoCtrlsALL += VertControls
    print( VertControls )
    print( TorsoCtrlsALL )
    
    Spine02Ctrl = VertControls[0]
    
    '''
    # ===============================================================================================
    
    # - Make the just-in-case control for spine. *I extract out of the loop :)*
    # Name the control and replace _Jnt with _Ctrl
    CtrlName = Spine02Joint.replace('_Jnt', '_Ctrl')
    # Create a spine control
    Ctrl = denUt.den_MakeBall(nodeName=CtrlName,pos=(0,2,0),radius=0.3,doT=True)
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Parent under the joint
    Ctrl = cmds.parent( Ctrl, Spine02Joint, relative=True )
    # Parent under Torso SpaceIN
    Ctrl = cmds.parent( Ctrl, TorsoSpaceIN )
    # Add 0 null
    Ctrl = denUt.den_AddZeroNull()
    # Lock scale attribute
    denUt.den_Lock(  0,0,0 , 0,0,0 , 1,1,1 , 0 )
    # DP
    denUt.den_DiagPause( seconds=dpTime )
    # Add the controls to Torso controls list
    TorsoCtrlsALL += Ctrl
    print( Ctrl )
    print( TorsoCtrlsALL )
    Spine02Ctrl = Ctrl
    
    # - Put locators (that is not a joint) for body parts which are spliting weight of 2 other parts- 
    # -such as(spine1: pelvis+chest, spine2:chest+neck), as something to constrain to
    # Make a locator for the pelvis
    PelvisLoc = cmds.spaceLocator (n=prefix+'Pelvis_Loc')
    # Parent under PelvisJoint
    PelvisLoc = cmds.parent( PelvisLoc, PelvisJoint, relative=True )
    # Re-parent under PelvisCtrl
    PelvisLoc = cmds.parent( PelvisLoc, PelvisCtrl )
    
    # Make a locator for the chest
    ChestLoc = cmds.spaceLocator (n=prefix+'Chest_Loc')
    # Parent under ChestJoint
    ChestLoc = cmds.parent( ChestLoc, ChestJoint, relative=True )
    # Re-parent under PelvisCtrl
    ChestLoc = cmds.parent( ChestLoc, ChestCtrl )
    
    # Make a locator for the head
    HeadLoc = cmds.spaceLocator (n=prefix+'Head_Loc')
    # Parent under HeadJoint
    HeadLoc = cmds.parent( HeadLoc, HeadJoint, relative=True )
    # Re-parent under HeadCtrl
    HeadLoc = cmds.parent( HeadLoc, HeadCtrl )
    
    # - Re-parent some handle created earlier
    # Make Spine01 IK goal point at Spine02, so it follows Spine02Ctrl
    Spine01Handle = cmds.parent( Spine01Handle, Spine02Ctrl )
    # Make Spine02 IK goal point at Chest, so it follows ChestCtrl
    Spine02Handle = cmds.parent( Spine02Handle, ChestCtrl )
    # Make Neck01 IK goal point at Head, so it follows HeadCtrl
    Neck01Handle = cmds.parent( Neck01Handle, HeadCtrl )
    
    # Parent controls hierarchy
    JawCtrl = cmds.parent( JawCtrl, HeadCtrl )
    HeadCtrl = cmds.parent( HeadCtrl, ChestCtrl )
    # Parent controls under SpaceIN
    ChestCtrl = cmds.parent( ChestCtrl, TorsoSpaceIN )
    PelvisCtrl = cmds.parent( PelvisCtrl, TorsoSpaceIN )
    
    # Add 0 null for the pelvis control
    cmds.select( PelvisCtrl )
    PelvisCtrl = denUt.den_AddZeroNull()
    # Lock scale attribute
    denUt.den_Lock(  0,0,0 , 0,0,0 , 1,1,1 , 0 )
    # Add 0 null for the chest control
    cmds.select( ChestCtrl )
    ChestCtrl = denUt.den_AddZeroNull()
    # Lock scale attribute
    denUt.den_Lock(  0,0,0 , 0,0,0 , 1,1,1 , 0 )
    # Add 0 null for the head control
    cmds.select( HeadCtrl )
    HeadCtrl = denUt.den_AddZeroNull()
    # Lock scale attribute
    denUt.den_Lock(  0,0,0 , 0,0,0 , 1,1,1 , 0 )
    # Find who the 0 null is for Head
    HeadCtrlZero = cmds.listRelatives( HeadCtrl, parent=True )
    # Add 0 null for the jaw control
    cmds.select( JawCtrl )
    JawCtrl = denUt.den_AddZeroNull()
    # Lock scale attribute
    denUt.den_Lock(  0,0,0 , 0,0,0 , 1,1,1 , 0 )
    # Find who the 0 null is for Jaw
    JawCtrlZero = cmds.listRelatives( JawCtrl, parent=True )
    
    # Make constraints
    # Parent pelvis joint to pelvis locator, so the joint follows pelvis contrl
    cmds.parentConstraint( PelvisLoc, PelvisJoint, mo=True )
    # Orient chest joint to chest locator, so it always stay with chest control
    cmds.orientConstraint( ChestLoc, ChestJoint, mo=True )
    # Orient head joint to head locator, so it always stay with head control
    cmds.orientConstraint( HeadLoc, HeadJoint, mo=True )
    # Parent jaw joint to jaw locator, so it follows jaw contrl
    cmds.parentConstraint( JawCtrl, JawJoint, mo=True )
    # Parent jaw ctrl0 to head joint, so the jaw control stay on the head joint
    cmds.parentConstraint( HeadJoint, JawCtrlZero, mo=True )
    # Parent head ctrl0 to chest joint, so the head control follows chest joint
    cmds.parentConstraint( ChestJoint, HeadCtrlZero, mo=True )
    
    # Split the influence of pelvis and chest controls in half, and make the small Vertebrae spine controls always inbetween pelvis and chest
    cmds.parentConstraint( PelvisCtrl, ChestCtrl, prefix+'Spine02_CtrlZero', mo=True )
    # Make 2 orient constraints on the joint, to split rotate/twist so all are even
    # sc1: spine constraint 1, split the rotate between pelvis and spine02Ctrl, target is Spine01Handle
    sc1 = cmds.orientConstraint( PelvisCtrl, prefix+'Spine02_Ctrl', Spine01Handle )
    # sc2: spine constraint 2, split the rotate between spine02Ctrl and chest, target is Spine02Handle
    sc2 = cmds.orientConstraint( prefix+'Spine02_Ctrl', ChestCtrl, Spine02Handle )
    # nc1: neck constraint 1, split the rotate between chest and head, target is Neck01Handle
    nc1 = cmds.orientConstraint( ChestLoc, HeadLoc, Neck01Handle, mo=True )
    
    # Change the condtrain's InterpType: use Shortest, to reduce the chance of flip
    for con in [ sc1, sc2, nc1 ]:
        print( con )
        cmds.setAttr( con[0]+'.interpType', 2 )
    
    
    # Capture torso joints in a list
    TorsoBindJoints += [ PelvisJoint, Spine01Joint, Spine02Joint, ChestJoint, Neck01Joint, HeadJoint, JawJoint ]
    
    # Create SpaceOUTs
    TorsoSpaceOUTs += denUt.den_AddSpaceOUTs(TorsoBindJoints)
    print( TorsoSpaceOUTs )
    
    # Return the top level root group node, SpaceINs, SpaceOUTs, BindJoints, CtrlsALL, GutsALL lists in order
    return TorsoRigGrp, TorsoSpaceINs, TorsoSpaceOUTs, TorsoBindJoints, TorsoCtrlsALL, TorsoGutsALL


# ---------------------------------------------------------------------------------------
# Create Arm Pivots

def jly_makeBipedArmPivs( side='L_', prefix='', name='Arm', radius=2.0, elbowDist=20.0, dpTime = 0.01 ):
    
    # - Create arm pivots to match the character
    # Create a root arm pivot group to hold all arm pivots
    ArmPivGrp = denUt.den_makeGrp( nodeName=side+prefix+name+'Piv_Grp', pos=(0,0,0) )
    # Lock all attributes except X-scale, X-scale will be used to do mirror later
    denUt.den_Lock(  1,1,1 , 1,1,1 , 0,1,1 , 0 )
    
    # Create clavicle pivot
    ClavPiv = denUt.den_makeLoc( nodeName=side+prefix+'Clav_Piv', pos=(5, 150, 0), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Color the pivot
    denUt.den_ColorShape(20)
    # Lock all attribute except translate
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Create shoulder pivot
    ShldPiv = denUt.den_makeLoc( nodeName=side+prefix+'Shld_Piv', pos=(20, 150, -5), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Color the pivot
    denUt.den_ColorShape(20)
    
    # Create elbow pivot
    ElbowPiv = denUt.den_makeLoc( nodeName=side+prefix+'Elbow_Piv', pos=(30, 120, -5), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Color the pivot
    denUt.den_ColorShape(20)
    # Lock all attribute except translate
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Create wrist pivot
    WristPiv = denUt.den_makeLoc( nodeName=side+prefix+'Wrist_Piv', pos=(40, 95, 5), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Color the pivot
    denUt.den_ColorShape(20)
    
    # - Make scapula triangle for scapula rig, use a 2 joint IK system to allow scapula to float over the ribcage
    # Create scapula 01 pivot
    Scap01Piv = denUt.den_makeLoc( nodeName=side+prefix+'Scap01_Piv', pos=(-5, 145, 5), radius=radius*0.7 ); denUt.den_DiagPause( seconds=dpTime )
    # Color the pivot
    denUt.den_ColorShape(20)
    
    # Create scapula 02 pivot, will be positioned at the central bulk of the scapula
    Scap02Piv = denUt.den_makeLoc( nodeName=side+prefix+'Scap02_Piv', pos=(5, 150, -10), radius=radius*0.7 ); denUt.den_DiagPause( seconds=dpTime )
    # Color the pivot
    denUt.den_ColorShape(20)
    # Lock all attribute except translate
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Create elbow mid locator
    ElbowMidLoc = denUt.den_makeLoc( nodeName=side+prefix+'ElbowMid_Loc', radius=radius/2 )
    # Color the pivot
    denUt.den_ColorShape(2)
    
    # Create elbow pole locator
    ElbowPoleLoc = denUt.den_makeLoc( nodeName=side+prefix+'ElbowPole_Loc', pos=(0, elbowDist, 0), radius=radius )
    # Color the pivot
    denUt.den_ColorShape(9)
    
    # Parent ElbowMid Locator under ElbowPole locator
    cmds.parent( ElbowPoleLoc,ElbowMidLoc, relative=True )
    # Lock all attributes of ElbowPole Locator, except translate-Y, so it cannot be moved away from the triangle plane
    denUt.den_Lock(  1,0,1 , 1,1,1 , 1,1,1 , 1 )
    
    # Make things not shift around when switching IK FK: solution is to put joint orient on a triangle
    # so here we build triangle with locators, allow use to move locator but won't break the triangle
    # 2 triangles: 1- scap01, scap02, shoulder; 2- shoulder, elbow, wrist
    
    # Make ElbowMid Locator stays in between Shoulder Pivot and Wrist Pivot
    cmds.pointConstraint( ShldPiv,WristPiv,ElbowMidLoc, maintainOffset=False )
    # Make ElbowMid Locator aim at the wrist pivot, and use ElbowPiv as its up object. so it stays on the triangle plane
    cmds.aimConstraint( WristPiv,ElbowMidLoc, maintainOffset=False, worldUpType='object', worldUpObject=ElbowPiv[0] )
    cmds.select(ElbowMidLoc)
    # Lock all attributes
    denUt.den_Lock(  1,1,1 , 1,1,1 , 1,1,1 , 1 )
    
    # Make Shoulder Pivot aim at elbow pivot, and use wrist as its up object, so the shoulder pivot stays on the triangle plane
    cmds.aimConstraint( ElbowPiv,ShldPiv, maintainOffset=False, worldUpType='object', worldUpObject=WristPiv[0] )
    cmds.select(ShldPiv)
    # Lock all attributes except translate
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Make Scap01 Pivot aim at scap02 pivot, and use shoulder as its up object, so the scap01 pivot stays on the triangle plane
    cmds.aimConstraint( Scap02Piv,Scap01Piv, maintainOffset=False, worldUpType='object', worldUpObject=ShldPiv[0] )
    cmds.select(Scap01Piv)
    # Lock all attributes except translate
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Make Wrist Pivot aim at the elbow pivot, and use L_ArmMid Locator as its up object, so the Wrist Pivot stays on the triangle plane, aimvector can flip it
    cmds.aimConstraint( ElbowPiv,WristPiv, maintainOffset=False, worldUpType='object', worldUpObject=ElbowMidLoc[0], aimVector=(-1,0,0) )
    cmds.select(WristPiv)
    # Lock all attributes except translate
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Parent all pivot under root group ArmPivGrp
    cmds.parent( ClavPiv,ShldPiv,ElbowPiv,WristPiv,Scap01Piv,Scap02Piv,ElbowMidLoc,ArmPivGrp )
    
    # Clear selection
    cmds.select(clear=True)
    # DP refresh
    denUt.den_DiagPause( seconds=dpTime )
    
    # If making right arm, mirror all pivots
    if side == 'R_':
        cmds.setAttr( ArmPivGrp+'.scaleX', -1 )
    
    return ArmPivGrp


# ---------------------------------------------------------------------------------------
# Create Arm Rig

# Twist type: none/twist/ribbon, choose different way to do limb twist
def jly_makeBipedArmRig( side='L_', prefix='', name='Arm', radius=2.0, ctrlRadius=10.0, displayLocalAxis=False, twistType='none', dpTime = 0.01 ):
    
    # Input twist type
    if( twistType == 'none' ) or ( twistType == 'twist' ) or ( twistType == 'ribbon' ):
        print( 'doing twistType \''+twistType+'\'' )
    else:
        print( 'ERROR - twistType must be  \'none\' or \'twist\' or \'ribbon\' - nothing else will work' )
    
    # If making right arm rig, set pivot group scaleX to 1, flip the pivot group to the left for good mirroring
    if side == 'R_':
        cmds.setAttr( side+prefix+name+'Piv_Grp.scaleX', 1 )
    
    # DP refresh viewport
    denUt.den_DiagPause( seconds=dpTime )
    
    
    # Create the top level root group for the arm rig
    ArmRigGrp = denUt.den_makeGrp( nodeName=side+prefix+name+'_Grp', pos=(0,0,0) )
    
    # Create 5 variables to store components of the arm rig (SpaceINs, SpaceOUTs, BindJoints, Controls, and Guts)
    ArmSpaceINs = []
    ArmSpaceOUTs = []
    ArmBindJoints = []
    ArmCtrlsALL = []
    ArmGutsALL = []
    
    # Create arm SpaceIN groups (to follow Head, Chest, Pelvis, Cog, All Space), and parent under ArmRigGrp
    HeadSpaceIN = denUt.den_makeGrp( nodeName=side+prefix+'Head_SpaceIN', pos=(0,0,0) )
    HeadSpaceIN = cmds.parent( HeadSpaceIN, ArmRigGrp )[0]
    ChestSpaceIN = denUt.den_makeGrp( nodeName=side+prefix+'Chest_SpaceIN', pos=(0,0,0) )
    ChestSpaceIN = cmds.parent( ChestSpaceIN, ArmRigGrp )[0]
    PelvisSpaceIN = denUt.den_makeGrp( nodeName=side+prefix+'Pelvis_SpaceIN', pos=(0,0,0) )
    PelvisSpaceIN = cmds.parent( PelvisSpaceIN, ArmRigGrp )[0]
    CogSpaceIN = denUt.den_makeGrp( nodeName=side+prefix+'Cog_SpaceIN', pos=(0,0,0) )
    CogSpaceIN = cmds.parent( CogSpaceIN, ArmRigGrp )[0]
    AllSpaceIN = denUt.den_makeGrp( nodeName=side+prefix+'All_SpaceIN', pos=(0,0,0) )
    AllSpaceIN = cmds.parent( AllSpaceIN, ArmRigGrp )[0]
    # Add all the SpaceINs to the list ArmSpaceINs
    ArmSpaceINs += [ HeadSpaceIN, ChestSpaceIN, PelvisSpaceIN, CogSpaceIN, AllSpaceIN ]
    
    # - Usually keep skeleton hierarchy separate from control hierarchy, enable more possible blending (FK/IK), blend different ctrl rigs, etc.
    # Create groups for arm skeleton
    ArmSkelGrp = denUt.den_makeGrp( nodeName=side+prefix+name+'Skel_Grp', pos=(0,0,0) )
    # Parent them under the ChestSpaceIN
    ArmSkelGrp = cmds.parent( ArmSkelGrp, ChestSpaceIN )
    # Create groups for arm controls
    ArmCtrlGrp = denUt.den_makeGrp( nodeName=side+prefix+name+'Ctrl_Grp', pos=(0,0,0) )
    # Parent them under the ChestSpaceIN
    ArmCtrlGrp = cmds.parent( ArmCtrlGrp, ChestSpaceIN )
    
    # Create Wrist control space to accept the blend spaces
    # Create a group to accept transform from all spaces
    WristCtrlSpace = denUt.den_makeGrp( nodeName=side+prefix+'WristCtrl_Space', pos=(0,0,0) )
    # Parent WristCtrlSpace under the ArmCtrlGrp
    WristCtrlSpace = cmds.parent( WristCtrlSpace, ArmCtrlGrp )
    # Parent constraint WristCtrlSpace to each spaceINs
    WristCtrlSpaceConstraint = cmds.parentConstraint( HeadSpaceIN, WristCtrlSpace, weight=0 )
    # Chest weight 1 as default
    WristCtrlSpaceConstraint = cmds.parentConstraint( ChestSpaceIN, WristCtrlSpace, weight=1 )
    WristCtrlSpaceConstraint = cmds.parentConstraint( PelvisSpaceIN, WristCtrlSpace, weight=0 )
    WristCtrlSpaceConstraint = cmds.parentConstraint( CogSpaceIN, WristCtrlSpace, weight=0 )
    WristCtrlSpaceConstraint = cmds.parentConstraint( AllSpaceIN, WristCtrlSpace, weight=0 )
        
    # Query all pivots for their worldspace positions
    ClavPos = cmds.xform( side+prefix+'Clav_Piv', ws=True, q=True, t=True )
    ShldPos = cmds.xform( side+prefix+'Shld_Piv', ws=True, q=True, t=True )
    ElbowPos = cmds.xform( side+prefix+'Elbow_Piv', ws=True, q=True, t=True )
    WristPos = cmds.xform( side+prefix+'Wrist_Piv', ws=True, q=True, t=True )
    ElbowPolePos = cmds.xform( side+prefix+'ElbowPole_Loc', ws=True, q=True, t=True )
    Scap01Pos = cmds.xform( side+prefix+'Scap01_Piv', ws=True, q=True, t=True )
    Scap02Pos = cmds.xform( side+prefix+'Scap02_Piv', ws=True, q=True, t=True )
    
    # Create all joints for the arm
    # Clear selection
    cmds.select( clear=True )
    # Create clavicle joint at the correct postion
    ClavJoint = cmds.joint( n=side+prefix+'Clav_Jnt', p=(ClavPos), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Parent under ArmSkelGrp
    ClavJoint = cmds.parent( ClavJoint, ArmSkelGrp )[0]
    # Create shoulder joint at the correct postion
    ShldJoint = cmds.joint( n=side+prefix+'Shld_Jnt', p=(ShldPos), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Create elbow joint at the correct postion
    ElbowJoint = cmds.joint( n=side+prefix+'Elbow_Jnt', p=(ElbowPos), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Create wrist joint at the correct postion
    WristJoint = cmds.joint( n=side+prefix+'Wrist_Jnt', p=(WristPos), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    
    # If displayLocalAxis=True, show all local axis for the joints
    if ( displayLocalAxis ):
        cmds.setAttr( ClavJoint+'.displayLocalAxis', displayLocalAxis )
        cmds.setAttr( ShldJoint+'.displayLocalAxis', displayLocalAxis )
        cmds.setAttr( ElbowJoint+'.displayLocalAxis', displayLocalAxis )
        cmds.setAttr( WristJoint+'.displayLocalAxis', displayLocalAxis )
    
    # Clear selection
    cmds.select( clear=True )
    # Create scapula joint 01 at the correct postion
    Scap01Joint = cmds.joint( n=side+prefix+'Scap01_Jx', p=(Scap01Pos), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Parent under ArmSkelGrp
    Scap01Joint = cmds.parent( Scap01Joint, ArmSkelGrp )[0]
    # Create scapula joint 02 at the correct postion
    Scap02Joint = cmds.joint( n=side+prefix+'Scap02_Jnt', p=(Scap02Pos), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Create scapula joint 03 at the correct postion (Scapula 2 End)
    Scap03Joint = cmds.joint( n=side+prefix+'Scap02_end', p=(ShldPos), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    
    # If displayLocalAxis=True, show all local axis for the joints
    if ( displayLocalAxis ):
        cmds.setAttr( Scap01Joint+'.displayLocalAxis', displayLocalAxis )
        cmds.setAttr( Scap02Joint+'.displayLocalAxis', displayLocalAxis )
        cmds.setAttr( Scap03Joint+'.displayLocalAxis', displayLocalAxis )
    
    # - Orient all the joints
    # Clear selection
    cmds.select( clear=True )
    # Edit to orient clavicle joint, orient xyz, y up
    cmds.joint( ClavJoint, e=True, oj='xyz', secondaryAxisOrient='yup', zso=True )
    
    # Clear selection
    cmds.select( clear=True )
    # Edit to orient elbow joint, orient xyz, y up (orient on the triangle plane)
    cmds.joint( ElbowJoint, e=True, oj='xyz', zso=True )
    # Edit to orient wrist joint, orient to the same as the parent joint
    cmds.joint( WristJoint, e=True, oj='none', zso=True )
    
    # - To orient shoulder joint, need to force it to orient on the arm triangle
    # Parent shoulder joint under shoulder pivot temporarily
    ShldJoint = cmds.parent( ShldJoint, side+prefix+'Shld_Piv' )
    # Orient the joint to the shoulder pivot
    cmds.joint( ShldJoint, e=True, oj='none', zso=True )
    # Put the shoulder joint back under the clavicle joint
    ShldJoint = cmds.parent( ShldJoint, ClavJoint )[0]
    
    # Clear selection
    cmds.select( clear=True )
    # Edit to orient scapula 02 joint, orient xyz, y up
    cmds.joint( Scap02Joint, e=True, oj='xyz', zso=True )
    # Edit to orient scapula 03 joint, orient to parent
    cmds.joint( Scap03Joint, e=True, oj='none', zso=True )
    
    # - To orient scapular 01, need to force it to orient on the scapula triangle
    # Temporarily parent scapular 01 joint under scapula 01 pivot
    Scap01Joint = cmds.parent( Scap01Joint, side+prefix+'Scap01_Piv' )
    # Orient the joint to the scapula 01 pivot
    cmds.joint( Scap01Joint, e=True, oj='none', zso=True )
    # Put the shoulder joint back under the ArmSkelGrp
    Scap01Joint = cmds.parent( Scap01Joint, ArmSkelGrp )[0]
    
    # --- Create IK and FK joint chains for the arm ---
    # Duplicate arm joints for to make IK joint chain
    ShldJointIK = cmds.duplicate (ShldJoint, name=side+prefix+'Shld_IK' )[0]
    # Rename joints to _IK
    ElbowJointIK = cmds.rename (ShldJointIK+'|'+side+prefix+'Elbow_Jnt', side+prefix+'Elbow_IK' )
    WristJointIK = cmds.rename (ElbowJointIK+'|'+side+prefix+'Wrist_Jnt', side+prefix+'Wrist_IK' )
    # Duplicate arm joints for to make FK joint chain
    ShldJointFK = cmds.duplicate (ShldJoint, name=side+prefix+'Shld_FK' )[0]
    # Rename joints to _FK
    ElbowJointFK = cmds.rename (ShldJointFK+'|'+side+prefix+'Elbow_Jnt', side+prefix+'Elbow_FK' )
    WristJointFK = cmds.rename (ElbowJointFK+'|'+side+prefix+'Wrist_Jnt', side+prefix+'Wrist_FK' )
    
    # --- Create the controls and 0 nulls ---
    # Create shoulder IK control (cube)
    ShldCtrl = denUt.den_MakeCube( nodeName=side+prefix+'Shld_Ctrl', pos=(0,0,0) ,radius=0.8*ctrlRadius, doT=False)
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Transform the control to the shoulder position
    cmds.xform( t=ShldPos )
    # Parent it under ArmCtrlGrp
    ShldCtrl = cmds.parent( ShldCtrl, ArmCtrlGrp )
    # Add 0 null
    ShldCtrl = denUt.den_AddZeroNull()
    # Store the 0 null in a variable
    ShldCtrlZero = cmds.listRelatives( ShldCtrl, parent=True, fullPath=True )
    # Add the control to the control list
    ArmCtrlsALL += ShldCtrl
    
    # Create shoulder FK control (spike), axis: -Z
    ShldFKCtrl = denUt.den_MakeSpike( nodeName=side+prefix+'ShldFK_Ctrl', pos=(0,0,0) ,radius=ctrlRadius, doT=False, axis='-Z' )
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Unlock control attributes before re-parent
    denUt.den_UnLockAttr(True,True,True,True)
    # Parent shoulder FK control under shoulder FK joint
    ShldFKCtrl = cmds.parent( ShldFKCtrl, ShldJointFK, relative=True )
    # Parent shoulder FK control under ArmCtrlGrp
    ShldFKCtrl = cmds.parent( ShldFKCtrl, ArmCtrlGrp )
    # Add 0 null and store it in a variable
    ShldFKCtrl = denUt.den_AddZeroNull()
    # Lock all attribute except rotate and visibility
    denUt.den_LockAttr(True,False,True,False)
    # Capture and store the 0 null in a variable
    ShldFKCtrlZero = cmds.listRelatives( ShldFKCtrl, parent=True, fullPath=True )
    # Connect rotate attribute of the joint to the control, so it gets exact rotate number
    cmds.connectAttr( ShldFKCtrl[0]+'.rotate', ShldJointFK+'.rotate' )
    # Parent constraint 0 null to the clavicle, so if clavicle move the control moves too, to be visually clear
    cmds.parentConstraint( ClavJoint, ShldFKCtrlZero, mo=True )
    # Add shoulder FK control to arm control group
    ArmCtrlsALL += ShldFKCtrl
    
    # Create Arm Utility Control (gear) (turn maya UI Move ctrl Tool Setting symmerty off when doing this)
    ArmUtilCtrl = denUt.den_MakeGear( nodeName=side+prefix+name+'Util_Ctrl', pos=(4,12,0), radius=ctrlRadius*0.2, doT=False, Plane='XY' )
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Unlock control attributes before re-parent
    denUt.den_UnLockAttr(True,True,True,True)
    # Parent utility gear control under shoulder control
    ArmUtilCtrl = cmds.parent( ArmUtilCtrl, ShldCtrl, relative=True )
    # Lock all attribute except visibility
    denUt.den_LockAttr(True,True,True,False)
    # Add attributes to the arm
    cmds.addAttr( ArmUtilCtrl, longName=side+prefix+name+'_FK_IK', defaultValue=1.0, minValue=0.0, maxValue=1.0 )
    cmds.setAttr( ArmUtilCtrl[0]+'.'+side+prefix+name+'_FK_IK', lock=False, keyable=True )
    # Add attributes to the wrist
    cmds.addAttr( ArmUtilCtrl, longName=side+prefix+'Wrist_FK_IK', defaultValue=0.0, minValue=0.0, maxValue=1.0 )
    cmds.setAttr( ArmUtilCtrl[0]+'.'+side+prefix+'Wrist_FK_IK', lock=False, keyable=True )
    # Add arm utility control to arm control group
    ArmCtrlsALL += ArmUtilCtrl
    
    # Create Elbow IK Control (pole)
    ElbowCtrl = denUt.den_MakePole( nodeName=side+prefix+'Elbow_Ctrl', pos=(0,0,0) , radius=ctrlRadius*0.4, doT=False )
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Transform to the correct position
    cmds.xform( t=ElbowPolePos )
    # Parent under ArmCtrlGrp
    ElbowCtrl = cmds.parent( ElbowCtrl, ArmCtrlGrp )
    # Add 0 null
    ElbowCtrl = denUt.den_AddZeroNull()
    # Add elbow IK control to arm control group
    ArmCtrlsALL += ElbowCtrl
    
    # Create elbow FK Control (arrow)
    ElbowFKCtrl = denUt.den_MakeArrowR( nodeName=side+prefix+'ElbowFK_Ctrl', pos=(0,-4,0), radius=ctrlRadius*0.4, doT=True, axis='-Y', flip=False )
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Unlock control attributes before re-parent
    denUt.den_UnLockAttr(True,True,True,True)
    # Parent under ElbowJointFK
    ElbowFKCtrl = cmds.parent( ElbowFKCtrl, ElbowJointFK, relative=True )
    # Parent under shoulder FK control
    ElbowFKCtrl = cmds.parent( ElbowFKCtrl, ShldFKCtrl )
    # Add 0 null
    ElbowFKCtrl = denUt.den_AddZeroNull()
    # Lock all attribute except rotate and visibility
    denUt.den_LockAttr(True,False,True,False)
    # Connect rotate attribute to ElbowJointFK
    cmds.connectAttr( ElbowFKCtrl[0]+'.rotate', ElbowJointFK+'.rotate' )
    # Add elbow FK control to arm control group
    ArmCtrlsALL += ElbowFKCtrl
    
    # Create wrist IK Control (ball)
    WristCtrl = denUt.den_MakeBall( nodeName=side+prefix+'Wrist_Ctrl', pos=(0,0,0), radius=ctrlRadius*0.7, doT=False )
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Transform to the correct position
    cmds.xform( t=WristPos )
    # Parent under Wrist Control Space
    WristCtrl = cmds.parent( WristCtrl, WristCtrlSpace )
    # Add 0 null
    WristCtrl = denUt.den_AddZeroNull()
    # Capture and store the 0 null in a variable
    WristCtrlZero = cmds.listRelatives( WristCtrl, parent=True, fullPath=True )
    # Add Wrist IK Control to arm control group
    ArmCtrlsALL += WristCtrl
    
    # Create wrist FK Control (spike)
    WristFKCtrl = denUt.den_MakeSpike( nodeName=side+prefix+'WristFK_Ctrl', pos=(0,0,0), radius=ctrlRadius, doT=False, axis='-Z' )
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Unlock control attributes before re-parent
    denUt.den_UnLockAttr(True,True,True,True)
    # Parent under WristJointFK
    WristFKCtrl = cmds.parent( WristFKCtrl, WristJointFK, relative=True )
    # Parent under Elbow FK Control
    WristFKCtrl = cmds.parent( WristFKCtrl, ElbowFKCtrl )
    # Add 0 null
    WristFKCtrl = denUt.den_AddZeroNull()
    # Lock all attribute except rotate and visibility
    denUt.den_LockAttr(True,False,True,False)
    # Change rotate order to make sense for wrist
    cmds.setAttr( WristFKCtrl[0]+'.rotateOrder', 1 )
    # Capture and store the 0 null in a variable
    WristFKCtrlZero = cmds.listRelatives( WristFKCtrl, parent=True, fullPath=True )
    # Add Wrist FK Control to arm control group
    ArmCtrlsALL += WristFKCtrl
    
    # --- Create IK/FK blending for wrist ---
    # Duplicate 0 nulls for wrist FK control, Duplicate A: world space, Duplicate B: end of arm space
    # Duplicate 0 nulls as group A for world space
    WristCtrlZeroDupA = cmds.duplicate( WristFKCtrlZero, name=side+prefix+'WristFK_CtrlZeroA', parentOnly=True )[0]
    # Parent under ElbowJoint
    WristCtrlZeroDupA = cmds.parent( WristCtrlZeroDupA, ElbowJoint )
    # Duplicate 0 nulls as group B for IK space
    WristCtrlZeroDupB = cmds.duplicate( WristFKCtrlZero, name=side+prefix+'WristFK_CtrlZeroB', parentOnly=True )[0]
    # Parent under WristCtrl
    WristCtrlZeroDupB = cmds.parent( WristCtrlZeroDupB, WristCtrl )
    # Set rotation for better orient, so it's flat to the world like T pose style
    cmds.setAttr( WristCtrlZeroDupB[0]+'.rotate', 90,0,-90 )
    # Aim Duplicate A towards WristFKCtrlZero so it stays in same space
    cmds.pointConstraint( WristCtrlZeroDupA, WristFKCtrlZero )
    # Orient constraint Duplicate A and B to WristFKCtrlZero, Default A turned on (FK hand)
    WristFKCtrlZeroOriCon = cmds.orientConstraint( WristCtrlZeroDupA, WristFKCtrlZero, weight=1 )
    WristFKCtrlZeroOriCon = cmds.orientConstraint( WristCtrlZeroDupB, WristFKCtrlZero, weight=0 )
    # Set constraint interpType: Shortest
    cmds.setAttr( WristFKCtrlZeroOriCon[0]+'.interpType', 2 )
    # Because wrist control rotateOrder is 1, so set WristJoint rotateOrder also be 1
    cmds.setAttr( WristJoint+'.rotateOrder', 1 )
    # Orient constraint WristJoint to WristFKCtrl
    cmds.orientConstraint( WristFKCtrl, WristJoint )
    
    # --- Create and connect attributes for IK Wrist control space switcher ---
    # Add attributes to arm utility control for HeadSpace
    cmds.addAttr( ArmUtilCtrl, longName=side+prefix+'HeadSpace', defaultValue=0.0, minValue=0.0, maxValue=1.0 )
    # Set attribute lock and keyable value so it shows up in channel box
    cmds.setAttr( ArmUtilCtrl[0]+'.'+side+prefix+'HeadSpace', lock=False, keyable=True )
    # Connect attribute to the actual space switching constraint
    cmds.connectAttr( ArmUtilCtrl[0]+'.'+side+prefix+'HeadSpace', WristCtrlSpaceConstraint[0]+'.'+side+prefix+'Head_SpaceINW0' )
    # Add attributes to arm utility control for ChestSpace
    cmds.addAttr( ArmUtilCtrl, longName=side+prefix+'ChestSpace', defaultValue=1.0, minValue=0.0, maxValue=1.0 )
    cmds.setAttr( ArmUtilCtrl[0]+'.'+side+prefix+'ChestSpace', lock=False, keyable=True )
    cmds.connectAttr( ArmUtilCtrl[0]+'.'+side+prefix+'ChestSpace', WristCtrlSpaceConstraint[0]+'.'+side+prefix+'Chest_SpaceINW1' )
    # Add attributes to arm utility control for PelvisSpace
    cmds.addAttr( ArmUtilCtrl, longName=side+prefix+'PelvisSpace', defaultValue=0.0, minValue=0.0, maxValue=1.0 )
    cmds.setAttr( ArmUtilCtrl[0]+'.'+side+prefix+'PelvisSpace', lock=False, keyable=True )
    cmds.connectAttr( ArmUtilCtrl[0]+'.'+side+prefix+'PelvisSpace', WristCtrlSpaceConstraint[0]+'.'+side+prefix+'Pelvis_SpaceINW2' )
    # Add attributes to arm utility control for CogSpace
    cmds.addAttr( ArmUtilCtrl, longName=side+prefix+'CogSpace', defaultValue=0.0, minValue=0.0, maxValue=1.0 )
    cmds.setAttr( ArmUtilCtrl[0]+'.'+side+prefix+'CogSpace', lock=False, keyable=True )
    cmds.connectAttr( ArmUtilCtrl[0]+'.'+side+prefix+'CogSpace', WristCtrlSpaceConstraint[0]+'.'+side+prefix+'Cog_SpaceINW3' )
    # Add attributes to arm utility control for AllSpace
    cmds.addAttr( ArmUtilCtrl, longName=side+prefix+'AllSpace', defaultValue=0.0, minValue=0.0, maxValue=1.0 )
    cmds.setAttr( ArmUtilCtrl[0]+'.'+side+prefix+'AllSpace', lock=False, keyable=True )
    cmds.connectAttr( ArmUtilCtrl[0]+'.'+side+prefix+'AllSpace', WristCtrlSpaceConstraint[0]+'.'+side+prefix+'All_SpaceINW4' )
    
    # --- Create Arm FK_IK blending ---
    # Use pair blend to blend 2 value
    # Create pairBlend shading node for shoulder
    Shld_pairBlend = cmds.shadingNode ('pairBlend', asUtility=True, n=side+prefix+'Shld_ikFk_pairBlend' )
    # Set rotInterpolation to quaternion, so it wont gimbal flip
    cmds.setAttr( Shld_pairBlend+'.rotInterpolation', 1 )
    # Connect shoulder FK rotate to input 1
    cmds.connectAttr( ShldJointFK+'.rotate', Shld_pairBlend+'.inRotate1' )
    # Connect shoulder IK rotate to input 2
    cmds.connectAttr( ShldJointIK+'.rotate', Shld_pairBlend+'.inRotate2' )
    # Connect arm FK.IK to shoulder 'weight'
    cmds.connectAttr( ArmUtilCtrl[0]+'.'+side+prefix+name+'_FK_IK', Shld_pairBlend+'.weight' )
    # Connect Output Rotate to shoulder joint 'rotate'
    cmds.connectAttr( Shld_pairBlend+'.outRotate', ShldJoint+'.rotate' )
    
    # Create pairBlend shading node for elbow
    Elbow_pairBlend = cmds.shadingNode ('pairBlend', asUtility=True, n=side+prefix+'Elbow_ikFk_pairBlend' )
    # Set rotInterpolation to quaternion, so it wont gimbal flip
    cmds.setAttr( Elbow_pairBlend+'.rotInterpolation', 1 )
    # Connect elbow FK rotate to input 1
    cmds.connectAttr( ElbowJointFK+'.rotate', Elbow_pairBlend+'.inRotate1' )
    # Connect elbow IK rotate to input 2
    cmds.connectAttr( ElbowJointIK+'.rotate', Elbow_pairBlend+'.inRotate2' )
    # Connect arm FK.IK to elbow 'weight'
    cmds.connectAttr( ArmUtilCtrl[0]+'.'+side+prefix+name+'_FK_IK', Elbow_pairBlend+'.weight' )
    # Connect Output Rotate to elbow joint 'rotate'
    cmds.connectAttr( Elbow_pairBlend+'.outRotate', ElbowJoint+'.rotate' )
    
    # --- Create Wrist FK_IK blending --- (*with my explanations :)*)
    # Find the 0 null for the wrist FK control
    WristFKCtrlZeroOC = cmds.listRelatives( WristFKCtrlZero, type='orientConstraint', fullPath=True)
    # Create a multiplyDivide utility node for blending FK/IK, this node will caculate input values
    Wrist_multiplyDivide = cmds.shadingNode ('multiplyDivide', asUtility=True, n=side+prefix+'Wrist_ikFk_multiplyDivide' )
    # Create a reverse utility node, which inverts the input values, used for blending IK/FK. Here it's used to reverse the result from the multiplyDivide node for proper IK/FK blending
    Wrist_reverse = cmds.shadingNode ('reverse', asUtility=True, n=side+prefix+'Wrist_ikFk_reverse' )
    # Connect the FK/IK blend attribute (stored in the ArmUtilCtrl) to the 1st input of the multiplyDivide node's X input for the global FK/IK switch
    cmds.connectAttr( ArmUtilCtrl[0]+'.'+side+prefix+name+'_FK_IK', Wrist_multiplyDivide+'.input1X' )
    # Connect the wrist-specific FK/IK blend attribute (Wrist_FK_IK) to the second input of the multiplyDivide node's X input, so the wrist to have its own FK/IK blend control between FK and IK.
    cmds.connectAttr( ArmUtilCtrl[0]+'.'+side+prefix+'Wrist_FK_IK', Wrist_multiplyDivide+'.input2X' )
    # Connect the output of the multiplyDivide node to the input of the reverse node, so reverse node can invert the result for blending
    cmds.connectAttr( Wrist_multiplyDivide+'.outputX', Wrist_reverse+'.inputX' )
    # Connect the output of the multiplyDivide node to the weight of the second orient constraint target (WristFK_CtrlZeroBW1) to controls FK/IK blending for the wrist
    cmds.connectAttr( Wrist_multiplyDivide+'.outputX', WristFKCtrlZeroOC[0]+'.'+side+prefix+'WristFK_CtrlZeroBW1' )
    # Connect the output of the reverse node to the weight of the first orient constraint target (WristFK_CtrlZeroAW0)
    # The reverse node ensures that as one control increases influence, the other decreases, creating smooth blending
    cmds.connectAttr( Wrist_reverse+'.outputX', WristFKCtrlZeroOC[0]+'.'+side+prefix+'WristFK_CtrlZeroAW0' )
    
    # --- Create IK Handles ---
    # Create a IK handel for arm, start with ShldJointIK, end with WristJointIK, and rename with 'Ikh'
    ArmIKhandle = cmds.ikHandle( startJoint=ShldJointIK, endEffector=WristJointIK, solver='ikRPsolver', setupForRPsolver=True, name=ShldJointIK.replace('IK','Ikh') )
    # Rename the effector with 'Eff'
    cmds.rename( ArmIKhandle[1], ArmIKhandle[0].replace('Ikh','Eff') )
    # Parent the effector under WristCtrl
    ArmIKhandle = cmds.parent( ArmIKhandle[0], WristCtrl )
    # Add poleVectorConstraint so the ElbowCtrl drive the ArmIKhandle
    cmds.poleVectorConstraint( ElbowCtrl, ArmIKhandle )
    
    # Create a IK handel for clavicle, start with ClavJoint, end with ShldJoint, and rename with 'Ikh'
    ClavIKhandle = cmds.ikHandle( startJoint=ClavJoint, endEffector=ShldJoint, solver='ikSCsolver', name=ClavJoint.replace('Jnt','Ikh') )
    # Rename the effector with 'Eff'
    cmds.rename( ClavIKhandle[1], ClavIKhandle[0].replace('Ikh','Eff') )
    # Parent the effector under Shoulder Control
    ClavIKhandle = cmds.parent( ClavIKhandle[0], ShldCtrl )
    
    # Create a IK handel for scapula, start with Scap01Joint, end with Scap03Joint, and rename with 'Ikh'
    ScapIKhandle = cmds.ikHandle( startJoint=Scap01Joint, endEffector=Scap03Joint, solver='ikSCsolver', name=Scap01Joint.replace('Jx','Ikh') )
    # Rename the effector with 'Eff'
    cmds.rename( ScapIKhandle[1], ScapIKhandle[0].replace('Ikh','Eff') )
    # Parent the effector under Clavicle Control
    ScapIKhandle = cmds.parent( ScapIKhandle[0], ClavJoint )
    
    # --- Create wrist SpaceOUT to attach hands ---
    # Create wrist SpaceOUT group
    WristSpaceOUT = denUt.den_makeGrp( nodeName=side+prefix+'Wrist_SpaceOUT', pos=(0,0,0) )
    # Parent under WristJoint
    WristSpaceOUT = cmds.parent( WristSpaceOUT, WristJoint )
    # Add it to the list of SpaceOUTs
    ArmSpaceOUTs += WristSpaceOUT
    
    # Creat a list of all the joints for binding skin
    ArmBindJoints = [ ClavJoint, ShldJoint, ElbowJoint, WristJoint, Scap02Joint ]
    
    # --- Create twist options ---
    if twistType == 'none':
        print( 'no twist joints added' )
        ArmBindJoints = [ ClavJoint, ShldJoint, ElbowJoint, WristJoint, Scap02Joint ]
        
    if twistType == 'twist':
        ArmTwistRigRet = den_makeTwists( side=side, prefix=prefix, name=name, radius=radius, Joints=['Shld','Elbow','Wrist'], ctrlPos=(-10,0,-10), ctrlUpVec=(0,0,-1), displayLocalAxis=False )
        print( ArmTwistRigRet )
        ArmTwistBindJoints = ArmTwistRigRet[3]; print( ArmTwistBindJoints )
        ArmTwistCtrlsALL = ArmTwistRigRet[4]; print( ArmTwistCtrlsALL )
        ArmBindJoints = [ ClavJoint, WristJoint, Scap02Joint ] + ArmTwistBindJoints
        ArmCtrlsALL += ArmTwistCtrlsALL        
    
    if twistType == 'ribbon':
        ArmRibbonRigRet = den_makeRibbons( side=side, prefix=prefix, name=name, radius=radius, Joints=['Shld','Elbow','Wrist'], ctrlPos=(-10,0,-10), ctrlUpVec=(0,0,-1), displayLocalAxis=False )
        print( ArmRibbonRigRet )
        ArmRibbonBindJoints = ArmRibbonRigRet[3]; print( ArmRibbonBindJoints )
        ArmRibbonCtrlsALL = ArmRibbonRigRet[4]; print( ArmRibbonCtrlsALL )
        ArmBindJoints = [ ClavJoint, WristJoint, Scap02Joint ] + ArmRibbonBindJoints
        ArmCtrlsALL += ArmRibbonCtrlsALL
        
    
    # Flip the right side arm back where it belongs
    if side == 'R_':
        # Mirror the arm rig top node
        cmds.setAttr( ArmRigGrp+'.scaleX', -1 )
        # Restore the mirroring on the pivot group
        cmds.setAttr( side+prefix+name+'Piv_Grp.scaleX', -1 )
    
    # Return the top level root group node, SpaceINs, SpaceOUTs, BindJoints, CtrlsALL, GutsALL lists in order
    return ArmRigGrp, ArmSpaceINs, ArmSpaceOUTs, ArmBindJoints, ArmCtrlsALL, ArmGutsALL


# ---------------------------------------------------------------------------------------
# Create Leg Pivots

def jly_makeBipedLegPivs( side='L_', prefix='', name='Leg', radius=2.0, kneeDist=20.0, footUpDist=10.0, dpTime = 0.01 ):
    
    # Create a leg pivot group to hold all the pivots
    LegPivGrp = denUt.den_makeGrp( nodeName=side+prefix+name+'Piv_Grp' )
    # Lock all the attributes, except visibility and scale-X
    denUt.den_Lock(  1,1,1 , 1,1,1 , 0,1,1 , 0 )
    
    # Create locator for hip pivot
    denUt.den_makeLoc( nodeName='Hip_Piv', pos=(8.2, 98.9, 1.3), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Color the locator
    denUt.den_ColorShape(20)
    
    # Create locator for knee pivot 
    denUt.den_makeLoc( nodeName='Knee_Piv', pos=(10.6, 53.5, -0.7), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Color the locator
    denUt.den_ColorShape(20)
    # Lock all the attributes, except translate
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Create locator for ankle pivot 
    denUt.den_makeLoc( nodeName='Ankle_Piv', pos=(12.1, 12.8, -7), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Color the locator
    denUt.den_ColorShape(20)
    
    # Create locator for ball pivot
    denUt.den_makeLoc( nodeName='Ball_Piv', pos=(12.1, 3.5, 4.7), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Color the locator
    denUt.den_ColorShape(20)
    # Lock all the attributes, except translate
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Create an empty group for ball sole pivot
    denUt.den_makeGrp ( 'BallSole_Piv', pos=(12.1, 1, 4.7) ); denUt.den_DiagPause( seconds=dpTime )
    
    # Create locator for toe pivot
    denUt.den_makeLoc( nodeName='Toe_Piv', pos=(12.1, 1, 15.3), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Color the locator
    denUt.den_ColorShape(20)
    
    # Create locator for heel pivot
    denUt.den_makeLoc( nodeName='Heel_Piv', pos=(12.1, 1, -12), radius=radius/2 ); denUt.den_DiagPause( seconds=dpTime )
    # Color the locator
    denUt.den_ColorShape(20)
    
    # Create a group of pivots to make a roughly foot shape, for building a reverse foot rig later
    # Create locator for soleLF pivot
    denUt.den_makeLoc( nodeName='SoleLF_Piv', pos=(18.4, 1, 4.1), radius=radius/2 ); denUt.den_DiagPause( seconds=dpTime )
    # Color the locator
    denUt.den_ColorShape(20)
    # Create locator for soleLB pivot
    denUt.den_makeLoc( nodeName='SoleLB_Piv', pos=(16.1, 1, -9.4), radius=radius/2 ); denUt.den_DiagPause( seconds=dpTime )
    # Color the locator
    denUt.den_ColorShape(20)
    # Create locator for soleRF pivot
    denUt.den_makeLoc( nodeName='SoleRF_Piv', pos=(7.8, 1, 7.8), radius=radius/2 ); denUt.den_DiagPause( seconds=dpTime )
    # Color the locator
    denUt.den_ColorShape(20)
    # Create locator for soleRB pivot
    denUt.den_makeLoc( nodeName='SoleRB_Piv', pos=(8.6, 1, -9), radius=radius/2 ); denUt.den_DiagPause( seconds=dpTime )
    # Color the locator
    denUt.den_ColorShape(20)
    
    # Connect BallSole_piv's X,Z translate attributes to Ball pivot, connect translate Y to Toe Pivot, to maintain a flat foot plane
    cmds.connectAttr( 'Ball_Piv.translateX', 'BallSole_Piv.translateX' )
    cmds.connectAttr( 'Ball_Piv.translateZ', 'BallSole_Piv.translateZ' )
    cmds.connectAttr( 'Toe_Piv.translateY', 'BallSole_Piv.translateY' )
    # Select and Lock all attributes for BallSole_Piv
    cmds.select( 'BallSole_Piv' )
    denUt.den_Lock(  1,1,1 , 1,1,1 , 1,1,1 , 1 )
    
    # Connect Heel_Piv and Soles_Piv 's translateY to Toe_Piv's translateY, to maintain a flat foot plane
    cmds.connectAttr( 'Toe_Piv.translateY', 'Heel_Piv.translateY' )
    cmds.connectAttr( 'Toe_Piv.translateY', 'SoleLF_Piv.translateY' )
    cmds.connectAttr( 'Toe_Piv.translateY', 'SoleRF_Piv.translateY' )
    cmds.connectAttr( 'Toe_Piv.translateY', 'SoleLB_Piv.translateY' )
    cmds.connectAttr( 'Toe_Piv.translateY', 'SoleRB_Piv.translateY' )
    
    # Create locator for KneeMid pivot
    denUt.den_makeLoc( nodeName='KneeMid_Loc', radius=radius/2)
    # Color the locator
    denUt.den_ColorShape(2)
    
    # Create locator for KneePole pivot
    denUt.den_makeLoc( nodeName='KneePole_Loc', radius=radius, pos=(0, kneeDist, 0) )
    # Color the locator
    denUt.den_ColorShape(9)
    # Parent KneePole under KneeMid
    cmds.parent( 'KneePole_Loc', 'KneeMid_Loc' )
    # Lock KneePole attributes except translateY
    denUt.den_Lock(  1,0,1 , 1,1,1 , 1,1,1 , 1 )
    
    # Create locator for AnkleUp pivot
    denUt.den_makeLoc( nodeName='AnkleUp_Loc', radius=radius/2, pos=(footUpDist, footUpDist, 0) )
    # Color the locator
    denUt.den_ColorShape(2)
    # Parent AnkleUp  under Ankle_Piv
    cmds.parent( 'AnkleUp_Loc', 'Ankle_Piv', relative=True )
    # Lock KneePole attributes except translate X and Y
    denUt.den_Lock(  0,0,1 , 1,1,1 , 1,1,1 , 1 )
    
    # Take the KneeMid_Loc, constrain to make it float between Hip_Piv and Ankle_Piv
    LegMidLocPtCon = cmds.pointConstraint( 'Hip_Piv','Ankle_Piv','KneeMid_Loc' )[0]
    # Aim KneeMid_Loc at Ankle_Piv, use Knee_Piv as its worldUpObject (keep IK solution in a flat triangle plane)
    LegMidLocAimCon = cmds.aimConstraint( 'Ankle_Piv','KneeMid_Loc', worldUpType='object', worldUpObject='Knee_Piv' )[0]
    # Lock all KneeMid_Loc attributes
    cmds.select('KneeMid_Loc')
    denUt.den_Lock(  1,1,1 , 1,1,1 , 1,1,1 , 1 )
    
    # Aim Hip_Piv at Knee_Piv, use Ankle_Piv as its worldUpObject 
    HipPivAimCon = cmds.aimConstraint( 'Knee_Piv','Hip_Piv', worldUpType='object', worldUpObject='Ankle_Piv' )[0]
    # Lock all Hip_Piv attributes, except translate
    cmds.select('Hip_Piv')
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Aim Ankle_Piv at Ball_Piv, use Toe_Piv as its worldUpObject 
    AnklePivAimCon = cmds.aimConstraint( 'Ball_Piv','Ankle_Piv', worldUpType='object', worldUpObject='Toe_Piv' )[0]
    # Lock all Ankle_Piv attributes, except translate
    cmds.select('Ankle_Piv')
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Aim SoleLF_Piv's aim -Z axis towards SoleLB_Piv
    SoleLFPivAimCon = cmds.aimConstraint( 'SoleLB_Piv','SoleLF_Piv', aimVector=(0,0,-1), mo=False )[0]
    cmds.select('SoleLF_Piv')
    
    # Aim SoleRF_Piv's aim -Z axis towards SoleRB_Piv
    SoleRFPivAimCon = cmds.aimConstraint( 'SoleRB_Piv','SoleRF_Piv', aimVector=(0,0,-1), mo=False )[0]
    cmds.select('SoleRF_Piv')
    
    # Aim Toe_Piv's aim -Z axis towards Ball_Piv
    ToePivAimCon = cmds.aimConstraint( 'Ball_Piv','Toe_Piv', aimVector=(0,0,-1), mo=False )[0]
    # Lock all Toe_Piv attributes, except translate
    cmds.select('Toe_Piv')
    denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    
    cmds.select( 'Heel_Piv', 'SoleLF_Piv', 'SoleRF_Piv', 'SoleLB_Piv', 'SoleRB_Piv' )
    # Lock all attributes, except translate X, Z
    denUt.den_Lock(  0,1,0 , 1,1,1 , 1,1,1 , 1 )
    
    # Rename pivots/locators with side and prefix
    cmds.rename( 'Hip_Piv', side+prefix+'Hip_Piv' )
    cmds.rename( 'Knee_Piv', side+prefix+'Knee_Piv' )
    cmds.rename( 'Ankle_Piv', side+prefix+'Ankle_Piv' )
    cmds.rename( 'Ball_Piv', side+prefix+'Ball_Piv' )
    cmds.rename( 'BallSole_Piv', side+prefix+'BallSole_Piv' )
    cmds.rename( 'Toe_Piv', side+prefix+'Toe_Piv' )
    cmds.rename( 'Heel_Piv', side+prefix+'Heel_Piv' )
    cmds.rename( 'KneeMid_Loc', side+prefix+'KneeMid_Loc' )
    cmds.rename( 'KneePole_Loc', side+prefix+'KneePole_Loc' )
    cmds.rename( 'AnkleUp_Loc', side+prefix+'AnkleUp_Loc' )
    cmds.rename( 'SoleLF_Piv', side+prefix+'SoleLF_Piv' )
    cmds.rename( 'SoleRF_Piv', side+prefix+'SoleRF_Piv' )
    cmds.rename( 'SoleLB_Piv', side+prefix+'SoleLB_Piv' )
    cmds.rename( 'SoleRB_Piv', side+prefix+'SoleRB_Piv' )
    cmds.rename( LegMidLocPtCon, side+prefix+LegMidLocPtCon )
    cmds.rename( LegMidLocAimCon, side+prefix+LegMidLocAimCon )
    cmds.rename( HipPivAimCon, side+prefix+HipPivAimCon )
    cmds.rename( AnklePivAimCon, side+prefix+AnklePivAimCon )
    cmds.rename( SoleLFPivAimCon, side+prefix+SoleLFPivAimCon )
    cmds.rename( SoleRFPivAimCon, side+prefix+SoleRFPivAimCon )
    cmds.rename( ToePivAimCon, side+prefix+ToePivAimCon )
    
    # Parent all the pivots under LegPivGrp
    cmds.parent( side+prefix+'Hip_Piv', side+prefix+'Knee_Piv', side+prefix+'Ankle_Piv', side+prefix+'Ball_Piv', side+prefix+'BallSole_Piv', side+prefix+'Toe_Piv', LegPivGrp )
    cmds.parent( side+prefix+'Heel_Piv', side+prefix+'SoleLF_Piv', side+prefix+'SoleLB_Piv', side+prefix+'SoleRF_Piv', side+prefix+'SoleRB_Piv', side+prefix+'KneeMid_Loc', LegPivGrp )
    
    # Lock all attributes of KneeMid_Loc
    cmds.select(side+prefix+'KneeMid_Loc')
    denUt.den_Lock(  1,1,1 , 1,1,1 , 1,1,1 , 1 )
    
    # Clear selcetion
    cmds.select(clear=True)
    # DP refresh
    denUt.den_DiagPause( seconds=dpTime )
    
    # If doing the right side, flip the root group to the other side by giveing scaleX -1
    if side == 'R_':
        cmds.setAttr( LegPivGrp+'.scaleX', -1 )
    
    return LegPivGrp


# ---------------------------------------------------------------------------------------
# Create Leg Rig

def jly_makeBipedLegRig( side='L_', prefix='', name='Leg', radius=2.0, ctrlRadius=15.0, displayLocalAxis=False, twistType='none', revKnee=False, dpTime = 0.01 ):
    
    # Input twist type
    if( twistType == 'none' ) or ( twistType == 'ribbon' ) or ( twistType == 'twist' ):
        print( 'doing twistType \''+twistType+'\'' )
    else:
        print( 'ERROR - twistType must be  \'none\' or \'ribon\' or \'upcar\' - nothing else will work' )
    
    # If making right leg rig, set pivot group scaleX to 1, flip the pivot group to the left for good mirroring
    sideColor = 6
    if side == 'R_':
        cmds.setAttr( side+prefix+name+'Piv_Grp.scaleX', 1 )
        sideColor = 13
    # DP refresh viewport
    denUt.den_DiagPause( seconds=dpTime )
    
    # Create the top level root group for the leg rig
    LegRigGrp = denUt.den_makeGrp( nodeName=side+prefix+name+'_Grp' )
    
    # Create 5 variables to store components of the leg rig (SpaceINs, SpaceOUTs, BindJoints, Controls, and Guts)
    LegSpaceINs = []
    LegSpaceOUTs = []
    LegBindJoints = []
    LegCtrlsALL = []
    LegGutsALL = []
    
    # Create leg SpaceIN groups (to follow Pelvis, Cog, All), and parent under LegRigGrp
    PelvisSpaceIN = denUt.den_makeGrp( nodeName=side+prefix+'PelvisSpace_IN' )
    PelvisSpaceIN = cmds.parent( PelvisSpaceIN, LegRigGrp )[0]
    CogSpaceIN = denUt.den_makeGrp( nodeName=side+prefix+'CogSpace_IN' )
    CogSpaceIN = cmds.parent( CogSpaceIN, LegRigGrp )[0]
    AllSpaceIN = denUt.den_makeGrp( nodeName=side+prefix+'AllSpace_IN' )
    AllSpaceIN = cmds.parent( AllSpaceIN, LegRigGrp )[0]
    # Add all the spaceINs to the list LegSpaceINs
    LegSpaceINs += [ PelvisSpaceIN, CogSpaceIN, AllSpaceIN ]
    
    # Create groups for leg skeleton
    LegSkelGrp = denUt.den_makeGrp( nodeName=side+prefix+name+'Skel_Grp' )
    # Parent them under the PelvisSpaceIN
    LegSkelGrp = cmds.parent( LegSkelGrp, PelvisSpaceIN )[0]
    # Create groups for leg control
    LegCtrlGrp = denUt.den_makeGrp( nodeName=side+prefix+name+'Ctrl_Grp' )
    # Parent them under the PelvisSpaceIN
    LegCtrlGrp = cmds.parent( LegCtrlGrp, PelvisSpaceIN )[0]
    
    # Create Ankle control space to accept the blend spaces
    # Create a group to accept transform from all spaces
    AnkleCtrlSpace = denUt.den_makeGrp( nodeName=side+prefix+'AnkleCtrl_Space' )
    # Parent AnkleCtrlSpace under the LegCtrlGrp
    AnkleCtrlSpace = cmds.parent( AnkleCtrlSpace, LegCtrlGrp )[0]
    # Parent constraint AnkleCtrlSpace to each spaceINs
    AnkleCtrlSpaceConstraint = cmds.parentConstraint( PelvisSpaceIN, AnkleCtrlSpace, weight=0 )
    AnkleCtrlSpaceConstraint = cmds.parentConstraint( CogSpaceIN, AnkleCtrlSpace, weight=0 )
    # AllSpaceIN weight 1 as default
    AnkleCtrlSpaceConstraint = cmds.parentConstraint( AllSpaceIN, AnkleCtrlSpace, weight=1 )
    
    # Query all pivots for their worldspace positions
    HipPos = cmds.xform( side+prefix+'Hip_Piv', ws=True, q=True, t=True )
    KneePos = cmds.xform( side+prefix+'Knee_Piv', ws=True, q=True, t=True )
    AnklePos = cmds.xform( side+prefix+'Ankle_Piv', ws=True, q=True, t=True )
    BallPos = cmds.xform( side+prefix+'Ball_Piv', ws=True, q=True, t=True )
    ToePos = cmds.xform( side+prefix+'Toe_Piv', ws=True, q=True, t=True )
    HeelPos = cmds.xform( side+prefix+'Heel_Piv', ws=True, q=True, t=True )
    SoleLFPos = cmds.xform( side+prefix+'SoleLF_Piv', ws=True, q=True, t=True )
    SoleLBPos = cmds.xform( side+prefix+'SoleLB_Piv', ws=True, q=True, t=True )
    SoleRFPos = cmds.xform( side+prefix+'SoleRF_Piv', ws=True, q=True, t=True )
    SoleRBPos = cmds.xform( side+prefix+'SoleLB_Piv', ws=True, q=True, t=True )
    # Caculate to get a flat BallSole Pivot position
    BallSolePos = [ BallPos[0], ToePos[1], BallPos[2] ]
    KneePolePos = cmds.xform( side+prefix+'KneePole_Loc', ws=True, q=True, t=True )
    
    # --- Create all joints for the leg ---
    # Clear selection
    cmds.select( clear=True )
    # Create hip joint at the correct postion
    HipJoint = cmds.joint( n=side+prefix+'Hip_Jnt', p=(HipPos), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Create knee joint at the correct postion
    KneeJoint = cmds.joint( n=side+prefix+'Knee_Jnt', p=(KneePos), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Create ankle joint at the correct postion
    AnkleJoint = cmds.joint( n=side+prefix+'Ankle_Jnt', p=(AnklePos), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Create ball joint at the correct postion
    BallJoint = cmds.joint( n=side+prefix+'Ball_Jnt', p=(BallPos), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    # Create toe joint at the correct postion
    ToeJoint = cmds.joint( n=side+prefix+'Toe_Jx', p=(ToePos), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
    
    # If displayLocalAxis=True, show all local axis for the joints
    if ( displayLocalAxis ):
        cmds.setAttr( HipJoint+'.displayLocalAxis', 1 )
        cmds.setAttr( KneeJoint+'.displayLocalAxis', 1 )
        cmds.setAttr( AnkleJoint+'.displayLocalAxis', 1 )
        cmds.setAttr( BallJoint+'.displayLocalAxis', 1 )
        cmds.setAttr( ToeJoint+'.displayLocalAxis', 1 )
    
    
    # --- Orient all the joints ---
    # Clear selection, DP time refresh
    cmds.select( clear=True ); denUt.den_DiagPause( seconds=dpTime )
    # Orient Knee Joint zdown
    cmds.joint( KneeJoint, e=True, oj='xyz', secondaryAxisOrient='zdown', zso=True ); denUt.den_DiagPause( seconds=dpTime )
    # Orient Ankle Joint to the Knee Joint
    cmds.joint( AnkleJoint, e=True, oj='none', zso=True ); denUt.den_DiagPause( seconds=dpTime )
    
    # *If want reverse knee:
    if revKnee:
        cmds.setAttr( side+prefix+'Hip_Piv_aimConstraint1.upVectorY', -1 ); denUt.den_DiagPause( seconds=dpTime )
    
    # - To orient hip joint, need to force it to orient on the leg triangle
    # Parent hip joint under hip pivot temporarily
    HipJoint = cmds.parent( HipJoint, side+prefix+'Hip_Piv' )[0]
    # Orient the joint to the hip pivot
    cmds.joint( HipJoint, e=True, oj='none', zso=True ); denUt.den_DiagPause( seconds=dpTime )
    # Put the hip joint back under the LegSkelGrp
    HipJoint = cmds.parent( HipJoint, LegSkelGrp )[0]
    
    # - To orient foot joints, need to force it to orient on the foot triangle
    # Parent ankle joint under ankle pivot temporarily
    AnkleJoint = cmds.parent( AnkleJoint, side+prefix+'Ankle_Piv' )[0]
    # Orient Ball Joint
    cmds.joint( BallJoint, e=True, oj='xyz', zso=True ); denUt.den_DiagPause( seconds=dpTime )
    # Orient Toe Joint
    cmds.joint( ToeJoint, e=True, oj='none', zso=True ); denUt.den_DiagPause( seconds=dpTime )
    # Put the ankle joint back under the KneeJoint
    AnkleJoint = cmds.parent( AnkleJoint, KneeJoint )[0]
    
    # --- Create IK and FK joint chains for the leg ---
    # Duplicate leg joints for to make IK joint chain
    HipJointIK = cmds.duplicate (HipJoint, name=side+prefix+'Hip_IK' )[0]
    # Rename joints to _IK
    KneeJointIK = cmds.rename (HipJointIK+'|'+side+prefix+'Knee_Jnt', side+prefix+'Knee_IK' )
    AnkleJointIK = cmds.rename (KneeJointIK+'|'+side+prefix+'Ankle_Jnt', side+prefix+'Ankle_IK' )
    BallJointIK = cmds.rename (AnkleJointIK+'|'+side+prefix+'Ball_Jnt', side+prefix+'Ball_IK' )
    ToeJointIK = cmds.rename (BallJointIK+'|'+side+prefix+'Toe_Jx', side+prefix+'Toe_IK' )
    # Duplicate leg joints for to make FK joint chain
    HipJointFK = cmds.duplicate (HipJoint, name=side+prefix+'Hip_FK' )[0]
    # Rename joints to _FK
    KneeJointFK = cmds.rename (HipJointFK+'|'+side+prefix+'Knee_Jnt', side+prefix+'Knee_FK' )
    AnkleJointFK = cmds.rename (KneeJointFK+'|'+side+prefix+'Ankle_Jnt', side+prefix+'Ankle_FK' )
    BallJointFK = cmds.rename (AnkleJointFK+'|'+side+prefix+'Ball_Jnt', side+prefix+'Ball_FK' )
    ToeJointFK = cmds.rename (BallJointFK+'|'+side+prefix+'Toe_Jx', side+prefix+'Toe_FK' )
    
    # --- Create the controls and 0 nulls ---
    # Create Hip FK control (spike)
    HipFKCtrl = denUt.den_MakeSpike( nodeName=side+prefix+'HipFK_Ctrl', radius=ctrlRadius, axis='+Z')
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Unlock all attribute before re-parent
    denUt.den_UnLockAttr(True,True,True,True)
    # Parent it under HipJointFK
    HipFKCtrl = cmds.parent( HipFKCtrl, HipJointFK, relative=True )
    # Parent it under LegCtrlGrp
    HipFKCtrl = cmds.parent( HipFKCtrl, LegCtrlGrp )
    # Add 0 null
    HipFKCtrl = denUt.den_AddZeroNull()
    # Lock all attribute except rotate and visibility
    denUt.den_LockAttr(True,False,True,False)
    # Store the 0 null in a variable
    HipFKCtrlZero = cmds.listRelatives( HipFKCtrl, parent=True, fullPath=True )[0]
    # Connect rotate attribute of the joint to the Hip FK control, so it gets exact rotate number
    cmds.connectAttr( HipFKCtrl[0]+'.rotate', HipJointFK+'.rotate' )
    # Parent constraint 0 null to the LegCtrlGrp, so if leg move the control moves too, to be visually clear
    cmds.parentConstraint( LegCtrlGrp, HipFKCtrlZero, mo=True )
    
    # Create Leg Utility Control (gear) (turn maya UI Move ctrl Tool Setting symmerty off when doing this)
    LegUtilCtrl = denUt.den_MakeGear( nodeName=side+prefix+name+'Util_Ctrl', pos=(ctrlRadius*0.5,0,ctrlRadius), radius=ctrlRadius*0.2, Plane='ZX')
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Unlock control attributes before re-parent
    denUt.den_UnLockAttr(True,True,True,True)
    # Parent utility gear control under hip control
    LegUtilCtrl = cmds.parent( LegUtilCtrl, HipJointFK, relative=True )
    # Parent utility gear control under LegCtrlGrp
    LegUtilCtrl = cmds.parent( LegUtilCtrl, LegCtrlGrp )
    # Lock all attribute except visibility
    denUt.den_LockAttr(True,True,True,False)
    # Add attributes to the leg
    cmds.addAttr( LegUtilCtrl, longName=side+prefix+name+'_FK_IK', defaultValue=1.0, minValue=0.0, maxValue=1.0 )
    cmds.setAttr( LegUtilCtrl[0]+'.'+side+prefix+name+'_FK_IK', lock=False, keyable=True )
    # Add attributes to the ankle
    cmds.addAttr( LegUtilCtrl, longName=side+prefix+'Ankle_FK_IK', defaultValue=0.0, minValue=0.0, maxValue=1.0 )
    cmds.setAttr( LegUtilCtrl[0]+'.'+side+prefix+'Ankle_FK_IK', lock=False, keyable=True )
    
    # Create Knee Control (pole)
    KneeCtrl = denUt.den_MakePole( nodeName=side+prefix+'Knee_Ctrl', radius=ctrlRadius*0.3 )
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Transform to the correct position
    cmds.xform( t=KneePolePos )
    # Parent under LegCtrlGrp
    KneeCtrl = cmds.parent( KneeCtrl, LegCtrlGrp )
    # Add 0 null
    KneeCtrl = denUt.den_AddZeroNull()
    # If Reverse knee:
    if revKnee:
        KneeFKCtrl = denUt.den_MakeArrowR( nodeName=side+prefix+'KneeFK_Ctrl', pos=(0,ctrlRadius*0.5,0), radius=ctrlRadius*0.3, doT=True, axis='+Y' )
    else:
        KneeFKCtrl = denUt.den_MakeArrowR( nodeName=side+prefix+'KneeFK_Ctrl', pos=(0,-ctrlRadius*0.5,0), radius=ctrlRadius*0.3, doT=True, axis='-Y' )
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Unlock control attributes before re-parent
    denUt.den_UnLockAttr(True,True,True,True)
    # Parent Knee FK Control under KneeJointFK
    KneeFKCtrl = cmds.parent( KneeFKCtrl, KneeJointFK, relative=True )
    # Parent Knee FK Control under HipFKCtrl
    KneeFKCtrl = cmds.parent( KneeFKCtrl, HipFKCtrl )
    # Add 0 null
    KneeFKCtrl = denUt.den_AddZeroNull()
    # Lock all attribute except rotate and visibility
    denUt.den_LockAttr(True,False,True,False)
    # Connect KneeFKCtrl rotate attribute to KneeJointFK so it gets exact rotate number
    cmds.connectAttr( KneeFKCtrl[0]+'.rotate', KneeJointFK+'.rotate' )
    
    # Create Ankle Control (ball)
    AnkleCtrl = denUt.den_MakeBall( nodeName=side+prefix+'Ankle_Ctrl', radius=ctrlRadius*0.7 )
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Transform to the correct position
    cmds.xform( t=AnklePos )
    # Parent under Ankle Control Space
    AnkleCtrl = cmds.parent( AnkleCtrl, AnkleCtrlSpace )
    # Add 0 null
    AnkleCtrl = denUt.den_AddZeroNull()
    # Change rotate order to make sense for ankle
    cmds.setAttr( AnkleCtrl[0]+'.rotateOrder', 1 )
    # Capture and store the 0 null in a variable
    AnkleCtrlZero = cmds.listRelatives( AnkleCtrl, parent=True, fullPath=True )[0]
    
    # Create Ankle FK Control (spike)
    AnkleFKCtrl = denUt.den_MakeSpike( nodeName=side+prefix+'AnkleFK_Ctrl', radius=ctrlRadius*0.7, axis='+Z')
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Unlock control attributes before re-parent
    denUt.den_UnLockAttr(True,True,True,True)
    # Parent under AnkleJointFK
    AnkleFKCtrl = cmds.parent( AnkleFKCtrl, AnkleJointFK, relative=True )
    # Parent under KneeFKCtrl
    AnkleFKCtrl = cmds.parent( AnkleFKCtrl, KneeFKCtrl )
    # Add 0 null
    AnkleFKCtrl = denUt.den_AddZeroNull()
    # Lock all attribute except rotate and visibility
    denUt.den_LockAttr(True,False,True,False)
    # Connect AnkleJointFK rotate attribute to AnkleFKCtrl so it gets exact rotate number
    cmds.connectAttr( AnkleFKCtrl[0]+'.rotate', AnkleJointFK+'.rotate' )
    # Capture and store the 0 null in a variable
    AnkleFKCtrlZero = cmds.listRelatives( AnkleFKCtrl, parent=True, fullPath=True )[0]
    
    # Create Ball FK Control (spike)
    BallFKCtrl = denUt.den_MakeSpike(nodeName=side+prefix+'BallFK_Ctrl', radius=ctrlRadius*0.7, axis='-Z')
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Unlock control attributes before re-parent
    denUt.den_UnLockAttr(True,True,True,True)
    # Parent under BallJointFK
    BallFKCtrl = cmds.parent( BallFKCtrl, BallJointFK, relative=True )
    # Parent under AnkleFKCtrl
    BallFKCtrl = cmds.parent( BallFKCtrl, AnkleFKCtrl )
    # Add 0 null
    BallFKCtrl = denUt.den_AddZeroNull()
    # Lock all attribute except rotate and visibility
    denUt.den_LockAttr(True,False,True,False)
    # Connect AnkleJointFK rotate attribute to AnkleFKCtrl so it gets exact rotate number
    cmds.connectAttr( BallFKCtrl[0]+'.rotate', BallJointFK+'.rotate' )
    # Capture and store the 0 null in a variable
    BallFKCtrlZero = cmds.listRelatives( BallFKCtrl, parent=True, fullPath=True )[0]
    
    # Create Foot Utility Control (gear) (turn maya UI Move ctrl Tool Setting symmerty off when doing this)
    FootUtilCtrl = denUt.den_MakeGear( nodeName=side+prefix+'FootUtil_Ctrl', pos=(ctrlRadius*0.5,ctrlRadius*0.5,0), radius=ctrlRadius*0.2, Plane='XY')
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Parent utility gear control under ankle control
    FootUtilCtrl = cmds.parent( FootUtilCtrl, AnkleCtrl, relative=True )
    # Add FootRock attributes to the control
    cmds.addAttr( FootUtilCtrl, longName=side+prefix+'FootRock', defaultValue=0.0, minValue=-90.0, maxValue=90.0 )
    cmds.setAttr( FootUtilCtrl[0]+'.'+side+prefix+'FootRock', lock=False, keyable=True )
    # Add FootRoll attributes to the control
    cmds.addAttr( FootUtilCtrl, longName=side+prefix+'FootRoll', defaultValue=0.0, minValue=-90.0, maxValue=90.0 )
    cmds.setAttr( FootUtilCtrl[0]+'.'+side+prefix+'FootRoll', lock=False, keyable=True )
    # Add FootPivot attributes to the control
    cmds.addAttr( FootUtilCtrl, longName=side+prefix+'FootPivot', defaultValue=0.0, minValue=-90.0, maxValue=90.0 )
    cmds.setAttr( FootUtilCtrl[0]+'.'+side+prefix+'FootPivot', lock=False, keyable=True )
    # Add FootTwist attributes to the control
    cmds.addAttr( FootUtilCtrl, longName=side+prefix+'FootTwist', defaultValue=0.0, minValue=-90.0, maxValue=90.0 )
    cmds.setAttr( FootUtilCtrl[0]+'.'+side+prefix+'FootTwist', lock=False, keyable=True )
    # Add HeelPivot attributes to the control
    cmds.addAttr( FootUtilCtrl, longName=side+prefix+'HeelPivot', defaultValue=0.0, minValue=-90.0, maxValue=90.0 )
    cmds.setAttr( FootUtilCtrl[0]+'.'+side+prefix+'HeelPivot', lock=False, keyable=True )
    # Add ToeRoll attributes to the control
    cmds.addAttr( FootUtilCtrl, longName=side+prefix+'ToeRoll', defaultValue=0.0, minValue=-90.0, maxValue=90.0 )
    cmds.setAttr( FootUtilCtrl[0]+'.'+side+prefix+'ToeRoll', lock=False, keyable=True )
    # Add ToePivot attributes to the control
    cmds.addAttr( FootUtilCtrl, longName=side+prefix+'ToePivot', defaultValue=0.0, minValue=-90.0, maxValue=90.0 )
    cmds.setAttr( FootUtilCtrl[0]+'.'+side+prefix+'ToePivot', lock=False, keyable=True )
    # Add ToeBend attributes to the control
    cmds.addAttr( FootUtilCtrl, longName=side+prefix+'ToeBend', defaultValue=0.0, minValue=-90.0, maxValue=90.0 )
    cmds.setAttr( FootUtilCtrl[0]+'.'+side+prefix+'ToeBend', lock=False, keyable=True )
    
    # --- Create and connect attributes for Ankle control space switcher ---
    # Add attributes to leg utility control for PelvisSpace
    cmds.addAttr( LegUtilCtrl, longName=side+prefix+'PelvisSpace', defaultValue=0.0, minValue=0.0, maxValue=1.0 )
    # Set attribute lock and keyable value so it shows up in channel box
    cmds.setAttr( LegUtilCtrl[0]+'.'+side+prefix+'PelvisSpace', lock=False, keyable=True )
    # Connect attribute to the actual space switching constraint
    cmds.connectAttr( LegUtilCtrl[0]+'.'+side+prefix+'PelvisSpace', AnkleCtrlSpaceConstraint[0]+'.'+side+prefix+'PelvisSpace_INW0' )
    # Add attributes to leg utility control for CogSpace
    cmds.addAttr( LegUtilCtrl, longName=side+prefix+'CogSpace', defaultValue=0.0, minValue=0.0, maxValue=1.0 )
    cmds.setAttr( LegUtilCtrl[0]+'.'+side+prefix+'CogSpace', lock=False, keyable=True )
    cmds.connectAttr( LegUtilCtrl[0]+'.'+side+prefix+'CogSpace', AnkleCtrlSpaceConstraint[0]+'.'+side+prefix+'CogSpace_INW1' )
    # Add attributes to leg utility control for AllSpace
    cmds.addAttr( LegUtilCtrl, longName=side+prefix+'AllSpace', defaultValue=1.0, minValue=0.0, maxValue=1.0 )
    cmds.setAttr( LegUtilCtrl[0]+'.'+side+prefix+'AllSpace', lock=False, keyable=True )
    cmds.connectAttr( LegUtilCtrl[0]+'.'+side+prefix+'AllSpace', AnkleCtrlSpaceConstraint[0]+'.'+side+prefix+'AllSpace_INW2' )
    
    # --- Create Leg FK_IK blending ---
    # Use pair blend to blend 2 value
    # Create pairBlend shading node for hip
    Hip_pairBlend = cmds.shadingNode ('pairBlend', asUtility=True, n=side+prefix+'Hip_ikFk_pairBlend' )
    # Set rotInterpolation to quaternion, so it wont gimbal flip
    cmds.setAttr( Hip_pairBlend+'.rotInterpolation', 1 )
    # Connect hip FK rotate to input 1
    cmds.connectAttr( HipJointFK+'.rotate', Hip_pairBlend+'.inRotate1' )
    # Connect hip IK rotate to input 2
    cmds.connectAttr( HipJointIK+'.rotate', Hip_pairBlend+'.inRotate2' )
    # Connect leg FK.IK to hip 'weight'
    cmds.connectAttr( LegUtilCtrl[0]+'.'+side+prefix+name+'_FK_IK', Hip_pairBlend+'.weight' )
    # Connect Output Rotate to hip joint 'rotate'
    cmds.connectAttr( Hip_pairBlend+'.outRotate', HipJoint+'.rotate' )
    
    # Create pairBlend shading node for knee
    Knee_pairBlend = cmds.shadingNode ('pairBlend', asUtility=True, n=side+prefix+'Knee_ikFk_pairBlend' )
    # Set rotInterpolation to quaternion, so it wont gimbal flip
    cmds.setAttr( Knee_pairBlend+'.rotInterpolation', 1 )
    # Connect knee FK rotate to input 1
    cmds.connectAttr( KneeJointFK+'.rotate', Knee_pairBlend+'.inRotate1' )
    # Connect knee IK rotate to input 2
    cmds.connectAttr( KneeJointIK+'.rotate', Knee_pairBlend+'.inRotate2' )
    # Connect leg FK.IK to knee 'weight'
    cmds.connectAttr( LegUtilCtrl[0]+'.'+side+prefix+name+'_FK_IK', Knee_pairBlend+'.weight' )
    # Connect Output Rotate to knee joint 'rotate'
    cmds.connectAttr( Knee_pairBlend+'.outRotate', KneeJoint+'.rotate' )
    
    # Create pairBlend shading node for ankle
    Ankle_pairBlend = cmds.shadingNode ('pairBlend', asUtility=True, n=side+prefix+'Ankle_ikFk_pairBlend' )
    # Set rotInterpolation to quaternion, so it wont gimbal flip
    cmds.setAttr( Ankle_pairBlend+'.rotInterpolation', 1 )
    # Connect ankle FK rotate to input 1
    cmds.connectAttr( AnkleJointFK+'.rotate', Ankle_pairBlend+'.inRotate1' )
    # Connect ankle IK rotate to input 2
    cmds.connectAttr( AnkleJointIK+'.rotate', Ankle_pairBlend+'.inRotate2' )
    # Connect leg FK.IK to ankle 'weight'
    cmds.connectAttr( LegUtilCtrl[0]+'.'+side+prefix+name+'_FK_IK', Ankle_pairBlend+'.weight' )
    # Connect Output Rotate to ankle joint 'rotate'
    cmds.connectAttr( Ankle_pairBlend+'.outRotate', AnkleJoint+'.rotate' )
    
    # Create pairBlend shading node for ball
    Ball_pairBlend = cmds.shadingNode ('pairBlend', asUtility=True, n=side+prefix+'Ball_ikFk_pairBlend' )
    # Set rotInterpolation to quaternion, so it wont gimbal flip
    cmds.setAttr( Ball_pairBlend+'.rotInterpolation', 1 )
    # Connect ball FK rotate to input 1
    cmds.connectAttr( BallJointFK+'.rotate', Ball_pairBlend+'.inRotate1' )
    # Connect ball IK rotate to input 2
    cmds.connectAttr( BallJointIK+'.rotate', Ball_pairBlend+'.inRotate2' )
    # Connect leg FK.IK to ball 'weight'
    cmds.connectAttr( LegUtilCtrl[0]+'.'+side+prefix+name+'_FK_IK', Ball_pairBlend+'.weight' )
    # Connect Output Rotate to ball joint 'rotate'
    cmds.connectAttr( Ball_pairBlend+'.outRotate', BallJoint+'.rotate' )
    
    
    # --- Create Reverse Foot ---
    # Create a list of foot pivots in order
    footPivs = [ 'Heel_Piv', 'BallSole_Piv', 'SoleLF_Piv', 'SoleRF_Piv', 'Toe_Piv', 'Ball_Piv', 'Ankle_Piv' ]
    # Create a list for foot joints
    footJnts = []
    # For each foot pivot, pair a number with each of them, 
    for number,footPiv in enumerate(footPivs):
        prevNum = number-1
        # Find the name, remove the suffix '_' from each pivots, return a list without '_', and use [0] to find the first one
        # The result return a name root, example: 'Heel_Piv' will return 'Heel'
        nameRoot = denUt.den_SplitAt(footPiv,'_',1)[0]
        # Create joint with correct name
        footJnt = cmds.joint( n=side+prefix+nameRoot+'Rev_Jx', radius=radius*0.7 )
        footPiv = side+prefix+footPivs[number]
        # Take the footPiv and parent under footJnt
        footJnt = cmds.parent( footJnt, footPiv, relative=True )
        # Orient the joint with the footPiv
        cmds.joint( footJnt, e=True, oj='none', zso=True, radius=radius*0.7 ); denUt.den_DiagPause( seconds=dpTime )
        # If it is not the very first joint
        if number != 0:
            # Parent footJnt under the previs footJnt created
            footJnt = cmds.parent( footJnt, footJnts[prevNum], relative=False )
        else:
            # Otherwise, parent under world, 1st joint wont have a parent
            footJnt = cmds.parent( footJnt, world=True )
        # Add new footJnts into footJnts list
        footJnts = footJnts + [footJnt]
    
    # Assign variavles for joints so they have names
    RevHeelJoint = footJnts[0]
    RevBallSoleJoint = footJnts[1]
    RevSoleLFJoint = footJnts[2]
    RevSoleRFJoint = footJnts[3]
    RevToeJoint = footJnts[4]
    RevBallJoint = footJnts[5]
    RevAnkleJoint = footJnts[6]
    
    # --- Create IK Handles ---
    # Create a IK handel for leg, start with HipJointIK, end with AnkleJointIK
    cmds.select( HipJointIK, AnkleJointIK )
    # Add ikRPsolver
    LegIKhandle = denUt.den_AddIKHandle( handleType='ikRPsolver' )
    # Parent ikRPsolver under RevAnkleJoint
    LegIKhandle = cmds.parent( LegIKhandle, RevAnkleJoint )[0]
    # Add poleVectorConstraint so the KneeCtrl drive the LegIKhandle
    cmds.poleVectorConstraint( KneeCtrl, LegIKhandle )
    
    # Create a IK handel for leg, start with AnkleJointIK, end with BallJointIK
    cmds.select( AnkleJointIK, BallJointIK )
    # Add ikRPsolver
    BallIKhandle = denUt.den_AddIKHandle( handleType='ikSCsolver' )
    # Parent ikRPsolver under RevBallJoint
    BallIKhandle = cmds.parent( BallIKhandle, RevBallJoint )[0]
    
    # Create a IK handel for leg, start with BallJointIK, end with ToeJointIK
    cmds.select( BallJointIK, ToeJointIK )
    # Add ikRPsolver
    ToeIKhandle = denUt.den_AddIKHandle( handleType='ikSCsolver' )
    # Parent ikRPsolver under RevToeJoint
    ToeIKhandle = cmds.parent( ToeIKhandle, RevToeJoint )[0]
    
    # --- Create utility nodes, connect attributes for foot roll ---
    # Foot Rool: rotate on Heel or Ball
    
    # - Rotate at Heel -
    # Create a unitConversion node, store in a variable, and give it a name
    # use unitConversion to convert degrees into radius
    footHeelRoll_unitConversion = cmds.shadingNode( 'unitConversion', asUtility=True, n=side+prefix+'footHeelRoll_unitConversion' )
    # Create a clamp node, Clamp value at 0 if >0 for rotate at heel
    footHeelRoll_clamp = cmds.shadingNode( 'clamp', asUtility=True, n=side+prefix+'footHeelRoll_clamp' )
    # Set footHeelRoll_unitConversion at correct value, 0.01745
    cmds.setAttr( footHeelRoll_unitConversion+'.conversionFactor', 0.01745 )
    # Set clamp min =  -180 (max = 0)
    cmds.setAttr( footHeelRoll_clamp+'.minR', -180 )
    
    # - Rotate at ball - 
    # Create a unitConversion node, store in a variable, and give it a name
    footBallRoll_unitConversion = cmds.shadingNode( 'unitConversion', asUtility=True, n=side+prefix+'footBallRoll_unitConversion' )
    # Create a clamp node, Clamp value at 0 if <0 for rotate at heel
    footBallRoll_clamp = cmds.shadingNode( 'clamp', asUtility=True, n=side+prefix+'footBallRoll_clamp' )
    # Set footBallRoll_unitConversion at correct value, 0.01745
    cmds.setAttr( footBallRoll_unitConversion+'.conversionFactor', 0.01745 )
    # Set clamp max = 180 (min = 0)
    cmds.setAttr( footBallRoll_clamp+'.maxR', 180 )
    # Connect attributes from foot utility control to footHeelRoll_clamp inputR (-180~0)
    cmds.connectAttr( FootUtilCtrl[0]+'.'+side+prefix+'FootRoll', footHeelRoll_clamp+'.inputR' )
    # Connect attributes from foot utility control to footBallRoll_clamp inputR (0~180)
    cmds.connectAttr( FootUtilCtrl[0]+'.'+side+prefix+'FootRoll', footBallRoll_clamp+'.inputR' )
    # Connect attributes from footHeelRoll_clamp output to footHeelRoll_unitConversion input
    cmds.connectAttr( footHeelRoll_clamp+'.outputR', footHeelRoll_unitConversion+'.input' )
    # Connect attributes from footBallRoll_clamp output to footBallRoll_unitConversion input
    cmds.connectAttr( footBallRoll_clamp+'.outputR', footBallRoll_unitConversion+'.input' )
    # Connect attributes from footHeelRoll_unitConversion output to RevHeelJoint rotateX
    cmds.connectAttr( footHeelRoll_unitConversion+'.output', RevHeelJoint[0]+'.rotateX' )
    # Connect attributes from footBallRoll_unitConversion output to RevBallJoint rotateX
    cmds.connectAttr( footBallRoll_unitConversion+'.output', RevBallJoint[0]+'.rotateX' )
    
    
    # --- Adding Utility Nodes and Connections for Foot Rock ---
    # Foot Rool: rotate on SoleLF or SoleRF
    
    # - Rotate at SoleLF -
    # Create a unitConversion node, store in a variable, and give it a name
    footSoleLFRock_unitConversion = cmds.shadingNode( 'unitConversion', asUtility=True, n=side+prefix+'footSoleLFRock_unitConversion' )
    # Create a clamp node, Clamp value at 0 if >0 for rotate at SoleLF
    footSoleLFRock_clamp = cmds.shadingNode( 'clamp', asUtility=True, n=side+prefix+'footSoleLFRock_clamp' )
    # Set footSoleLFRock_unitConversion at correct value, 0.01745
    cmds.setAttr( footSoleLFRock_unitConversion+'.conversionFactor', 0.01745 )
    # Set clamp min =  -180 (max = 0)
    cmds.setAttr( footSoleLFRock_clamp+'.minR', -180 )
    
    # - Rotate at SoleRF -
    # Create a unitConversion node, store in a variable, and give it a name
    footSoleRFRock_unitConversion = cmds.shadingNode( 'unitConversion', asUtility=True, n=side+prefix+'footSoleRFRock_unitConversion' )
    # Create a clamp node, Clamp value at 0 if <0 for rotate at SoleRF
    footSoleRFRock_clamp = cmds.shadingNode( 'clamp', asUtility=True, n=side+prefix+'footSoleRFRock_clamp' )
    # Set footSoleRFRock_unitConversion at correct value, 0.01745
    cmds.setAttr( footSoleRFRock_unitConversion+'.conversionFactor', 0.01745 )
    # Set clamp max = 180 (min = 0)
    cmds.setAttr( footSoleRFRock_clamp+'.maxR', 180 )
    # Connect attributes from foot utility control to footSoleLFRock_clamp inputR (-180~0)
    cmds.connectAttr( FootUtilCtrl[0]+'.'+side+prefix+'FootRock', footSoleLFRock_clamp+'.inputR' )
    # Connect attributes from foot utility control to footSoleRFRock_clamp inputR (0~180)
    cmds.connectAttr( FootUtilCtrl[0]+'.'+side+prefix+'FootRock', footSoleRFRock_clamp+'.inputR' )
    # Connect attributes from footSoleLFRock_clamp output to footSoleLFRock_unitConversion input
    cmds.connectAttr( footSoleLFRock_clamp+'.outputR', footSoleLFRock_unitConversion+'.input' )
    # Connect attributes from footSoleRFRock_clamp output to footSoleRFRock_unitConversion input
    cmds.connectAttr( footSoleRFRock_clamp+'.outputR', footSoleRFRock_unitConversion+'.input' )
    # Connect attributes from footSoleLFRock_unitConversion output to RevSoleLFJoint rotateZ
    cmds.connectAttr( footSoleLFRock_unitConversion+'.output', RevSoleLFJoint[0]+'.rotateZ' )
    # Connect attributes from footSoleRFRock_unitConversion output to RevSoleRFJoint rotateZ
    cmds.connectAttr( footSoleRFRock_unitConversion+'.output', RevSoleRFJoint[0]+'.rotateZ' )
    
    
    # --- Connect foot pivot ---
    # Create a unitConversion node, store in a variable, and give it a name
    footBallSolePivot_unitConversion = cmds.shadingNode( 'unitConversion', asUtility=True, n=side+prefix+'footBallSolePivot_unitConversion' )
    # Set the unitConversion at correct value, 0.01745
    cmds.setAttr( footBallSolePivot_unitConversion+'.conversionFactor', 0.01745 )
    # Connect attributes from foot utility to footBallSolePivot_unitConversion input
    cmds.connectAttr( FootUtilCtrl[0]+'.'+side+prefix+'FootPivot', footBallSolePivot_unitConversion+'.input' )
    # Connect attributes from footBallSolePivot_unitConversion output to RevBallSoleJoint rotateY
    cmds.connectAttr( footBallSolePivot_unitConversion+'.output', RevBallSoleJoint[0]+'.rotateY' )
    
    # -- Connect foot twist ---
    # Create a unitConversion node, store in a variable, and give it a name
    footBallTwist_unitConversion = cmds.shadingNode( 'unitConversion', asUtility=True, n=side+prefix+'footBallTwist_unitConversion' )
    # Set the unitConversion at correct value, 0.01745
    cmds.setAttr( footBallTwist_unitConversion+'.conversionFactor', 0.01745 )
    # Connect attributes from foot utility to footBallTwist_unitConversion input
    cmds.connectAttr( FootUtilCtrl[0]+'.'+side+prefix+'FootTwist', footBallTwist_unitConversion+'.input' )
    # Connect attributes from footBallTwist_unitConversion output to RevBallSoleJoint rotateZ
    cmds.connectAttr( footBallTwist_unitConversion+'.output', RevBallJoint[0]+'.rotateZ' )
    
    # -- Connect heel pivot ---
    # Create a unitConversion node, store in a variable, and give it a name
    footHeelPivot_unitConversion = cmds.shadingNode( 'unitConversion', asUtility=True, n=side+prefix+'footHeelPivot_unitConversion' )
    # Set the unitConversion at correct value, 0.01745
    cmds.setAttr( footHeelPivot_unitConversion+'.conversionFactor', 0.01745 )
    # Connect attributes from foot utility to footHeelPivot_unitConversion input
    cmds.connectAttr( FootUtilCtrl[0]+'.'+side+prefix+'HeelPivot', footHeelPivot_unitConversion+'.input' )
    # Connect attributes from footHeelPivot_unitConversion output to RevHeelJoint rotateY
    cmds.connectAttr( footHeelPivot_unitConversion+'.output', RevHeelJoint[0]+'.rotateY' )
    
    # -- Connect toe roll ---
    # Create a unitConversion node, store in a variable, and give it a name
    footToeRoll_unitConversion = cmds.shadingNode( 'unitConversion', asUtility=True, n=side+prefix+'footToeRoll_unitConversion' )
    # Create a clamp node, Clamp value at 0 if <0 for rotate at Toe
    footToeRoll_clamp = cmds.shadingNode( 'clamp', asUtility=True, n=side+prefix+'footToeRoll_clamp' )
    # Set the unitConversion at correct value, 0.01745
    cmds.setAttr( footToeRoll_unitConversion+'.conversionFactor', 0.01745 )
    # Set clamp max = 180 (min = 0)
    cmds.setAttr( footToeRoll_clamp+'.maxR', 180 )
    # Connect attributes from foot utility to footToeRoll_clamp input
    cmds.connectAttr( FootUtilCtrl[0]+'.'+side+prefix+'ToeRoll', footToeRoll_clamp+'.inputR' )
    # Connect attributes from footToeRoll_clamp output to footToeRoll_unitConversion input
    cmds.connectAttr( footToeRoll_clamp+'.outputR', footToeRoll_unitConversion+'.input' )
    # Connect attributes from footToeRoll_unitConversion output to RevHeelJoint rotateX
    cmds.connectAttr( footToeRoll_unitConversion+'.output', RevToeJoint[0]+'.rotateX' )
    
    # -- Connect toe pivot ---
    # Create a unitConversion node, store in a variable, and give it a name
    footToePivot_unitConversion = cmds.shadingNode( 'unitConversion', asUtility=True, n=side+prefix+'footToePivot_unitConversion' )
    # Set the unitConversion at correct value, 0.01745
    cmds.setAttr( footToePivot_unitConversion+'.conversionFactor', 0.01745 )
    # Connect attributes from foot utility to footToePivot_unitConversion input
    cmds.connectAttr( FootUtilCtrl[0]+'.'+side+prefix+'ToePivot', footToePivot_unitConversion+'.input' )
    # Connect attributes from footToePivot_unitConversion output to RevHeelJoint rotateY
    cmds.connectAttr( footToePivot_unitConversion+'.output', RevToeJoint[0]+'.rotateY' )
    
    # -- Connect toe bend ---
    # Create unitConversion node for Input and Output, store in variable, and give them name
    footToeBend_unitConversionIn = cmds.shadingNode( 'unitConversion', asUtility=True, n=side+prefix+'footToeBend_unitConversionIn' )
    footToeBend_unitConversionOut = cmds.shadingNode( 'unitConversion', asUtility=True, n=side+prefix+'footToeBend_unitConversionOut' )
    # Set the conversion factor for the input and output unitConversion nodes
    # Convert radians to degrees, correct number 57.29578
    cmds.setAttr( footToeBend_unitConversionIn+'.conversionFactor', 57.29578 )
    # Convert degrees to radians, correct number 0.01745
    cmds.setAttr( footToeBend_unitConversionOut+'.conversionFactor', 0.01745 )
    # Create an addDoubleLinear node to combine values from the toe bend and joint rotation
    footToeBend_addDoubleLinear = cmds.shadingNode( 'addDoubleLinear', asUtility=True, n=side+prefix+'footToeBend_addDoubleLinear' )
    # Disconnect the current ball joint rotation and prepare to blend the toe bend value
    cmds.disconnectAttr( BallJointIK+'.rotate', Ball_pairBlend+'.inRotate2' )
    # Connect attributes from BallJointIK's Z-axis rotation to footToeBend_unitConversionIn input
    cmds.connectAttr( BallJointIK+'.rotateZ', footToeBend_unitConversionIn+'.input' )
    # Connect attributes from ToeBend to footToeBend_addDoubleLinear input1
    cmds.connectAttr( FootUtilCtrl[0]+'.'+side+prefix+'ToeBend', footToeBend_addDoubleLinear+'.input1' )
    # Connect attributes from footToeBend_unitConversionIn output to footToeBend_addDoubleLinear input
    cmds.connectAttr( footToeBend_unitConversionIn+'.output', footToeBend_addDoubleLinear+'.input2' )
    # Connect attributes from footToeBend_addDoubleLinear output to footToeBend_unitConversionOut input
    cmds.connectAttr( footToeBend_addDoubleLinear+'.output', footToeBend_unitConversionOut+'.input' )
    # Connect the BallJointIK's X and Y-axis rotations to Ball_pairBlend rotate input
    cmds.connectAttr( BallJointIK+'.rotateX', Ball_pairBlend+'.inRotate2.inRotateX2' )
    cmds.connectAttr( BallJointIK+'.rotateY', Ball_pairBlend+'.inRotate2.inRotateY2' )
    # Connect attributes from footToeBend_unitConversionOut output to Ball_pairBlend Z-axis rotation input
    cmds.connectAttr( footToeBend_unitConversionOut+'.output', Ball_pairBlend+'.inRotate2.inRotateZ2' )
    
    # Add the spaceOut to attach toes in the future
    AnkleSpaceOUT = denUt.den_makeGrp( nodeName=side+prefix+'AnkleSpace_OUT' )
    # Parent under AnkleJoint
    AnkleSpaceOUT = cmds.parent( AnkleSpaceOUT, AnkleJoint )
    # Add to spaceOut list
    LegSpaceOUTs += AnkleSpaceOUT
    
    # Parent RevHeelJoint under AnkleCtrl so it follows ankle control
    RevHeelJoint = cmds.parent( RevHeelJoint, AnkleCtrl )
    
    # Add bind joints to BindJoint List
    LegBindJoints += [ HipJoint, KneeJoint, AnkleJoint, BallJoint ]
    
    # Add all controls to control List
    LegCtrlsALL += [ HipFKCtrl[0], KneeFKCtrl[0], AnkleFKCtrl[0], BallFKCtrl[0], KneeCtrl[0], AnkleCtrl[0], LegUtilCtrl[0], FootUtilCtrl[0] ]
    
    
    # --- Create twist options ---
    if twistType == 'none':
        print( 'no twist joints added' )
        LegBindJoints = [ HipJoint, KneeJoint, AnkleJoint, BallJoint ]
        
    if twistType == 'twist':
        LegTwistRigRet = den_makeTwists( side=side, prefix=prefix, radius=radius, Joints=['Hip','Knee','Ankle'], ctrlPos=(-10,0,-10), ctrlUpVec=(0,0,-1), displayLocalAxis=False )
        print( LegTwistRigRet )
        LegTwistBindJoints = LegTwistRigRet[3]; print( LegTwistBindJoints )
        LegTwistCtrlsALL = LegTwistRigRet[4]; print( LegTwistCtrlsALL )
        LegBindJoints = [ AnkleJoint, BallJoint ] + LegTwistBindJoints
        LegCtrlsALL += LegTwistCtrlsALL        
    
    if twistType == 'ribbon':
        LegRibbonRigRet = den_makeRibbons( side=side, prefix=prefix, radius=radius, Joints=['Hip','Knee','Ankle'], ctrlPos=(-10,0,-10), ctrlUpVec=(0,0,-1), displayLocalAxis=False )
        print( LegRibbonRigRet )
        LegRibbonBindJoints = LegRibbonRigRet[3]; print( LegRibbonBindJoints )
        LegRibbonCtrlsALL = LegRibbonRigRet[4]; print( LegRibbonCtrlsALL )
        LegBindJoints = [ AnkleJoint, BallJoint ] + LegRibbonBindJoints
        LegCtrlsALL += LegRibbonCtrlsALL
        
    
    # Flip the right side leg back where it belongs
    if side == 'R_':
        cmds.setAttr( LegRigGrp+'.scaleX', -1 )
        cmds.setAttr( side+prefix+name+'Piv_Grp.scaleX', -1 )
    
    # Return theZZ top level root group node, SpaceINs, SpaceOUTs, BindJoints, CtrlsALL, GutsALL lists in order
    return LegRigGrp, LegSpaceINs, LegSpaceOUTs, LegBindJoints, LegCtrlsALL, LegGutsALL


# ---------------------------------------------------------------------------------------

# ===============================================================================================
#
#  make fingers and twists
#
# ===============================================================================================

# ---------------------------------------------------------------------------------------
# Create Hand Pivots

def jly_makeBipedHandPivs2( side='L_', prefix='', name='Hand', radius=1.0, dpTime = 0.01 ):
    
    # - Create hand pivots to match the character
    # Create a root arm pivot group to hold all arm pivots
    HandPivGrp = denUt.den_makeGrp( nodeName=side+prefix+name+'Piv_Grp' )
    # Capture fingers in a list
    fingList = [side+prefix+'Thumb',side+prefix+'Index',side+prefix+'Middle',side+prefix+'Ring',side+prefix+'Pinky']
    
    # Build and set a good starting position for the hand pivots
    for i,fing in enumerate(fingList):
        # If the finger is not the thumb
        if fing!=side+prefix+'Thumb':
            # Create a pivot locator 00 for the finger's base
            denUt.den_makeLoc( nodeName=fing+'00_Piv', pos=(50, 100, -i*5+10), rot=(0,0,0), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
            # Color the pivot
            denUt.den_ColorShape(17)
            # Parent the pivot under HandPivGrp
            cmds.parent( fing+'00_Piv', HandPivGrp )
            
            denUt.den_makeLoc( nodeName=fing+'01_Piv', pos=(10, 0, 0), rot=(0,0,0), radius=2*radius ); denUt.den_DiagPause( seconds=dpTime )
            # Color the pivot
            denUt.den_ColorShape(20)
            cmds.parent( fing+'01_Piv', fing+'00_Piv', relative=True )
            # Parent the pivot under HandPivGrp
            cmds.parent( fing+'01_Piv', HandPivGrp, relative=False )
        else:
            denUt.den_makeLoc( nodeName=fing+'01_Piv', pos=(55, 100, -i*5+10), rot=(60,-45,-15), radius=2*radius ); denUt.den_DiagPause( seconds=dpTime )
            # Color the pivot
            denUt.den_ColorShape(20)
            # Parent the pivot under HandPivGrp
            cmds.parent( fing+'01_Piv', HandPivGrp )
        
        denUt.den_makeLoc( nodeName=fing+'Up_Piv', pos=(0, -5, 0), rot=(0,0,0), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
        # Color the pivot
        denUt.den_ColorShape(23)
        # Parent the pivot under 01_Piv for orientation
        cmds.parent( fing+'Up_Piv', fing+'01_Piv', relative=True )
        # Parent the pivot under HandPivGrp
        cmds.parent( fing+'Up_Piv', HandPivGrp, relative=False )
        
        denUt.den_makeLoc( nodeName=fing+'02_Piv', pos=(5, 0, 0), rot=(0,0,-10), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
        # Color the pivot
        denUt.den_ColorShape(21)
        # Parent the pivot under 01_Piv for orientation
        cmds.parent( fing+'02_Piv', fing+'01_Piv', relative=True )
        # Parent the pivot under HandPivGrp
        cmds.parent( fing+'02_Piv', HandPivGrp, relative=False )
        
        denUt.den_makeLoc( nodeName=fing+'03_Piv', pos=(5, 0, 0), rot=(0,0,-10), radius=radius ); denUt.den_DiagPause( seconds=dpTime )
        # Color the pivot
        denUt.den_ColorShape(25)
        # Parent the pivot under 02_Piv for orientation
        cmds.parent( fing+'03_Piv', fing+'02_Piv', relative=True )
        # Parent the pivot under HandPivGrp
        cmds.parent( fing+'03_Piv', HandPivGrp, relative=False )
        
        denUt.den_makeLoc( nodeName=fing+'End_Piv', pos=(5, 0, 0), rot=(0,0,0), radius=0.5*radius ); denUt.den_DiagPause( seconds=dpTime )
        # Color the pivot
        denUt.den_ColorShape(26)
        # Parent the pivot under 03_Piv for orientation
        cmds.parent( fing+'End_Piv', fing+'03_Piv', relative=True )
        # Parent the pivot under HandPivGrp
        cmds.parent( fing+'End_Piv', HandPivGrp, relative=False )
        
        # - Constrain pivot locators to provide orientation for the hand
        # Aim constraint for the first joint pivot of fingers which is not a thumb, to deal with extra joint
        if fing!=side+prefix+'Thumb':
            cmds.aimConstraint( fing+'01_Piv',fing+'00_Piv', worldUpType='object', worldUpObject=fing+'Up_Piv', upVector=(0,1,0) )
        # Aim constraints for other pivots
        cmds.aimConstraint( fing+'02_Piv',fing+'01_Piv', worldUpType='object', worldUpObject=fing+'Up_Piv', upVector=(0,1,0) )
        cmds.aimConstraint( fing+'03_Piv',fing+'02_Piv', worldUpType='object', worldUpObject=fing+'Up_Piv', upVector=(0,1,0) )
        cmds.aimConstraint( fing+'End_Piv',fing+'03_Piv', worldUpType='object', worldUpObject=fing+'Up_Piv', upVector=(0,1,0) )
        # Orient constraints piv03 to end pivot
        cmds.orientConstraint( fing+'03_Piv', fing+'End_Piv', mo=False )
        
        # List all pivots associated with the current finger
        pivs = cmds.ls( fing+'*_Piv' )
        # Lock all attributes except translate and visibility
        for piv in pivs:
            cmds.select( piv )
            denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 0 )
    
    # Clear selecttion, avoid accident
    cmds.select(clear=True)
    # DP refresh
    denUt.den_DiagPause( seconds=dpTime )
    
    # If making right hand, mirror all pivots
    if side == 'R_':
        cmds.setAttr( HandPivGrp+'.scaleX', -1 )
    
    print( 'den_makeHandPivs -- done\n' )
    
    return HandPivGrp


# ---------------------------------------------------------------------------------------
# Create Hand Rig

def jly_makeBipedHandRig2( side='L_', prefix='', name='Hand', radius=1.0, displayLocalAxis=False, dpTime = 0.01 ):
    
    # Initialize color for the left side
    sideColor = 6
    # If doing the right side
    if side == 'R_':
        # Set pivot group scaleX to 1, flip the pivot group to the left for good mirroring
        cmds.setAttr( side+prefix+name+'Piv_Grp.scaleX', 1 )
        # and change color
        sideColor = 13
    
    # Create 5 variables to store components of the hand rig (SpaceINs, SpaceOUTs, BindJoints, Controls, and Guts)
    HandSpaceINs = []
    HandSpaceOUTs = []
    HandBindJoints = []
    HandCtrlsALL = []
    HandGutsALL = []
    
    # Capture fingers in a list
    fingList = [side+prefix+'Thumb',side+prefix+'Index',side+prefix+'Middle',side+prefix+'Ring',side+prefix+'Pinky']
    # Create the top level root group for the hand rig
    HandRigGrp = denUt.den_makeGrp( nodeName=side+prefix+name+'_Grp' )
    
    # Create hand SpaceIN groups, and parent under HandRigGrp
    WristSpaceIN = denUt.den_makeGrp( nodeName=side+prefix+'Wrist_SpaceIN' )
    WristSpaceIN = cmds.parent( WristSpaceIN, HandRigGrp )
    # Add WristSpaceIN to the SpaceIN list
    HandSpaceINs += WristSpaceIN
    
    # Create hand SpaceIN groups, and parent under HandRigGrp
    HandSkelGrp = denUt.den_makeGrp( nodeName=side+prefix+name+'Skel_Grp' )
    HandSkelGrp = cmds.parent( HandSkelGrp, WristSpaceIN )
    HandCtrlGrp = denUt.den_makeGrp( nodeName=side+prefix+name+'Ctrl_Grp' )
    HandCtrlGrp = cmds.parent( HandCtrlGrp, WristSpaceIN )
    
    # Loop through each fingers
    for fing in fingList:
        if fing == side+prefix+'Thumb':
            # If is thumb, dont create the palm/metacarpal joint, and set parent as the root group
            fingSkelParent = HandSkelGrp
            fingCtrlParent = HandCtrlGrp
        else:
            # - Create the palm joints for fingers that is not a thumb
            # Query pivot 00 for their worldspace positions
            fing00Pos = cmds.xform( fing+'00_Piv', ws=True, q=True, t=True )
            # Clear selection
            cmds.select( clear=True )
            # Create 00 joint at the correct postion
            fing00Joint = cmds.joint( n=fing+'00_Jnt', radius=radius )
            
            # If displayLocalAxis=True, show all local axis for the joints
            if( displayLocalAxis ):
                cmds.setAttr( fing00Joint+'.displayLocalAxis', 1 )
            
            # - Orient the joint
            # Parent 00 joint under 00 pivot temporarily
            fing00Joint = cmds.parent( fing00Joint, fing+'00_Piv', relative=True )
            # Orient the joint to the pivot
            cmds.joint( fing00Joint, e=True, oj='none', zso=True )
            # Put the joint back under HandSkelGrp
            fing00Joint = cmds.parent( fing00Joint, HandSkelGrp )[0]
            
            # - Create the controls and 0 nulls
            # Create finger FK control (spike)
            fing00Ctrl = denUt.den_MakeSpike( nodeName=fing+'00_Ctrl', radius=3*radius, axis='-Y' )
            # Color the control
            denUt.den_ColorShapeRGB(rgb=(1,0,1))
            # Unlock control attributes before re-parent
            denUt.den_UnLockAttr(True,True,True,True)
            # Parent the control under fing00Joint
            fing00Ctrl = cmds.parent( fing00Ctrl, fing00Joint, relative=True )
            # Parent the control under HandCtrlGrp
            fing00Ctrl = cmds.parent( fing00Ctrl, HandCtrlGrp )
            # Add 0 null
            fing00Ctrl = denUt.den_AddZeroNull()
            # Lock all attribute except rotate and visibility
            denUt.den_LockAttr(True,False,True,False)
            # Connect control 00 Rotate to joint 00
            cmds.connectAttr( fing00Ctrl[0]+'.rotate', fing00Joint+'.rotate' )
            # Update finger skeleton and control parent
            fingSkelParent = fing00Joint
            fingCtrlParent = fing00Ctrl
            
        # Query the rest of the pivot for their worldspace positions
        fing01Pos = cmds.xform( fing+'01_Piv', ws=True, q=True, t=True )
        fing02Pos = cmds.xform( fing+'02_Piv', ws=True, q=True, t=True )
        fing03Pos = cmds.xform( fing+'03_Piv', ws=True, q=True, t=True )
        fingEndPos = cmds.xform( fing+'End_Piv', ws=True, q=True, t=True )
        
        # Create finger joint 01 at the correct postion
        cmds.select( clear=True )
        fing01Joint = cmds.joint( n=fing+'01_Jnt', radius=radius ); denUt.den_DiagPause( seconds=dpTime )
        # Parent 01 joint under 01 pivot temporarily
        fing01Joint = cmds.parent( fing01Joint, fing+'01_Piv', relative=True )
        # Orient the joint to the pivot
        cmds.joint( fing01Joint, e=True, oj='none', zso=True ); denUt.den_DiagPause( seconds=dpTime )
        # Put the joint back under fingSkelParent
        fing01Joint = cmds.parent( fing01Joint, fingSkelParent )[0]
        
        # Create finger joint 02 at the correct postion
        cmds.select( clear=True )
        fing02Joint = cmds.joint( n=fing+'02_Jnt', radius=radius ); denUt.den_DiagPause( seconds=dpTime )
        # Parent 02 joint under 02 pivot temporarily
        fing02Joint = cmds.parent( fing02Joint, fing+'02_Piv', relative=True )
        # Orient the joint to the pivot
        cmds.joint( fing02Joint, e=True, oj='none', zso=True ); denUt.den_DiagPause( seconds=dpTime )
        # Put the joint back under fing01Joint
        fing02Joint = cmds.parent( fing02Joint, fing01Joint )[0]
        
        # Create finger joint 03 at the correct postion
        cmds.select( clear=True )
        fing03Joint = cmds.joint( n=fing+'03_Jnt', radius=radius ); denUt.den_DiagPause( seconds=dpTime )
        # Parent 03 joint under 03 pivot temporarily
        fing03Joint = cmds.parent( fing03Joint, fing+'03_Piv', relative=True )
        # Orient the joint to the pivot
        cmds.joint( fing03Joint, e=True, oj='none', zso=True ); denUt.den_DiagPause( seconds=dpTime )
        # Put the joint back under fing02Joint
        fing03Joint = cmds.parent( fing03Joint, fing02Joint )[0]
        
        # Create finger joint End at the correct postion
        cmds.select( clear=True )
        fingEndJoint = cmds.joint( n=fing+'_end', radius=radius*0.5 ); denUt.den_DiagPause( seconds=dpTime )
        # Parent End joint under End pivot temporarily
        fingEndJoint = cmds.parent( fingEndJoint, fing+'End_Piv', relative=True )
        # Orient the joint to the pivot
        cmds.joint( fing02Joint, e=True, oj='none', zso=True ); denUt.den_DiagPause( seconds=dpTime )
        # Put the joint back under fing03Joint
        fingEndJoint = cmds.parent( fingEndJoint, fing03Joint )[0]
        
        # If displayLocalAxis=True, show all local axis for the joints
        if( displayLocalAxis ):
            cmds.setAttr( fing01Joint+'.displayLocalAxis', 1 )
            cmds.setAttr( fing02Joint+'.displayLocalAxis', 1 )
            cmds.setAttr( fing03Joint+'.displayLocalAxis', 1 )
            cmds.setAttr( fingEndJoint+'.displayLocalAxis', 1 )
        
        
        # - Create the controls and 0 nulls
        # Create finger FK control (spike) for fing01
        fing01Ctrl = denUt.den_MakeSpike( nodeName=fing+'01_Ctrl', radius=3*radius, axis='-Y' )
        # Color the control
        denUt.den_ColorShapeRGB(rgb=(1,0,1))
        # Unlock control attributes before re-parent
        denUt.den_UnLockAttr(True,True,True,True)
        # Parent the control under fing01Joint
        fing01Ctrl = cmds.parent( fing01Ctrl, fing01Joint, relative=True )
        # Parent the control under fingCtrlParent
        fing01Ctrl = cmds.parent( fing01Ctrl, fingCtrlParent )
        # Add 0 null
        fing01Ctrl = denUt.den_AddZeroNull()
        # Lock all attribute except rotate and visibility
        denUt.den_LockAttr(True,False,True,False)
        # DP refresh
        denUt.den_DiagPause( seconds=dpTime )
        
        # Create finger FK control (spike) for fing02
        fing02Ctrl = denUt.den_MakeSpike( nodeName=fing+'02_Ctrl', radius=3*radius, axis='-Y' )
        # Color the control
        denUt.den_ColorShapeRGB(rgb=(1,0,1))
        # Unlock control attributes before re-parent
        denUt.den_UnLockAttr(True,True,True,True)
        # Parent the control under fing02Joint
        fing02Ctrl = cmds.parent( fing02Ctrl, fing02Joint, relative=True )
        # Parent the control under fing01Ctrl
        fing02Ctrl = cmds.parent( fing02Ctrl, fing01Ctrl )
        # Add 0 null
        fing02Ctrl = denUt.den_AddZeroNull()
        # Lock all attribute except rotate and visibility
        denUt.den_LockAttr(True,False,True,False)
        # DP refresh
        denUt.den_DiagPause( seconds=dpTime )
        
        # Create finger FK control (spike) for fing03
        fing03Ctrl = denUt.den_MakeSpike( nodeName=fing+'03_Ctrl', radius=3*radius, axis='-Y' )
        # Color the control
        denUt.den_ColorShapeRGB(rgb=(1,0,1))
        # Unlock control attributes before re-parent
        denUt.den_UnLockAttr(True,True,True,True)
        # Parent the control under fing03Joint
        fing03Ctrl = cmds.parent( fing03Ctrl, fing03Joint, relative=True )
        # Parent the control under fing02Ctrl
        fing03Ctrl = cmds.parent( fing03Ctrl, fing02Ctrl )
        # Add 0 null
        fing03Ctrl = denUt.den_AddZeroNull()
        # Lock all attribute except rotate and visibility
        denUt.den_LockAttr(True,False,True,False)
        # DP refresh
        denUt.den_DiagPause( seconds=dpTime )
        
        # Connect control Rotate attribute to the joint
        cmds.connectAttr( fing01Ctrl[0]+'.rotate', fing01Joint+'.rotate' )
        cmds.connectAttr( fing02Ctrl[0]+'.rotate', fing02Joint+'.rotate' )
        cmds.connectAttr( fing03Ctrl[0]+'.rotate', fing03Joint+'.rotate' )
        
        # Add all joints in a list for binding
        # Deal with the thumb
        if fing==side+prefix+'Thumb':
            HandBindJoints += [ fing01Joint, fing02Joint, fing03Joint ]
            HandCtrlsALL += [ fing01Ctrl[0], fing02Ctrl[0], fing03Ctrl[0] ]
        else:
            # Add extra palm joint (fing00) for other fingers 
            HandBindJoints += [ fing00Joint, fing01Joint, fing02Joint, fing03Joint ]
            HandCtrlsALL += [ fing00Ctrl[0], fing01Ctrl[0], fing02Ctrl[0], fing03Ctrl[0] ]
    
    # Flip the right side hand back where it belongs
    if side == 'R_':
        cmds.setAttr( HandRigGrp+'.scaleX', -1 )
        cmds.setAttr( side+prefix+name+'Piv_Grp.scaleX', -1 )
    
    # Return the top level group node, SpaceINs, SpaceOUTs, BindJoints, CtrlsALL, GutsALL lists in order
    return HandRigGrp, HandSpaceINs, HandSpaceOUTs, HandBindJoints, HandCtrlsALL, HandGutsALL


# ---------------------------------------------------------------------------------------
# Create Twist

def jly_makeTwists( side='L_', prefix='', name='Arm', radius=2.0, Joints=['Shld','Elbow','Wrist'], ctrlPos=(-10,0,-10), ctrlUpVec=(0,0,-1), displayLocalAxis=True, dpTime = 0.01 ):
    
    # Initialize color for the left side
    sideColor = 6
    # If doing the right side, change color
    if side == 'R_':
        sideColor = 13
    
    # Assign prefix for twist group
    TwistRigGrp = ''
    
    # Create 5 variables to store components of the arm rig (SpaceINs, SpaceOUTs, BindJoints, Controls, and Guts)
    TwistSpaceINs = []
    TwistSpaceOUTs = []
    TwistBindJoints = []
    TwistCtrlsALL = []
    TwistGutsALL = []
    
    # Create joint names based on input
    FirstName = side+prefix+Joints[0]
    SecondName = side+prefix+Joints[1]
    ThirdName = side+prefix+Joints[2]
    
    # Find first joint, its parent, and the 2nd(elbow) and 3rd joint(wrist)
    FirstJoint = cmds.ls( FirstName+'_Jnt' )[0]
    FirstParent = cmds.listRelatives( FirstJoint, parent=True, fullPath=True )[0]
    SecondJoint = cmds.ls( SecondName+'_Jnt' )[0]
    ThirdJoint = cmds.ls( ThirdName+'_Jnt' )[0]
    
    # Print warning, should not have existing arm rig with saftycover
    print( '\nden_makeTwists -- WARNING -- Twist does not build a separate rig part, but modifies the existing limb.' )
    print( '                             If it fails, you will likely need to bebuild the limb before trying again.' )
    
    # Sets the INs to be its joint
    FirstIN = FirstJoint
    SecondIN = SecondJoint
    ThirdIN = ThirdJoint
    
    # Create the twist 01 joints for the first joints for the shoulder
    FirstTwist01Joint = cmds.joint( n=FirstName+'Twist01_Jnt', radius=radius )
    # Parent under FirstIN (shoulder)
    FirstTwist01Joint = cmds.parent( FirstTwist01Joint, FirstIN, relative=True )[0]
    # Parent back to where the joint belongs
    FirstTwist01Joint = cmds.parent( FirstTwist01Joint, FirstParent )[0]
    # Create the twist 02 joints for the shoulder
    FirstTwist02Joint = cmds.joint( n=FirstName+'Twist02_Jnt', radius=radius )
    FirstTwist02Joint = cmds.parent( FirstTwist02Joint, FirstIN, relative=True )[0]
    # Create the twist 03 joints for the shoulder
    FirstTwist03Joint = cmds.joint( n=FirstName+'Twist03_Jnt', radius=radius )
    FirstTwist03Joint = cmds.parent( FirstTwist03Joint, FirstIN, relative=True )[0]
    
    # Create the twist 01 joints for the first joints for the elbow
    SecondTwist01Joint = cmds.joint( n=SecondName+'Twist01_Jnt', radius=radius )
    SecondTwist01Joint = cmds.parent( SecondTwist01Joint, SecondIN, relative=True )[0]
    SecondTwist01Joint = cmds.parent( SecondTwist01Joint, FirstIN )[0]
    # Create the twist 02 joints for the elbow
    SecondTwist02Joint = cmds.joint( n=SecondName+'Twist02_Jnt', radius=radius )
    SecondTwist02Joint = cmds.parent( SecondTwist02Joint, SecondIN, relative=True )[0]
    # Create the twist 03 joints for the elbow
    SecondTwist03Joint = cmds.joint( n=SecondName+'Twist03_Jnt', radius=radius )
    SecondTwist03Joint = cmds.parent( SecondTwist03Joint, SecondIN, relative=True )[0]
    
    # Duplicate joints for rest and up pose
    # Rest joint store the orient when the shoulder in its rest position
    FirstRestJoint = cmds.duplicate( FirstTwist01Joint, n=FirstName+'Rest_Jx' )[0]
    # Upcar hold the up for the shoulder, to keep it out of the way of the elbow
    FirstUpCarJoint = cmds.duplicate( FirstRestJoint, n=FirstName+'UpCar_Jx' )[0]
    # Make a pole control for upCtrl
    FirstTwist01UpCtrl = denUt.den_MakePole( nodeName=FirstName+'Twist01Up_Ctrl' )
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Position the control
    cmds.xform( t=ctrlPos, relative=True, ws=True )
    # Parent the control under FirstUpCarJoint
    FirstTwist01UpCtrl = cmds.parent( FirstTwist01UpCtrl, FirstUpCarJoint, relative=True )[0]
    # Add zero null
    FirstTwist01UpCtrl = denUt.den_AddZeroNull()
    # Find the zero null and hold it in a variable
    FirstTwist01UpCtrlZero = cmds.listRelatives( FirstTwist01UpCtrl, parent=True, fullPath=True )[0]
    
    # If displayLocalAxis=True, show all local axis for the joints
    if ( displayLocalAxis ):
        cmds.setAttr( FirstTwist01Joint+'.displayLocalAxis', 1 )
        cmds.setAttr( FirstTwist02Joint+'.displayLocalAxis', 1 )
        cmds.setAttr( FirstTwist03Joint+'.displayLocalAxis', 1 )
        cmds.setAttr( SecondTwist01Joint+'.displayLocalAxis', 1 )
        cmds.setAttr( SecondTwist02Joint+'.displayLocalAxis', 1 )
        cmds.setAttr( SecondTwist03Joint+'.displayLocalAxis', 1 )
    
    # - Create Constraints - 
    
    # den - set up a carrier for the shoulder up that stays mostly out of the way, rotates in y only
    # Create an orient constraint for the FirstUpCarJoint to follow the rotation of FirstIN and FirstRestJoint, result is stored in FirstUpCarJointOriCon
    FirstUpCarJointOriCon = cmds.orientConstraint( FirstIN, FirstRestJoint, FirstUpCarJoint )[0]
    # Set the interpolation type of the orient constraint to 2 (shortest)
    cmds.setAttr( FirstUpCarJointOriCon+'.interpType', 2 )
    # Disconnect the X rotation of the constraint from the FirstUpCarJoint to prevent it from rotating in that axis
    cmds.disconnectAttr( FirstUpCarJointOriCon+'.constraintRotateX', FirstUpCarJoint+'.rotateX' )
    # Disconnect the Z rotation of the constraint similarly to keep the rotation in the Y axis only
    cmds.disconnectAttr( FirstUpCarJointOriCon+'.constraintRotateZ', FirstUpCarJoint+'.rotateZ' )
    # den - set up the First Twist01 so it does not twist with the Second
    # Create an aim constraint for FirstTwist01Joint to aim at SecondIN using a specified up vector, maintaining no offset and using an object as the world up direction
    cmds.aimConstraint( SecondIN, FirstTwist01Joint, upVector=ctrlUpVec, maintainOffset=False, worldUpType='object', worldUpObject=FirstTwist01UpCtrl[0] )
    # den - connect Second twist03 rotateX to the Third rotateX
    # Connect the rotateX attribute of ThirdIN to the rotateX attribute of SecondTwist03Joint to synchronize their rotations.
    cmds.connectAttr( ThirdIN+'.rotateX', SecondTwist03Joint+'.rotateX' )
    # den -  set up First twist02 so it splits the difference between First twist01 and First twist03
    # Create a unit conversion node for FirstTwist02 and name it according to FirstName
    FirstTwist02t_unitConversion = cmds.shadingNode( 'unitConversion', asUtility=True, n=FirstName+'Twist02t_unitConversion' )
    # Create another unit conversion node for FirstTwist03 with a similar naming convention
    FirstTwist03t_unitConversion = cmds.shadingNode( 'unitConversion', asUtility=True, n=FirstName+'Twist03t_unitConversion' )
    # Set the conversion factor for FirstTwist02's unit conversion to 0.33
    cmds.setAttr( FirstTwist02t_unitConversion+'.conversionFactor', 0.33 )
    # Set the conversion factor for FirstTwist03's unit conversion to 0.66
    cmds.setAttr( FirstTwist03t_unitConversion+'.conversionFactor', 0.66 )
    # Connect the translate attribute of SecondIN to the input of the FirstTwist02 unit conversion node
    cmds.connectAttr( SecondIN+'.translate', FirstTwist02t_unitConversion+'.input' )
    # Connect the output of the FirstTwist02 unit conversion node to the translate attribute of FirstTwist02Joint
    cmds.connectAttr( FirstTwist02t_unitConversion+'.output', FirstTwist02Joint+'.translate' )
    # Connect the translate attribute of SecondIN to the input of the FirstTwist03 unit conversion node.
    cmds.connectAttr( SecondIN+'.translate', FirstTwist03t_unitConversion+'.input' )
    # Connect the output of the FirstTwist03 unit conversion node to the translate attribute of FirstTwist03Joint
    cmds.connectAttr( FirstTwist03t_unitConversion+'.output', FirstTwist03Joint+'.translate' )
    # Create an orient constraint for FirstTwist02Joint to interpolate its orientation between FirstTwist01Joint and FirstTwist03Joint
    FirstTwist02OriCon = cmds.orientConstraint( FirstTwist01Joint, FirstTwist03Joint, FirstTwist02Joint )
    # Set the interpolation type of the FirstTwist02 orient constraint to 2
    cmds.setAttr( FirstTwist02OriCon[0]+'.interpType', 2 )
    # den - set up First twist02 so it splits the difference between First twist01 and First twist03
    # Create a unit conversion node for SecondTwist02 and name it based on SecondName
    SecondTwist02t_unitConversion = cmds.shadingNode( 'unitConversion', asUtility=True, n=SecondName+'Twist02t_unitConversion' )
    # Create another unit conversion node for SecondTwist03 with a similar naming convention
    SecondTwist03t_unitConversion = cmds.shadingNode( 'unitConversion', asUtility=True, n=SecondName+'Twist03t_unitConversion' )
    # Set the conversion factor for SecondTwist02's unit conversion to 0.33
    cmds.setAttr( SecondTwist02t_unitConversion+'.conversionFactor', 0.33 )
    # Set the conversion factor for SecondTwist03's unit conversion to 0.66
    cmds.setAttr( SecondTwist03t_unitConversion+'.conversionFactor', 0.66 )
    # Connect the translate attribute of ThirdIN to the input of the SecondTwist02 unit conversion node
    cmds.connectAttr( ThirdIN+'.translate', SecondTwist02t_unitConversion+'.input' )
    # Connect the output of the SecondTwist02 unit conversion node to the translate attribute of SecondTwist02Joint
    cmds.connectAttr( SecondTwist02t_unitConversion+'.output', SecondTwist02Joint+'.translate' )
    # Connect the translate attribute of ThirdIN to the input of the SecondTwist03 unit conversion node
    cmds.connectAttr( ThirdIN+'.translate', SecondTwist03t_unitConversion+'.input' )
    # Connect the output of the SecondTwist03 unit conversion node to the translate attribute of SecondTwist03Joint
    cmds.connectAttr( SecondTwist03t_unitConversion+'.output', SecondTwist03Joint+'.translate' )
    # Connect the rotate attribute of SecondIN to the rotate attribute of SecondTwist01Joint to synchronize their rotations
    cmds.connectAttr( SecondIN+'.rotate', SecondTwist01Joint+'.rotate' )
    # Create an orient constraint for SecondTwist02Joint to interpolate its orientation between SecondTwist01Joint and SecondTwist03Joint
    SecondTwist02OriCon = cmds.orientConstraint( SecondTwist01Joint, SecondTwist03Joint, SecondTwist02Joint )
    # Set the interpolation type of the SecondTwist02 orient constraint to 2
    cmds.setAttr( SecondTwist02OriCon[0]+'.interpType', 2 )
    
    
    # - Rename all bind joints and hide proxy geo which are no longer needed
    # Create a new name for the first bind joint by replacing 'Jnt' with 'Jx'
    NewFirstJointName = FirstJoint.replace('Jnt','Jx')
    # List the objects matching FirstJoint to handle them
    FirstBindJoint = cmds.ls( FirstJoint )
    if FirstBindJoint != []:
        # Rename the found bind joint to the new name if it exists
        FirstBindJoint = cmds.rename( FirstBindJoint, NewFirstJointName )
        print( 'den_makeTwists ---------', FirstBindJoint, 'renamed to', NewFirstJointName )
    # List the proxy mesh associated with FirstJoint, typically constructed from its name
    FirstProxy = cmds.ls( denUt.den_SplitAt(FirstJoint,'_',2)[0]+'_Mesh' )
    if FirstProxy != []:
        # Set the visibility of the proxy mesh to 0 (hide it) if it exists
        cmds.setAttr( FirstProxy[0]+'.visibility', 0 )
        print( 'den_makeTwists ---------', FirstProxy[0], 'visibility set to 0' )
    
    # Create a new name for the second bind joint by replacing 'Jnt' with 'Jx'
    NewSecondJointName = SecondJoint.replace('Jnt','Jx')
    # List the objects matching SecondJoint to handle them
    SecondBindJoint = cmds.ls( SecondJoint )
    if SecondBindJoint != []:
        # Rename the found bind joint to the new name if it exists
        SecondBindJoint = cmds.rename( SecondBindJoint, NewSecondJointName )
        print( 'den_makeTwists ---------', SecondBindJoint, 'renamed to', NewSecondJointName )
    # List the proxy mesh associated with SecondJoint, constructed from its name
    SecondProxy = cmds.ls( denUt.den_SplitAt(SecondJoint,'_',2)[0]+'_Mesh' )
    if SecondProxy != []:
        # Set the visibility of the proxy mesh to 0 (hide it) if it exists
        cmds.setAttr( SecondProxy[0]+'.visibility', 0 )
        print( 'den_makeTwists ---------', SecondProxy[0], 'visibility set to 0' )
    
    # Add the twist joints and controls to a list for later use
    TwistBindJoints += [ FirstTwist01Joint, FirstTwist02Joint, FirstTwist03Joint, SecondTwist01Joint, SecondTwist02Joint, SecondTwist03Joint ]
    TwistCtrlsALL += FirstTwist01UpCtrl
    
    
    # Return the top level group node, SpaceINs, SpaceOUTs, BindJoints, CtrlsALL, GutsALL lists in order
    return TwistRigGrp, TwistSpaceINs, TwistSpaceOUTs, TwistBindJoints, TwistCtrlsALL, TwistGutsALL


# ---------------------------------------------------------------------------------------
# Create Angle Splitter

def jly_makeAngleSplitter( name='L_Seat02', firstJnt='L_HipRest_Jx', secondJnt='L_HipTwist01_Jnt', radius=1.0 ):
    
    # Find the 1st joint
    firstJnt = cmds.ls( firstJnt )
    # Find the first joint's parent
    firstJntParent = cmds.listRelatives( firstJnt, parent=True )
    # Find the second joint
    secondJnt = cmds.ls( secondJnt )
    print(firstJnt)
    print(firstJntParent)
    print(secondJnt)
    
    # Create a locator to use to split the different between the 2 joints
    SplitLoc = denUt.den_makeLoc( nodeName=name+'_Loc', radius=radius )
    # Create a split joint at the location
    SplitJnt = cmds.joint( name=name+'_Jnt', radius=radius )
    
    cmds.select( SplitLoc, SplitJnt )
    # Lock all attribute except translate and rotate
    denUt.den_Lock(  0,0,0 , 0,0,0 , 1,1,1 , 1 )
    
    # Set the split joint translate value to be 'radius', so joint dont overlap
    cmds.setAttr( SplitJnt+'.t', 0, radius, 0 )
    # Parent the SplitLoc to firstJnt
    SplitLoc = cmds.parent( SplitLoc, firstJnt, relative=True )
    # Parent SplitLoc back under the firstJntParent
    SplitLoc = cmds.parent( SplitLoc, firstJntParent, relative=False )
    # Orient constraint the SplitLoc to firstJnt and secondJnt
    cmds.orientConstraint( firstJnt, secondJnt, SplitLoc )
    cmds.select( SplitLoc, SplitJnt )
    # Lock all attributes
    denUt.den_Lock(  1,1,1 , 1,1,1 , 1,1,1 , 1 )
    cmds.select( clear=True )
    
    return SplitJnt

# ---------------------------------------------------------------------------------------
# Create Half Muscle Pivots

def jly_makeHalfMusclePivs( side='L_', prefix='', name='Foo', radius=1.0, dpTime=0.01 ):
    # Create a pivot group
    MusclePivGrp = denUt.den_makeGrp( nodeName=side+prefix+name+'Piv_Grp', pos=(0,0,0) )
    # Lock all attributes except X scale and visibility
    denUt.den_Lock(  1,1,1 , 1,1,1 , 0,1,1 , 0 )
    # Create a pivot for the root of the half muscle
    RootPiv = denUt.den_makeLoc( nodeName=side+prefix+name+'Root_Piv', pos=(2*radius, 0, 2*radius), radius=radius )
    # Color the pivot
    denUt.den_ColorShape(20); denUt.den_DiagPause( seconds=dpTime )
    # Create a pivot for the root-up of the half muscle
    RootUpPiv = denUt.den_makeLoc( nodeName=side+prefix+name+'RootUp_Piv', pos=(2*radius, 2*radius, 2*radius), radius=0.5*radius )
    # Color the pivot
    denUt.den_ColorShape(23); denUt.den_DiagPause( seconds=dpTime )
    # Create a pivot for the tip of the half muscle
    TipPiv = denUt.den_makeLoc( nodeName=side+prefix+name+'Tip_Piv', pos=(6*radius, 0, 6*radius), radius=radius )
    # Color the pivot
    denUt.den_ColorShape(20); denUt.den_DiagPause( seconds=dpTime )
    
    # Aim the root at the tip
    cmds.aimConstraint( TipPiv,RootPiv, maintainOffset=False, worldUpType='object', worldUpObject=RootUpPiv[0] )
    # Orient the tip to the root
    cmds.orientConstraint( RootPiv,TipPiv, maintainOffset=False )
    
    # Lock the attributes except translate, to prevent pivots moving
    cmds.select( RootPiv ); denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    cmds.select( RootUpPiv ); denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    cmds.select( TipPiv ); denUt.den_Lock(  0,0,0 , 1,1,1 , 1,1,1 , 1 )
    # Parent the pivots under root MusclePivGrp
    cmds.parent( RootPiv,RootUpPiv,TipPiv,MusclePivGrp )
    # DP refresh
    denUt.den_DiagPause( seconds=dpTime )
    
    # If doing right side, flip the right side back where it belongs
    if side == 'R_':
        cmds.setAttr( MusclePivGrp+'.scaleX', -1 )
    
    return MusclePivGrp


# ---------------------------------------------------------------------------------------
# Create Half Muscle Rig

def jly_makeHalfMuscleRig( side='L_', prefix='', name='foo', radius=1.0, dpTime=0.01 ):
    
    # Set the left side color = 6
    sideColor = 6
    # If doing the right side
    if side == 'R_':
        # Set pivot group scaleX to 1, flip the pivot group to the left for good mirroring
        cmds.setAttr( side+prefix+name+'Piv_Grp.scaleX', 1 )
        # and change color
        sideColor = 13
    # DP refresh
    denUt.den_DiagPause( seconds=0.1 )
    
    # Create a top-level group for the muscle rig
    MuscleRigGrp = denUt.den_makeGrp( nodeName=side+prefix+name+'_Grp', pos=(0,0,0) )
    
    # Create 5 variables to store components of the arm rig (SpaceINs, SpaceOUTs, BindJoints, Controls, and Guts)
    MuscleSpaceINs = []
    MuscleSpaceOUTs = []
    MuscleBindJoints = []
    MuscleCtrlsALL = []
    MuscleGutsALL = []
    
    # Create muscle root and tip SpaceIN groups, and parent under MuscleRigGrp
    RootSpaceIN = denUt.den_makeGrp( nodeName=side+prefix+name+'Root_SpaceIN', pos=(0,0,0) )
    RootSpaceIN = cmds.parent( RootSpaceIN, MuscleRigGrp )[0]
    TipSpaceIN = denUt.den_makeGrp( nodeName=side+prefix+name+'Tip_SpaceIN', pos=(0,0,0) )
    TipSpaceIN = cmds.parent( TipSpaceIN, MuscleRigGrp )[0]
    
    # Capture all the SpaceINs to a list
    MuscleSpaceINs += [ RootSpaceIN, TipSpaceIN ]
    
    # Get world position and rotation of Root and Tip pivots, capture them in variables    
    RootPos = cmds.xform( side+prefix+name+'Root_Piv', ws=True, q=True, t=True )
    RootRot = cmds.xform( side+prefix+name+'Root_Piv', ws=True, q=True, ro=True )
    TipPos = cmds.xform( side+prefix+name+'Tip_Piv', ws=True, q=True, t=True )
    TipRot = cmds.xform( side+prefix+name+'Tip_Piv', ws=True, q=True, ro=True )
    
    # Create locators for the root and tip
    RootLoc = denUt.den_makeLoc ( nodeName=side+prefix+name+'_RLoc', radius=radius )
    TipLoc = denUt.den_makeLoc ( nodeName=side+prefix+name+'_TLoc', radius=radius )
    
    cmds.select( clear=True )
    # Create joints for the muscle rig
    Joint = denUt.den_makeJoint( nodeName=side+prefix+name+'_Jnt', pos=(0,0,0), radius=radius, leaveSelected=True )
    EndJoint = denUt.den_makeJoint( nodeName=side+prefix+name+'_end', pos=(radius*10,0,0), radius=radius*0.1, leaveSelected=False )
    # Parent the joint to the RootLoc
    Joint = cmds.parent( Joint, RootLoc, relative=True )[0]
    # Add the joint to the bind joints list
    MuscleBindJoints += [ Joint ]
    # Set position and rotation of RootLoc
    cmds.xform( RootLoc, t=RootPos, ro=RootRot )
    # Set position and rotation of TipLoc
    cmds.xform( TipLoc, t=TipPos, ro=TipRot )
    # Parent RootLoc and TipLoc to their SpaceINs
    RootLoc = cmds.parent( RootLoc, RootSpaceIN, relative=True )
    TipLoc = cmds.parent( TipLoc, TipSpaceIN, relative=True )
    
    # Create vectors for the root and tip positions
    RootPosVec = om.MVector(RootPos[0],RootPos[1],RootPos[2]) 
    TipPosVec = om.MVector(TipPos[0],TipPos[1],TipPos[2])
    
    # Calculate vector from tip to root
    vecA = RootPosVec - TipPosVec
    # Get the length of the vector
    lenA = om.MVector.length(vecA)
    print( lenA )
    # Set the X translation of EndJoint to the length
    cmds.setAttr( EndJoint+'.translateX', lenA )
    # Create and set attributes for RestDistance on RootLoc
    cmds.addAttr( RootLoc[0], longName='RestDistance', attributeType='float', defaultValue=lenA )
    cmds.setAttr ( RootLoc[0]+'.RestDistance', lock=False, keyable=True )
    # Create nodes for calculating distances and matrix decompositions
    DistNode = cmds.shadingNode( 'distanceBetween', name=side+prefix+name+'_distanceBetween', asUtility=True )
    MatrixNode = cmds.shadingNode( 'decomposeMatrix', name=side+prefix+name+'_decomposeMatrix', asUtility=True )
    print( RootLoc, DistNode )
    # Connect the world matrices to the distance node
    cmds.connectAttr( RootLoc[0]+'.worldMatrix[0]', DistNode+'.inMatrix1' )
    cmds.connectAttr( TipLoc[0]+'.worldMatrix[0]', DistNode+'.inMatrix2' )
    cmds.connectAttr( RootLoc[0]+'.worldMatrix[0]', MatrixNode+'.inputMatrix' )
    # Create multiplication nodes for scaling
    DivNode = cmds.shadingNode( 'multiplyDivide', name=side+prefix+name+'_multiplyDivide', asUtility=True )
    DivNode4scale = cmds.shadingNode( 'multiplyDivide', name=side+prefix+name+'4scale_multiplyDivide', asUtility=True )
    cmds.setAttr( DivNode+'.operation', 2 )
    # Connect distance outputs to the divide node
    cmds.connectAttr( DistNode+'.distance', DivNode+'.input1X' )
    cmds.connectAttr( MatrixNode+'.outputScaleX', DivNode4scale+'.input1X' )
    cmds.connectAttr( RootLoc[0]+'.RestDistance', DivNode4scale+'.input2X' )
    cmds.connectAttr( DivNode4scale+'.outputX', DivNode+'.input2X' )
    # Connect output to joint's scaleX
    cmds.connectAttr( DivNode+'.outputX', Joint+'.scaleX' )
    # Aim the joint towards the tip location
    cmds.aimConstraint( TipLoc, Joint, worldUpType='none' )
    
    # den - needs a parented duplicate of the proxy Mesh for stretchiness to display properly
    # Get the main mesh
    Mesh = cmds.ls( side+prefix+name+'_Mesh' )
    # Duplicate the mesh for display
    DispMesh = cmds.duplicate( Mesh, name=side+prefix+name+'_DispMesh' )
    # If doing right side, flip the display mesh
    if side == 'R_':
        cmds.xform( DispMesh, s=( -1.0, 1.0, 1.0 ) )
        cmds.makeIdentity( DispMesh, apply=True, preserveNormals=True )
    # Parent the display mesh to the joint
    DispMesh = cmds.parent( DispMesh, Joint )
    # Connect visibility to a control attribute
    cmds.connectAttr( 'All_Ctrl.Show_Proxy_Geo', DispMesh[0]+'Shape.visibility' )
    # Hide the original mesh
    cmds.setAttr( Mesh[0]+'.visibility', 0 )
    
    # If doing the right side, flip the root group to the other side by giveing scaleX -1
    if side == 'R_':
        cmds.setAttr( MuscleRigGrp+'.scaleX', -1 )
        cmds.setAttr( side+prefix+name+'Piv_Grp.scaleX', -1 )
    
    # Return the top level group node, SpaceINs, SpaceOUTs, BindJoints, CtrlsALL, GutsALL lists in order
    return MuscleRigGrp, MuscleSpaceINs, MuscleSpaceOUTs, MuscleBindJoints, MuscleCtrlsALL, MuscleGutsALL


# ---------------------------------------------------------------------------------------
# Create Eye Pivots

def jly_makeEyePiv( side='L_', prefix='', radius=1.0, dpTime = 0.01 ):
    # Create a eye pivot group to hold all the pivots
    EyePivGrp = denUt.den_makeGrp( nodeName=side+prefix+'EyePiv_Grp' )
    # Create locator for eye pivot
    EyeCenterPiv = denUt.den_makeLoc( nodeName=side+prefix+'Eye_Piv', pos=(3.358,172.112,9.931), rot=(8,0,2), radius=10*radius )
    # Parent eye pivots under EyePivGrp
    cmds.parent( EyeCenterPiv, EyePivGrp )
    
    # If doing the right side, flip the root group to the other side by giveing scaleX -1
    if side == 'R_':
        cmds.setAttr( EyePivGrp+'.scaleX', -1 )
    
    return EyePivGrp


# ---------------------------------------------------------------------------------------
# Create Eye Rig

def jly_makeEyeRig( side='L_', prefix='', name='Eye', radius=1.0, ctrlRadius=6.0, displayLocalAxis=False, dpTime = 0.01 ):
    # Initialize color for the left side
    sideColor = 6
    # If doing the right side
    if side == 'R_':
        # Set pivot group scaleX to 1, flip the pivot group to the left for good mirroring
        cmds.setAttr( side+prefix+name+'Piv_Grp.scaleX', 1 )
        # and change color
        sideColor = 13
    
    # DP refresh
    denUt.den_DiagPause( seconds=dpTime )
    
    # Create the top level root group for the eye rig
    EyeRigGrp = denUt.den_makeGrp( nodeName=side+prefix+name+'Rig_Grp' )
    
    # Create 5 variables to store components of the arm rig (SpaceINs, SpaceOUTs, BindJoints, Controls, and Guts)
    EyeSpaceINs = []
    EyeSpaceOUTs = []
    EyeJoints = []
    EyeCtrlsALL = []
    EyeGutsALL = []
    
    # Create eye SpaceIN groups, and parent under EyeRigGrp
    EyeSpaceIN = denUt.den_makeGrp( nodeName=side+prefix+name+'Space_IN' )
    EyeSpaceIN = cmds.parent( EyeSpaceIN, EyeRigGrp )
    # Add EyeSpaceIN to the SpaceIN list
    EyeSpaceINs += EyeSpaceIN
    
    # Query pivots for their worldspace positions
    EyePos = cmds.xform( side+prefix+name+'_Piv', ws=True, q=True, t=True )
    EyeRot = cmds.xform( side+prefix+name+'_Piv', ws=True, q=True, ro=True )
    # Make a locator to be eye pivot
    EyeLoc = denUt.den_makeLoc( nodeName=side+prefix+name+'_Loc', pos=EyePos, rot=EyeRot, radius=radius )
    # Parent under EyeSpaceIN
    EyeLoc = cmds.parent( EyeLoc, EyeSpaceIN )
    # Create eye joint at the correct postion
    EyeJnt = cmds.joint( n=side+prefix+name+'_Jnt', radius=radius )
    # Add the joint to eye joint list
    EyeJoints += [EyeJnt]
    
    # If displayLocalAxis=True, show all local axis for the joints
    if ( displayLocalAxis ):
        cmds.setAttr( EyeJnt+'.displayLocalAxis', 1 )
    
    # - Create the controls and 0 nulls
    # Create eye FK control (spike)
    EyeCtrl = denUt.den_MakeSpike( nodeName=side+prefix+name+'_Ctrl', pos=(0,0,ctrlRadius), radius=ctrlRadius*0.3, axis='+Z' )
    # Parent the control under EyeLoc
    EyeCtrl = cmds.parent( EyeCtrl, EyeLoc, relative=True )
    # Color the control
    denUt.den_ColorShapeRGB(rgb=(1,0,1))
    # Add the control to the eye control all list
    EyeCtrlsALL += EyeCtrl
    # Connect control Rotate attribute to the joint
    cmds.connectAttr( EyeCtrl[0]+'.rotate', EyeJnt+'.rotate' )
    
    # Flip the right side eye back where it belongs
    if side == 'R_':
        cmds.setAttr( EyeRigGrp+'.scaleX', -1 )
        cmds.setAttr( side+prefix+name+'Piv_Grp.scaleX', -1 )
    
    # Return the top level group node, SpaceINs, SpaceOUTs, BindJoints, CtrlsALL, GutsALL lists in order
    return EyeRigGrp, EyeSpaceINs, EyeSpaceOUTs, EyeJoints, EyeCtrlsALL, EyeGutsALL
