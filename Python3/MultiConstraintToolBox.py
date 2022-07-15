# -*- coding: utf-8 -*-
# Multi Constraint Python 2019.07.25
# Note 스케일 고정
import maya.cmds as cmds
#
def Multi_Constraint_UI():
    ## define Function Base Layout
    def Base_Layout( consType,ctFrom ):
        rAxTmp=False
        if consType=='Parent':
            rAxTmp=True
        ctMoTxt=cmds.text( l='Maintain offset:' )
        ctMoChkBox=cmds.checkBox( '%sMaintainOffsetCheckBox'% consType, w=30, v=0, l='' )
        ctCaTxt=cmds.text( l='Contraint axis:' )
        ctAxChkBox=cmds.checkBox( '%sConstraintAxisCheckBox'% consType, w=30, v=1, l='All',
                                   ofc='cmds.checkBox("%sConstraintAxisCheckBox", e=1, v=1)'% consType,
                                   onc= lambda c: EditAxisCheckBoxCmd(consType,0) )
        ctAxXChkBox=cmds.checkBox( '%sConstraintAxisXCheckBox'% consType, w=30, v=0, l='X',
                                    onc='cmds.checkBox("%sConstraintAxisCheckBox", e=1, v=0)'% consType )
        ctAxYChkBox=cmds.checkBox( '%sConstraintAxisYCheckBox'% consType, w=30, v=0, l='Y',
                                    onc='cmds.checkBox("%sConstraintAxisCheckBox", e=1, v=0)'% consType )
        ctAxZChkBox=cmds.checkBox( '%sConstraintAxisZCheckBox'% consType, w=30, v=0, l='Z',
                                    onc='cmds.checkBox("%sConstraintAxisCheckBox", e=1, v=0)'% consType )
        ctRaxChkBox=cmds.checkBox( '%sConstraintAxisRotCheckBox'% consType, w=30, v=1, l='All', en=rAxTmp,
                                   onc= lambda c:EditAxisCheckBoxCmd(consType,1) )
        ctRaxXChkBox=cmds.checkBox( '%sConstraintAxisRotXCheckBox'% consType, w=30, v=0, l='X', en=rAxTmp,
                                    onc=lambda c:cmds.checkBox('%sConstraintAxisRotCheckBox'% consType, e=1, v=0) )
        ctRaxYChkBox=cmds.checkBox( '%sConstraintAxisRotYCheckBox'% consType, w=30, v=0, l='Y', en=rAxTmp,
                                    onc=lambda c:cmds.checkBox('%sConstraintAxisRotCheckBox'% consType, e=1, v=0) )
        ctRaxZChkBox=cmds.checkBox( '%sConstraintAxisRotZCheckBox'% consType,w=30, v=0, l='Z', en=rAxTmp,
                                    onc=lambda c:cmds.checkBox('%sConstraintAxisRotCheckBox'% consType, e=1, v=0) )
        ctOpTxt=cmds.text( l='Only position:' )
        ctOnlyChkBox=cmds.checkBox( '%sOnlyPositionCheckBox'% consType, w=100, v=0, l='' )
        ctCmTxt=cmds.text( l='Constraint method:' )
        ctCmRdsBtn=cmds.radioButtonGrp( '%sConstraintMethodRadioBtn'% consType,
                                                  nrb=3,la3=['Each other','First select', 'Orig'],
                                                  sl=1,cw3=[70,70,70] )
        ctApplyBtn=cmds.button( '%sApplyBtn'% consType,l='Apply',w=120,h=30,c=lambda c:MultiConstraintCmd(consType) )
        ctCncBtn=cmds.button( '%sCancelBtn'% consType,l='Cancel',w=120,h=30,c='cmds.deleteUI( "MultiConstraintWin",wnd=1 )' )
        # Layout
        moChkTopNum=10
        moChkLfNum=10
        cmds.formLayout( ctFrom,e=True,af=[(ctMoTxt,'top',moChkTopNum),(ctMoTxt,'left',moChkLfNum)] )
        cmds.formLayout( ctFrom,e=True,af=[(ctMoChkBox,'top',moChkTopNum+1),(ctMoChkBox,'left',moChkLfNum+90)] )
        axChkTopNum=32
        axChkLfNum=100
        cmds.formLayout( ctFrom,e=True,af=[(ctCaTxt,'top',axChkTopNum+1),(ctCaTxt,'left',axChkLfNum-90)] )
        cmds.formLayout( ctFrom,e=True,af=[(ctAxChkBox,'top',axChkTopNum),(ctAxChkBox,'left',axChkLfNum)] )
        cmds.formLayout( ctFrom,e=True,af=[(ctAxXChkBox,'top',axChkTopNum),(ctAxXChkBox,'left',axChkLfNum+40)] )
        cmds.formLayout( ctFrom,e=True,af=[(ctAxYChkBox,'top',axChkTopNum),(ctAxYChkBox,'left',axChkLfNum+70)] )
        cmds.formLayout( ctFrom,e=True,af=[(ctAxZChkBox,'top',axChkTopNum),(ctAxZChkBox,'left',axChkLfNum+100)] )
        rAxChkTopNum=52
        rAxChkLfNum=100
        cmds.formLayout( ctFrom,e=True,af=[(ctRaxChkBox,'top',rAxChkTopNum),(ctRaxChkBox,'left',rAxChkLfNum)] )
        cmds.formLayout( ctFrom,e=True,af=[(ctRaxXChkBox,'top',rAxChkTopNum),(ctRaxXChkBox,'left',rAxChkLfNum+40)] )
        cmds.formLayout( ctFrom,e=True,af=[(ctRaxYChkBox,'top',rAxChkTopNum),(ctRaxYChkBox,'left',rAxChkLfNum+70)] )
        cmds.formLayout( ctFrom,e=True,af=[(ctRaxZChkBox,'top',rAxChkTopNum),(ctRaxZChkBox,'left',rAxChkLfNum+100)] )
        opTopNum=75
        opLfNum=10
        cmds.formLayout( ctFrom,e=True,af=[(ctOpTxt,'top',opTopNum),(ctOpTxt,'left',opLfNum)] )
        cmds.formLayout( ctFrom,e=True,af=[(ctOnlyChkBox,'top',opTopNum+1),(ctOnlyChkBox,'left',opLfNum+90)] )
        cmTopNum=95
        cmLfNum=10
        cmds.formLayout( ctFrom,e=True,af=[(ctCmTxt,'top',cmTopNum),(ctCmTxt,'left',cmLfNum)] )
        cmds.formLayout( ctFrom,e=True,af=[(ctCmRdsBtn,'top',cmTopNum-3),(ctCmRdsBtn,'left',cmLfNum+100)] )
        btnTopNum=121
        btnLfNum=92
        cmds.formLayout( ctFrom,e=True,af=[(ctApplyBtn,'top',btnTopNum),(ctApplyBtn,'left',btnLfNum-67)] )
        cmds.formLayout( ctFrom,e=True,af=[(ctCncBtn,'top',btnTopNum),(ctCncBtn,'left',btnLfNum+67)] )
        #
        def EditAxisCheckBoxCmd(consType,var):
            if var==0:
                axes=['X','Y','Z']
            else:
                axes=['RotX','RotY','RotZ']
            for ax in axes:
                cmds.checkBox( '%sConstraintAxis%sCheckBox'%(consType,ax), e=1, v=0 )
        #
    #
    # Make Window
    mcWin='MultiConstraintWin' # Assign Window Name
    mcWinTitle='MJ_Multi Constraint ToolBox'
    if cmds.window( mcWin,ex=1 ):
        cmds.deleteUI( mcWin,wnd=1 )
    cmds.window( mcWin,t=mcWinTitle, mb=True, tlb=1 )
    #cmds.menu( l='About',tearOff=False )
    # Layout
    groundForm=cmds.formLayout( 'GroundForm' )
    groundTab=cmds.tabLayout( 'GroundTab', w=314,h=184 )
    cmds.formLayout( groundForm,e=True,af=[(groundTab,'top',1),(groundTab,'left',1)] )
    # Point Tab
    pointForm=cmds.formLayout( 'PointForm' )
    Base_Layout( 'Point',pointForm )
    # Orient Tab
    cmds.setParent( groundTab )
    orientForm=cmds.formLayout( 'OrientForm' )
    Base_Layout( 'Orient',orientForm )
    # Parent Tab
    cmds.setParent( groundTab )
    parentForm=cmds.formLayout( 'ParentForm' )
    Base_Layout( 'Parent',parentForm )
    cmds.tabLayout('GroundTab',e=1,tl=( (pointForm,'Point'),(orientForm,'Orient'),(parentForm,'Parent')) )
    cmds.window( mcWin,e=1, wh=[318,210],s=0 )
    # Show Window
    cmds.showWindow( mcWin )
