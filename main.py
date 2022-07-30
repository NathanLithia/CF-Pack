import os
from tkinter import *
from tkinter import ttk
import json
import shutil
try:
    with open('./res/variables/curseforge.txt', 'r') as file :
        Instances = file.read()
except:
    Instances = "None"
LastExportType = None
LastPackSelect = None
BackSlash = "\\"
DefaultCurseForgeExcludes = ["minecraftinstance.json", ".curseclient", "downloads"]
InstancesFolder = False

while InstancesFolder == False:
    if Instances.endswith("Curseforge\Instances") == False or Instances == "Curseforge\Instances" or os.path.exists(Instances) == False:
        print("Please input the path to Curseforges instances folder.")
        print(r"Example: C:\Users\Username\Curseforge\Instances")
        Instances = input("Path: ")
    else:
        with open('./res/variables/curseforge.txt', 'w') as file:
            file.write(Instances)
        print(f"Found CurseForge Instances: {Instances}")
        InstancesFolder = True

root = Tk()
win = ttk.Frame(root, padding=10)
win.grid()


def verify():
    PackPath = Instances+BackSlash+PackSelectBox['values'][PackSelectBox.current()]
    MinecraftInstance = json.load(open(PackPath+BackSlash+"minecraftinstance.json"))
    print("\n-----")
    print(f"Export Type: {ExportTypeBox['values'][ExportTypeBox.current()]}")
    print(f"InstanceName: {PackSelectBox['values'][PackSelectBox.current()]}")
    print(f"MinecraftVersion: {MinecraftInstance['baseModLoader']['minecraftVersion']}")
    print(f"Modloader: {MinecraftInstance['baseModLoader']['filename']}")
    print(f"PackName: {MinecraftInstance['name']}")
    print(f"Path: {PackPath}")
    print(f"Mod Count: {len(os.listdir(Instances+BackSlash+PackSelectBox['values'][PackSelectBox.current()]+BackSlash+'mods'))} Objects")
    print("-----")


def compile():
    verify()
    print("Starting Export!")
    ExportType = ExportTypeBox['values'][ExportTypeBox.current()]
    InstanceName = PackSelectBox['values'][PackSelectBox.current()]
    PackPath = Instances+BackSlash+PackSelectBox['values'][PackSelectBox.current()]
    MinecraftInstance = json.load(open(PackPath+BackSlash+"minecraftinstance.json"))
    MinecraftVersion = MinecraftInstance['baseModLoader']['minecraftVersion']
    ModLoader = MinecraftInstance['baseModLoader']['filename']
    ModLoaderVersion = MinecraftInstance['baseModLoader']['forgeVersion']
    PackName = MinecraftInstance['name']
    Mods = os.listdir(Instances+BackSlash+PackSelectBox['values'][PackSelectBox.current()]+BackSlash+'mods')
    ModCount = len(Mods)

    if ExportType == "Full Pack":
        if os.path.exists("./temp") == True: 
            print("Temp directory detected. removing.")
            shutil.rmtree("./temp")
        print("Creating. temp dir")
        os.mkdir("./temp")
        print("Creating MultiMC Manifest file.")
        if ModLoader.startswith('forge'):
            print("Using Forge MMC layout.")
            shutil.copyfile("./res/forge-mmc-pack.json", "./temp/mmc-pack.json")
            with open('./temp/mmc-pack.json', 'r') as file :
                filedata = file.read()
            filedata = filedata.replace('PLACEHOLDER-MINECRAFT-VERSION', MinecraftVersion)
            filedata = filedata.replace('PLACEHOLDER-FORGE-VERSION', ModLoaderVersion)
            print("Writing Forge MMC Changes")
            with open('./temp/mmc-pack.json', 'w') as file:
                file.write(filedata)
        elif ModLoader.startswith('fabric'):
            print("Using Fabric MMC layout.")
            shutil.copyfile("./res/fabric-mmc-pack.json", "./temp/mmc-pack.json")
            with open('./temp/mmc-pack.json', 'r') as file :
                filedata = file.read()
            filedata = filedata.replace('PLACEHOLDER-MINECRAFT-VERSION', MinecraftVersion)
            filedata = filedata.replace('PLACEHOLDER-FABRIC-VERSION', ModLoaderVersion)
            print("Writing Fabric MMC Changes")
            with open('./temp/mmc-pack.json', 'w') as file:
                file.write(filedata)
        else:
            return print(f"Error: Could not find pack type from following variable: {ModLoader}")
        shutil.copyfile("./res/instance.cfg", "./temp/instance.cfg")
        with open('./temp/instance.cfg', 'r') as file :
            filedata = file.read()
        filedata = filedata.replace('PLACEHOLDER-PACK-NAME', PackName)
        with open('./temp/instance.cfg', 'w') as file:
            file.write(filedata)
        shutil.copyfile("./res/.packignore", "./temp/.packignore")
        print("Copying instance contents.")
        shutil.copytree(PackPath, "./temp/.minecraft/")
        print("Done copying instance files!")
        print("Starting clean-up")
        for FileOrFolder in DefaultCurseForgeExcludes:
            if os.path.isfile(f"./temp/.minecraft/{FileOrFolder}") == True:
                print(f"Removing File: {FileOrFolder}")
                os.remove(f"./temp/.minecraft/{FileOrFolder}")
            elif os.path.isdir(f"./temp/.minecraft/{FileOrFolder}") == True:
                print(f"Removing Folder: {FileOrFolder}")
                shutil.rmtree(f"./temp/.minecraft/{FileOrFolder}")
        print("Done Cleanup!")
        print("Creating Importable Zip!")
        os.rename("./temp", f"./{InstanceName}")
        os.mkdir("./temp")
        shutil.move(f"./{InstanceName}", "./temp")
        shutil.make_archive(InstanceName, 'zip', "./temp")
        shutil.rmtree("./temp")
        print("Packing Complete!")
        shutil.move(f"./{InstanceName}.zip", f"./exports/{InstanceName}.zip")
        print('\a')
        print(f"Exported: ./exports/{InstanceName}.zip")



    elif ExportType == "Links Pack":
        print("Unfinished Please Use Full Pack!")
    else:
        return print("PackType not found!")



ExportTypeBox = ttk.Combobox(win, width=30, values=["Full Pack", "Links Pack"], state='readonly')
ExportTypeBox.grid(column=0, row=0)
ExportTypeBox.current(0)

PackSelectBox = ttk.Combobox(win, width=30, values=os.listdir(Instances))
PackSelectBox.grid(column=0, row=1)
PackSelectBox.current(0)

ttk.Button(win, text="Verify", command=verify).grid(column=1, row=0)
ttk.Button(win, text="Compile", command=compile).grid(column=1, row=1)

root.mainloop()

