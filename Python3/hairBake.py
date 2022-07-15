# -*- coding: utf-8 -*-
'''
    MillionVolt Hair Bake System
    date: 21.05.10
    scipt: Affogato
'''
import pymel.core as pm, maya.cmds as cmds, maya.OpenMayaUI as omui
try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from shiboken import wrapInstance

def ConnectBakeJnt(ev=None):
    jnts=pm.ls(sl=1)
    if len(jnts)==0: return
    for jnt in jnts:
        if jnt.root().hasAttr('mvHairBake'):
            hairBakeLs=jnt.root().mvHairBake.inputs()
            if jnt.nodeType()=='joint':
                jnt.msg >> jnt.root().mvHairBake[len(hairBakeLs)]
                print('%s ----> %s.mvHairBake[%d]'% (jnt, jnt.root(), len(hairBakeLs)))
        else:
            jnt.root().addAttr('mvHairBake',nn='HairBake',at='message',m=1)
            jnt.root().mvHairBake.set(cb=1,k=1)
            if jnt.nodeType()=='joint':
                jnt.msg >> jnt.root().mvHairBake[0]
                print('%s ----> %s.mvHairBake[0]'% (jnt, jnt.root()))

def RemoveMVHairAttr(ev=None):
    objs=pm.ls(sl=1)
    if len(objs)==0: return
    [objs[0].mvHairBake.delete() for obj in objs  if objs[0].hasAttr('mvHairBake')]

class ArrangeBakeJoint:
    def __init__(self,jnt,stFrm,edFrm):
        self.jnt=jnt
        self.stFrm=int(stFrm)
        self.edFrm=int(edFrm)
        self.jnts=[]
        self.eff=None
        self.findBakeJoint(self.jnt)

    def findBakeJoint(self,slJnt):
        tmpJnts=self.jnt.listRelatives(ad=1)
        tmpJnts.reverse()
        self.jnts.append(self.jnt)
        for i in range(len(tmpJnts)):
            if tmpJnts[i].nodeType()=='joint':
                self.jnts.append(tmpJnts[i])
            if tmpJnts[i].nodeType()=='ikEffector':
                self.eff=tmpJnts[i]


