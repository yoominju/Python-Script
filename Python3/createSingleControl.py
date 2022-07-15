#load maya.cmds command and set shortcut as "cmds"
import maya.cmds as cmds

#0. Select Joints
selectedJoint = cmds.ls(sl=True)
#return the control name as List
print(selectedJoint)

#1. Create nurbs circle control
createControl = cmds.circle(center=(0,0,0), normal=(0,1,0), sweep=360, radius=1, degree=3, useTolerance=False, 
                            tolerance=0, constructionHistory=False, name= selectedJoint[0] + "_FK")
#return the control name as List
print(createControl)

#2. Create POS group on top of circle control
controlPOS = cmds.group(createControl[0], name= createControl[0] + "_POS")
#return the group name as String
print(controlPOS)

#3. Do parentConstraint with maintain offset turned off to move the control position to match with the joint
moveControlPos = cmds.parentConstraint(selectedJoint[0], controlPOS, maintainOffset=False)
#return the control name as List
print(moveControlPos)

#4. remove parentConstraint
cmds.delete(moveControlPos)

#5. Do parentConstraint to connect the joint to the Controller to make the controller can control the joint
connectJoint = cmds.parentConstraint(createControl[0], selectedJoint[0], maintainOffset=True)
connectScaleJoint = cmds.scaleConstraint(createControl[0], selectedJoint[0], maintainOffset=True)
