import os.path

JPG_FORMAT = "jpg"
PNG_FORMAT = "png"

class Config(object):
    def __init__(self):
        # reduce number of texture files (Lily Texture Packer addon is necessary https://gumroad.com/l/DFExj)
        self.bake_textures_enabled = True

        # folder where the scenery projects are placed
        self.projects_folder = """C:\Project\Path"""

        # folder of the scenery project you want to optimize
        self.project_name = "project-name"

        # author name
        self.author_name = "authorname"

        # folder that contains the node js script that retrieves the Google Earth coords
        self.node_js_folder = os.path.dirname(__file__) #"""D:\Documents\Flight Simulator\Google-Earth-Decoder-optimisation-tools-main"""

        # folder that contains the fspackagetool exe that builds the MSFS packages
        self.fspackagetool_folder = "C:\\MSFS SDK\\Tools\\bin"

        # minsize values per LOD, starting from a minLod of 17 (from the less detailed lod to the most detailed)
        self.target_lods = [0, 15, 50, 70, 80, 90, 100]
        # if you use a minLod of 16, consider using this array instead
        # target_lods = [0, 5, 15, 50, 70, 80, 90, 100]

        # name of the xml file that embeds the project definition (by default, project_name.xml or author_name+project_name.xml)
        self.project_file_name = 'SceneryProject.xml'

        # name of the xml file that embeds the tile descriptions (by default, objects.xml)
        self.scene_file_name = "objects.xml"

        # name of the xml file that embeds the package definitions (by default, project_name.xml or author_name+project_name.xml)
        self.package_definitions_file_name = "{:s}-{:s}.xml".format(self.author_name, self.project_name)

        # enable the package compilation when the script has finished
        self.build_package_enabled = True

        # output format of the texture files (jpg or png)
        self.output_texture_format = PNG_FORMAT

        # Backup files
        self.backup = True
        # ***************** merge sceneries specific options *****************
        # folder of the scenery project you want to add to the final scenery project
        self.src_project_name = "src-project-name"

        # name of the xml file that embeds the project definition (by default, project_name.xml or author_name+conf.src_project_name.xml)
        # for the scenery project you want to add to the final scenery project
        self.src_project_file_name = "SceneryProject.xml"

        # name of the xml file that embeds the package definitions (by default, project_name.xml or author_name+conf.src_project_name.xml)
        # for the final scenery project you want to merge into
        self.src_package_definitions_file_name = "{:s}-{:s}.xml".format(self.author_name, self.src_project_name)


if not 'conf' in dir():
    conf = Config()