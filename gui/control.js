console.log('Start')
//var dragabble_items = []
var inputReady = false
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
async function slice_out(currentNode, fileName, offset, size){
    console.log('slicing file' + fileName + " " + offset + ' ' + size)
    document.getElementById('loadingAnim').style.visibility = 'visible'
    var success = 0
    //get the file name
    document.getElementById('fileNameInput').style.visibility = 'visible'
    console.log('visibility set')
    while(true){
        if (inputReady){
            inputReady = false
            newFile = document.getElementById('newFileName').value
            success = await eel.slice_file(newFile, fileName, offset, size)
            break
        }
        await sleep(100)
    }
    document.getElementById('fileNameInput').style.visibility = 'hidden'
    document.getElementById('loadingAnim').style.visibility = 'hidden'

    //create new node
    add_node(currentNode, newFile)
    

}

async function extract_file(currentNode, fileName){
    console.log('[JS] Extracting file ' + fileName)
    document.getElementById('loadingAnim').style.visibility = 'visible'
    var outputFolder = fileName.replace(/[^a-zA-Z0-9 ]/g, "") + '_extracted'
    var fileList = await eel.extract(fileName, outputFolder)()
    document.getElementById('loadingAnim').style.visibility = 'hidden'
    console.log(fileList)
    fileList.forEach(file => {
        if(file['dir']){

        }
        else{
            add_node(currentNode, outputFolder + '\\' + file['name'])
        }
    })

}

async function view_entropy(inputFile){
    document.getElementById('loadingAnim').style.visibility = 'visible'
    console.log('Fetching Entropy')
    eel.view_entropy(inputFile)()
    await sleep(4000)
    document.getElementById('loadingAnim').style.visibility = 'hidden'
    console.log('done')
}
async function add_node(currentNode, fileName){
    /*
    Call python function to perform a binwalk scan on the file and add the signatures as children to the current node
    */
    document.getElementById('loadingAnim').style.visibility = 'visible'
    console.log('Obtaining Signatures')
    var sigs = await eel.get_data(fileName)()
    console.log('Received Signatures')
    var oneFile = false
    if(sigs.length == 1) oneFile = true
    
    //create node
    //var nodeHtml = '<div class = "node" id = "' + fileName + '"><table><thead><tr><th>' + fileName + '</th></tr></thead>'
    var nodeHtml = '<div class = "node" id = "' + fileName + '"><table><tr><th colspan = "2">' + fileName + '</th></tr>'
    nodeHtml += '<tr><td colspan = "2">' + '<button class = "btn" onclick = "view_entropy(\'' + fileName + '\')">Entropy</button>' + '</td></tr></table><div class = "detail"><table>'
    sigs.forEach(sig => {
        let sigHtml = '<tr><td>' + sig.description + '</td><td> <button class = "btn" id = "' + sig.description + '"'
        if(oneFile){
            sigHtml += 'onclick = "extract_file(\'' + fileName + '\',\'' + fileName + '\')"> Extract'
        }
        else{
            sigHtml += 'onclick = "slice_out(\'' + fileName + '\',\'' + fileName + '\', ' + sig.offset +', ' + sig.size + ')"> Slice out'
        }
        sigHtml += '</button></td></tr>'
        nodeHtml += sigHtml
    });
    nodeHtml += '</table></div></div>'
    document.getElementById('bin-graph').innerHTML += nodeHtml 
    

    //add lines
    lines_connected[fileName] = []
    if (currentNode != ''){       
        create_line(currentNode, fileName)
    }
    dragElements.push(document.getElementById(fileName))
    refresh_drag_elements()
    document.getElementById('loadingAnim').style.visibility = 'hidden'
}

add_node('', 'dlink_router.bin')


