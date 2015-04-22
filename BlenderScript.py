import bpy
import os
import io

def main():
    i = 120
    fileExists = True    
    testfile = io.open("changelog.txt",'ab')
    
    while(fileExists):
        file = '{0:05d}'.format(i)
        fileLocation = "O://geras//"+file
        if(not os.path.exists(fileLocation)):
            fileExists = False
        else:
            if(os.path.exists(fileLocation+"//"+file+".obj")):
                process(file, testfile)
        i+=1    
    
def process(file, log):
    bpy.ops.object.select_all()
    bpy.ops.object.delete()
    # import GERAS
    filePath = "O://geras/{0}/{0}.obj".format(file)
    bpy.ops.import_scene.obj(filepath=filePath)
    tablet = bpy.data.objects[0]
    # find dimensions and scale accordingly
    tabletDimensions = tablet.dimensions
    scale = min(10/tabletDimensions[0],10/tabletDimensions[1],10/tabletDimensions[2])
    bpy.ops.mesh.primitive_uv_sphere_add(size=200,location=(5,5,5))
    scalar = bpy.data.objects["Sphere"]
    bpy.context.scene.objects.active = tablet
    tablet.scale = (scale,scale,scale)
    
    # give 3dcursor new coordinates 
    bpy.context.scene.cursor_location = (0.0,0.0,0.0) 
    # set the origin on the current object to the 3dcursor location 
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN') 
    bpy.ops.transform.resize(value=(scale,scale,scale))
    bpy.context.scene.objects.active = scalar
    bpy.ops.transform.resize(value=(scale,scale,scale))
    
    bpy.ops.object.select_all()
    bpy.ops.object.join()
    try:
        bpy.ops.export.threejs(filepath = "O://geras/{0}/{0}.json".format(file))
    except:
	   log.writeLines("Unexpected Error: ", sys.exc_info()[0])
    
main()
    
