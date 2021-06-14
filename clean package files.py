import sys

# Path to where you extracted the Google-Earth-Decoder-optimisation-tools package:
sys.path.append("""C:\Path\To\Google-Earth-Decoder-optimisation-tools""")
from importlib import reload
from earth2msfstools.config import conf, JPG_FORMAT, PNG_FORMAT

# folder where the scenery projects are placed
conf.projects_folder = """C:\Project\Path"""

# folder of the scenery project you want to optimize
conf.project_name = "project-name"

# author name
conf.author_name = "authorname"

# folder that contains the fspackagetool exe that builds the MSFS packages
conf.fspackagetool_folder = "C:\\MSFS SDK\\Tools\\bin"

# minsize values per LOD, starting from a minLod of 17 (from the less detailed lod to the most detailed)
conf.target_lods = [0, 15, 50, 70, 80, 90, 100]
# if you use a minLod of 16, consider using this array instead
# conf.target_lods = [0, 5, 15, 50, 70, 80, 90, 100]

# name of the xml file that embeds the project definition (by default, project_name.xml or author_name+project_name.xml)
conf.project_file_name = 'SceneryProject.xml'

# name of the xml file that embeds the tile descriptions (by default, objects.xml)
conf.scene_file_name = "objects.xml"

# name of the xml file that embeds the package definitions (by default, project_name.xml or author_name+project_name.xml)
conf.package_definitions_file_name = "{:s}-{:s}.xml".format(conf.author_name, conf.project_name)

# enable the package compilation when the script has finished
conf.build_package_enabled = True

# use with care
conf.backup = True

if not 'clean_package_files' in sys.modules:
    from earth2msfstools import clean_package_files
else:
    reload(clean_package_files)
