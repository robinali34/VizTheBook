function draw(data) {
    var width = 695;
    var height = 442;
    var stratify = d3.stratify()
        .parentId(function(d) { 
            if (d.keyword == "root") {
                return ""
            } else {
                return "root";
            }
        })
        .id(function(d) {
            return d.keyword;
        })

    var root = stratify(data).sum(function(d) { return d.value ;});
    var treemap = d3.treemap()
        .tile(d3.treemapSquarify)
        .size([width, height])
        .padding(1)
        .round(true);

    treemap(root);
    drawTreemap(root);
}


function drawTreemap(root) {
    var div = d3.select("#imagecloud");

    var node = div.selectAll(".node").data(root.children);

    var newNode = node.enter()
    .append("div").attr("class", "node")
        .style("background-image", function(d){
            encoded = encodeURI(d.data.img)
            return "url(" + encoded + ")";
        })
        .style("background-position", "center")

	newNode.append("text")
		.style("stroke-width", "5px")
	    .attr("x", "2")
	    .attr("y", "0")
		.text(function(d){return d.data.keyword})

    node.merge(newNode)
        .transition()
        .duration(1000)
        .style("left", function(d) { return d.x0 + "px" ;})
        .style("top", function(d) { return d.y0 + "px" ;})
        .style("width", function(d) { return (d.x1 - d.x0) + "px" ;})
        .style("height", function(d) { return (d.y1 - d.y0) + "px" ;});

}