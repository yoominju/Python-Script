from maya import cmds as mc

def findNodesTypeBelow(nodeType):
    mc.select(hi=1)
    sel = mc.ls(sl=1, type=nodeType)
    print(sel)
    return sel


def selectNodesTypeBelow(nodeType):
    nodesToSelect = []
    nodes = findNodesTypeBelow(nodeType)
    
    for n in nodes:
        nodesToSelect.append(n)
    mc.select(nodesToSelect, r=1)
    return True



selectNodesTypeBelow('joint')