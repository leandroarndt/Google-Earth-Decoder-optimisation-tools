import sys
sys.path.append("""C:\Path\To\earth2msfstools""")
from importlib import reload
from earth2msfstools.config import conf

# backup files?
conf.backup = True

# folder where the scenery projects are placed
conf.projects_folder = """C:\Project\Path"""

# folder of the scenery project you want to add to the final scenery project
conf.src_project_name = "src-project-name"

# folder of the final scenery project you want to merge into
conf.project_name = "dest-project-name"

# author name
conf.author_name = "authorname"

# folder that contains the fspackagetool exe that builds the MSFS packages
conf.fspackagetool_folder = "C:\\MSFS SDK\\Tools\\bin"

# name of the xml file that embeds the project definition (by default, project_name.xml or conf.author_name+conf.src_project_name.xml)
# for the scenery project you want to add to the final scenery project
conf.src_project_file_name = "SceneryProject.xml"

# name of the xml file that embeds the project definition (by default, project_name.xml or conf.author_name+conf.project_name.xml)
# for the final scenery project you want to merge into
conf.project_file_name = "SceneryProject.xml"

# name of the xml file that embeds the tile descriptions (by default, objects.xml)
# for the scenery project you want to add to the final scenery project
conf.src_scene_file_name = "objects.xml"

# name of the xml file that embeds the tile descriptions (by default, objects.xml) 
# for the final scenery project you want to merge into
conf.scene_file_name = "objects.xml"

# name of the xml file that embeds the package definitions (by default, project_name.xml or conf.author_name+conf.project_name.xml)
# for the scenery project you want to add to the final scenery project
conf.src_package_definitions_file_name = "{:s}-{:s}.xml".format(self.author_name, self.src_project_name)

# name of the xml file that embeds the package definitions (by default, project_name.xml or conf.author_name+conf.src_project_name.xml)
# for the final scenery project you want to merge into
conf.package_definitions_file_name = "{:s}-{:s}.xml".format(self.author_name, self.project_name)

# enable the package compilation when the script has finished
conf.build_package_enabled = True

# Backup files may not be needed if original meshes have not been modified (fresh download)
conf.backup = True

if not 'merge_sceneries' in sys.modules:
    from earth2msfstools import merge_sceneries
else:
    reload(merge_sceneries)