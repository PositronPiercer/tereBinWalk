lines_connected = {} // "id : {ids of lines connected}"

function create_line(start, end){
    //create a line between items with ids : start and end
    var lineId = start + end
    var gph = document.getElementById('bin-graph')
    gph.innerHTML += '<svg height = "100%" width = "100%""><line id = "' + lineId + '" stroke = "black"></svg>'
    lines_connected[start].push({
        lineId : lineId,
        start : start,
        end : end
    })
    lines_connected[end].push({
        lineId : lineId,
        start : start,
        end : end
    })
    adjust_lines(start)
}
function adjust_lines(nodeId){
    //updates the lines connected to the node with id = nodeId
    lines = lines_connected[nodeId]
    lines.forEach(line => {
        //get start position
        //console.log('selecting ' + line['start'])
        st = $(document.getElementById(line['start']))
        startPos = st.position()
        //get end position
        ed = $(document.getElementById(line['end']))
        endPos = ed.position()
        //update line
        var lineId = line['lineId']
        $(document.getElementById(lineId))
                                        .attr('x1', startPos.left)
                                        .attr('y1', startPos.top)
                                        .attr('x2', endPos.left)
                                        .attr('y2', endPos.top);

    });
}