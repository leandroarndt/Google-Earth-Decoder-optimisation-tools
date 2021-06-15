import glob, os, shutil, subprocess
from xml.dom.minidom import *
import xml.etree.ElementTree as ET
from .config import conf

######################################################
# script settings
######################################################

# constants
CEND = "\033[0m"
BOLD = "\033[01m"
CRED = "\033[31m"
CGREEN = "\033[32m"
CORANGE = "\033[38;5;214m"
CREDBG = "\033[41m"
CGREENBG = "\033[6;30;42m"
OK = "OK"
KO = "KO"
EOL = "\n"
MSFS_BUILD_EXE_FILE = "fspackagetool.exe"

#######################****************###########################

class ScriptError(Exception):
    def __init__(self, value):
        self.value = CREDBG + value + CEND + EOL
    def __str__(self):
        return repr(CREDBG + self.value + CEND + EOL)

# clear the system console
os.system("cls")

# initial directory
cwd = os.path.dirname(__file__)

src_project_folder = os.path.join(conf.projects_folder, conf.src_project_name)
dest_project_folder = os.path.join(conf.projects_folder, conf.project_name)

# project file names fallback
if not os.path.isfile(os.path.join(src_project_folder, conf.src_project_file_name)):
    if os.path.isfile(os.path.join(src_project_folder, '{author_name:s}-{project_name:s}.xml'.format(author_name=conf.author_name.lower(), project_name=conf.src_project_name.lower()))):
        conf.src_project_file_name = '{author_name:s}-{project_name:s}.xml'.format(author_name=conf.author_name.lower(), project_name=conf.src_project_name.lower())
    else:
        conf.src_project_file_name = conf.src_project_name.lower() + ".xml"

if not os.path.isfile(os.path.join(dest_project_folder, conf.project_file_name)):
    if os.path.isfile(os.path.join(dest_project_folder, '{author_name:s}-{project_name:s}.xml'.format(author_name=conf.author_name.lower(), project_name=conf.project_name.lower()))):
        conf.project_file_name = '{author_name:s}-{project_name:s}.xml'.format(author_name=conf.author_name.lower(), project_name=conf.project_name.lower())
    else:
        conf.project_file_name = conf.project_name.lower() + ".xml"

# package definitions folder
src_package_definitions_folder = os.path.join(src_project_folder, "PackageDefinitions")
dest_package_definitions_folder = os.path.join(dest_project_folder, "PackageDefinitions")

# package definitions file names fallback
if not os.path.isfile(os.path.join(src_package_definitions_folder, conf.src_package_definitions_file_name)):
    if os.path.isfile(os.path.join(src_package_definitions_folder, '{author_name:s}-{project_name:s}.xml'.format(author_name=conf.author_name.lower(), project_name=conf.src_project_name.lower()))):
        conf.src_package_definitions_file_name = '{author_name:s}-{project_name:s}.xml'.format(author_name=conf.author_name.lower(), project_name=conf.src_project_name.lower())
    else:
        conf.src_package_definitions_file_name = conf.src_project_name.lower() + ".xml"

if not os.path.isfile(os.path.join(dest_package_definitions_folder, conf.package_definitions_file_name)):
    if os.path.isfile(os.path.join(dest_package_definitions_folder, '{author_name:s}-{project_name:s}.xml'.format(author_name=conf.author_name.lower(), project_name=conf.project_name.lower()))):
        conf.package_definitions_file_name = '{author_name:s}-{project_name:s}.xml'.format(author_name=conf.author_name.lower(), project_name=conf.project_name.lower())
    else:
        conf.package_definitions_file_name = conf.project_name.lower() + ".xml"

