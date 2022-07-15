# mocapTools
# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
from functools import partial

##############################################################################################################################
#		os : windows
#		maya 2018 sp6
#		coding: utf-8
#		command : execfile(r'\\mofac\bob01\bob_tong\ip_tlool\work\animation\05_maya_scripts\Scripts\mocapTools.py')
#		require file : //mofac/bob01/bob_tong/ip_tlool/work/animation/05_maya_scripts/Scripts/HikDefCustomRig.mel
#		You want to change the path to "HikDefCustomRig.mel", please correct line 20.
##############################################################################################################################

# print help(cmds)
# MAYA_LOCATION = os.environ['MAYA_LOCATION']
# mel.eval('source "'+MAYA_LOCATION+'/scripts/others/hikGlobalUtils.mel"')
# mel.eval('source "'+MAYA_LOCATION+'/scripts/others/hikCharacterControlsUI.mel"')
# mel.eval('source "'+MAYA_LOCATION+'/scripts/others/hikDefinitionOperations.mel"')
mel.eval('source "D:/RiggingStudy/MJ/Tool_Mocap/HikDefCustomRig.mel"')


# mel.eval('source "C:/Users/PC/Downloads/scripts/HikDefCustomRig.mel"')

def removeNS():
    defaults = ['UI', 'shared']

    # Used as a sort key, this will sort namespaces by how many children they have.
    def num_children(ns):
        return ns.count(':')

    namespaces = [ns for ns in cmds.namespaceInfo(lon=True, r=True) if ns not in defaults]
    # We want to reverse the list, so that namespaces with more children are at the front of the list.
    namespaces.sort(key=num_children, reverse=True)
    for ns in namespaces:
        try:
            cmds.namespace(rm=ns)
        except RuntimeError as e:
            # namespace isn't empty, so you might not want to kill it?
            pass


def cleanUp():
    allLoc = cmds.ls(l=True, type='locator')
    allLocParents = cmds.listRelatives(*allLoc, p=True, f=True)
    if cmds.objExists('*:Hips'):
        jntLocParents = cmds.listRelatives('*:Hips', p=True, f=True)
        jntLocNumb = len(jntLocParents)

        for s in range(0, jntLocNumb):
            allLocParents.remove(jntLocParents[s])

    if cmds.objExists('*Hips'):
        jntLocParents = cmds.listRelatives('*Hips', p=True, f=True)
        jntLocNumb = len(jntLocParents)

        for s in range(0, jntLocNumb):
            allLocParents.remove(jntLocParents[s])

    cmds.delete(allLocParents)
    cmds.SelectNone()
    removeNS()


def createNS():
    NS = cmds.textField(nsTxt, q=True, tx=True)
    selObj = cmds.ls(sl=True, type='transform')
    selObjFirst = cmds.ls(sl=True, type='transform')
    showName = cmds.ls(showNamespace=True, selection=True)
    if len(selObj) == 1:
        if (cmds.referenceQuery(selObj, isNodeReferenced=True)) == False:
            if selObj == (cmds.ls(sl=True, type='joint')):
                cmds.confirmDialog(t='info', m='선택한 오브젝트에 joint가 있습니다.', b='OK')
                pass
            else:
                if showName[1] == ':':
                    if NS != '':
                        selObjChildren = cmds.listRelatives(selObj, ad=True, ni=True, f=True)
                        selObjChildrenNumb = len(selObjChildren)
                        # print selObjChildrenNumb
                        cmds.select(selObjChildren)

                        selObjShape = cmds.listRelatives(selObj, shapes=True, f=True)
                        selObjShapeNumb = len(selObjShape)
                        # print selObjShapeNumb
                        cmds.select(selObjShape)

                        for x in range(0, selObjChildrenNumb):
                            selObj.append(selObjChildren[x])

                        for s in range(0, selObjShapeNumb):
                            selObj.remove(selObjShape[s])

                        cmds.select(selObj)
                        selNumb = len(selObj)
                        # print selNumb

                        cmds.namespace(set=':')

                        nsList = cmds.namespaceInfo(lon=True, r=True)
                        nsListNum = len(nsList)
                        nsNum = []
                        for i in range(0, nsListNum):
                            if NS == nsList[i]:
                                nsNum.append(NS)
                        # print len(nsNum)
                        if len(nsNum) == 0:
                            cmds.namespace(add=NS)
                            selObj = cmds.ls(sl=True, type='transform')
                            selObj.sort(key=len, reverse=True)
                            for obj in selObj:
                                shortName = obj.split("|")[-1]
                                children = cmds.listRelatives(obj, c=True, f=True) or []
                                if len(children) == 1:
                                    child = children[0]
                                    objtype = cmds.objectType(child)
                                else:
                                    objType = cmds.objectType(obj)

                                # print obj, shortName
                                cmds.rename(obj, (NS + ':' + shortName))
                                try:
                                    cmds.select(selObjFirst)
                                except:
                                    pass
                        else:
                            cmds.select(selObjFirst)
                            cmds.confirmDialog(t='info', m='중복된 namespace가 있습니다.', b='OK')
                    else:
                        cmds.select(selObjFirst)
                        cmds.confirmDialog(t='info', m='변경할 namespace를 입력하세요.', b='OK')
                else:
                    cmds.SelectNone()
                    cmds.confirmDialog(t='info', m='이미 namespace가 있습니다.', b='OK')
        else:
            cmds.SelectNone()
            cmds.confirmDialog(t='info', m='레퍼런스에는 적용이 안됩니다.', b='OK')
    else:
        if len(selObj) == 0:
            cmds.confirmDialog(t='info', m='오브젝트를 선택하세요.', b='OK')
        else:
            cmds.confirmDialog(t='info', m='오브젝트 하나만 선택하세요.', b='OK')


