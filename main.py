import binwalk
import os
import eel
import magic
import glob
from enum import Enum

class ARCH_TYPE(Enum):
    MIPS = 1
    ARM = 2

ARCH = None

eel.init('gui')

@eel.expose
def slice_file(outputFile, inputFile, offset, len):
    print('[SLICE]\nInput : ' + inputFile + '\nOutput : ' + outputFile + '\nOffset : ' +str(offset) + '\nlen : ' + str(len))
    with open(inputFile, 'rb') as i:
        with open(outputFile,'wb') as o:
            i.seek(offset)
            for _ in range(0, len):
                o.write(i.read(1))
    return 1

@eel.expose
def extract(fileName, outputFolder):
    print('[INFO] Extracting file ' + fileName)
    command = '7z e ' + fileName + ' -o' + outputFolder
    print(command)
    os.system(command)
    obj = os.scandir(outputFolder)
    files = []
    for e in obj:
        d = {
                'name' : e.name,
                'dir' : e.is_dir() 
            }
        files.append(d)
    
    return files
            

        

    

@eel.expose 
def view_entropy(inputFile):
    """
    display entropy graph of the input file
    """
    print('[Python] Entropy for ' + inputFile)
    binwalk.scan (inputFile, **{'entropy' : True, 'quiet' : True})

@eel.expose
def get_data (inputFile):
    """
    Perform binwalk scan on the input file and return the signatures as a list of nodes
    """
    print('[INFO] Running binwalk scan on ' + inputFile)
    nodes = []
    fileSize = os.path.getsize(inputFile)
    res = binwalk.scan (inputFile, **{'signature' : True, 'quiet' : True})[0].results
    nResults = len(res)
    for i in range(0, nResults):
        nodeInfo = {
            'description' : res[i].description,
            'offset' : res[i].offset,
            'size' : (fileSize - res[i].offset) if (i == (nResults - 1)) else (res[i + 1].offset - res[i].offset),
        }
        nodes.append(nodeInfo)
    print('Scan Complete')
    return nodes

def find_arch(fsRoot):
    #get an executable
    #get header info
    #search for arch keywords in header
    global ARCH
    archName = None
    archBit = 32
    for fileName in glob.iglob(fsRoot + '**/**', recursive = True):
        if os.path.isdir(fileName):
            continue
        try:
            headerDescription = magic.from_file(fileName)
        except:
            continue
        if headerDescription:
            headerDescription = headerDescription.lower()
            if 'mips' in headerDescription:
                archName = ARCH_TYPE.MIPS
            elif 'arm' in headerDescription:
                archName = ARCH_TYPE.ARM
            
            if '64' in headerDescription and ('32' not in headerDescription):
                archBit = 64
    
    if archName:
        ARCH = {
                'type' : archName,
                'bit' : archBit
                }
        print('Architecture : ' + str(ARCH['type']) + ' ' + str(ARCH['bit']))

    else:
        print('Failed to infer architecture. Please select manually.')
        #create method for manual selection


    
@eel.expose
def spawn_shell(fsRoot):
    global ARCH
    #fsRoot has trailing /
    #find the arch
    arch = None
    if not ARCH:
        find_arch(fsRoot)
    
    arch = ARCH['type']

    if arch == ARCH_TYPE.MIPS:
        archName = 'mips'
    #copy qemu static binary
    staticName = 'qemu-' + archName + '-static'
    os.system('sudo cp /bin/' + staticName + ' ' + fsRoot + 'usr/bin/')
    
    #spawn shell
    os.system('gnome-terminal --command="sudo chroot ' + fsRoot + ' /bin/sh" &')
    return 1
@eel.expose
def open_in_explorer(fsRoot):
    return os.system('nautilus ' + fsRoot)



@eel.expose
def extract_file_system (inputFile, outputFolder):
    if 'squashfs' in magic.from_file(inputFile).lower():
        print('Extracting squashfs File System')
        command = 'sudo unsquashfs -f -d ./' + outputFolder + '/ ./' + inputFile
        os.system(command)
    return os.path.abspath(outputFolder) + '/'


@eel.expose
def create_vm():
    global ARCH
    arch = None
    if not ARCH:
        find_arch(fsRoot)
    
    if ARCH['type'] == ARCH_TYPE.MIPS:
        if ARCH['bit'] == 32:
            os.system('qemu-system-mipsel -M malta -kernel ./emu/vmlinux-3.2.0-4-4kc-malta -hda ./emu/debian_wheezy_mipsel_standard.qcow2 -append "root=/dev/sda1 console=tty0')
    
    return 1
    

eel.start('index.html')