# objects folders
src_objects_folder = os.path.join(src_project_folder, "PackageSources", "modelLib")
dest_objects_folder = os.path.join(dest_project_folder, "PackageSources", "modelLib")
# scene folders
src_scene_folder = os.path.join(src_project_folder, "PackageSources", "scene")
dest_scene_folder = os.path.join(dest_project_folder, "PackageSources", "scene")
# backup folders
src_backup_folder = os.path.join(src_project_folder, "backup")
dest_backup_folder = os.path.join(dest_project_folder, "backup", "merge_sceneries")
# backup fps_modelLib folders
src_backup_modelLib_folder = os.path.join(src_backup_folder, "modelLib")
dest_backup_modelLib_folder = os.path.join(dest_backup_folder, "modelLib")
# backup scene folders
src_backup_scene_folder = os.path.join(src_backup_folder, "scene")
dest_backup_scene_folder = os.path.join(dest_backup_folder, "scene")
# positions folders
src_positions_folder = os.path.join(src_project_folder, "positions")
dest_positions_folder = os.path.join(dest_project_folder, "positions")
# MSFS temp folder
msfs_temp_folder = os.path.join(dest_project_folder, "_PackageInt")

######################################################
# colored print methods
######################################################
def pr_red(skk):       print(CRED, format(skk), CEND)
def pr_green(skk):     print(CGREEN, format(skk), CEND)
def pr_ko_red(skk):    print("-", format(skk), BOLD + CRED, KO, CEND)
def pr_ko_orange(skk): print("-", format(skk), BOLD + CORANGE, KO, CEND)
def pr_ok_green(skk):  print("-", format(skk), BOLD + CGREEN, OK, CEND)
def pr_bg_red(skk):    print(CREDBG, format(skk), CEND)
def pr_bg_green(skk):  print(CGREENBG, format(skk), CEND)

######################################################
# check configuration methods
######################################################

def check_configuration():
    error_msg = "Configuration error found ! "
    warning_msg = "Configuration warning ! "

    # check if the projects folder exists
    if not os.path.isdir(conf.projects_folder):
        pr_ko_red   ("conf.projects_folder value                   ")
        raise ScriptError(error_msg + "The folder containing your projects (" + conf.projects_folder + ") was not found. Please check the conf.projects_folder value")
    pr_ok_green     ("conf.projects_folder value                   ")

    # check the projects names
    if not os.path.isdir(src_project_folder):
        pr_ko_red   ("conf.src_project_name value                  ")
        raise ScriptError(error_msg + "Source project folder " + src_project_folder + " not found. Please check the conf.src_project_name value")
    pr_ok_green     ("conf.src_project_name value                  ")
    if not os.path.isdir(dest_project_folder):
        pr_ko_red   ("conf.project_name value                 ")
        raise ScriptError(error_msg + "Destination project folder " + dest_project_folder + " not found. Please check the conf.project_name value")
    pr_ok_green     ("conf.project_name value                 ")

    # check if the project files are reachable
    if not os.path.isfile(os.path.join(src_project_folder, conf.src_project_file_name)):
        pr_ko_red   ("conf.src_project_file_name value             ")
        raise ScriptError(error_msg + "Source project file (" + os.path.join(src_project_folder, conf.src_project_file_name) + ") not found. Please check the conf.src_project_file_name value")
    pr_ok_green     ("conf.src_project_file_name value             ")
    if not os.path.isfile(os.path.join(dest_project_folder, conf.project_file_name)):
        pr_ko_red   ("conf.project_file_name value            ")
        raise ScriptError(error_msg + "Destination project file (" + os.path.join(dest_project_folder, conf.project_file_name) + ") not found. Please check the conf.project_file_name value")
    pr_ok_green     ("conf.project_file_name value            ")

    # check if the fspackagetool.exe file is reachable
    if not os.path.isfile(os.path.join(conf.fspackagetool_folder, MSFS_BUILD_EXE_FILE)):
        pr_ko_orange("conf.fspackagetool_folder value              ")
        conf.build_package_enabled = False
        print(CORANGE + warning_msg + MSFS_BUILD_EXE_FILE + " bin file not found. Automatic package building disabled" + CEND + EOL)
    pr_ok_green     ("conf.fspackagetool_folder value              ")

    # check if the package definitions folders exist
    if not os.path.isdir(src_package_definitions_folder):
        pr_ko_red   ("src_package_definitions_folder value    ")
        raise ScriptError(error_msg + "The folder containing the package definitions of the source project (" + src_package_definitions_folder + ") was not found. Please check the src_package_definitions_folder value")
    pr_ok_green     ("src_package_definitions_folder value    ")
    if not os.path.isdir(dest_package_definitions_folder):
        pr_ko_red   ("dest_package_definitions_folder value   ")
        raise ScriptError(error_msg + "The folder containing the package definitions of the destination project (" + dest_package_definitions_folder + ") was not found. Please check the dest_package_definitions_folder value")
    pr_ok_green     ("dest_package_definitions_folder value   ")

    # check if the package definitions file names are reachable
    if not os.path.isfile(os.path.join(src_package_definitions_folder, conf.src_package_definitions_file_name)):
        pr_ko_red   ("conf.src_package_definitions_file_name value ")
        raise ScriptError(error_msg + "Source package definitions file (" + os.path.join(src_package_definitions_folder, conf.src_package_definitions_file_name) + ") not found. Please check the conf.src_package_definitions_file_name value")
    pr_ok_green     ("conf.src_package_definitions_file_name value ")
    if not os.path.isfile(os.path.join(dest_package_definitions_folder, conf.package_definitions_file_name)):
        pr_ko_red   ("conf.package_definitions_file_name value")
        raise ScriptError(error_msg + "Destination package definitions file (" + os.path.join(dest_package_definitions_folder, conf.package_definitions_file_name) + ") not found. Please check the conf.package_definitions_file_name value")
    pr_ok_green     ("conf.package_definitions_file_name value")