def deleteNS():
    selObj = cmds.ls(sl=True, type='transform')
    selObjFirst = cmds.ls(sl=True, type='transform')

    showName = cmds.ls(showNamespace=True, selection=True)
    if len(selObj) == 1:
        if (cmds.referenceQuery(selObj, isNodeReferenced=True)) == False:
            if selObj == (cmds.ls(sl=True, type='joint')):
                cmds.confirmDialog(t='info', m='선택한 오브젝트에 joint가 있습니다.', b='OK')
                pass
            else:
                if showName[1] != ':':
                    selObjChildren = cmds.listRelatives(selObj, ad=True, ni=True, f=True)
                    selObjChildrenNumb = len(selObjChildren)
                    # print selObjChildrenNumb
                    cmds.select(selObjChildren)
                    selObjShape = cmds.listRelatives(selObj, shapes=True, f=True)
                    selObjShapeNumb = len(selObjShape)
                    # print selObjShapeNumb
                    cmds.select(selObjShape)
                    for x in range(0, selObjChildrenNumb):
                        selObj.append(selObjChildren[x])
                    for s in range(0, selObjShapeNumb):
                        selObj.remove(selObjShape[s])
                    cmds.select(selObj)
                    selNumb = len(selObj)
                    cmds.namespace(set=':')
                    selObj.sort(key=len, reverse=True)
                    for obj in selObj:
                        shortName = obj.split(":")[-1]
                        children = cmds.listRelatives(obj, c=True, f=True) or []
                        if len(children) == 1:
                            child = children[0]
                            objtype = cmds.objectType(child)
                        else:
                            objType = cmds.objectType(obj)
                        # print obj, shortName
                        cmds.rename(obj, shortName)
                    cmds.select(shortName)
                    removeNS()
                else:
                    cmds.SelectNone()
                    cmds.confirmDialog(t='info', m='삭제할 namespace가 없습니다.', b='OK')
        else:
            cmds.confirmDialog(t='info', m='레퍼런스에는 적용이 안됩니다.', b='OK')
    else:
        if len(selObj) == 0:
            cmds.confirmDialog(t='info', m='오브젝트를 선택하세요.', b='OK')
        else:
            cmds.confirmDialog(t='info', m='오브젝트 하나만 선택하세요.', b='OK')


def renameNS():
    NS = cmds.textField(nsTxt, q=True, tx=True)
    selObj = cmds.ls(sl=True, type='transform')
    selObjFirst = cmds.ls(sl=True, type='transform')

    showName = cmds.ls(showNamespace=True, selection=True)
    if len(selObj) == 1:
        if (cmds.referenceQuery(selObj, isNodeReferenced=True)) == False:
            if showName[1] != ':':
                if NS != '':
                    if selObj == (cmds.ls(sl=True, type='joint')):
                        cmds.confirmDialog(t='info', m='선택한 오브젝트에 joint가 포함되어 있습니다.', b='OK')
                        pass
                    else:
                        deleteNS()
                        createNS()
                        cmds.confirmDialog(t='info', m='선택한 오브젝트의 namespace가 삭제되었습니다.', b='OK')
                else:
                    cmds.select(selObjFirst)
                    cmds.confirmDialog(t='info', m='변경할 namespace를 입력하세요.', b='OK')
            else:
                cmds.SelectNone()
                cmds.confirmDialog(t='info', m='선택한 오브젝트에 namespace가 없습니다.', b='OK')
        else:
            cmds.confirmDialog(t='info', m='레퍼런스에는 적용이 안됩니다.', b='OK')
    else:
        if len(selObj) == 0:
            cmds.confirmDialog(t='info', m='오브젝트를 선택하세요.', b='OK')
        else:
            cmds.confirmDialog(t='info', m='오브젝트 하나만 선택하세요.', b='OK')


def selectMocap():
    try:
        # cmds.select('*:suit*')
        selObj = cmds.ls('*:suit*', sns=True, type='transform')
        RN = []
        NS = []

        for i in range(0, len(selObj), 2):
            RN.append(selObj[i])

        for x in range(1, len(selObj), 2):
            NS.append(selObj[x])
        # print NS
        cmds.select(RN)
    except:
        pass


def selectRig():
    try:
        # cmds.select('*:Main')
        cmds.select('*:WorldCtrl')
        cmds.pickWalk(d='up')
        cmds.pickWalk(d='up')
    # cmds.pickWalk (d = 'up')
    # cmds.pickWalk (d = 'up')

    except:
        pass


def customTpose():
    mel.eval('optionVar -iv refLockEditable true;')
    selObj = cmds.ls(sl=True, type='transform')
    selObjNum = len(selObj)
    NS = []

    if selObjNum >= 1:
        showName = cmds.ls(showNamespace=True, selection=True)
        if showName[1] != ':':
            # print (cmds.ls(showNamespace = True, selection = True))[1]
            for i in range(0, selObjNum):
                showName = cmds.ls(selObj[i], showNamespace=True, selection=True)
                NS.append(showName[1])
            if cmds.objExists('FK_arm_R_loc'):
                pass
            else:
                cmds.spaceLocator(n='FK_arm_R_loc', p=(0, 0, 0))
                cmds.setAttr('FK_arm_R_loc.rotate', 90, 0, -180, type="double3")

                cmds.spaceLocator(n='FK_arm_L_loc', p=(0, 0, 0))
                cmds.setAttr('FK_arm_L_loc.rotate', -90, 0, 180, type="double3")

                cmds.spaceLocator(n='FK_leg_R_loc', p=(0, 0, 0))
                cmds.setAttr('FK_leg_R_loc.rotate', 90, 0, -90, type="double3")

                cmds.spaceLocator(n='FK_leg_L_loc', p=(0, 0, 0))
                cmds.setAttr('FK_leg_L_loc.rotate', -90, 0, 90, type="double3")

                cmds.SelectNone()
            for x in NS:
                try:
                    cmds.setAttr((x + ':' + 'FKIKLeg_L.FKIKBlend'), 0)
                    cmds.setAttr((x + ':' + 'FKIKLeg_R.FKIKBlend'), 0)
                    cmds.setAttr((x + ':' + 'FKIKArm_R.FKIKBlend'), 0)
                    cmds.setAttr((x + ':' + 'FKIKArm_L.FKIKBlend'), 0)
                    cmds.setAttr((x + ':' + 'FKIKSpine_M.FKIKBlend'), 0)

                    # print (x + ':' + 'FKIKLeg_R.FKIKBlend')

                    cmds.matchTransform((x + ':' + 'FKScapula_R'), (x + ':' + 'FKShoulder_R'), (x + ':' + 'FKElbow_R'),
                                        (x + ':' + 'FKWrist_R'), 'FK_arm_R_loc', rot=True)
                    cmds.matchTransform((x + ':' + 'FKScapula_L'), (x + ':' + 'FKShoulder_L'), (x + ':' + 'FKElbow_L'),
                                        (x + ':' + 'FKWrist_L'), 'FK_arm_L_loc', rot=True)
                    cmds.matchTransform((x + ':' + 'FKHip_R'), (x + ':' + 'FKKnee_R'), (x + ':' + 'FKAnkle_R'),
                                        'FK_leg_R_loc', rot=True)
                    cmds.matchTransform((x + ':' + 'FKHip_L'), (x + ':' + 'FKKnee_L'), (x + ':' + 'FKAnkle_L'),
                                        'FK_leg_L_loc', rot=True)

                    cmds.setAttr((x + ':' + 'FKIKLeg_L.FKIKBlend'), 10)
                    cmds.setAttr((x + ':' + 'FKIKLeg_R.FKIKBlend'), 10)

                    cmds.matchTransform((x + ':' + 'IKLeg_R'), (x + ':' + 'FKAnkle_R'), pos=True)
                    cmds.matchTransform((x + ':' + 'IKLeg_L'), (x + ':' + 'FKAnkle_L'), pos=True)

                    cmds.setAttr((x + ':' + 'PoleLeg_R.rx'), lock=False)
                    cmds.setAttr((x + ':' + 'PoleLeg_R.ry'), lock=False)
                    cmds.setAttr((x + ':' + 'PoleLeg_R.rz'), lock=False)
                    cmds.matchTransform((x + ':' + 'PoleLeg_R'), (x + ':' + 'FKKnee_R'), pos=True)
                    cmds.move(0, 0, 0.001, (x + ':' + 'PoleLeg_R'), relative=True)

                    cmds.setAttr((x + ':' + 'PoleLeg_L.rx'), lock=False)
                    cmds.setAttr((x + ':' + 'PoleLeg_L.ry'), lock=False)
                    cmds.setAttr((x + ':' + 'PoleLeg_L.rz'), lock=False)
                    cmds.matchTransform((x + ':' + 'PoleLeg_L'), (x + ':' + 'FKKnee_L'), pos=True)
                    cmds.move(0, 0, 0.001, (x + ':' + 'PoleLeg_L'), relative=True)

                except:
                    pass
            cmds.SelectNone()
            cmds.delete('FK_arm_R_loc', 'FK_arm_L_loc', 'FK_leg_R_loc', 'FK_leg_L_loc')
            cmds.select(selObj)
            print ("sel:", selObj)
        else:
            cmds.confirmDialog(t='info', m='namespace가 있는 레퍼런스 캐릭터만 적용됩니다.', b='OK')
    else:
        cmds.confirmDialog(t='info', m='캐릭터를 선택하세요.', b='OK')
    mel.eval('optionVar -iv refLockEditable false;')


