import binwalk
import os
import filetype
import eel
import magic

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
    print('[PYTHON] Extracting file ' + fileName)
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
    print('Running binwalk scan on ' + inputFile)
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

@eel.expose
def extract_file_system (inputFile, outputFolder):
    if 'squashfs' in magic.from_file(inputFile).lower():
        print('Extracting squashfs File System')
        command = 'unsquashfs -f -d ./' + outputFolder + '/ ./' + inputFile
        os.system(command)
eel.start('index.html')