def check_package_sources_configuration():
    error_msg = "Configuration error found ! "

    # check if the objects folders exist
    if not os.path.isdir(src_objects_folder):
        pr_ko_red   ("src_objects_folder value                ")
        raise ScriptError(error_msg + "The folder containing the objects of the source project (" + src_objects_folder + ") was not found. Please check the src_objects_folder value")
    pr_ok_green     ("src_objects_folder value                ")
    if not os.path.isdir(dest_objects_folder):
        pr_ko_red   ("dest_objects_folder value               ")
        raise ScriptError(error_msg + "The folder containing the objects of the destination project (" + dest_objects_folder + ") was not found. Please check the dest_objects_folder value")
    pr_ok_green     ("dest_objects_folder value               ")

    # check if the folders containing the description files of the scene exist
    if not os.path.isdir(src_scene_folder):
        pr_ko_red   ("src_scene_folder value                  ")
        raise ScriptError(error_msg + "The folder containing the description files of the source scene (" + src_scene_folder + ") was not found. Please check the src_scene_folder value")
    pr_ok_green     ("src_scene_folder value                  ")
    if not os.path.isdir(dest_scene_folder):
        pr_ko_red   ("dest_scene_folder value                 ")
        raise ScriptError(error_msg + "The folder containing the description files of the destination scene (" + dest_scene_folder + ") was not found. Please check the dest_scene_folder value")
    pr_ok_green     ("dest_scene_folder value                 ")

    # check if the description file of the scene is reachable
    if not os.path.isfile(os.path.join(src_scene_folder, conf.src_scene_file_name)):
        pr_ko_red   ("conf.src_scene_file_name value               ")
        raise ScriptError(error_msg + "Description file of the source scene (" + os.path.join(src_scene_folder, conf.src_scene_file_name) + ") not found. Please check the conf.src_scene_file_name value")
    pr_ok_green     ("conf.src_scene_file_name value               ")
    if not os.path.isfile(os.path.join(dest_scene_folder, conf.scene_file_name)):
        pr_ko_red   ("conf.scene_file_name value              ")
        raise ScriptError(error_msg + "Description file of the destination scene (" + os.path.join(dest_scene_folder, conf.scene_file_name) + ") not found. Please check the conf.scene_file_name value")
    pr_ok_green     ("conf.scene_file_name value              ")

    # check if the folders containing the textures of the scene exist
    if not os.path.isdir(src_textures_folder):
        pr_ko_red   ("src_textures_folder value               ")
        raise ScriptError(error_msg + "The folder containing the textures of the source scene (" + src_textures_folder + ") was not found. Please check the src_textures_folder value")
    pr_ok_green     ("src_textures_folder value               ")
    if not os.path.isdir(dest_textures_folder):
        pr_ko_red   ("dest_textures_folder value              ")
        raise ScriptError(error_msg + "The folder containing the textures of the destination scene (" + dest_textures_folder + ") was not found. Please check the dest_textures_folder value")
    pr_ok_green     ("dest_textures_folder value              ")

    print(EOL + "-------------------------------------------------------------------------------")

