import os
import zipfile


if __name__ == "__main__":

    print("Packaging addon into zip file...")

    zipf = zipfile.ZipFile("hypermesh.zip", "w", zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk("addon"):
        for f in filenames + dirnames: #include empty directories
            #the folder inside the zip should be called 'hypermesh', not 'addon'
            archive_dirpath = "hypermesh" + dirpath[5:]
            print("  Writing " + f)
            zipf.write(os.path.join(dirpath, f), os.path.join(archive_dirpath, f))
    zipf.close()

    print("Done.")
    print("")
    print("You can install the addon in Blender using")
    print("   File -> User Preferences... -> Install from File...")
    print("and selecting hypermesh.zip from this folder.")


