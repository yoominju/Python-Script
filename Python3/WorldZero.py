import pymel.core as pm

sel=pm.ls(sl=1)
for x in sel:
    [pm.setAttr(x + '.translate' + attr_ ,0 ) for attr_ in ['X','Y','Z']]
    [pm.setAttr(x + '.rotate' + attr_ ,0 ) for attr_ in ['X','Y','Z']]
    [pm.setAttr(x + '.scale' + attr_ ,1 ) for attr_ in ['X','Y','Z']]