def mocapBasicTpose():
    selObj = cmds.ls(sl=True, type='transform')
    selObjNum = len(selObj)
    NS = []
    # print selObjNum
    # showName = cmds.ls(showNamespace = True, selection = True)
    # NS.append(showName[1])

    # selObjChildren.sort(reverse=True)
    # print selObjChildren[0]
    if selObjNum >= 1:
        showName = cmds.ls(showNamespace=True, selection=True)
        if showName[1] != ':':
            # print (cmds.ls(showNamespace = True, selection = True))[1]
            for i in range(0, selObjNum):
                try:
                    showName = cmds.ls(selObj[i], showNamespace=True, selection=True)
                    NS.append(showName[1])
                    selObjShape = cmds.listRelatives(selObj[i], shapes=True, f=True)
                    selObjChildren = cmds.listRelatives(selObj[i], ad=True, ni=True, f=True)
                    # selObjChildren.sort(reverse=True)
                    selObjChildren.remove(selObjShape[0])
                    # cmds.select(selObjChildren)
                    selObjChildren.sort(reverse=True)
                    # print selObjChildren
                    selObjChildrenNumb = len(selObjChildren)
                    # print selObjChildrenNumb
                    SN = []
                    for x in NS:
                        for obj in selObjChildren:
                            shortName = obj.split(":")[-1]
                            SN.append(shortName)
                            # print shortName
                            cmds.setAttr((x + ':' + shortName + '.rotate'), 0, 0, 0, type="double3")
                            cmds.setAttr((x + ':' + 'Hips' + '.rotate'), 0, 0, 0, type="double3")
                            cmds.setAttr((x + ':' + 'RightShoulder' + '.translateX'), -0.01)
                            cmds.setAttr((x + ':' + 'LeftShoulder' + '.translateX'), 0.01)
                    LeftUpLegTY = cmds.getAttr(x + ':' + 'LeftUpLeg.translateY')
                    LeftLegTY = cmds.getAttr(x + ':' + 'LeftLeg.translateY')
                    LeftFootTY = cmds.getAttr(x + ':' + 'LeftFoot.translateY')
                    LeftToeBaseTY = cmds.getAttr(x + ':' + 'LeftToeBase.translateY')
                    HipsTY = -(LeftUpLegTY + LeftLegTY + LeftFootTY + LeftToeBaseTY)

                    if (cmds.checkBox(offSetBox, q=True, v=True)) == 0:
                        cmds.setAttr((x + ':' + 'Hips' + '.translate'), 0, HipsTY, 0, type="double3")
                    else:
                        cmds.setAttr((x + ':' + 'Hips' + '.translateY'), HipsTY)
                # SN.sort(reverse=True)
                # print SN[-1]
                except:
                    pass
        else:
            cmds.confirmDialog(t='info', m='namespace가 있는 mocap 캐릭터만 적용됩니다.', b='OK')
    else:
        cmds.confirmDialog(t='info', m='캐릭터를 선택하세요.', b='OK')


