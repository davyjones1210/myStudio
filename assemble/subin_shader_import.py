from maya import cmds
from publish import utils

# Referencer the anim cache
char_name = "dobby_anim"
sourcefile = "C:/works/projects/NewTestProj2/shot/shot-101/animation/alembicFile/v15/dobby.abc"
anim_nodes = cmds.file(sourcefile, namespace=char_name, type="Alembic", reference=True, returnNewNodes=True)
char_group = cmds.group(empty=True, name=f"{char_name}_cache")
cmds.parent(anim_nodes, char_group)

cache_dir = cmds.referenceQuery(anim_nodes[0] ,  filename=True)
cache_name_space = cmds.file(cache_dir, query=True, namespace=True)  

# Referencer the lookdev shader
char_name = "dobby_look"
look_sourcefile = "C:/works/projects/NewTestProj2/asset/dobby/lookdev/shaderfile/v6/dobby.mb"
look_nodes = cmds.file(look_sourcefile, namespace=char_name, type="mayaBinary", reference=True, returnNewNodes=True)

look_dir = cmds.referenceQuery(look_nodes[0] ,  filename=True)
look_name_space = cmds.file(look_dir, query=True, namespace=True)  

# anim_nodes,look_nodes 
path = "C:/works/projects/NewTestProj2/asset/dobby/lookdev/metadata/v1/dobby.json"
contents = utils.readJson(path)


for content in contents:
    shader = "{}:{}".format(look_name_space, content["shader"])    
    print(shader)
    
    if cmds.objExists(shader):

        shaderSG = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"{shader}SG")
        # assign shader to shading group
        cmds.connectAttr(f"{shader}.outColor", f"{shaderSG}.surfaceShader" )
        
        if content["mesh"]:
            for mesh in content["mesh"]:
                mesh_name = "{}:{}".format(cache_name_space, mesh)
                print("\tmesh - ", mesh_name)
                
                
                flatten_mesh = cmds.ls(mesh_name,  flatten=True)  
    
                cmds.sets(flatten_mesh, e=True, forceElement=shaderSG)