# Multi Constraint Function
def MultiConstraintCmd(type):
    sl=cmds.ls(sl=1)
    moVl=cmds.checkBox( '%sMaintainOffsetCheckBox'% type, q=1, v=1 )
    caAllvl=cmds.checkBox( '%sConstraintAxisCheckBox'% type, q=1, v=1)
    caVl=[ ( cmds.checkBox( '%sConstraintAxisXCheckBox'% type, q=1, v=1 ) ),
           ( cmds.checkBox( '%sConstraintAxisYCheckBox'% type, q=1, v=1 ) ),
           ( cmds.checkBox( '%sConstraintAxisZCheckBox'% type, q=1, v=1 ) ) ]
    rCaAllvl=cmds.checkBox( '%sConstraintAxisRotCheckBox'% type, q=1, v=1)
    rCaVl=[ ( cmds.checkBox( '%sConstraintAxisRotXCheckBox'% type, q=1, v=1 ) ),
       ( cmds.checkBox( '%sConstraintAxisRotYCheckBox'% type, q=1, v=1 ) ),
       ( cmds.checkBox( '%sConstraintAxisRotZCheckBox'% type, q=1, v=1 ) ) ]
    XYZ=['x','y','z']
    skVl=['none','none','none']
    i=0
    if caAllvl==0:
        for ca in caVl:
            if ca==1:
                skVl[i]='none'
            else:
                skVl[i]=XYZ[i]
            i+=1
    srVl=['none','none','none']
    i=0
    if rCaAllvl==0:
        for rca in rCaVl:
            if rca==1:
                srVl[i]='none'
            else:
                srVl[i]=XYZ[i]
            i+=1
    if type=='Parent':
        skipVl='st=%s, sr=%s'% (str(skVl),str(srVl))
    else:
        skipVl='sk=%s'% str(skVl)
    opVl=cmds.checkBox( '%sOnlyPositionCheckBox'% type, q=1, v=1 )
    cmVl=cmds.radioButtonGrp( '%sConstraintMethodRadioBtn'% type, q=1, sl=1 )
    #
    consNm=type.lower()
    i=0
    iSz=len(sl)
    if type=='Parent': simpleNm='PR'
    elif type=='Orient': simpleNm='OR'
    elif type=='Point': simpleNm='PT'
    if cmVl==1:
        while i<iSz/2:
            ubrmNm=sl[iSz/2+i].replace('_','')
            if '|' in ubrmNm: ubrmNm=ubrmNm.split('|')[-1]

            eval( 'cmds.%sConstraint("%s","%s",mo=%d,%s,n="%s%sCons")' % (consNm,sl[i],sl[iSz/2+i],moVl,skipVl,ubrmNm,simpleNm))
            if opVl==1:
                cmds.delete('%s%sCons'% (ubrmNm,simpleNm))
            i+=1
    elif cmVl==2:
        while i<iSz:
            if i==0:
                i+=1
                continue
            ubrmNm=sl[i].replace('_','')
            if '|' in ubrmNm: ubrmNm=ubrmNm.split('|')[-1]
            eval( 'cmds.%sConstraint("%s","%s",mo=%d,%s,n="%s%sCons")' % (consNm,sl[0],sl[i],moVl,skipVl,ubrmNm,simpleNm))
            if opVl==1:
                cmds.delete('%s%sCons'% (ubrmNm,simpleNm))
            i+=1
    else :
        ubrmNm=sl[-1].replace('_','')
        if '|' in ubrmNm: ubrmNm=ubrmNm.split('|')[-1]
        eval( 'cmds.%sConstraint(%s,mo=%d,%s,n="%s%sCons")' % (consNm,sl,moVl,skipVl,ubrmNm,simpleNm))
        if opVl==1:
            cmds.delete('%s%sCons'% (ubrmNm,simpleNm))
            
Multi_Constraint_UI()