######################################################
# File manipulation methods
######################################################
def line_prepender(filename, line):
    with open(filename, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip("\r\n") + "\n" + content)

######################################################
# File replacement methods
######################################################
def replace_in_file(file, text, replacement):
    updated_file = open(file, "rt")
    data = updated_file.read()
    data = data.replace(text,replacement)
    updated_file.close()
    updated_file = open(file, "wt")
    updated_file.write(data)
    updated_file.close()

##########################################################################
# function to pretty print the XML code
##########################################################################
def prettyPrint(element, level=0):
    '''
    Function taken from elementTree site:
    http://effbot.org/zone/element-lib.htm#prettyprint

    '''
    indent = '\n' + level * '  '
    if len(element):
        if not element.text or not element.text.strip():
            element.text = indent + '  '

        if not element.tail or not element.tail.strip():
            element.tail = indent

        for element in element:
            prettyPrint(element, level + 1)

        if not element.tail or not element.tail.strip():
            element.tail = indent

    else:
        if level and (not element.tail or not element.tail.strip()):
            element.tail = indent

    return element

##########################################################################
# Backup the destination packageSources files before the merging process
##########################################################################
def backup_files():
    os.chdir(dest_objects_folder)
    for file in glob.glob("*.*"):
        file_name = os.path.basename(file)
        if not os.path.isfile(os.path.join(dest_backup_modelLib_folder, file_name)):
            print("backup file ", file_name)
            shutil.copyfile(file, os.path.join(dest_backup_modelLib_folder, file_name))

    os.chdir(dest_textures_folder)
    for file in glob.glob("*.*"):
        file_name = os.path.basename(file)
        if not os.path.isfile(os.path.join(dest_backup_modelLib_folder, "texture", file_name)):
            print("backup texture file ", file_name)
            shutil.copyfile(file, os.path.join(dest_backup_modelLib_folder, "texture", file_name))

    os.chdir(dest_scene_folder)
    for file in glob.glob("*.*"):
        file_name = os.path.basename(file)
        if not os.path.isfile(os.path.join(dest_backup_scene_folder, file_name)):
            shutil.copyfile(file, os.path.join(dest_backup_scene_folder, file_name))

##########################################################################################
# Copy files from the destination packageSources to the destination packageSources folder
##########################################################################################

def copy_file(file, dest_folder):
    file_name = os.path.basename(file)

    if not os.path.isfile(os.path.join(dest_folder, file_name)):
        print("copy file ", file_name)
    else:
        print("overwrite file ", file_name)

    shutil.copyfile(file, os.path.join(dest_folder, file_name))

def copy_files():
    os.chdir(src_objects_folder)
    for file in glob.glob("*.*"):
        copy_file(file, dest_objects_folder)

    os.chdir(src_textures_folder)
    for file in glob.glob("*.*"):
        copy_file(file, dest_textures_folder)

    os.chdir(src_scene_folder)
    for file in glob.glob("*.*"):
        file_name = os.path.basename(file)
        if file_name != conf.src_scene_file_name and file_name != conf.scene_file_name:
            copy_file(file, dest_scene_folder)


