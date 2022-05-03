#CtrlShape cvPos get

import pickle
import pymel.core as pm

sel = pm.ls(sl=1)
posDict = {}

for ctl in sel:
    getPos = []
    for cv in ctl.cv:
        pos = cv.getPosition(space = 'world')
        getPos.append(pos.get()[0:-1])
    posDict[ctl.name()] = getPos
    