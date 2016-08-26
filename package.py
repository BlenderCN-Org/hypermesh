import os
import zipfile
import re

if __name__ == "__main__":

    print("Packaging addon into zip file...")

    # determine the version of the addon from the bl_info field in __init__.py
    major = -1
    minor = -1
    with open("addon/__init__.py") as f:
        for line in f:
            match = re.match(r"\s*\"version\"\s*:\s*\(\s*(\d+)\s*,\s*(\d+)\s*(,\s*\d+)?\s*\)", line)
            if match:
                major = match.group(1)
                minor = match.group(2)
                break
    if major != -1: # succeeded in determination
        zipname = "hypermesh-" + major + "." + minor + ".zip"
    else: # failed to find version number
        zipname = "hypermesh.zip"


    zipf = zipfile.ZipFile(zipname, "w", zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk("addon"):
        for f in filenames + dirnames: #include empty directories
            if "__pycache__" in dirpath or "__pycache__" in f:
                continue
            #the folder inside the zip should be called 'hypermesh', not 'addon'
            archive_dirpath = "hypermesh" + dirpath[5:]
            print("  Writing " + f)
            zipf.write(os.path.join(dirpath, f), os.path.join(archive_dirpath, f))
    zipf.close()

    print("Done.")
    print("")
    print("You can install the addon in Blender using")
    print("   File -> User Preferences... -> Install from File...")
    print("and selecting " + zipname + " from this folder.")
    print("Afterwards, enable it in the user preferences.")