##########################################################################################
# Update the destination scene xml file to display the source tiles
##########################################################################################

def update_dest_scene_file():
    os.chdir(src_objects_folder)
    for file in glob.glob("*.xml"):
        file_name = os.path.basename(file)
        print(os.path.join(src_objects_folder, file_name))
        parser = ET.XMLParser(encoding='utf-8')
        tree = ET.parse(file, parser=parser)
        root = tree.getroot()
        new_guid  = root.get("guid")
        add_guid = False

        dest_objects_tree = ET.parse(os.path.join(dest_scene_folder, conf.scene_file_name))
        dest_objects_root = dest_objects_tree.getroot()

        src_objects_tree = ET.parse(os.path.join(src_scene_folder, conf.src_scene_file_name))
        src_objects_root = src_objects_tree.getroot()

        if not os.path.isfile(os.path.join(dest_objects_folder, file_name)):
            add_guid = True

        if not add_guid:
            guid_found = False
            print(os.path.join(dest_objects_folder, file_name))
            dest_tree = ET.parse(os.path.join(dest_objects_folder, file_name))
            dest_root = dest_tree.getroot()
            guid  = dest_root.get("guid")

            for scenery_object in dest_objects_root.findall("./SceneryObject/LibraryObject[@name='" + guid.upper() + "']"):
                print("old guid: ", scenery_object.get("name"))
                print("new guid: ", str(new_guid).upper())
                scenery_object.set("name", str(new_guid).upper())
                guid_found = True

            for scenery_object in dest_objects_root.findall("./Group/SceneryObject/LibraryObject[@name='" + guid.upper() + "']"):
                print("old guid: ", scenery_object.get("name"))
                print("new guid: ", str(new_guid).upper())
                scenery_object.set("name", str(new_guid).upper())
                guid_found = True

            if not guid_found:
                add_guid = True

        if add_guid:
            for scenery_object in src_objects_root.findall("./SceneryObject/LibraryObject[@name='" + new_guid.upper() + "']/.."):
                print("new guid: ", str(new_guid).upper())
                src_scenery_object = scenery_object
                print("add new SceneryObject", src_scenery_object.tag, src_scenery_object.attrib)
                dest_objects_root.append(src_scenery_object)

            for scenery_object in src_objects_root.findall("./Group/SceneryObject/LibraryObject[@name='" + new_guid.upper() + "']/.."):
                print("new guid: ", str(new_guid).upper())
                src_scenery_object = scenery_object
                print("add new SceneryObject", src_scenery_object.tag, src_scenery_object.attrib)
                dest_objects_root.append(src_scenery_object)


        dest_objects_tree.write(os.path.join(dest_scene_folder, conf.scene_file_name))
        prettyPrint(element=dest_objects_root)
        line_prepender(os.path.join(dest_scene_folder, conf.scene_file_name), '<?xml version="1.0"?>')

######################################################
# build merged scenery into new MSFS package
######################################################
def build_package():
    error_msg = "MSFS SDK tools not installed"

    try:
        os.chdir(conf.fspackagetool_folder)
        print("fspackagetool.exe \"" + os.path.join(dest_project_folder, conf.project_file_name) + "\" -rebuild -outputdir \"" + dest_project_folder)
        subprocess.run("fspackagetool.exe \"" + os.path.join(dest_project_folder, conf.project_file_name) + "\" -rebuild -outputdir \"" + dest_project_folder, shell=True, check=True)
    except:
        raise ScriptError(error_msg)

#######################****************###########################

##################################################################
#                        Main process
##################################################################

