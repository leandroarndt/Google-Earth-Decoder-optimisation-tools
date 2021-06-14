import sys

# Path to where you extracted the Google-Earth-Decoder-optimisation-tools package:
sys.path.append("""C:\Path\To\Google-Earth-Decoder-optimisation-tools""")
from importlib import reload
from earth2msfstools.config import conf

# reduce number of texture files (Lily Texture Packer addon is necessary https://gumroad.com/l/DFExj)
conf.bake_textures_enabled = True

# folder where the scenery projects are placed
conf.projects_folder = """C:\Project\Path"""

# folder of the scenery project you want to optimize
conf.project_name = "project-name"

# author name
conf.author_name = "authorname"

# folder that contains the compressonator exe that converts dds files
compressonatortool_folder = "compressonator_folder"

# number of compressonator tasks running at the same time
nb_parallel_tasks = 20

if not 'compress_built_package' in sys.modules:
    from earth2msfstools import compress_built_package
else:
    reload(compress_built_package)