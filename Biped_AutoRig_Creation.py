# ---------------------------------------------------------------------------------------
# Biped Auto-Rig Tool – Execution Script
# Developed by Arrow Lyu
#
# ---------------------------------------------------------------------------------------
# This script sets up the scene and calls the main rig-building functions for a biped.
# It is tailored for a specific character (RigSuitMan) but can be adjusted for others.
#
# The rig is based on Python modules and concepts learned from my professor Dennis Turner.
# Some module structures are quoted with permission and adapted for this use.
#
# Use this together with the definition script: Biped_AutoRig_Python_Tool.py
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
import string

import den_Utilities_v12 as denUt
importlib.reload(denUt)
print(denUt.__file__)

import Biped_AutoRig_Python_Tool as jlyBR
importlib.reload(jlyBR)
print(jlyBR.__file__)


# ---------------------------------------------------------------------------------------

# Find the path of the current project workspace. The path will be used for reading data files, such as skinClusters and ATOM animation
projDir = cmds.workspace( q=True, rootDirectory=True )
print( projDir )

# Give the rig a name
rigName = 'Suit Man'


# ---------------------------------------------------------------------------------------
# Make Root Pivot

# Create base pivot, and capture it in a list
BasePivRet = jlyBR.jly_makeBasePiv( name=rigName, radius=5.0 )
print( BasePivRet )
# Create a variable for root pivot grp
RootPivGrp = BasePivRet
# Put the root pivot in the character's center of gravity
cmds.xform( 'Cog_Piv', t=( 0.0, 100.0, 0.0 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )


# ---------------------------------------------------------------------------------------
# Make Base Rig

# Create base rig, and capture it in a list
BaseRigRet = jlyBR.jly_makeBaseRig(label=rigName,ctrlRadius=50.0)
print( BaseRigRet )
# Capture smaller rig groups in 6 variables, so the master rig group will contain them
RootRigGrp = BaseRigRet[0]; print( RootRigGrp )
BaseSpaceINs = BaseRigRet[1]; print( BaseSpaceINs )
BaseSpaceOUTs = BaseRigRet[2]; print( BaseSpaceOUTs )
BaseBindJnts = BaseRigRet[3]; print( BaseBindJnts )
BaseCtrlsALL = BaseRigRet[4]; print( BaseCtrlsALL )
BaseGutsALL = BaseRigRet[5]; print( BaseGutsALL )
# Set 2 new variables for later connecting visibility (torso, arms)
CogSpaceOUT = BaseSpaceOUTs[0]
AllSpaceOUT = BaseSpaceOUTs[1]
# Capture AllCtrl in the variable
AllCtrl = BaseCtrlsALL[2]
# Connect geometry visibility (render/proxy/box geo groups) to the AllCtrl
cmds.connectAttr( AllCtrl+'.Show_Render_Geo', 'Render_Grp.visibility' )
cmds.connectAttr( AllCtrl+'.Show_Proxy_Geo', 'Proxies_Grp.visibility' )
cmds.connectAttr( AllCtrl+'.Show_Box_Geo', 'Boxes_Grp.visibility' )

print('========================= made base rig')


# ---------------------------------------------------------------------------------------
# Make Torso Pivots

# Create torso pivots
TorsoPivGrp = jlyBR.jly_makeBipedTorsoPivs( prefix='', radius=3.1 )
# Parent created pivots under root pivot group
TorsoPivGrp = cmds.parent( TorsoPivGrp, RootPivGrp )
print('========================= made torso pivs')
# Put pivots to the correct place of the character
cmds.xform( 'Pelvis_Piv', t=( 0.0, 103.38795808512201, -1.6771380450789835 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'Spine01_Piv', t=( 0.0, 108.80793579101143, -0.2610264357851122 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'Spine02_Piv', t=( 0.0, 122.45119722615232, 1.1869691761274055 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'Chest_Piv', t=( 0.0, 138.5741583265994, -0.6758536188602378 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'Neck01_Piv', t=( 0.0, 160.9683284221534, -0.4008357973861294 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'Head_Piv', t=( 0.0, 173.38963432813995, 2.952921757981326 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'HeadEnd_Piv', t=( 0.0, 191.7653077198163, 5.306798825299326 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'Jaw_Piv', t=( 0.0, 172.27654366577747, 6.184404422294352 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'JawEnd_Piv', t=( 0.0, 167.63148872248527, 15.004553695587806 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )


# ---------------------------------------------------------------------------------------
# Make Torso Rig

# Create torso rig
TorsoRigRet = jlyBR.jly_makeBipedTorsoRig( prefix='', radius=3, ctrlRadius=(19.0,21.0,12.0,2.0) )
# Print root rig group, spaceINs, spaceOUTs, joints, contrls, guts
print( TorsoRigRet )
# Capture the list content (rig group, spaceINs, spaceOUTs, joints, contrls, guts) in 6 variables, so the master torso rig group will contain them
TorsoRigGrp = TorsoRigRet[0]; print( TorsoRigGrp )
TorsoSpaceINs = TorsoRigRet[1]; print( TorsoSpaceINs )
TorsoSpaceOUTs = TorsoRigRet[2]; print( TorsoSpaceOUTs )
TorsoBindJnts = TorsoRigRet[3]; print( TorsoBindJnts )
TorsoCtrlsALL = TorsoRigRet[4]; print( TorsoCtrlsALL )
TorsoGutsALL = TorsoRigRet[5]; print( TorsoGutsALL )
# Capture specific things in 5 variables (torso spaceIN, spaceOuts) for future connection
TorsoSpaceIN = TorsoSpaceINs[0]; print( TorsoSpaceIN )
PelvisSpaceOUT = TorsoSpaceOUTs[0]; print( PelvisSpaceOUT )
ChestSpaceOUT = TorsoSpaceOUTs[3]; print( ChestSpaceOUT )
HeadSpaceOUT = TorsoSpaceOUTs[5]; print( HeadSpaceOUT )
JawSpaceOUT = TorsoSpaceOUTs[6]; print( JawSpaceOUT )

# Connect box geometry, looks for matching geometry to match each of the bind joints, the geometry should have no children
denUt.den_connectBoxGeo( Jnts=TorsoBindJnts )
# Connect proxy geometry, looks for matching geometry to match each of the bind joints
denUt.den_connectProxyGeo( Jnts=TorsoBindJnts )

# Parent TorsoRigGrp under RootRigGrp
TorsoRigGrp = cmds.parent( TorsoRigGrp, RootRigGrp )

# Add parent constrait for CogSpaceOUT so it follows TorsoSpaceIN (translate/rotate)
cmds.parentConstraint( CogSpaceOUT, TorsoSpaceIN, mo=True )
# Add scale constrait for CogSpaceOUT so it follows TorsoSpaceIN(scale)
cmds.scaleConstraint( CogSpaceOUT, TorsoSpaceIN, mo=True )

# Add safety cover, lock things we dont want to touch, add attributes needed, etc.
denUt.den_AddSafetyCovers( rigGroup=TorsoRigGrp[0] )

# Connect torso control attributes to all control attributes
cmds.connectAttr( 'All_Ctrl.Show_Controls', 'Torso_Grp.Show_Controls' )
# Connect magenta control color to the center color, so the contrls get its correct color, make the control color yellow
cmds.connectAttr( 'All_Ctrl.Center_Color', 'Torso_Grp.Ctrl_Color' )
cmds.connectAttr( 'All_Ctrl.Show_Guts', 'Torso_Grp.Show_Guts' )
cmds.connectAttr(' All_Ctrl.Bone_Draw_Style', 'Torso_Grp.Bone_Draw_Style' )


# ---------------------------------------------------------------------------------------
# Make Arm Pivots

# Make Left arm
# Create arm pivots
L_ArmPivsRet = jlyBR.jly_makeBipedArmPivs( side='L_', prefix='', name='Arm', radius=1.99 )
# Parent all pivots under RootPivGrp
L_ArmPivsRet = cmds.parent( L_ArmPivsRet, RootPivGrp )

# Make Right arm
# Create arm pivots
R_ArmPivsRet = jlyBR.jly_makeBipedArmPivs( side='R_', prefix='', name='Arm', radius=1.99 )
# Parent all pivots under RootPivGrp
R_ArmPivsRet = cmds.parent( R_ArmPivsRet, RootPivGrp )

print('========================= made arm pivs')

# Put arm pivots in correct position
# Reposition left arm pivots
cmds.xform( 'L_Clav_Piv', t=( 1.9135768586143171, 153.72120871220972, 8.111426611008746 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Shld_Piv', t=( 17.53802266762109, 155.15684653162617, 1.7796898630562212 ), ro=( 86.74712240873176, -0.7694259632853707, -48.345528000997085 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Elbow_Piv', t=( 37.9558915859689, 132.20363758393628, 2.19225858830389 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Wrist_Piv', t=( 53.38627565861546, 116.50632068585766, 21.774206955784923 ), ro=( 85.64473902980747, -41.6571505323795, -45.491322807411514 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Scap01_Piv', t=( -1.5201945535034973, 153.65927057639274, 8.433975250892258 ), ro=( 84.851587064278, 63.52300106372328, 0.6807021253204542 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Scap02_Piv', t=( 6.294676078407078, 153.75211946313178, -7.257108077849578 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
# Reposition right arm pivots
cmds.xform( 'R_Clav_Piv', t=( 1.9135768586143171, 153.72120871220972, 8.111426611008746 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Shld_Piv', t=( 17.53802266762109, 155.15684653162617, 1.7796898630562212 ), ro=( 86.74712240873176, -0.7694259632853707, -48.345528000997085 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Elbow_Piv', t=( 37.9558915859689, 132.20363758393628, 2.19225858830389 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Wrist_Piv', t=( 53.38627565861546, 116.50632068585766, 21.774206955784923 ), ro=( 85.64473902980747, -41.6571505323795, -45.491322807411514 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Scap01_Piv', t=( -1.5201945535034973, 153.65927057639274, 8.433975250892258 ), ro=( 84.851587064278, 63.52300106372328, 0.6807021253204542 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Scap02_Piv', t=( 6.294676078407078, 153.75211946313178, -7.257108077849578 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )


# ---------------------------------------------------------------------------------------
# Create Arm Rig

# Create the left arm rig
L_ArmRigRet = jlyBR.jly_makeBipedArmRig( side='L_', prefix='', name='Arm', radius=2.0, ctrlRadius=10.0, displayLocalAxis=False, twistType='none' )
#L_ArmRigRet = denBR.den_makeBipedArmRig( side='L_', prefix='', name='Arm', radius=2.0, ctrlRadius=10.0, displayLocalAxis=False, twistType='twist' )

print( L_ArmRigRet )

# Capture the list content (rig group, spaceINs, spaceOUTs, joints, contrls, guts) in 6 variables, so the master arm rig group will contain them
L_ArmRigGrp = L_ArmRigRet[0]; print( L_ArmRigGrp )
L_ArmSpaceINs = L_ArmRigRet[1]; print( L_ArmSpaceINs )
L_ArmSpaceOUTs = L_ArmRigRet[2]; print( L_ArmSpaceOUTs )
L_ArmBindJoints = L_ArmRigRet[3]; print( L_ArmBindJoints )
L_ArmCtrlsALL = L_ArmRigRet[4]; print( L_ArmCtrlsALL )
L_ArmGutsALL = L_ArmRigRet[5]; print( L_ArmGutsALL )
# Capture specific things in 5 variables (torso spaceIN, spaceOuts) for future connection
L_ArmPelvisSpaceIN = L_ArmSpaceINs[2]
L_ArmChestSpaceIN = L_ArmSpaceINs[1]
L_ArmHeadSpaceIN = L_ArmSpaceINs[0]
L_ArmCogSpaceIN = L_ArmSpaceINs[3]
L_ArmAllSpaceIN = L_ArmSpaceINs[4]
L_WristSpaceOUT = L_ArmSpaceOUTs[0]

# Connect box geometry, looks for matching geometry to match each of the bind joints
denUt.den_connectBoxGeo( Jnts=L_ArmBindJoints )
# Connect proxy geometry, looks for matching geometry to match each of the bind joints
denUt.den_connectProxyGeo( Jnts=L_ArmBindJoints )

# Parent left arm rig group under root rig group
L_ArmRigGrp = cmds.parent( L_ArmRigGrp, RootRigGrp )

# Connect arm spaceINs to its spaceOUTs with parent constraint (translate, rotate)
cmds.parentConstraint( PelvisSpaceOUT, L_ArmPelvisSpaceIN, mo=True )
cmds.parentConstraint( ChestSpaceOUT, L_ArmChestSpaceIN, mo=True )
cmds.parentConstraint( HeadSpaceOUT, L_ArmHeadSpaceIN, mo=True )
cmds.parentConstraint( CogSpaceOUT, L_ArmCogSpaceIN, mo=True )
cmds.parentConstraint( AllSpaceOUT, L_ArmAllSpaceIN, mo=True )
# Connect arm spaceINs to its spaceOUTs with scale constraint (scale)
cmds.scaleConstraint( PelvisSpaceOUT, L_ArmPelvisSpaceIN, mo=True )
cmds.scaleConstraint( ChestSpaceOUT, L_ArmChestSpaceIN, mo=True )
cmds.scaleConstraint( HeadSpaceOUT, L_ArmHeadSpaceIN, mo=True )
cmds.scaleConstraint( CogSpaceOUT, L_ArmCogSpaceIN, mo=True )
cmds.scaleConstraint( AllSpaceOUT, L_ArmAllSpaceIN, mo=True )

#### Add twists to the left Arm after creation and do it before add safty covers
# Create twist rig
L_ArmTwistRigRet = jlyBR.jly_makeTwists( side='L_', radius=1.997, Joints=['Shld','Elbow','Wrist'], ctrlPos=(-10,0,-10), ctrlUpVec=(0,0,-1), displayLocalAxis=False )
print( L_ArmTwistRigRet )
# Create twist joints
L_ArmTwistJoints = L_ArmTwistRigRet[3]; print( L_ArmTwistJoints )
# Create twist control
L_ArmTwistCtrlsALL = L_ArmTwistRigRet[4]; print( L_ArmTwistCtrlsALL )
# Connect the procy geo to the twist rig
denUt.den_connectProxyGeo( Jnts=L_ArmTwistJoints )

# Add safety cover, lock things we dont want to touch, add attributes needed, etc. at the top level of arm rig
denUt.den_AddSafetyCovers( rigGroup=L_ArmRigGrp[0] )

# Connect control attributes (visibility, show guts, bone draw style, color) to the All_Ctrl
cmds.connectAttr( AllCtrl+'.Show_Controls', L_ArmRigGrp[0]+'.Show_Controls' )
cmds.connectAttr( AllCtrl+'.Show_Guts', L_ArmRigGrp[0]+'.Show_Guts' )
cmds.connectAttr( AllCtrl+'.Bone_Draw_Style', L_ArmRigGrp[0]+'.Bone_Draw_Style' )
cmds.connectAttr( AllCtrl+'.Left_Color', L_ArmRigGrp[0]+'.Ctrl_Color' )

print('========================= made L_ arm rig')

# Create the right arm rig
R_ArmRigRet = jlyBR.jly_makeBipedArmRig( side='R_', prefix='', name='Arm', radius=2.0, ctrlRadius=10.0, displayLocalAxis=False, twistType='none', dpTime=0.1 )
#R_ArmRigRet = denBR.den_makeBipedArmRig( side='R_', prefix='', name='Arm', radius=2.0, ctrlRadius=10.0, displayLocalAxis=False, twistType='twist' )

print( R_ArmRigRet )

# Capture the list content (rig group, spaceINs, spaceOUTs, joints, contrls, guts) in 6 variables, so the master arm rig group will contain them
R_ArmRigGrp = R_ArmRigRet[0]; print( R_ArmRigGrp )
R_ArmSpaceINs = R_ArmRigRet[1]; print( R_ArmSpaceINs )
R_ArmSpaceOUTs = R_ArmRigRet[2]; print( R_ArmSpaceOUTs )
R_ArmBindJoints = R_ArmRigRet[3]; print( R_ArmBindJoints )
R_ArmCtrlsALL = R_ArmRigRet[4]; print( R_ArmCtrlsALL )
R_ArmGutsALL = R_ArmRigRet[5]; print( R_ArmGutsALL )
# Capture specific things in 5 variables (torso spaceIN, spaceOuts) for future connection
R_ArmPelvisSpaceIN = R_ArmSpaceINs[2]
R_ArmChestSpaceIN = R_ArmSpaceINs[1]
R_ArmHeadSpaceIN = R_ArmSpaceINs[0]
R_ArmCogSpaceIN = R_ArmSpaceINs[3]
R_ArmAllSpaceIN = R_ArmSpaceINs[4]
R_WristSpaceOUT = R_ArmSpaceOUTs[0]



# Connect box geometry, looks for matching geometry to match each of the bind joints
denUt.den_connectBoxGeo( Jnts=R_ArmBindJoints )
# Connect proxy geometry, looks for matching geometry to match each of the bind joints
denUt.den_connectProxyGeo( Jnts=R_ArmBindJoints )

# Parent right arm rig group under root rig group
R_ArmRigGrp = cmds.parent( R_ArmRigGrp, RootRigGrp )

# Connect arm spaceINs to its spaceOUTs with parent constraint (translate, rotate)
cmds.parentConstraint( PelvisSpaceOUT, R_ArmPelvisSpaceIN, mo=True )
cmds.parentConstraint( ChestSpaceOUT, R_ArmChestSpaceIN, mo=True )
cmds.parentConstraint( HeadSpaceOUT, R_ArmHeadSpaceIN, mo=True )
cmds.parentConstraint( CogSpaceOUT, R_ArmCogSpaceIN, mo=True )
cmds.parentConstraint( AllSpaceOUT, R_ArmAllSpaceIN, mo=True )
# Connect arm spaceINs to its spaceOUTs with scale constraint (scale)
cmds.scaleConstraint( PelvisSpaceOUT, R_ArmPelvisSpaceIN, mo=True )
cmds.scaleConstraint( ChestSpaceOUT, R_ArmChestSpaceIN, mo=True )
cmds.scaleConstraint( HeadSpaceOUT, R_ArmHeadSpaceIN, mo=True )
cmds.scaleConstraint( CogSpaceOUT, R_ArmCogSpaceIN, mo=True )
cmds.scaleConstraint( AllSpaceOUT, R_ArmAllSpaceIN, mo=True )

#### Add twists to the right Arm
# Create twist rig
R_ArmTwistRigRet = jlyBR.jly_makeTwists( side='R_', radius=1.997, Joints=['Shld','Elbow','Wrist'], ctrlPos=(-10,0,-10), ctrlUpVec=(0,0,-1), displayLocalAxis=False )
print( L_ArmTwistRigRet )
# Create twist joint
R_ArmTwistJoints = R_ArmTwistRigRet[3]; print( R_ArmTwistJoints )
# Create twist control
R_ArmTwistCtrlsALL = R_ArmTwistRigRet[4]; print( R_ArmTwistCtrlsALL )
# Connect the procy geo to the twist rig
denUt.den_connectProxyGeo( Jnts=R_ArmTwistJoints )

# Add safety cover, lock things we dont want to touch, add attributes needed, etc. at the top level of arm rig
denUt.den_AddSafetyCovers( rigGroup=R_ArmRigGrp[0] )

# Connect control attributes (visibility, show guts, bone draw style, color) to the All_Ctrl
cmds.connectAttr( AllCtrl+'.Show_Controls', R_ArmRigGrp[0]+'.Show_Controls' )
cmds.connectAttr( AllCtrl+'.Show_Guts', R_ArmRigGrp[0]+'.Show_Guts' )
cmds.connectAttr( AllCtrl+'.Bone_Draw_Style', R_ArmRigGrp[0]+'.Bone_Draw_Style' )
cmds.connectAttr( AllCtrl+'.Right_Color', R_ArmRigGrp[0]+'.Ctrl_Color' )

print('========================= made R_ arm rig')



# ---------------------------------------------------------------------------------------
# Create Leg Pivots

# Make Left Leg
# Create the left leg pivots
L_LegPivGrp = jlyBR.jly_makeBipedLegPivs( side='L_', prefix='', name='Leg', radius=2.03 )
# Parent all pivots under RootPivGrp
L_LegPivGrp = cmds.parent( L_LegPivGrp, RootPivGrp )
print('========================= made leg pivs')
# Reposition left leg pivots in correct position
cmds.xform( 'L_Hip_Piv', t=( 11.620753002549673, 100.753737395051, 3.9544591343279754 ), ro=( -88.52304623900268, -0.8868921966587131, -84.11921586316016 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Knee_Piv', t=( 16.42263871967709, 54.13393918809286, 4.679971642013455 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
#cmds.xform( 'L_Hip_Piv', t=( 7.47910212414683, 100.753737395051, 3.9544591343279754 ), ro=( -135.6848710665911, -0.9196381838546824, -79.6579444660907 ), s=( 1.0, 1.0, 1.0 ) )
#cmds.xform( 'L_Knee_Piv', t=( 15.593131898895091, 56.290656922126054, 4.679971642013455 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Ankle_Piv', t=( 21.24613479575349, 8.05050525592242, 2.431744496222167 ), ro=( 104.97051935197712, -67.76898056802453, -90.00000000000004 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Ball_Piv', t=( 21.24613479575349, 2.464627006420442, 16.098366494160746 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Toe_Piv', t=( 20.76061572470766, 1.3057221824458058, 23.73293275485289 ), ro=( 8.614298014201049, -3.6388161010887714, -4.916414241727251e-13 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Heel_Piv', t=( 21.769001487649007, 1.3057221824458058, -3.453600374570645 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_SoleLF_Piv', t=( 27.396744312354766, 1.3057221824458058, 11.921488389961274 ), ro=( 0.0, 9.260658719175954, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_SoleLB_Piv', t=( 25.24613479575349, 1.3057221824458058, -1.268282959177832 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_SoleRF_Piv', t=( 16.460615724707658, 1.3057221824458058, 17.296835228910673 ), ro=( 0.0, -6.959773856000521, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_SoleRB_Piv', t=( 18.715937506270244, 1.3057221824458058, -1.1785116100387256 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )

# DP refresh
denUt.den_DiagPause( 0.1 ) 

# Make Right Leg
# Create the eight leg pivots
R_LegPivGrp = jlyBR.jly_makeBipedLegPivs( side='R_', prefix='', name='Leg', radius=2.03 )
# Parent all pivots under RootPivGrp
R_LegPivGrp = cmds.parent( R_LegPivGrp, RootPivGrp )
print('========================= made leg pivs')
# Reposition right leg pivots in correct position
cmds.xform( 'R_Hip_Piv', t=( 11.620753002549673, 100.753737395051, 3.9544591343279754 ), ro=( -88.52304623900268, -0.8868921966587131, -84.11921586316016 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Knee_Piv', t=( 16.42263871967709, 54.13393918809286, 4.679971642013455 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Ankle_Piv', t=( 21.24613479575349, 8.05050525592242, 2.431744496222167 ), ro=( 104.97051935197712, -67.76898056802453, -90.00000000000004 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Ball_Piv', t=( 21.24613479575349, 2.464627006420442, 16.098366494160746 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Toe_Piv', t=( 20.76061572470766, 1.3057221824458058, 23.73293275485289 ), ro=( 8.614298014201049, -3.6388161010887714, -4.916414241727251e-13 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Heel_Piv', t=( 21.769001487649007, 1.3057221824458058, -3.453600374570645 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_SoleLF_Piv', t=( 27.396744312354766, 1.3057221824458058, 11.921488389961274 ), ro=( 0.0, 9.260658719175954, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_SoleLB_Piv', t=( 25.24613479575349, 1.3057221824458058, -1.268282959177832 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_SoleRF_Piv', t=( 16.460615724707658, 1.3057221824458058, 17.296835228910673 ), ro=( 0.0, -6.959773856000521, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_SoleRB_Piv', t=( 18.715937506270244, 1.3057221824458058, -1.1785116100387256 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )

# DP refresh
denUt.den_DiagPause( 0.1 ) 
# DP time
denUt.den_DiagPause( seconds=1 )


# ---------------------------------------------------------------------------------------
# Create Leg Rig

# Create the left leg rig
L_LegRigRet = jlyBR.jly_makeBipedLegRig( side='L_', prefix='', name='Leg', radius=2.05, ctrlRadius=15.0, displayLocalAxis=False, twistType='none' )
#L_LegRigRet = denBR.den_makeBipedLegRig( side='L_', prefix='', name='Leg', radius=2.05, ctrlRadius=15.0, displayLocalAxis=False, twistType='twist' )

print( L_LegRigRet )

# Capture the list content (rig group, spaceINs, spaceOUTs, joints, contrls, guts) in 6 variables, so the master leg rig group will contain them
L_LegRigGrp = L_LegRigRet[0]; print( L_LegRigGrp )
L_LegSpaceINs = L_LegRigRet[1]; print( L_LegSpaceINs )
L_LegSpaceOUTs = L_LegRigRet[2]; print( L_LegSpaceOUTs )
L_LegBindJoints = L_LegRigRet[3]; print( L_LegBindJoints )
L_LegCtrlsALL = L_LegRigRet[4]; print( L_LegCtrlsALL )
L_LegGutsALL = L_LegRigRet[5]; print( L_LegGutsALL )
# Capture specific things in 5 variables (torso spaceIN, spaceOuts) for future connection
L_LegPelvisSpaceIN = L_LegSpaceINs[0]; print( L_LegPelvisSpaceIN )
L_LegCogSpaceIN = L_LegSpaceINs[1]; print( L_LegCogSpaceIN )
L_LegAllSpaceIN = L_LegSpaceINs[2]; print( L_LegAllSpaceIN )
L_AnkleSpaceOUT = L_LegSpaceOUTs[0]; print( L_AnkleSpaceOUT )

# Connect box geometry, looks for matching geometry to match each of the bind joints
denUt.den_connectBoxGeo( Jnts=L_LegBindJoints )
# Connect proxy geometry, looks for matching geometry to match each of the bind joints
denUt.den_connectProxyGeo( Jnts=L_LegBindJoints )

# Parent left leg rig group under root rig group
L_LegRigGrp = cmds.parent( L_LegRigGrp, RootRigGrp )

# Connect leg spaceINs to its spaceOUTs with parent constraint (translate, rotate)
cmds.parentConstraint( PelvisSpaceOUT, L_LegPelvisSpaceIN, mo=True )
cmds.parentConstraint( CogSpaceOUT, L_LegCogSpaceIN, mo=True )
cmds.parentConstraint( AllSpaceOUT, L_LegAllSpaceIN, mo=True )
# Connect leg spaceINs to its spaceOUTs with scale constraint (scale)
cmds.scaleConstraint( PelvisSpaceOUT, L_LegPelvisSpaceIN, mo=True )
cmds.scaleConstraint( CogSpaceOUT, L_LegCogSpaceIN, mo=True )
cmds.scaleConstraint( AllSpaceOUT, L_LegAllSpaceIN, mo=True )


#### Create twist rig for the left leg
# Create the twist rig
L_LegTwistRigRet = jlyBR.jly_makeTwists( side='L_', radius=1.997, Joints=['Hip','Knee','Ankle'], ctrlPos=(0,0,20), ctrlUpVec=(0,0,1), displayLocalAxis=False )
print( L_LegTwistRigRet )
# Create the twist joints
L_LegTwistJoints = L_LegTwistRigRet[3]; print( L_LegTwistJoints )
# Create the twist control
L_LegTwistCtrlsALL = L_LegTwistRigRet[4]; print( L_LegTwistCtrlsALL )
# Connect the twist rig to the proxy geo
denUt.den_connectProxyGeo( Jnts=L_LegTwistJoints )


# Add safety cover, lock things we dont want to touch, add attributes needed, etc. at the top level of leg rig
denUt.den_AddSafetyCovers( rigGroup=L_LegRigGrp[0] )

# Connect control attributes (visibility, show guts, bone draw style, color) to the All_Ctrl
cmds.connectAttr( AllCtrl+'.Show_Controls', L_LegRigGrp[0]+'.Show_Controls' )
cmds.connectAttr( AllCtrl+'.Show_Guts', L_LegRigGrp[0]+'.Show_Guts' )
cmds.connectAttr( AllCtrl+'.Bone_Draw_Style', L_LegRigGrp[0]+'.Bone_Draw_Style' )
cmds.connectAttr( AllCtrl+'.Left_Color', L_LegRigGrp[0]+'.Ctrl_Color' )

print('========================= made L_ leg rig')

# Create the right leg rig
R_LegRigRet = jlyBR.jly_makeBipedLegRig( side='R_', prefix='', name='Leg', radius=2.05, ctrlRadius=15.0, displayLocalAxis=False, twistType='none' )
#R_LegRigRet = denBR.den_makeBipedLegRig( side='R_', prefix='', name='Leg', radius=2.05, ctrlRadius=15.0, displayLocalAxis=False, twistType='twist' )

print( R_LegRigRet )
# Capture the list content (rig group, spaceINs, spaceOUTs, joints, contrls, guts) in 6 variables, so the master leg rig group will contain them
R_LegRigGrp = R_LegRigRet[0]; print( R_LegRigGrp )
R_LegSpaceINs = R_LegRigRet[1]; print( R_LegSpaceINs )
R_LegSpaceOUTs = R_LegRigRet[2]; print( R_LegSpaceOUTs )
R_LegBindJoints = R_LegRigRet[3]; print( R_LegBindJoints )
R_LegCtrlsALL = R_LegRigRet[4]; print( R_LegCtrlsALL )
R_LegGutsALL = R_LegRigRet[5]; print( R_LegGutsALL )
# Capture specific things in 5 variables (torso spaceIN, spaceOuts) for future connection
R_LegPelvisSpaceIN = R_LegSpaceINs[0]; print( R_LegPelvisSpaceIN )
R_LegCogSpaceIN = R_LegSpaceINs[1]; print( R_LegCogSpaceIN )
R_LegAllSpaceIN = R_LegSpaceINs[2]; print( R_LegAllSpaceIN )
R_AnkleSpaceOUT = R_LegSpaceOUTs[0]; print( R_AnkleSpaceOUT )

# Connect box geometry, looks for matching geometry to match each of the bind joints
denUt.den_connectBoxGeo( Jnts=R_LegBindJoints )
# Connect proxy geometry, looks for matching geometry to match each of the bind joints
denUt.den_connectProxyGeo( Jnts=R_LegBindJoints )

# Parent right leg rig group under root rig group
R_LegRigGrp = cmds.parent( R_LegRigGrp, RootRigGrp )

# Connect leg spaceINs to its spaceOUTs with parent constraint (translate, rotate)
cmds.parentConstraint( PelvisSpaceOUT, R_LegPelvisSpaceIN, mo=True )
cmds.parentConstraint( CogSpaceOUT, R_LegCogSpaceIN, mo=True )
cmds.parentConstraint( AllSpaceOUT, R_LegAllSpaceIN, mo=True )
# Connect leg spaceINs to its spaceOUTs with scale constraint (scale)
cmds.scaleConstraint( PelvisSpaceOUT, R_LegPelvisSpaceIN, mo=True )
cmds.scaleConstraint( CogSpaceOUT, R_LegCogSpaceIN, mo=True )
cmds.scaleConstraint( AllSpaceOUT, R_LegAllSpaceIN, mo=True )


#### Create twist rig for the right leg
# Create the twist rig
R_LegTwistRigRet = jlyBR.jly_makeTwists( side='R_', radius=1.997, Joints=['Hip','Knee','Ankle'], ctrlPos=(0,0,20), ctrlUpVec=(0,0,1), displayLocalAxis=False )
print( R_LegTwistRigRet )
# Create the twist joints
R_LegTwistJoints = R_LegTwistRigRet[3]; print( R_LegTwistJoints )
# Create the twist control
R_LegTwistCtrlsALL = R_LegTwistRigRet[4]; print( R_LegTwistCtrlsALL )
# Connect the twist rig to the proxy geo
denUt.den_connectProxyGeo( Jnts=R_LegTwistJoints )

# Add safety cover, lock things we dont want to touch, add attributes needed, etc. at the top level of leg rig
denUt.den_AddSafetyCovers( rigGroup=R_LegRigGrp[0] )

# Connect control attributes (visibility, show guts, bone draw style, color) to the All_Ctrl
cmds.connectAttr( AllCtrl+'.Show_Controls', R_LegRigGrp[0]+'.Show_Controls' )
cmds.connectAttr( AllCtrl+'.Show_Guts', R_LegRigGrp[0]+'.Show_Guts' )
cmds.connectAttr( AllCtrl+'.Bone_Draw_Style', R_LegRigGrp[0]+'.Bone_Draw_Style' )
cmds.connectAttr( AllCtrl+'.Right_Color', R_LegRigGrp[0]+'.Ctrl_Color' )

print('========================= made R_ leg rig')


# --- Make hands for Blocking or Final rig ---

# ---------------------------------------------------------------------------------------
# Create Hand Pivots

# Make left Hand
# Create hand pivots
L_HandPivGrp = jlyBR.jly_makeBipedHandPivs2( side='L_', prefix='', name='Hand', radius=1.0, dpTime=0.01 )
# Parent all pivots under RootPivGrp
L_HandPivGrp = cmds.parent( L_HandPivGrp, RootPivGrp )
# Reposition left arm pivots to put hand pivots in correct position
cmds.xform( 'L_Thumb01_Piv', t=( 51.71137641234973, 116.67312339099023, 25.47348478558281 ), ro=( -39.8947625982986, -56.7071204730737, -139.69666169500059 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_ThumbUp_Piv', t=( 50.61892662939668, 112.77676853236433, 27.130738845970797 ), ro=( 59.99999999999997, -45.0, -14.99999999999999 ), s=( 0.9999999999999999, 0.9999999999999999, 1.0 ) )
cmds.xform( 'L_Thumb02_Piv', t=( 49.84159973362872, 115.08725015066152, 29.206922483763012 ), ro=( -65.16551994656963, -59.7807693076043, -103.81640978662007 ), s=( 0.9999999999999999, 0.9999999999999998, 1.0 ) )
cmds.xform( 'L_Thumb03_Piv', t=( 49.46725087378105, 113.56505674194602, 31.898163185147368 ), ro=( -64.69972428037357, -53.13635279232142, -120.07544019579171 ), s=( 0.9999999999999999, 1.0, 1.0 ) )
cmds.xform( 'L_ThumbEnd_Piv', t=( 48.38854217529297, 111.70234680175781, 34.768829345703125 ), ro=( -64.69972428037356, -53.13635279232141, -120.07544019579171 ), s=( 0.9999999999999999, 1.0, 1.0 ) )
cmds.xform( 'L_Index00_Piv', t=( 53.11217181564158, 116.35131052005582, 25.169589426763334 ), ro=( -163.20764601717653, -53.14415903054522, -58.44823530851284 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Index01_Piv', t=( 55.85566049304257, 111.88340965424453, 32.163807306201015 ), ro=( -151.1153688866354, -52.37332637851746, -81.70082426908142 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_IndexUp_Piv', t=( 50.91209817069331, 112.68522955879091, 25.893032850590785 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Index02_Piv', t=( 56.09724894478808, 110.22721421398224, 34.33508900593874 ), ro=( -141.78687737524504, -45.59022253636459, -87.57930149847931 ), s=( 0.9999999999999999, 0.9999999999999999, 1.0 ) )
cmds.xform( 'L_Index03_Piv', t=( 56.16706874836903, 108.57562498422541, 36.02256660006212 ), ro=( -146.678766414907, -49.241913059489484, -87.72076112116369 ), s=( 0.9999999999999998, 0.9999999999999998, 1.0 ) )
cmds.xform( 'L_IndexEnd_Piv', t=( 56.24721908569336, 106.56185913085938, 38.36083984375 ), ro=( -146.678766414907, -49.241913059489484, -87.72076112116369 ), s=( 0.9999999999999998, 0.9999999999999998, 1.0 ) )
cmds.xform( 'L_Middle00_Piv', t=( 53.97385484156486, 115.66627974904733, 24.363047927627623 ), ro=( -169.13414785334268, -43.077182690240036, -53.89993174294101 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Middle01_Piv', t=( 57.71381603759647, 110.53752561989282, 30.2982432726056 ), ro=( -153.40929727682982, -35.562552030712396, -73.47222049996613 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_MiddleUp_Piv', t=( 51.80051335914538, 112.5044113932926, 24.60345724698563 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Middle02_Piv', t=( 58.48052025704356, 107.95377637904734, 32.22508643074421 ), ro=( -158.36914463314463, -39.69260778997632, -81.26585805108078 ), s=( 0.9999999999999999, 0.9999999999999999, 1.0 ) )
cmds.xform( 'L_Middle03_Piv', t=( 58.834759587662376, 105.64800211748822, 34.16132810373252 ), ro=( -155.0268339033137, -37.91685497559025, -75.99918428740959 ), s=( 0.9999999999999998, 0.9999999999999998, 1.0 ) )
cmds.xform( 'L_MiddleEnd_Piv', t=( 59.41785430908203, 103.30947875976562, 36.0386962890625 ), ro=( -155.0268339033137, -37.91685497559025, -75.99918428740959 ), s=( 0.9999999999999998, 0.9999999999999998, 1.0 ) )
cmds.xform( 'L_Ring00_Piv', t=( 54.70150197275118, 114.82538416767329, 23.317512681466592 ), ro=( -174.72754819309498, -35.72643492198604, -54.266451383062105 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Ring01_Piv', t=( 58.59129438074794, 109.4188483845535, 28.10816684443967 ), ro=( -161.60162176541613, -29.516775317149524, -66.42089073389057 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_RingUp_Piv', t=( 52.207937704461514, 112.13473502420376, 23.432303443751273 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Ring02_Piv', t=( 59.573154690029234, 107.16922347769484, 29.497838595520502 ), ro=( -160.65430757191137, -29.409672477180404, -79.34808539913094 ), s=( 0.9999999999999999, 0.9999999999999999, 1.0 ) )
cmds.xform( 'L_Ring03_Piv', t=( 60.0404100890381, 104.68491772180138, 30.922779748730708 ), ro=( -162.10051752624923, -30.390227141532673, -70.92975066317837 ), s=( 0.9999999999999998, 0.9999999999999998, 1.0 ) )
cmds.xform( 'L_RingEnd_Piv', t=( 60.90991973876953, 102.1697006225586, 32.48352813720703 ), ro=( -162.10051752624923, -30.390227141532673, -70.92975066317837 ), s=( 0.9999999999999998, 0.9999999999999998, 1.0 ) )
cmds.xform( 'L_Pinky00_Piv', t=( 55.29434242769428, 114.07596515951221, 22.03170453360608 ), ro=( 179.8180535342594, -30.231911543857347, -56.19667909736308 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Pinky01_Piv', t=( 58.823111322830115, 108.80541397473681, 25.728024356363626 ), ro=( -159.25472453652614, -17.077191250498828, -73.3804017704521 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_PinkyUp_Piv', t=( 52.91119101537268, 111.6406823718575, 22.45058460054719 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Pinky02_Piv', t=( 59.38698173624223, 106.91630870633279, 26.333666752369446 ), ro=( -166.12065070456956, -22.241230425556083, -76.52805035424907 ), s=( 0.9999999999999999, 0.9999999999999999, 1.0 ) )
cmds.xform( 'L_Pinky03_Piv', t=( 59.831176896900054, 105.06210412760035, 27.1133646901398 ), ro=( -171.4316384297003, -25.845440927685893, -80.28008960246207 ), s=( 0.9999999999999998, 0.9999999999999998, 1.0 ) )
cmds.xform( 'L_PinkyEnd_Piv', t=( 60.16964340209961, 103.08612823486328, 28.084463119506836 ), ro=( -171.4316384297003, -25.845440927685893, -80.28008960246206 ), s=( 0.9999999999999998, 0.9999999999999998, 1.0 ) )

# DP refresh
denUt.den_DiagPause( 0.1 ) 

# Make right Hand
# Create hand pivots
R_HandPivGrp = jlyBR.jly_makeBipedHandPivs2( side='R_', prefix='', name='Hand', radius=1.0 )
# Parent all pivots under RootPivGrp
R_HandPivGrp = cmds.parent( R_HandPivGrp, RootPivGrp )
# Reposition left arm pivots to put hand pivots in correct position
cmds.xform( 'R_Thumb01_Piv', t=( 51.71137641234973, 116.67312339099023, 25.47348478558281 ), ro=( -39.8947625982986, -56.7071204730737, -139.69666169500059 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_ThumbUp_Piv', t=( 50.61892662939668, 112.77676853236433, 27.130738845970797 ), ro=( 59.99999999999997, -45.0, -14.99999999999999 ), s=( 0.9999999999999999, 0.9999999999999999, 1.0 ) )
cmds.xform( 'R_Thumb02_Piv', t=( 49.84159973362872, 115.08725015066152, 29.206922483763012 ), ro=( -65.16551994656963, -59.7807693076043, -103.81640978662007 ), s=( 0.9999999999999999, 0.9999999999999998, 1.0 ) )
cmds.xform( 'R_Thumb03_Piv', t=( 49.46725087378105, 113.56505674194602, 31.898163185147368 ), ro=( -64.69972428037357, -53.13635279232142, -120.07544019579171 ), s=( 0.9999999999999999, 1.0, 1.0 ) )
cmds.xform( 'R_ThumbEnd_Piv', t=( 48.38854217529297, 111.70234680175781, 34.768829345703125 ), ro=( -64.69972428037356, -53.13635279232141, -120.07544019579171 ), s=( 0.9999999999999999, 1.0, 1.0 ) )
cmds.xform( 'R_Index00_Piv', t=( 53.11217181564158, 116.35131052005582, 25.169589426763334 ), ro=( -163.20764601717653, -53.14415903054522, -58.44823530851284 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Index01_Piv', t=( 55.85566049304257, 111.88340965424453, 32.163807306201015 ), ro=( -151.1153688866354, -52.37332637851746, -81.70082426908142 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_IndexUp_Piv', t=( 50.91209817069331, 112.68522955879091, 25.893032850590785 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Index02_Piv', t=( 56.09724894478808, 110.22721421398224, 34.33508900593874 ), ro=( -141.78687737524504, -45.59022253636459, -87.57930149847931 ), s=( 0.9999999999999999, 0.9999999999999999, 1.0 ) )
cmds.xform( 'R_Index03_Piv', t=( 56.16706874836903, 108.57562498422541, 36.02256660006212 ), ro=( -146.678766414907, -49.241913059489484, -87.72076112116369 ), s=( 0.9999999999999998, 0.9999999999999998, 1.0 ) )
cmds.xform( 'R_IndexEnd_Piv', t=( 56.24721908569336, 106.56185913085938, 38.36083984375 ), ro=( -146.678766414907, -49.241913059489484, -87.72076112116369 ), s=( 0.9999999999999998, 0.9999999999999998, 1.0 ) )
cmds.xform( 'R_Middle00_Piv', t=( 53.97385484156486, 115.66627974904733, 24.363047927627623 ), ro=( -169.13414785334268, -43.077182690240036, -53.89993174294101 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Middle01_Piv', t=( 57.71381603759647, 110.53752561989282, 30.2982432726056 ), ro=( -153.40929727682982, -35.562552030712396, -73.47222049996613 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_MiddleUp_Piv', t=( 51.80051335914538, 112.5044113932926, 24.60345724698563 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Middle02_Piv', t=( 58.48052025704356, 107.95377637904734, 32.22508643074421 ), ro=( -158.36914463314463, -39.69260778997632, -81.26585805108078 ), s=( 0.9999999999999999, 0.9999999999999999, 1.0 ) )
cmds.xform( 'R_Middle03_Piv', t=( 58.834759587662376, 105.64800211748822, 34.16132810373252 ), ro=( -155.0268339033137, -37.91685497559025, -75.99918428740959 ), s=( 0.9999999999999998, 0.9999999999999998, 1.0 ) )
cmds.xform( 'R_MiddleEnd_Piv', t=( 59.41785430908203, 103.30947875976562, 36.0386962890625 ), ro=( -155.0268339033137, -37.91685497559025, -75.99918428740959 ), s=( 0.9999999999999998, 0.9999999999999998, 1.0 ) )
cmds.xform( 'R_Ring00_Piv', t=( 54.70150197275118, 114.82538416767329, 23.317512681466592 ), ro=( -174.72754819309498, -35.72643492198604, -54.266451383062105 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Ring01_Piv', t=( 58.59129438074794, 109.4188483845535, 28.10816684443967 ), ro=( -161.60162176541613, -29.516775317149524, -66.42089073389057 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_RingUp_Piv', t=( 52.207937704461514, 112.13473502420376, 23.432303443751273 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Ring02_Piv', t=( 59.573154690029234, 107.16922347769484, 29.497838595520502 ), ro=( -160.65430757191137, -29.409672477180404, -79.34808539913094 ), s=( 0.9999999999999999, 0.9999999999999999, 1.0 ) )
cmds.xform( 'R_Ring03_Piv', t=( 60.0404100890381, 104.68491772180138, 30.922779748730708 ), ro=( -162.10051752624923, -30.390227141532673, -70.92975066317837 ), s=( 0.9999999999999998, 0.9999999999999998, 1.0 ) )
cmds.xform( 'R_RingEnd_Piv', t=( 60.90991973876953, 102.1697006225586, 32.48352813720703 ), ro=( -162.10051752624923, -30.390227141532673, -70.92975066317837 ), s=( 0.9999999999999998, 0.9999999999999998, 1.0 ) )
cmds.xform( 'R_Pinky00_Piv', t=( 55.29434242769428, 114.07596515951221, 22.03170453360608 ), ro=( 179.8180535342594, -30.231911543857347, -56.19667909736308 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Pinky01_Piv', t=( 58.823111322830115, 108.80541397473681, 25.728024356363626 ), ro=( -159.25472453652614, -17.077191250498828, -73.3804017704521 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_PinkyUp_Piv', t=( 52.91119101537268, 111.6406823718575, 22.45058460054719 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Pinky02_Piv', t=( 59.38698173624223, 106.91630870633279, 26.333666752369446 ), ro=( -166.12065070456956, -22.241230425556083, -76.52805035424907 ), s=( 0.9999999999999999, 0.9999999999999999, 1.0 ) )
cmds.xform( 'R_Pinky03_Piv', t=( 59.831176896900054, 105.06210412760035, 27.1133646901398 ), ro=( -171.4316384297003, -25.845440927685893, -80.28008960246207 ), s=( 0.9999999999999998, 0.9999999999999998, 1.0 ) )
cmds.xform( 'R_PinkyEnd_Piv', t=( 60.16964340209961, 103.08612823486328, 28.084463119506836 ), ro=( -171.4316384297003, -25.845440927685893, -80.28008960246206 ), s=( 0.9999999999999998, 0.9999999999999998, 1.0 ) )

# DP refresh
denUt.den_DiagPause( 0.1 ) 


# ---------------------------------------------------------------------------------------
# Create Hand Rig

# Create the left hand rig
L_HandRigRet = jlyBR.jly_makeBipedHandRig2( side='L_', prefix='', name='Hand', radius=1.03, displayLocalAxis=False, dpTime=0.01 )
print( L_HandRigRet )

# Capture the list content (rig group, spaceINs, spaceOUTs, joints, contrls, guts) in 6 variables, so the master rig group will contain them
L_HandRigGrp = L_HandRigRet[0]; print( L_HandRigGrp )
L_HandSpaceINs = L_HandRigRet[1]; print( L_HandSpaceINs )
L_HandSpaceOUTs = L_HandRigRet[2]; print( L_HandSpaceOUTs )
L_HandBindJoints = L_HandRigRet[3]; print( L_HandBindJoints )
L_HandCtrlsALL = L_HandRigRet[4]; print( L_HandCtrlsALL )
L_HandGutsALL = L_HandRigRet[5]; print( L_HandGutsALL )
# Capture specific things in variables (wrist spaceIN) for future connection
L_WristSpaceIN = L_HandSpaceINs[0]

# Connect proxy geometry, looks for matching geometry to match each of the bind joints
denUt.den_connectProxyGeo( Jnts=L_HandBindJoints )

# Connect arm spaceINs to its spaceOUTs with parent constraint (translate, rotate)
cmds.parentConstraint( L_WristSpaceOUT, L_WristSpaceIN, mo=True  )
# Connect arm spaceINs to its spaceOUTs with scale constraint (scale)
cmds.scaleConstraint( L_WristSpaceOUT, L_WristSpaceIN, mo=True  )

# Parent left hand rig group under root rig group
L_HandRigGrp = cmds.parent( L_HandRigGrp, RootRigGrp )

# Add safety cover, lock things we dont want to touch, add attributes needed, etc. at the top level of the rig
denUt.den_AddSafetyCovers( rigGroup=L_HandRigGrp[0] )

# Connect control attributes (visibility, show guts, bone draw style, color) to the All_Ctrl
cmds.connectAttr( AllCtrl+'.Show_Controls', L_HandRigGrp[0]+'.Show_Controls' )
cmds.connectAttr( AllCtrl+'.Show_Guts', L_HandRigGrp[0]+'.Show_Guts' )
cmds.connectAttr( AllCtrl+'.Bone_Draw_Style', L_HandRigGrp[0]+'.Bone_Draw_Style' )
cmds.connectAttr( AllCtrl+'.Left_Color', L_HandRigGrp[0]+'.Ctrl_Color' )

print('========================= made L_ hand rig')


# Create the right hand rig
R_HandRigRet = jlyBR.jly_makeBipedHandRig2( side='R_', prefix='', name='Hand', radius=1.03, displayLocalAxis=False )
print( R_HandRigRet )

# Capture the list content (rig group, spaceINs, spaceOUTs, joints, contrls, guts) in 6 variables, so the master rig group will contain them
R_HandRigGrp = R_HandRigRet[0]; print( R_HandRigGrp )
R_HandSpaceINs = R_HandRigRet[1]; print( R_HandSpaceINs )
R_HandSpaceOUTs = R_HandRigRet[2]; print( R_HandSpaceOUTs )
R_HandBindJoints = R_HandRigRet[3]; print( R_HandBindJoints )
R_HandCtrlsALL = R_HandRigRet[4]; print( R_HandCtrlsALL )
R_HandGutsALL = R_HandRigRet[5]; print( R_HandGutsALL )
# Capture specific things in variables (wrist spaceIN) for future connection
R_WristSpaceIN = R_HandSpaceINs[0]

# Connect proxy geometry, looks for matching geometry to match each of the bind joints
denUt.den_connectProxyGeo( Jnts=R_HandBindJoints )

# Connect arm spaceINs to its spaceOUTs with parent constraint (translate, rotate)
cmds.parentConstraint( R_WristSpaceOUT, R_WristSpaceIN, mo=True  )

# Parent right hand rig group under root rig group
R_HandRigGrp = cmds.parent( R_HandRigGrp, RootRigGrp )

# Add safety cover, lock things we dont want to touch, add attributes needed, etc. at the top level of the rig
denUt.den_AddSafetyCovers( rigGroup=R_HandRigGrp[0] )

# Connect control attributes (visibility, show guts, bone draw style, color) to the All_Ctrl
cmds.connectAttr( AllCtrl+'.Show_Controls', R_HandRigGrp[0]+'.Show_Controls' )
cmds.connectAttr( AllCtrl+'.Show_Guts', R_HandRigGrp[0]+'.Show_Guts' )
cmds.connectAttr( AllCtrl+'.Bone_Draw_Style', R_HandRigGrp[0]+'.Bone_Draw_Style' )
cmds.connectAttr( AllCtrl+'.Right_Color', R_HandRigGrp[0]+'.Ctrl_Color' )

print('========================= made R_ hand rig')


# ===========================================================================================
# ---------------------------------------------------------------------------------------
# Create extra seat and thigh helper rigs to improve deformation
# ---------------------------------------------------------------------------------------
# Create split helper for Left and Right ass
L_Seat = jlyBR.jly_makeAngleSplitter( name='L_Seat02', firstJnt='L_HipRest_Jx', secondJnt='L_HipTwist01_Jnt', radius=1.0 )
R_Seat = jlyBR.jly_makeAngleSplitter( name='R_Seat02', firstJnt='R_HipRest_Jx', secondJnt='R_HipTwist01_Jnt', radius=1.0 )

# Connect proxy geometry, looks for matching geometry to match each of the bind joints
denUt.den_connectProxyGeo(Jnts=[L_Seat, R_Seat])


# ---------------------------------------------------------------------------------------
# Create half muscle pivots for the 4 muscle groups

# Create 4 different half muscle pivots for thigh, and parent them under the root piv group
L_Thigh01PivGrp = jlyBR.jly_makeHalfMusclePivs( side='L_', prefix='', name='Thigh01', radius=2.0, dpTime=0.01 )
cmds.parent( L_Thigh01PivGrp, RootPivGrp )

R_Thigh01PivGrp = jlyBR.jly_makeHalfMusclePivs( side='R_', prefix='', name='Thigh01', radius=2.0, dpTime=0.01 )
cmds.parent( R_Thigh01PivGrp, RootPivGrp )

L_Thigh01PivGrp = jlyBR.jly_makeHalfMusclePivs( side='L_', prefix='', name='Thigh02', radius=2.0, dpTime=0.01 )
cmds.parent( L_Thigh01PivGrp, RootPivGrp )

R_Thigh01PivGrp = jlyBR.jly_makeHalfMusclePivs( side='R_', prefix='', name='Thigh02', radius=2.0, dpTime=0.01 )
cmds.parent( R_Thigh01PivGrp, RootPivGrp )

# Reposition the pivots in correct position
cmds.xform( 'L_Thigh01Root_Piv', t=( 8.18672105889799, 110.15641829480403, 13.103315251041547 ), ro=( 80.22597469797739, -0.751229063837106, -85.93709126984183 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Thigh01RootUp_Piv', t=( 9.189463122997797, 109.87594373477955, 18.799406069430134 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Thigh01Tip_Piv', t=( 10.977568868750481, 70.8654319656375, 13.619803428649902 ), ro=( 80.23664311099986, -0.7855102308340269, -85.75133089662721 ), s=( 1.0, 1.0, 1.0 ) )

cmds.xform( 'L_Thigh02Root_Piv', t=( 16.749150510793726, 110.83746545085914, 4.540830423921371 ), ro=( -0.004690867708520119, -0.24460102484470458, -83.25934289867274 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Thigh02RootUp_Piv', t=( 23.16639078928144, 111.4714300203224, 4.540830423921371 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'L_Thigh02Tip_Piv', t=( 21.261876064455148, 72.65630080180334, 4.704964927668026 ), ro=( -0.006320025973459553, -0.2559955114369971, -82.94377116162292 ), s=( 1.0, 1.0, 1.0 ) )

cmds.xform( 'R_Thigh01Root_Piv', t=( 8.18672105889799, 110.15641829480403, 13.103315251041547 ), ro=( 80.22597469797739, -0.751229063837106, -85.93709126984183 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Thigh01RootUp_Piv', t=( 9.189463122997797, 109.87594373477955, 18.799406069430134 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Thigh01Tip_Piv', t=( 10.977568868750481, 70.8654319656375, 13.619803428649902 ), ro=( 80.23664311099986, -0.7855102308340269, -85.75133089662721 ), s=( 1.0, 1.0, 1.0 ) )

cmds.xform( 'R_Thigh02Root_Piv', t=( 16.749150510793726, 110.83746545085914, 4.540830423921371 ), ro=( -0.004690867708520119, -0.24460102484470458, -83.25934289867274 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Thigh02RootUp_Piv', t=( 23.16639078928144, 111.4714300203224, 4.540830423921371 ), ro=( 0.0, 0.0, 0.0 ), s=( 1.0, 1.0, 1.0 ) )
cmds.xform( 'R_Thigh02Tip_Piv', t=( 21.261876064455148, 72.65630080180334, 4.704964927668026 ), ro=( -0.006320025973459553, -0.2559955114369971, -82.94377116162292 ), s=( 1.0, 1.0, 1.0 ) )

# Add SpaceOUTs to the joints to attach this function properly
# Do this to the joints that connects to the root or tip of the halfMuscles
L_HipRest_Jx_SpaceOUT = denUt.den_AddSpaceOUTs(Jnts=['L_HipRest_Jx'])
L_HipTwist03_Jnt_SpaceOUT = denUt.den_AddSpaceOUTs(Jnts=['L_HipTwist03_Jnt'])
R_HipRest_Jx_SpaceOUT = denUt.den_AddSpaceOUTs(Jnts=['R_HipRest_Jx'])
R_HipTwist03_Jnt_SpaceOUT = denUt.den_AddSpaceOUTs(Jnts=['R_HipTwist03_Jnt'])


# ---------------------------------------------------------------------------------------
# Create half muscle rig for the 4 muscle groups

# - Make half muscle rig for left side thigh01 -
L_Thigh01RigRet = jlyBR.jly_makeHalfMuscleRig( side='L_', prefix='', name='Thigh01', radius=2.0 )
print( L_Thigh01RigRet )
# Capture the list content (rig group, spaceINs, spaceOUTs, joints, contrls, guts) in 6 variables, so the master rig group will contain them
L_Thigh01RigGrp = L_Thigh01RigRet[0]; print( L_Thigh01RigGrp )
L_Thigh01SpaceINs = L_Thigh01RigRet[1]; print( L_Thigh01SpaceINs )
L_Thigh01SpaceOUTs = L_Thigh01RigRet[2]; print( L_Thigh01SpaceOUTs )
L_Thigh01BindJoints = L_Thigh01RigRet[3]; print( L_Thigh01BindJoints )
L_Thigh01CtrlsALL = L_Thigh01RigRet[4]; print( L_Thigh01CtrlsALL )
L_Thigh01GutsALL = L_Thigh01RigRet[5]; print( L_Thigh01GutsALL )
# Capture specific things in variables (thigh spaceINs) for future connection
L_Thigh01RootSpaceIN = L_Thigh01SpaceINs[0]
L_Thigh01TipSpaceIN = L_Thigh01SpaceINs[1]
# Parent the muscle rig under RootRigGrp
L_Thigh01RigGrp = cmds.parent( L_Thigh01RigGrp, RootRigGrp )
# Connect arm spaceINs to its spaceOUTs with parent constraint (translate, rotate)
cmds.parentConstraint( L_HipRest_Jx_SpaceOUT, L_Thigh01RootSpaceIN, mo=True )
cmds.parentConstraint( L_HipTwist03_Jnt_SpaceOUT, L_Thigh01TipSpaceIN, mo=True )
# Connect arm spaceINs to its spaceOUTs with scale constraint (scale)
cmds.scaleConstraint( L_HipRest_Jx_SpaceOUT, L_Thigh01RootSpaceIN, mo=True )
cmds.scaleConstraint( L_HipTwist03_Jnt_SpaceOUT, L_Thigh01TipSpaceIN, mo=True )

# Add safety cover, lock things we dont want to touch, add attributes needed, etc. at the top level of the rig
denUt.den_AddSafetyCovers( rigGroup=L_Thigh01RigGrp[0] )

# Connect visibility of the stretchable proxy for half muscles to the AllCtrl
cmds.connectAttr( AllCtrl+'.Show_Proxy_Geo', 'L_Thigh01_DispMesh.visibility', force=True, lock=True )

# Connect visibility of the Controls to the AllCtrl
cmds.connectAttr( AllCtrl+'.Show_Controls', L_Thigh01RigGrp[0]+'.Show_Controls' )
cmds.connectAttr( AllCtrl+'.Show_Guts', L_Thigh01RigGrp[0]+'.Show_Guts' )
cmds.connectAttr( AllCtrl+'.Bone_Draw_Style', L_Thigh01RigGrp[0]+'.Bone_Draw_Style' )


# - Make half muscle rig for left side thigh02 -
L_Thigh02RigRet = jlyBR.jly_makeHalfMuscleRig( side='L_', prefix='', name='Thigh02', radius=2.0 )
print( L_Thigh02RigRet )
# Capture the list content (rig group, spaceINs, spaceOUTs, joints, contrls, guts) in 6 variables, so the master rig group will contain them
L_Thigh02RigGrp = L_Thigh02RigRet[0]; print( L_Thigh02RigGrp )
L_Thigh02SpaceINs = L_Thigh02RigRet[1]; print( L_Thigh02SpaceINs )
L_Thigh02SpaceOUTs = L_Thigh02RigRet[2]; print( L_Thigh02SpaceOUTs )
L_Thigh02BindJoints = L_Thigh02RigRet[3]; print( L_Thigh02BindJoints )
L_Thigh02CtrlsALL = L_Thigh02RigRet[4]; print( L_Thigh02CtrlsALL )
L_Thigh02GutsALL = L_Thigh02RigRet[5]; print( L_Thigh02GutsALL )
# Capture specific things in variables (thigh spaceINs) for future connection
L_Thigh02RootSpaceIN = L_Thigh02SpaceINs[0]
L_Thigh02TipSpaceIN = L_Thigh02SpaceINs[1]
# Parent the muscle rig under RootRigGrp
L_Thigh02RigGrp = cmds.parent( L_Thigh02RigGrp, RootRigGrp )

# Connect arm spaceINs to its spaceOUTs with parent constraint (translate, rotate)
cmds.parentConstraint( L_HipRest_Jx_SpaceOUT, L_Thigh02RootSpaceIN, mo=True )
cmds.parentConstraint( L_HipTwist03_Jnt_SpaceOUT, L_Thigh02TipSpaceIN, mo=True )
# Connect arm spaceINs to its spaceOUTs with scale constraint (scale)
cmds.scaleConstraint( L_HipRest_Jx_SpaceOUT, L_Thigh02RootSpaceIN, mo=True )
cmds.scaleConstraint( L_HipTwist03_Jnt_SpaceOUT, L_Thigh02TipSpaceIN, mo=True )

# Add safety cover, lock things we dont want to touch, add attributes needed, etc. at the top level of the rig
denUt.den_AddSafetyCovers( rigGroup=L_Thigh02RigGrp[0] )
# Connect visibility of the stretchable proxy for half muscles to the AllCtrl
cmds.connectAttr( AllCtrl+'.Show_Proxy_Geo', 'L_Thigh02_DispMesh.visibility', force=True, lock=True )
# Connect visibility of the Controls to the AllCtrl
cmds.connectAttr( AllCtrl+'.Show_Controls', L_Thigh02RigGrp[0]+'.Show_Controls' )
cmds.connectAttr( AllCtrl+'.Show_Guts', L_Thigh02RigGrp[0]+'.Show_Guts' )
cmds.connectAttr( AllCtrl+'.Bone_Draw_Style', L_Thigh02RigGrp[0]+'.Bone_Draw_Style' )

# - Make half muscle rig for right side thigh01 -
R_Thigh01RigRet = jlyBR.jly_makeHalfMuscleRig( side='R_', prefix='', name='Thigh01', radius=2.0 )
print( R_Thigh01RigRet )
# Capture the list content (rig group, spaceINs, spaceOUTs, joints, contrls, guts) in 6 variables, so the master rig group will contain them
R_Thigh01RigGrp = R_Thigh01RigRet[0]; print( R_Thigh01RigGrp )
R_Thigh01SpaceINs = R_Thigh01RigRet[1]; print( R_Thigh01SpaceINs )
R_Thigh01SpaceOUTs = R_Thigh01RigRet[2]; print( R_Thigh01SpaceOUTs )
R_Thigh01BindJoints = R_Thigh01RigRet[3]; print( R_Thigh01BindJoints )
R_Thigh01CtrlsALL = R_Thigh01RigRet[4]; print( R_Thigh01CtrlsALL )
R_Thigh01GutsALL = R_Thigh01RigRet[5]; print( R_Thigh01GutsALL )
# Capture specific things in variables (thigh spaceINs) for future connection
R_Thigh01RootSpaceIN = R_Thigh01SpaceINs[0]
R_Thigh01TipSpaceIN = R_Thigh01SpaceINs[1]
# Parent the muscle rig under RootRigGrp
R_Thigh01RigGrp = cmds.parent( R_Thigh01RigGrp, RootRigGrp )

# Connect arm spaceINs to its spaceOUTs with parent constraint (translate, rotate)
cmds.parentConstraint( R_HipRest_Jx_SpaceOUT, R_Thigh01RootSpaceIN, mo=True )
cmds.parentConstraint( R_HipTwist03_Jnt_SpaceOUT, R_Thigh01TipSpaceIN, mo=True )
# Connect arm spaceINs to its spaceOUTs with scale constraint (scale)
cmds.scaleConstraint( R_HipRest_Jx_SpaceOUT, R_Thigh01RootSpaceIN, mo=True )
cmds.scaleConstraint( R_HipTwist03_Jnt_SpaceOUT, R_Thigh01TipSpaceIN, mo=True )

# Add safety cover, lock things we dont want to touch, add attributes needed, etc. at the top level of the rig
denUt.den_AddSafetyCovers( rigGroup=R_Thigh01RigGrp[0] )

# Connect visibility of the stretchable proxy for half muscles to the AllCtrl
cmds.connectAttr( AllCtrl+'.Show_Proxy_Geo', 'R_Thigh01_DispMesh.visibility', force=True, lock=True )
# Connect visibility of the Controls to the AllCtrl
cmds.connectAttr( AllCtrl+'.Show_Controls', R_Thigh01RigGrp[0]+'.Show_Controls' )
cmds.connectAttr( AllCtrl+'.Show_Guts', R_Thigh01RigGrp[0]+'.Show_Guts' )
cmds.connectAttr( AllCtrl+'.Bone_Draw_Style', R_Thigh01RigGrp[0]+'.Bone_Draw_Style' )

# - Make half muscle rig for right side thigh02 -
R_Thigh02RigRet = jlyBR.jly_makeHalfMuscleRig( side='R_', prefix='', name='Thigh02', radius=2.0 )
print( R_Thigh02RigRet )
# Capture the list content (rig group, spaceINs, spaceOUTs, joints, contrls, guts) in 6 variables, so the master rig group will contain them
R_Thigh02RigGrp = R_Thigh02RigRet[0]; print( R_Thigh02RigGrp )
R_Thigh02SpaceINs = R_Thigh02RigRet[1]; print( R_Thigh02SpaceINs )
R_Thigh02SpaceOUTs = R_Thigh02RigRet[2]; print( R_Thigh02SpaceOUTs )
R_Thigh02BindJoints = R_Thigh02RigRet[3]; print( R_Thigh02BindJoints )
R_Thigh02CtrlsALL = R_Thigh02RigRet[4]; print( R_Thigh02CtrlsALL )
R_Thigh02GutsALL = R_Thigh02RigRet[5]; print( R_Thigh02GutsALL )
# Capture specific things in variables (thigh spaceINs) for future connection
R_Thigh02RootSpaceIN = R_Thigh02SpaceINs[0]
R_Thigh02TipSpaceIN = R_Thigh02SpaceINs[1]
# Parent the muscle rig under RootRigGrp
R_Thigh02RigGrp = cmds.parent( R_Thigh02RigGrp, RootRigGrp )

# Connect arm spaceINs to its spaceOUTs with parent constraint (translate, rotate)
cmds.parentConstraint( R_HipRest_Jx_SpaceOUT, R_Thigh02RootSpaceIN, mo=True )
cmds.parentConstraint( R_HipTwist03_Jnt_SpaceOUT, R_Thigh02TipSpaceIN, mo=True )
# Connect arm spaceINs to its spaceOUTs with scale constraint (scale)
cmds.scaleConstraint( R_HipRest_Jx_SpaceOUT, R_Thigh02RootSpaceIN, mo=True )
cmds.scaleConstraint( R_HipTwist03_Jnt_SpaceOUT, R_Thigh02TipSpaceIN, mo=True )

# Add safety cover, lock things we dont want to touch, add attributes needed, etc. at the top level of the rig
denUt.den_AddSafetyCovers( rigGroup=R_Thigh02RigGrp[0] )

# Connect visibility of the stretchable proxy for half muscles to the AllCtrl
cmds.connectAttr( AllCtrl+'.Show_Proxy_Geo', 'R_Thigh02_DispMesh.visibility', force=True, lock=True )
# Connect visibility of the Controls to the AllCtrl
cmds.connectAttr( AllCtrl+'.Show_Controls', R_Thigh02RigGrp[0]+'.Show_Controls' )
cmds.connectAttr( AllCtrl+'.Show_Guts', R_Thigh02RigGrp[0]+'.Show_Guts' )
cmds.connectAttr( AllCtrl+'.Bone_Draw_Style', R_Thigh02RigGrp[0]+'.Bone_Draw_Style' )



# ===========================================================================================
# ---------------------------------------------------------------------------------------
# Create Eyeball Pivots 

# Make eyeball pivots for both sides
L_EyePivGrp = jlyBR.jly_makeEyePiv( side='L_', prefix='', radius=1.1 )
R_EyePivGrp = jlyBR.jly_makeEyePiv( side='R_', prefix='', radius=1.1  )

# Parent pivots under RootPivGrp
L_EyePivGrp = cmds.parent( L_EyePivGrp, RootPivGrp )
R_EyePivGrp = cmds.parent( R_EyePivGrp, RootPivGrp )

# Reposition the pivots, put them at the center of the eyeball geometry and lined up with the iris
cmds.setAttr( 'L_Eye_Piv.t', 3.32915752436325, 178.8296774824052, 13.760299417461985 )
cmds.setAttr( 'L_Eye_Piv.r', 2, 3,  -1.244 )

cmds.setAttr( 'R_Eye_Piv.t', 3.32915752436325, 178.8296774824052, 13.760299417461985 )
cmds.setAttr( 'R_Eye_Piv.r', 2, 3,  -1.244 )

# ---------------------------------------------------------------------------------------
# Create Eyeball Rig

# Create the left eyeball rig
L_EyeRigRet = jlyBR.jly_makeEyeRig( side='L_', prefix='', name='Eye', radius=1.03, ctrlRadius=10.0, displayLocalAxis=False )
print( L_EyeRigRet )

# Capture the list content (rig group, spaceINs, spaceOUTs, joints, contrls, guts) in 6 variables, so the master rig group will contain them
L_EyeRigGrp = L_EyeRigRet[0]; print( L_EyeRigGrp )
L_EyeSpaceINs = L_EyeRigRet[1]; print( L_EyeSpaceINs )
L_EyeSpaceOUTs = L_EyeRigRet[2]; print( L_EyeSpaceOUTs )
L_EyeBindJoints = L_EyeRigRet[3]; print( L_EyeBindJoints )
L_EyeCtrlsALL = L_EyeRigRet[4]; print( L_EyeCtrlsALL )
L_EyeGutsALL = L_EyeRigRet[5]; print( L_EyeGutsALL )
# Capture specific things in variables (head spaceIN) for future connection
L_EyeHeadSpaceIN = L_EyeSpaceINs[0]
# Parent left eyeball rig group under root rig group
L_EyeRigGrp = cmds.parent( L_EyeRigGrp, RootRigGrp )


# Create the right eyeball rig
R_EyeRigRet = jlyBR.jly_makeEyeRig( side='R_', prefix='', name='Eye', radius=1.03, ctrlRadius=10.0, displayLocalAxis=False )
print( R_EyeRigRet )
# Capture the list content (rig group, spaceINs, spaceOUTs, joints, contrls, guts) in 6 variables, so the master rig group will contain them
R_EyeRigGrp = R_EyeRigRet[0]; print( R_EyeRigGrp )
R_EyeSpaceINs = R_EyeRigRet[1]; print( R_EyeSpaceINs )
R_EyeSpaceOUTs = R_EyeRigRet[2]; print( R_EyeSpaceOUTs )
R_EyeBindJoints = R_EyeRigRet[3]; print( R_EyeBindJoints )
R_EyeCtrlsALL = R_EyeRigRet[4]; print( R_EyeCtrlsALL )
R_EyeGutsALL = R_EyeRigRet[5]; print( R_EyeGutsALL )
# Capture specific things in variables (head spaceIN) for future connection
R_EyeHeadSpaceIN = R_EyeSpaceINs[0]
# Parent right eyeball rig group under root rig group
R_EyeRigGrp = cmds.parent( R_EyeRigGrp, RootRigGrp )

# Connect proxy geometry, looks for matching geometry to match each of the bind joints
denUt.den_connectProxyGeo( Jnts=L_EyeBindJoints+R_EyeBindJoints )

# Connect eye spaceINs to its spaceOUTs with parent constraint (translate, rotate)
L_EyeHeadSpaceConstraint = cmds.parentConstraint( HeadSpaceOUT, L_EyeHeadSpaceIN, mo=True  )
R_EyeHeadSpaceConstraint = cmds.parentConstraint( HeadSpaceOUT, R_EyeHeadSpaceIN, mo=True  )
# Connect eye spaceINs to its spaceOUTs with scale constraint (scale)
L_EyeHeadSpaceConstraint = cmds.scaleConstraint( HeadSpaceOUT, L_EyeHeadSpaceIN, mo=True  )
R_EyeHeadSpaceConstraint = cmds.scaleConstraint( HeadSpaceOUT, R_EyeHeadSpaceIN, mo=True  )

# Add safety cover for left eye control, lock things we dont want to touch, add attributes needed, etc. at the top level of the rig
denUt.den_AddSafetyCovers( rigGroup=L_EyeRigGrp[0] )
# Connect control attributes (visibility, show guts, bone draw style, color) to the All_Ctrl
cmds.connectAttr( AllCtrl+'.Show_Controls', L_EyeRigGrp[0]+'.Show_Controls' )
cmds.connectAttr( AllCtrl+'.Show_Guts', L_EyeRigGrp[0]+'.Show_Guts' )
cmds.connectAttr( AllCtrl+'.Bone_Draw_Style', L_EyeRigGrp[0]+'.Bone_Draw_Style' )
cmds.connectAttr( AllCtrl+'.Left_Color', L_EyeRigGrp[0]+'.Ctrl_Color' )

# Add safety cover for right eye control, lock things we dont want to touch, add attributes needed, etc. at the top level of the rig
denUt.den_AddSafetyCovers( rigGroup=R_EyeRigGrp[0] )
# Connect control attributes (visibility, show guts, bone draw style, color) to the All_Ctrl
cmds.connectAttr( AllCtrl+'.Show_Controls', R_EyeRigGrp[0]+'.Show_Controls' )
cmds.connectAttr( AllCtrl+'.Show_Guts', R_EyeRigGrp[0]+'.Show_Guts' )
cmds.connectAttr( AllCtrl+'.Bone_Draw_Style', R_EyeRigGrp[0]+'.Bone_Draw_Style' )
cmds.connectAttr( AllCtrl+'.Right_Color', R_EyeRigGrp[0]+'.Ctrl_Color' )




'''
#################################


# ---------------------------------------------------------------------------------------


# ===================================================================================================
# ---------------------------- Paint Weight Transfer ----------------------------
# Use this section of code after you've completed the proxy model rig.
# This script transfers skin weights from the proxy model to your final render geometry,
# giving you a solid starting point for further weight painting and refinement.
# ===================================================================================================


# -------------------------------------------------------------------------------------------
# set up the body point weighting
# Capture skin weights from proxy meshes to the body geometry

# Capture all joints in a BindJoints list
BindJoints = cmds.ls( '*_Jnt' )
# Prints the entire list of bind joints and meshes
print(BindJoints)

# Make a list for idea mesh parts for each joint in a list, to do that, just for each joint in BindJoints, replaces '_Jnt' with '_Mesh'
Meshes = [s.replace('_Jnt', '_Mesh') for s in BindJoints] 
print(Meshes)

# To check if each joint has a mesh part for it, prints the entire list of bind joints and meshes
for i, node in enumerate(BindJoints):
    # For each joint in the list, finds the corresponding mesh from the Meshes list.
    mesh = cmds.ls( Meshes[i] )
    # Print the list, and looking for empty [] if there is a mesh piece missing
    print(i, BindJoints[i], mesh)


# Add skin cluster temporarily to the full body worth of joints, bind the proxy geometry part weifht 100% to its matching joint temporarily
denUt.den_tempBindProxyGeo( Jnts=BindJoints )

# Create the body geo skin cluster with the same list of bind joint, capture from the body _Jnt joints
BodySkinClust = cmds.skinCluster( 'Body_Geo', BindJoints, tsb=True, name='Body_Geo_skinCluster' )[0]

# Select the all proxy meshes, and then selecr the body geometry to copy skin weight
cmds.select( Meshes )
cmds.select( 'Body_Geo', add=True )

# Transfer weights from proxy meshes to body geometry, make this a good starting point for weight painting
cmds.copySkinWeights( noMirror=True, surfaceAssociation='closestPoint', influenceAssociation='closestJoint' )

# Remove temporary binding of proxy geometry, so it does no double transforms
for i, node in enumerate(BindJoints):
    print(i, BindJoints[i], Meshes[i])
    cmds.skinCluster( Meshes[i], e=True, ub=True )


# -------------------------------------------------------------------------------------------
# ===============================================================================================
# Bind both eyeballs to the render geo rig
EyeBindJoints = cmds.ls( '*_Eye_Jnt' )
print(EyeBindJoints)
# Bind weight for both eyeballs
EyesSkinClust = cmds.skinCluster( 'Eyes_Geo', EyeBindJoints, tsb=True, name='Eyes_Geo_skinCluster', mi=1 )[0]

# Bind the hair to the head
cmds.parentConstraint('Head_Jnt', 'Hair_Geo', mo=True, name=f'Hair_Geo_parentConstraint1')

# Bind the top teeth to the head
cmds.parentConstraint('Head_Jnt', 'T_Teeth_Geo', mo=True, name=f'T_Teeth_Geo_parentConstraint1')

# Bind the tongue and botton teeth to the Jaw
cmds.parentConstraint('Jaw_Jnt', 'Tongue_Geo', mo=True, name=f'Tongue_Geo_parentConstraint1')
cmds.parentConstraint('Jaw_Jnt', 'B_Teeth_Geo', mo=True, name=f'B_Teeth_Geo_parentConstraint1')

# -------------------------------------------------------------------------------------------
# Now we have the basic skin weights. You can refine your weight manuly.
# -------------------------------------------------------------------------------------------
#################################

'''