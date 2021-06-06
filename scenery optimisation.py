import sys, importlib, os.path
sys.path.append("""C:\Path\To\earth2msfstools""")

from earth2msfstools import config

# reduce number of texture files (Lily Texture Packer addon is necessary https://gumroad.com/l/DFExj)
config.conf.bake_textures_enabled = True

# folder where the scenery projects are placed
config.conf.projects_folder = """C:\Project\Path"""

# folder of the scenery project you want to optimize
config.conf.project_name = "project-name"

# author name
config.conf.author_name = "authorname"

# folder that contains the fspackagetool exe that builds the MSFS packages
config.conf.fspackagetool_folder = "C:\\MSFS SDK\\Tools\\bin"

# minsize values per LOD, starting from a minLod of 17 (from the less detailed lod to the most detailed)
config.conf.target_lods = [0, 15, 50, 70, 80, 90, 100]
# if you use a minLod of 16, consider using this array instead
# config.conf.target_lods = [0, 5, 15, 50, 70, 80, 90, 100]

# name of the xml file that embeds the project definition (by default, project_name.xml or author_name+project_name.xml)
config.conf.project_file_name = 'SceneryProject.xml'

# name of the xml file that embeds the tile descriptions (by default, objects.xml)
config.conf.scene_file_name = "objects.xml"

# name of the xml file that embeds the package definitions (by default, project_name.xml or author_name+project_name.xml)
config.conf.package_definitions_file_name = "{:s}-{:s}.xml".format(config.conf.author_name, config.conf.project_name)

# enable the package compilation when the script has finished
config.conf.build_package_enabled = True

# output format of the texture files (jpg or png)l
config.conf.output_texture_format = config.PNG_FORMAT

if not 'scenery_optimisation' in sys.modules:
    from earth2msfstools import scenery_optimisation
else:
    reload(scenery_optimisation)