class HairBakeSystem_UI():
    def __init__(self):
        self.mayaWin = wrapInstance(int(omui.MQtUtil.mainWindow()), QWidget)
        self.mainWin = QWidget(self.mayaWin)
        self.mainWin.setWindowFlags(Qt.Window)
        self.mainWin.resize(150, 250)
        self.mainWin.setWindowTitle('Hair Bake System')
        self.mnBar = QMenuBar(parent=self.mainWin)
        self.mn = QMenu(self.mainWin)
        self.mn.setTitle('Menu')
        self.mnBar.addMenu(self.mn)

        self.cnnBakeJntMenu=QAction('Connect Bake Jnt',self.mainWin)
        self.mn.addAction(self.cnnBakeJntMenu)
        self.cnnBakeJntMenu.triggered.connect(ConnectBakeJnt)

        self.rmvBakeAttrMenu=QAction('Remove mvHairBake Attr',self.mainWin)
        self.mn.addAction(self.rmvBakeAttrMenu)
        self.rmvBakeAttrMenu.triggered.connect(RemoveMVHairAttr)

        self.selectBakeJntMenu=QAction('Select Bake Joint',self.mainWin)
        self.mn.addAction(self.selectBakeJntMenu)
        self.selectBakeJntMenu.triggered.connect(self.selectBakeJoint)

        self.UI()

    def UI(self):
        self.mainQVLayout = QVBoxLayout(self.mainWin)
        self.mainQVLayout.setContentsMargins(10,25,10,10)
        self.qh1=QHBoxLayout()
        self.qh1.setSpacing(5)
        self.mainQVLayout.addLayout(self.qh1)

        startLabel = QLabel()
        startLabel.setText('StartFrame')
        self.qh1.addWidget(startLabel)

        self.startFrameLine = QLineEdit()
        self.startFrameLine.setFixedWidth(50)
        self.qh1.addWidget(self.startFrameLine)

        endLabel = QLabel()
        endLabel.setText('EndFrame')
        self.qh1.addWidget(endLabel)

        self.endFrameLine = QLineEdit()
        self.endFrameLine.setFixedWidth(50)
        self.qh1.addWidget(self.endFrameLine)

        self.frameLine('start')
        self.frameLine('end')

        self.assetList = QListWidget()
        self.assetList.setFixedHeight(100)
        self.assetList.setSelectionMode(QListWidget.ExtendedSelection)
        self.assetList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.mainQVLayout.addWidget(self.assetList)
        self.findHairBakeAsset()

        refreshBtn = QPushButton()
        refreshBtn.setIcon(QIcon(':/teKeyRefresh.png'))
        refreshBtn.setIconSize(QSize(20,20))
        self.mainQVLayout.addWidget(refreshBtn)
        refreshBtn.clicked.connect(self.toolRefresh)

        bakeBtn = QPushButton()
        bakeBtn.setIcon(QIcon(':/bakeAnimation.png'))
        bakeBtn.setIconSize(QSize(20,20))
        self.mainQVLayout.addWidget(bakeBtn)
        bakeBtn.clicked.connect(self.bakeJoint)

        restoreBtn = QPushButton()
        restoreBtn.setIcon(QIcon(':/Erase.png'))
        restoreBtn.setIconSize(QSize(20,20))
        self.mainQVLayout.addWidget(restoreBtn)
        restoreBtn.clicked.connect(self.restoreBake)

    def frameLine(self,se):
        if se=='start':
            frame=int( cmds.playbackOptions(q=1, min=1)-1 )
            self.startFrameLine.setText(str(frame))
        elif se=='end':
            frame=int( cmds.playbackOptions(q=1, max=1)+1 )
            self.endFrameLine.setText(str(frame))

    def findHairBakeAsset(self):
        hairAssets=pm.ls('*.mvHairBake',r=1)
        for hAsset in hairAssets:
            self.assetList.addItem(hAsset.node().name())

    def toolRefresh(self):
        self.frameLine('start')
        self.frameLine('end')
        self.assetList.clear()
        self.findHairBakeAsset()

    def selectBakeJoint(self):
        slItem=self.assetList.selectedItems()
        if len(slItem)==0:
            pm.warning('No Select Item')
            return
        for i,itm in enumerate(slItem):
            bakeJnts=pm.PyNode(itm.text()).mvHairBake.inputs()
            if i==0: pm.select(bakeJnts)
            else: pm.select(bakeJnts,add=1)

    def bakeJoint(self):
        stFrm=int(self.startFrameLine.text())
        edFrm=int(self.endFrameLine.text())
        self.selectBakeJoint()
        bakeTopJnts=pm.ls(sl=1)
        bakeJnts=[]
        effs=[]
        for btj in bakeTopJnts:
            tmpBK=ArrangeBakeJoint(btj,stFrm,edFrm)
            bakeJnts=bakeJnts+tmpBK.jnts
            effs.append(tmpBK.eff)
        cycSz=abs(edFrm-stFrm)
        progress = QProgressDialog()
        progress.setWindowTitle('BakeProgress')
        progress.show()
        for i in range(cycSz):
            pm.currentTime(i+stFrm,e=1,u=1)
            list(map( lambda bakeJnt: pm.setKeyframe(bakeJnt,at=['t','r','s']), bakeJnts ))
            progress.setValue((100.0/cycSz)*i)
            qApp.processEvents()
        progress.reset()
        for eff in effs:
            try:
                ikh=eff.handlePath[0].outputs()[0]
                ikh.ikb.set(0)
            except:
                pm.warning('%s can not found ikHandle'% eff.name())
        pm.select(bakeJnts)

    def restoreBake(self):
        stFrm=int(self.startFrameLine.text())
        edFrm=int(self.endFrameLine.text())
        self.selectBakeJoint()
        bakeTopJnts=pm.ls(sl=1)
        bakeJnts=[]
        effs=[]
        for bakeTopJnt in bakeTopJnts:
            tmpBK=ArrangeBakeJoint(bakeTopJnt,stFrm,edFrm)
            bakeJnts=bakeJnts+tmpBK.jnts
            effs.append(tmpBK.eff)
        list(map(lambda jnt: pm.cutKey(jnt), bakeJnts))
        for eff in effs:
            try:
                ikh=eff.handlePath[0].outputs()[0]
                ikh.ikb.set(1)
            except:
                pm.warning('%s can not found ikHandle'% eff.name())
        pm.select(bakeJnts)

    def show(self):
        self.mainWin.show()

    def getWindow(self):
        return self.mainWin

    def close(self):
        self.mainWin.close()
        self.mainWin.deleteLater()

try:
    hairBakeSysUI.close()
except:
    pass
hairBakeSysUI=HairBakeSystem_UI()
hairBakeSysUI.show()