def mocapMonkTpose():
    selObj = cmds.ls(sl=True, type='transform')
    selObjNum = len(selObj)
    NS = []
    # print selObjNum
    # showName = cmds.ls(showNamespace = True, selection = True)
    # NS.append(showName[1])

    # selObjChildren.sort(reverse=True)
    # print selObjChildren[0]
    if selObjNum >= 1:
        showName = cmds.ls(showNamespace=True, selection=True)
        if showName[1] != ':':
            # print (cmds.ls(showNamespace = True, selection = True))[1]
            for i in range(0, selObjNum):
                try:
                    showName = cmds.ls(selObj[i], showNamespace=True, selection=True)
                    NS.append(showName[1])
                    selObjShape = cmds.listRelatives(selObj[i], shapes=True, f=True)
                    selObjChildren = cmds.listRelatives(selObj[i], ad=True, ni=True, f=True)
                    # selObjChildren.sort(reverse=True)
                    selObjChildren.remove(selObjShape[0])
                    # cmds.select(selObjChildren)
                    selObjChildren.sort(reverse=True)
                    # print selObjChildren
                    selObjChildrenNumb = len(selObjChildren)
                    # print selObjChildrenNumb
                    SN = []
                    for x in NS:
                        for obj in selObjChildren:
                            shortName = obj.split(":")[-1]
                            SN.append(shortName)
                            print (shortName)
                            cmds.setAttr((x + ':' + shortName + '.rotate'), 0, 0, 0, type="double3")
                            cmds.setAttr((x + ':' + 'Root_Jnt' + '.translate'), 0, 87.917, -0.31, type="double3")
                            cmds.setAttr((x + ':' + 'Pelvis_Jnt' + '.translate'), 0, -0.5, 0, type="double3")
                            cmds.setAttr((x + ':' + 'UpLeg_R_Jnt' + '.translate'), -5.043, -4.524, 0, type="double3")
                            cmds.setAttr((x + ':' + 'UpLeg_L_Jnt' + '.translate'), 5.043, -4.524, 0, type="double3")
                            cmds.setAttr((x + ':' + 'LowLeg_R_Jnt' + '.translate'), 0, -34.974, -0.879, type="double3")
                            cmds.setAttr((x + ':' + 'LowLeg_L_Jnt' + '.translate'), 0, 34.974, 0.879, type="double3")
                            cmds.setAttr((x + ':' + 'Ankle_R_Jnt' + '.translate'), 0, -39.966, 0.879, type="double3")
                            cmds.setAttr((x + ':' + 'Ankle_L_Jnt' + '.translate'), 0, 39.966, -0.879, type="double3")
                            cmds.setAttr((x + ':' + 'Ball_R_Jnt' + '.translate'), 0, -8.05, -12.649, type="double3")
                            cmds.setAttr((x + ':' + 'Ball_L_Jnt' + '.translate'), 0, 8.05, 12.649, type="double3")
                        # cmds.setAttr((x + ':' + 'Clav_R_Jnt' + '.translateX'), -0.01)
                        # cmds.setAttr((x + ':' + 'Clav_L_Jnt' + '.translateX'), 0.01)

                    UpLeg_L_JntTY = cmds.getAttr(x + ':' + 'UpLeg_L_Jnt.translateY')
                    LowLeg_L_JntTY = cmds.getAttr(x + ':' + 'LowLeg_L_Jnt.translateY')
                    Ankle_L_JntTY = cmds.getAttr(x + ':' + 'Ankle_L_Jnt.translateY')
                    # Ball_L_JntTY = cmds.getAttr(x + ':' + 'Ball_L_Jnt.translateY')
                    Ball_L_JntTY = cmds.getAttr(x + ':' + 'Ball_L_Jnt.translateY')
                    # rootTZ = -(LowLeg_L_JntTY + Ankle_L_JntTY + Ball_L_JntTY-1)
                    rootTY = (UpLeg_L_JntTY + LowLeg_L_JntTY + Ankle_L_JntTY + Ball_L_JntTY)

                    if (cmds.checkBox(offSetBox, q=True, v=True)) == 0:
                        cmds.setAttr((x + ':' + 'Root_Jnt' + '.translate'), 0, rootTY, 0, type="double3")
                    else:
                        cmds.setAttr((x + ':' + 'Root_Jnt' + '.translateY'), rootTY)
                # SN.sort(reverse=True)
                # print SN[-1]
                except:
                    pass
        else:
            cmds.confirmDialog(t='info', m='namespace가 있는 mocap 캐릭터만 적용됩니다.', b='OK')
    else:
        cmds.confirmDialog(t='info', m='캐릭터를 선택하세요.', b='OK')


def mocapModifyTpose():
    selObj = cmds.ls(sl=True, type='transform')
    selObjNum = len(selObj)
    NS = []
    # showName = cmds.ls(showNamespace = True, selection = True)
    # NS.append(showName[1])

    # selObjChildren.sort(reverse=True)
    # print selObjChildren[0]
    if selObjNum >= 1:
        showName = cmds.ls(showNamespace=True, selection=True)
        if showName[1] != ':':
            # print (cmds.ls(showNamespace = True, selection = True))[1]
            for i in range(0, selObjNum):
                try:
                    showName = cmds.ls(selObj[i], showNamespace=True, selection=True)
                    NS.append(showName[1])
                    selObjShape = cmds.listRelatives(selObj[i], shapes=True, f=True)
                    selObjChildren = cmds.listRelatives(selObj[i], ad=True, ni=True, f=True)
                    # selObjChildren.sort(reverse=True)
                    selObjChildren.remove(selObjShape[0])
                    # cmds.select(selObjChildren)
                    selObjChildren.sort(reverse=True)
                    # print selObjChildren
                    selObjChildrenNumb = len(selObjChildren)
                    # print selObjChildrenNumb
                    SN = []
                    for x in NS:
                        for obj in selObjChildren:
                            shortName = obj.split(":")[-1]
                            SN.append(shortName)
                            # print shortName
                            LeftLegTY = cmds.getAttr(x + ':' + 'LeftLeg.translateY')
                            LeftFootTY = cmds.getAttr(x + ':' + 'LeftFoot.translateY')
                            LeftForeFootTY = cmds.getAttr(x + ':' + 'LeftForeFoot.translateY')
                            rootTZ = -(LeftLegTY + LeftFootTY + LeftForeFootTY - 1)
                            cmds.setAttr((x + ':' + shortName + '.rotate'), 0, 0, 0, type="double3")
                            cmds.setAttr((x + ':' + 'Hips' + '.rotate'), 82.25, 0, 0, type="double3")
                            cmds.setAttr((x + ':' + 'RightUpLeg' + '.rotate'), 12.73, 0, 0, type="double3")
                            cmds.setAttr((x + ':' + 'LeftUpLeg' + '.rotate'), 12.73, 0, 0, type="double3")
                            cmds.setAttr((x + ':' + 'Spine' + '.rotate'), 5.202, 0, 0, type="double3")
                            cmds.setAttr((x + ':' + 'Spine1' + '.rotate'), -1.13, 0, 0, type="double3")
                            cmds.setAttr((x + ':' + 'Spine2' + '.rotate'), 8.068, 0, 0, type="double3")
                            cmds.setAttr((x + ':' + 'Spine3' + '.rotate'), 4.493, 0, 0, type="double3")
                            cmds.setAttr((x + ':' + 'RightShoulder' + '.translateX'), -0.01)
                            cmds.setAttr((x + ':' + 'LeftShoulder' + '.translateX'), 0.01)
                            if (cmds.checkBox(offSetBox, q=True, v=True)) == 0:
                                cmds.setAttr((x + ':' + 'Hips' + '.translate'), 0, 0, rootTZ, type="double3")
                            else:
                                cmds.setAttr((x + ':' + 'Hips' + '.translateZ'), rootTZ)
                # SN.sort(reverse=True)
                # print SN[-1]
                except:
                    pass
        else:
            cmds.confirmDialog(t='info', m='namespace가 있는 mocap 캐릭터만 적용됩니다.', b='OK')
    else:
        cmds.confirmDialog(t='info', m='캐릭터를 선택하세요.', b='OK')


