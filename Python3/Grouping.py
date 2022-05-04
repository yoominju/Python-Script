import pymel.core as pm

sel_ = pm.ls(sl=1)

mesh_list = []
joint_list = []
curve_list = []
nurbs_list = []

for item in sel_:
    shape = item.getShape()
    
    if shape :
        if shape.type() == 'mesh':
            mesh_list.append(item)
        elif shape.type() == 'nurbsSurface':
            nurbs_list.append(item)
        elif shape.type() == 'nurbsCurve':
            curve_list.append(item)
    else :
        if item.type() == 'joint':
            joint_list.append(item)
            
pm.group(mesh_list,n='mesh_Grp')
pm.group(joint_list,n='joint_Grp')
pm.group(curve_list,n='curve_Grp')
pm.group(nurbs_list,n='nurbs_Grp')