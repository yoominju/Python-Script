from maya import cmds, mel
from functools import partial
def changeOperationType(event):
    idx = cmds.radioButtonGrp('SkinWeightWindow|MainLayout|Operation', q=True, select=True)
    if idx == 1: value='Replace'
    elif idx == 2: value='Add'
    elif idx == 3: value='Scale'        
    elif idx == 4: value='Smooth'       
    else: raise ValueError('unknown button')
    print(value)
    template = '''
    artAttrPaintOperation artAttrSkinPaintCtx {value};
    '''.format(value=value)
    mel.eval(template)
def changeWeightValue(value, event):
    print(value)
    template = '''
    artSkinSetSelectionValue {value} false artAttrSkinPaintCtx artAttrSkin;
    '''.format(value=value)
    mel.eval(template)
def flood(event):
    mel.eval('artAttrSkinPaintCtx -e -clear `currentCtx`;')
def skinWeightWindow():
    if cmds.window('SkinWeightWindow', ex=True):
        cmds.deleteUI('SkinWeightWindow', window=True)
    cmds.window('SkinWeightWindow',t='Skin Weight Window',mb=1,tlb=1)
    cmds.columnLayout('MainLayout', adj=True)
    cmds.radioButtonGrp('Operation', label='', labelArray4=['Rp', 'Ad','Sc','Sm'], numberOfRadioButtons=4, columnWidth5=[10, 40, 40,40,40], changeCommand=changeOperationType)
    cmds.separator(height=20)
    for i in ['0','0.001', '0.01', '0.1','0.33', '0.5','0.66','0.9', '0.99', '0.999', '1']:
        cmds.button(i,w=100,height=25, command=partial(changeWeightValue, i))
    cmds.separator(height=20)
    cmds.button('flood', command=flood,h=30)
    cmds.window('SkinWeightWindow',e=1,wh=[200,380],s=0)
    cmds.showWindow('SkinWeightWindow')
skinWeightWindow()