def hikMocapDefinition():
    if (cmds.checkBox(TposeBox, q=True, v=True)) == 0:
        mel.eval('hikMonkMocapDefinition()')
    else:
        mel.eval('hikSelectMocapDefinition()')
    refreshMocapList()
    refreshSourceList()


def hikAdvancedDefinition():
    # mel.eval('hikSelectAdvancedDefinition()')
    mel.eval('hikMonkAdvancedDefinition()')
    refreshCustomList()


def hikAdvancedCustomRig():
    # mel.eval('hikSelectAdvancedCustomRig()')
    mel.eval('hikMonkAdvancedCustomRig()')
    refreshCustomList()
    refreshCharacterList()


def mocapTposeHIKDone():
    selObj = cmds.ls(sl=True, type='transform')
    selObjNum = len(selObj)
    if selObjNum == 0:
        selectMocap()
    else:
        pass
    if (cmds.checkBox(TposeBox, q=True, v=True)) == 0:
        mocapMonkTpose()
    else:
        mocapBasicTpose()
    hikMocapDefinition()
    cmds.SelectNone()


def AdvancedTposeHIKDone():
    selObj = cmds.ls(sl=True, type='transform')
    selObjNum = len(selObj)
    if selObjNum == 0:
        selectRig()
        customTpose()
        hikAdvancedDefinition()
        selectRig()
        hikAdvancedCustomRig()
        cmds.SelectNone()
    else:
        customTpose()
        hikAdvancedDefinition()
        cmds.select(selObj)
        hikAdvancedCustomRig()
        cmds.SelectNone()


def hikKeyBake():
    # mel.eval('hikBakeAnimation()')
    selObj = cmds.ls(sl=True, sns=True, type='transform')
    selObjP = cmds.ls(sl=True, type='transform')
    RN = []
    NS = []
    cuHIKList = []

    for i in range(0, len(selObj), 2):
        RN.append(selObj[i])

    for x in range(1, len(selObj), 2):
        NS.append(selObj[x])
        cuHIKList.append(selObj[x] + "_rig")

    for s in range(0, len(cuHIKList)):
        if (cmds.referenceQuery(selObjP[s], isNodeReferenced=True)) == True:
            cmds.select(cuHIKList[s])
            mel.eval('HIKCharacterControlsTool;')
            mel.eval('string $retObj[] = `ls -sl`;')
            mel.eval('hikSetCurrentCharacter($retObj[0]);')
            mel.eval('hikUpdateCharacterList();')
            mel.eval('hikUpdateCurrentCharacterFromUI()')
            mel.eval('hikUpdateContextualUI()')
            mel.eval('hikUpdateCharacterControlsUI(false);')
            mel.eval('statusLineUpdateInputField;')
            mel.eval('hikUpdateCharacterListCallback;')
            mel.eval('hikBakeCharacter 0;')
        else:
            cmds.confirmDialog(t='info', m='namespace가 있는 레퍼런스 캐릭터를 선택하세요.', b='OK')