try:
    check_configuration()

    if not os.path.isdir(os.path.join(src_project_folder, "PackageSources", "modelLib")) and not os.path.isdir(os.path.join(src_project_folder, "PackageSources", conf.src_project_name.lower() + "-modelLib")):
        print("The modelLib folder was not found for the projet", conf.src_project_name, ". Abort optimization script. Please rename your modelLib folder like this:", os.path.join(src_project_folder, "PackageSources", conf.src_project_name.lower() + "-modelLib"))
    else:
        if not os.path.isdir(os.path.join(dest_project_folder, "PackageSources", "modelLib")) and not os.path.isdir(os.path.join(dest_project_folder, "PackageSources", conf.project_name.lower() + "-modelLib")):
            print("The modelLib folder was not found for the projet", conf.project_name, ". Abort optimization script. Please rename your modelLib folder like this:", os.path.join(dest_project_folder, "PackageSources", conf.project_name.lower() + "-modelLib"))
        else:
            # change modelib folder to fix CTD issues (see https://flightsim.to/blog/creators-guide-fix-ctd-issues-on-your-scenery/)
            os.chdir(src_project_folder)
            if os.path.isdir(src_objects_folder):
                os.rename(src_objects_folder, os.path.join(src_project_folder, "PackageSources", conf.src_project_name.lower() + "-modelLib"))

            os.chdir(dest_project_folder)
            if os.path.isdir(dest_objects_folder):
                os.rename(dest_objects_folder, os.path.join(dest_project_folder, "PackageSources", conf.project_name.lower() + "-modelLib"))

            src_objects_folder = os.path.join(src_project_folder, "PackageSources", conf.src_project_name.lower() + "-modelLib")
            dest_objects_folder = os.path.join(dest_project_folder, "PackageSources", conf.project_name.lower() + "-modelLib")
            # textures folder
            src_textures_folder = os.path.join(src_objects_folder, "texture")
            dest_textures_folder = os.path.join(dest_objects_folder, "texture")

            check_package_sources_configuration()

            # fix package definitions
            replace_in_file(os.path.join(src_package_definitions_folder, conf.src_package_definitions_file_name), os.path.join("PackageSources", "modelLib"), os.path.join("PackageSources", conf.src_project_name.lower() + "-modelLib"))
            replace_in_file(os.path.join(dest_package_definitions_folder, conf.package_definitions_file_name), os.path.join("PackageSources", "modelLib"), os.path.join("PackageSources", conf.project_name.lower() + "-modelLib"))

            if conf.backup:
                # create the backup folders
                if not os.path.isdir(os.path.join(dest_project_folder, "backup")):
                    os.mkdir(os.path.join(dest_project_folder, "backup"))
                if not os.path.isdir(dest_backup_folder):
                    os.mkdir(dest_backup_folder)
                if not os.path.isdir(dest_backup_scene_folder):
                    os.mkdir(dest_backup_scene_folder)
                if not os.path.isdir(dest_backup_modelLib_folder):
                    os.mkdir(dest_backup_modelLib_folder)
                if not os.path.isdir(os.path.join(dest_backup_modelLib_folder, "texture")):
                    os.mkdir(os.path.join(dest_backup_modelLib_folder, "texture"))

                print("-------------------------------------------------------------------------------")
                print("--------------------------------- BACKUP FILES --------------------------------")
                print("-------------------------------------------------------------------------------")

                backup_files()

            print("-------------------------------------------------------------------------------")
            print("------------------------ UPDATE DESTINATION SCENE FILE ------------------------")
            print("-------------------------------------------------------------------------------")

            update_dest_scene_file()

            print("-------------------------------------------------------------------------------")
            print("---------------------------------- COPY FILES ---------------------------------")
            print("-------------------------------------------------------------------------------")

            copy_files()

            if conf.build_package_enabled:
                if os.path.isdir(msfs_temp_folder):
                    print("Remove MSFS temp folder for future build...")
                    shutil.rmtree(msfs_temp_folder)
                build_package()

        print(EOL)
        pr_bg_green("Script correctly applied" + CEND)

except ScriptError as ex:
    error_report = "".join(ex.value)
    print(EOL + error_report)
    pr_bg_red("Script aborted" + CEND)
except RuntimeError as ex:
    print(EOL + ex)
    pr_bg_red("Script aborted" + CEND)
finally:
    os.chdir(cwd)