def hikKeyBakeAnimation():
    selObjA = cmds.ls(sl=True, type='transform')
    selObjNum = len(selObjA)
    startFrame = cmds.playbackOptions(q=True, min=True)
    endFrame = cmds.playbackOptions(q=True, max=True)
    fps = mel.eval('float $fps = `currentTimeUnitToFPS`')
    if selObjNum == 0:
        result = cmds.confirmDialog(title='Confirm', message="전체 캐릭터를 bake 할까요?\n "" \n %d fps : %d f ~ %d f" % (
        fps, startFrame, endFrame), button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
        selectRig()
        if result == 'Yes':
            hikKeyBake()
    else:
        result = cmds.confirmDialog(title='Confirm', message="선택한 캐릭터를 bake 할까요?\n "" \n %d fps : %d f ~ %d f" % (
        fps, startFrame, endFrame), button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
        if result == 'Yes':
            hikKeyBake()
    refreshList()


def AdvancedForceActorSpace():
    try:
        cmds.select('*_rig_HIKproperties')
        HIKpNum = cmds.ls(sl=True)
        # print HIKpNum
        for HIKp in HIKpNum:
            cmds.setAttr((HIKp + '.ForceActorSpace'), 1)
        cmds.SelectNone()
    except:
        cmds.confirmDialog(t='info', m='HIKproperties가 없습니다.', b='OK')
        pass


def hikDelMocapDefinition():
    mel.eval('hikDeleteMocapDefinition()')
    refreshMocapList()
    refreshSourceList()


def hikDelCustomDefinition():
    mel.eval('hikDeleteCustomEdit()')
    mel.eval('hikDeleteCustomDefinition()')
    # hikDelCustomTrash()
    refreshCustomList()
    refreshCharacterList()


def refreshMocapList():
    try:
        # cmds.select('*:suit*')
        selObj = cmds.ls('*:suit*', sns=True, type='transform')
        RN = []
        NS = []
        moHIKList = []
        mocapList = []

        for i in range(0, len(selObj), 2):
            RN.append(selObj[i])
        for x in range(1, len(selObj), 2):
            NS.append(selObj[x])
            moHIKList.append(selObj[x] + "_mocap")
        # cmds.SelectNone()
        for z in range(0, len(RN)):
            if cmds.objExists(NS[z] + "_mocap"):
                mocapList.append(RN[z] + "     =>     " + moHIKList[z])
            else:
                mocapList.append(RN[z])
        s = cmds.textScrollList("mocapDef", edit=True, ra=True, allowMultiSelection=True, append=mocapList,
                                uniqueTag=RN)
        cmds.textScrollList(s, e=True, sc=partial(selectUniqueItem, s))
    except:
        pass


def refreshCustomList():
    try:
        # cmds.select('*:Main')
        cmds.select('*:WorldCtrl')
        cmds.pickWalk(d='up')
        cmds.pickWalk(d='up')
        # cmds.pickWalk (d = 'up')
        # cmds.pickWalk (d = 'up')
        selObj = cmds.ls(sl=True, sns=True, type='transform')
        RN = []
        NS = []
        cuHIKList = []
        customList = []

        for i in range(0, len(selObj), 2):
            RN.append(selObj[i])
        for x in range(1, len(selObj), 2):
            NS.append(selObj[x])
            cuHIKList.append(selObj[x] + "_rig")
        cmds.SelectNone()
        try:
            cmds.select('*:suit*')
            moSelObj = cmds.ls(sl=True, sns=True, type='transform')
            moRN = []
            moNS = []
            moHIKList = []
            mocapList = []

            for a in range(0, len(moSelObj), 2):
                moRN.append(moSelObj[a])
            for b in range(1, len(moSelObj), 2):
                moNS.append(moSelObj[b])
                moHIKList.append(moSelObj[b] + "_mocap")

            for d in range(0, len(moRN)):
                if cmds.objExists(moNS[d] + "_mocap_HIKSK2St"):
                    mocapList.append(moNS[d] + "_mocap_HIKSK2St")

            cmds.SelectNone()

            print (moHIKList)
            print (mocapList)
        except:
            pass
        for z in range(0, len(RN)):
            if cmds.objExists(NS[z] + "_rig"):
                try:
                    # keyCount = cmds.keyframe((NS[z] + ":RootX_M"), index=(1,2000), query = True, keyframeCount = True)
                    keyCountA = cmds.keyframe((NS[z] + ":Root_Ctrl"), index=(1, 2000), query=True, keyframeCount=True)
                    print (keyCountA)
                    keyCountB = cmds.keyframe((NS[z] + ":RootCtrl"), index=(1, 2000), query=True, keyframeCount=True)
                    print (keyCountB)
                except:
                    pass
                if cmds.objExists(NS[z] + "_rig_HIKSt2GolSK"):
                    if cmds.objExists(NS[z] + "_rig_HIKRetNode"):
                        if (cmds.getAttr(NS[z] + "_rig_CustomRigRetargeterNode1.connected")) == 1 and cmds.objExists(
                                NS[z] + "_rig_HIKRetNode"):
                            for sourItem in mocapList:
                                parentConnect = cmds.listConnections((NS[z] + "_rig_HIKRetNode"), d=True, s=False,
                                                                     skipConversionNodes=True)
                                sourConnect = cmds.listConnections(sourItem, d=True, s=False)
                                for sourConnList in sourConnect:
                                    if parentConnect != None and sourConnList == (NS[z] + "_rig_HIKRetNode"):
                                        customList.append(RN[z] + "     =>     " + cuHIKList[
                                            z] + " (custom rig)     =>     " + sourItem[:-9])
                                    elif parentConnect == None and sourConnList == (NS[z] + "_rig_HIKRetNode"):
                                        customList.append(
                                            RN[z] + "     =>     " + cuHIKList[z] + " (custom rig)     =>     Stance")
                                    else:
                                        print (NS[z] + "_rig_HIKSt2GolSK")
                                        pass
                        else:
                            if (
                            cmds.getAttr(NS[z] + "_rig_CustomRigRetargeterNode1.connected")) == 0 and cmds.objExists(
                                    NS[z] + "_rig_HIKRetNode"):

                                if keyCountA >= 1 or keyCountB >= 1:
                                    customList.append(
                                        RN[z] + "     =>     " + cuHIKList[z] + " (custom rig)     =>     Bake Done")
                                else:
                                    customList.append(
                                        RN[z] + "     =>     " + cuHIKList[z] + " (custom rig)     =>     None")
                            else:
                                pass
                    else:
                        if (cmds.getAttr(NS[z] + "_rig_CustomRigRetargeterNode1.connected")) == 1:
                            if keyCountA >= 1 or keyCountB >= 1:
                                customList.append(RN[z] + "     =>     " + cuHIKList[
                                    z] + " (custom rig)     =>     Only Keyframe Exist")
                            else:
                                customList.append(
                                    RN[z] + "     =>     " + cuHIKList[z] + " (custom rig)     =>     Stance Only")
                        else:
                            if keyCountA >= 1 or keyCountB >= 1:
                                customList.append(RN[z] + "     =>     " + cuHIKList[
                                    z] + " (custom rig)     =>     Only Keyframe Exist")
                            else:
                                customList.append(
                                    RN[z] + "     =>     " + cuHIKList[z] + " (custom rig)     =>     Not connect")
                else:
                    customList.append(RN[z] + "     =>     " + cuHIKList[z])
            else:
                customList.append(RN[z])
        s = cmds.textScrollList("customDef", edit=True, ra=True, allowMultiSelection=True, append=customList,
                                uniqueTag=RN)
        cmds.textScrollList(s, e=True, sc=partial(selectUniqueItem, s))
    except:
        pass


def refreshCharacterList():
    try:
        # cmds.select('*:Main')
        cmds.select('*:WorldCtrl')
        cmds.pickWalk(d='up')
        cmds.pickWalk(d='up')
        # cmds.pickWalk (d = 'up')
        # cmds.pickWalk (d = 'up')
        selObj = cmds.ls(sl=True, sns=True, type='transform')
        RN = []
        NS = []
        cuHIKList = []
        customList = []
        HIKSt2GolSKList = []

        for i in range(0, len(selObj), 2):
            RN.append(selObj[i])
        for x in range(1, len(selObj), 2):
            NS.append(selObj[x])
            cuHIKList.append(selObj[x] + "_rig")

        cmds.SelectNone()
        for z in range(0, len(RN)):
            if cmds.objExists(NS[z] + "_rig_HIKSt2GolSK"):
                customList.append(cuHIKList[z])
                HIKSt2GolSKList.append(NS[z] + "_rig_HIKproperties")
            else:
                pass
        s = cmds.textScrollList("CHARACTER", edit=True, ra=True, allowMultiSelection=True, append=customList,
                                uniqueTag=HIKSt2GolSKList)
        cmds.textScrollList(s, e=True, sc=partial(selectChrItem, s), dcc=partial(doubleSelectItem, s))
    # cmds.textScrollList(e=True, da=True )
    except:
        pass


def refreshSourceList():
    try:
        # cmds.select('*:suit*')
        selObj = cmds.ls('*:suit*', sns=True, type='transform')
        RN = ['None', 'Stance']
        NS = ['None', 'Stance']
        moHIKList = ['None', 'Stance']
        mocapList = ['None', 'Stance']

        for i in range(0, len(selObj), 2):
            RN.append(selObj[i])
        for x in range(1, len(selObj), 2):
            NS.append(selObj[x])
            moHIKList.append(selObj[x] + "_mocap")
        # cmds.SelectNone()
        for z in range(0, len(RN)):
            if cmds.objExists(NS[z] + "_mocap"):
                mocapList.append(moHIKList[z])
        s = cmds.textScrollList("SOURCE", edit=True, ra=True, allowMultiSelection=False, append=mocapList, uniqueTag=RN)
        cmds.textScrollList(s, e=True, selectCommand=partial(selectItem, s))
    except:
        pass


def refreshList():
    refreshMocapList()
    refreshCustomList()
    refreshCharacterList()
    refreshSourceList()


def selectChrItem(this_textScrollList):
    ret = cmds.textScrollList(this_textScrollList, q=True, selectItem=True)
    cmds.select(ret)
    mel.eval('string $retObj[] = `ls -sl`;')
    # mel.eval('global string $gHIKCurrentCharacter = "{}";'.format(ret[0]))
    mel.eval('hikSetCurrentCharacter($retObj[0]);')
    mel.eval('hikUpdateCharacterList();')
    mel.eval('hikUpdateCurrentCharacterFromUI()')
    # mel.eval('hikUpdateCurrentSourceFromUI()')
    mel.eval('hikUpdateContextualUI()')
    mel.eval('hikControlRigSelectionChangedCallback')
    mel.eval('hikUpdateCharacterListCallback')
    mel.eval('hikUpdateCharacterControlsUICallback')
    mel.eval('hikUpdateCharacterListCallback')


def selectItem(this_textScrollList):
    ret = cmds.textScrollList(this_textScrollList, q=True, selectItem=True)
    try:
        cmds.select(ret)
    except:
        pass


def selectUniqueItem(this_textScrollList):
    ret = cmds.textScrollList(this_textScrollList, q=True, selectUniqueTagItem=True)
    cmds.select(ret)


def doubleSelectItem(this_textScrollList):
    ret = cmds.textScrollList(this_textScrollList, q=True, selectUniqueTagItem=True)
    cmds.select(ret)
    mel.eval('openAEWindow')


def HIKconnect():
    chrList = cmds.textScrollList("CHARACTER", q=True, selectItem=True)
    sourList = cmds.textScrollList("SOURCE", q=True, selectItem=True)
    allSourceChar = cmds.optionMenuGrp("hikSourceList", query=True, itemListLong=True)
    for chrItem in chrList:
        mel.eval('global string $gHIKCurrentCharacter = "{}";'.format(chrItem))
        i = 1
        for item in allSourceChar:
            optMenu = "hikSourceList|OptionMenu"
            sourceChar = cmds.menuItem(item, query=True, label=True)
            if sourceChar == (" " + sourList[0]):
                cmds.optionMenu(optMenu, edit=True, select=i)
                mel.eval('hikUpdateCurrentSourceFromUI()')
                mel.eval('hikUpdateContextualUI()')
                mel.eval('hikControlRigSelectionChangedCallback')
                mel.eval('hikUpdateCharacterListCallback')
                mel.eval('hikUpdateCharacterControlsUICallback')
                mel.eval('hikUpdateCharacterListCallback')
                # sourConnect = cmds.listConnections( sourList[0], d=True, s=False )
                try:
                    cmds.rename('HIKRetargeterNode1', (chrItem + '_HIKRetNode'))

                    cmds.rename('HIKSK2State1', (sourceChar + '_HIKSK2St'))
                except:
                    pass
                break
            i += 1
    refreshMocapList()
    refreshCustomList()


def ActiveSource():
    optMenu = "hikSourceList|OptionMenu"
    cmds.optionMenu(optMenu, edit=True, enable=True)


def rigExport():
    selObj = cmds.ls(sl=True, sns=True, type='transform')
    cuHIKList = []

    for x in range(1, len(selObj), 2):
        cuHIKList.append(selObj[x] + "_rig_CustomRigRetargeterNode1")
    cmds.select(cuHIKList)
    cmds.ExportSelection(type='mayaAscii')


def temp_hikDelCustomTrash():
    try:
        cmds.delete('*CustomRigRetargeterNode*', '*HIKState2GlobalSK*')
    except:
        pass


def temp_hikKeyBakeAnimation():
    # mel.eval('hikBakeAnimation()')
    selObj = cmds.ls(sl=True, sns=True, type='transform')
    selObjP = cmds.ls(sl=True, type='transform')
    RN = []
    NS = []
    cuHIKList = []
    startFrame = cmds.playbackOptions(q=True, min=True)
    endFrame = cmds.playbackOptions(q=True, max=True)
    fps = mel.eval('float $fps = `currentTimeUnitToFPS`')

    for i in range(0, len(selObj), 2):
        RN.append(selObj[i])

    for x in range(1, len(selObj), 2):
        NS.append(selObj[x])
        cuHIKList.append(selObj[x] + "_rig")
    if len(selObjP) >= 1:
        result = cmds.confirmDialog(title='Confirm', message="선택한 캐릭터를 bake 할까요?\n "" \n %d fps : %d f ~ %d f" % (
        fps, startFrame, endFrame), button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
        if result == 'Yes':
            for s in range(0, len(cuHIKList)):
                if (cmds.referenceQuery(selObjP[s], isNodeReferenced=True)) == True:
                    cmds.select(cuHIKList[s])
                    mel.eval('HIKCharacterControlsTool;')
                    mel.eval('string $retObj[] = `ls -sl`;')
                    mel.eval('hikSetCurrentCharacter($retObj[0]);')
                    mel.eval('hikUpdateCharacterList();')
                    mel.eval('hikUpdateCurrentCharacterFromUI()')
                    mel.eval('hikUpdateContextualUI()')
                    mel.eval('hikUpdateCharacterControlsUI(false);')
                    mel.eval('statusLineUpdateInputField;')
                    mel.eval('hikUpdateCharacterListCallback;')
                    mel.eval('hikBakeCharacter 0;')
                else:
                    cmds.confirmDialog(t='info', m='namespace가 있는 레퍼런스 캐릭터를 선택하세요.', b='OK')
    else:
        cmds.confirmDialog(t='info', m='리깅 캐릭터를 선택하세요.', b='OK')
    refreshList()


#########################################
#					UI					#
#########################################
if cmds.window('Mywin_main', ex=True):
    cmds.deleteUI('Mywin_main')
Mywin = cmds.window('Mywin_main', title="mocap tool")
cmds.paneLayout(configuration='vertical2')
cmds.columnLayout(columnAttach=('both', 2), rowSpacing=2, columnWidth=204)

# cmds.columnLayout()

cmds.text(l="MOTION CAPTURE", h=30, bgc=[0.3, 0.5, 1], fn='boldLabelFont')
# cmds.text (l = " T-pose ", h = 30)
cmds.button(l="select all", w=200, c="selectMocap()")
cmds.separator(h=5, style='none')
# cmds.text (l = "!! HIK editor !!", h = 30)
offSetBox = cmds.checkBox(label='root off set')

# cmds.rowColumnLayout (nr = 2)
cmds.button(l="monk T pose", w=100, c="mocapMonkTpose()")
cmds.button(l="mixamo T pose", w=100, c="mocapBasicTpose()")
# cmds.rowColumnLayout (nc = 1)
cmds.button(l="definition", w=200, c="hikMocapDefinition()")
cmds.separator(h=5, style='none')
TposeBox = cmds.checkBox(label='mixamo T pose')
cmds.button(l="auto set", w=200, c="mocapTposeHIKDone()", bgc=[0, 1, 1])
cmds.separator(h=5, style='none')
cmds.button(l="delete definition", w=200, c="hikDelMocapDefinition()", bgc=[0.5, 0, 0])

cmds.text(l="", h=88)

cmds.separator(h=5, style='in')
cmds.text(l="MONK RIG", h=30, bgc=[0.3, 0.5, 1], fn='boldLabelFont')

cmds.button(l="select all", w=200, c="selectRig()")
cmds.separator(h=5, style='none')
cmds.button(l="T pose", w=200, c="customTpose()")
cmds.button(l="definition", w=200, c="hikAdvancedDefinition()")
cmds.button(l="custom rig", w=200, c="hikAdvancedCustomRig()")
cmds.separator(h=5, style='none')
cmds.button(l="auto set", w=200, c="AdvancedTposeHIKDone()", bgc=[0, 1, 1])
cmds.separator(h=5, style='none')
cmds.button(l="delete definition", w=200, c="hikDelCustomDefinition()", bgc=[0.5, 0, 0])

cmds.separator(h=10, style='none')
cmds.button(l="export selection", w=200, c="rigExport()", bgc=[1, 1, 0])

cmds.text(l="", h=90)

cmds.separator(h=5, style='in')
cmds.text(l="UTILITIES", h=30, bgc=[0.3, 0.5, 1], fn='boldLabelFont')

# cmds.separator(h = 5, style='none')
cmds.button(l="match source on all", w=200, c="AdvancedForceActorSpace()")

# cmds.separator(h = 5, style='none')
cmds.button(l="refresh all", w=200, c="refreshList()", bgc=[1, 1, 0])

# cmds.separator(h = 5, style='none')
cmds.button(l="bake", w=200, c="hikKeyBakeAnimation()", bgc=[0.5, 0, 0])
cmds.button(l="active source list", w=200, c="ActiveSource()")
cmds.separator(h=5, style='in')
cmds.text(l="SCENE", h=30, bgc=[0.3, 0.5, 1], fn='boldLabelFont')
cmds.button(l="mocap optimize", w=200, c="cleanUp()")

cmds.separator(h=5, style='in')
cmds.text(l="NAMESPACE", h=30, bgc=[0.3, 0.5, 1], fn='boldLabelFont')
nsTxt = cmds.textField(tx='', ed=True, w=200)
cmds.button(l="create", w=200, c="createNS()")
cmds.button(l="delete", w=200, c="deleteNS()")
cmds.button(l="rename", w=200, c="renameNS()")

cmds.setParent('..')
cmds.setParent('..')

cmds.columnLayout(columnAttach=('both', 2), rowSpacing=2, columnWidth=500)
# cmds.text (l = "MOTION CAPTURE & DEFINITION", h = 30, bgc = [0.3, 0.5, 1], fn = 'boldLabelFont')
cmds.button(l="MOTION CAPTURE & DEFINITION", h=30, bgc=[0.3, 0.5, 1], c="refreshMocapList()")
cmds.textScrollList("mocapDef", numberOfRows=20, allowMultiSelection=True, append=[])
# cmds.separator(h = 5, style='none')

# cmds.text (l = "ADVANCED SKELETON RIG & DEFINITION", h = 30, bgc = [0.3, 0.5, 1], fn = 'boldLabelFont')
cmds.button(l="MONK RIG & DEFINITION", h=30, bgc=[0.3, 0.5, 1], c="refreshCustomList()")
cmds.textScrollList("customDef", numberOfRows=20, allowMultiSelection=True, append=[])
# cmds.separator(h = 5, style='none')
cmds.rowColumnLayout(nc=3, columnAttach=(2, 'both', 2))
# cmds.text (l = "CHARACTER (custom rig)", h = 30, bgc = [0.3, 0.5, 1], fn = 'boldLabelFont')
cmds.button(l="CHARACTER (custom rig)", h=30, bgc=[0.3, 0.5, 1], c="refreshCharacterList()")
cmds.text(l="", h=30)
# cmds.text (l = "SOURCE", h = 30, bgc = [0.3, 0.5, 1], fn = 'boldLabelFont')
cmds.button(l="SOURCE", h=30, bgc=[0.3, 0.5, 1], c="refreshSourceList()")
cmds.textScrollList("CHARACTER", numberOfRows=20, allowMultiSelection=True, width=230, append=[])
cmds.button(l=u'\u1405'u'\u1405'u'\u1405', w=40, c="HIKconnect()")  # right arrow
cmds.textScrollList("SOURCE", numberOfRows=20, allowMultiSelection=False, width=230, append=[])
# cmds.separator(h = 5, style='none')
# cmds.text (l = "")
# cmds.separator(h = 5, style='none')
cmds.setParent('..')
cmds.setParent('..')

refreshList()
mel.eval('HIKCharacterControlsTool;')

optMenu = "hikSourceList|OptionMenu"
cmds.optionMenu(optMenu, edit=True, enable=False)

cmds.showWindow(Mywin)