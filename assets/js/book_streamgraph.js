// set the dimensions and margins of the graph
var margin = {top: 0, right: 30, bottom: 0, left: 10},
    width = 700- margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#book_streamgraph")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")")
    .attr("id", "streamgraph-svg");

function linspace(a,b,n) {
    if(typeof n === "undefined") n = Math.max(Math.round(b-a)+1,1);
    if(n<2) { return n===1?[a]:[]; }
    var i,ret = Array(n);
    n--;
    for(i=n;i>=0;i--) { ret[i] = (i*b+(n-i)*a)/n; }
    return ret;
}

function drawStreamgraph(data) {
    var reducedData = [];

    data.forEach(function(d, i) {
        if (i % 50 == 0) {
            reducedData.push(d)
        }
    })

    var keys = d3.keys(reducedData[0]);
    keys.splice(keys.indexOf('decile'), 1);

    var xDomain = d3.extent(reducedData, function (d) {return d.decile;})
    // Add X axis
    var x = d3.scaleLinear()
        .domain(xDomain)
        .range([0, width]);
    svg.append("g")
        .attr("transform", "translate(0," + height * 0.8 + ")")
        .attr("class", "axisbottom")
        //TODO
        .call(d3.axisBottom(x).tickSize(-height * .7).tickValues(linspace(xDomain[0],xDomain[1],10)))
        .select(".domain").remove()

    // Customization
    svg.selectAll(".tick line").attr("stroke", "#b8b8b8")

    // Add X axis label:
    svg.append("text")
        .attr("text-anchor", "end")
        .attr("x", width)
        .attr("y", height - 70)
        .text("Length of Book")
        .style("fill","white");

    

    // color palette
    var color = d3.scaleOrdinal()
        .domain(keys)
        .range(["#003f5c","#2f4b7c","#665191","#a05195","#d45087", "#f95d6a", "#ff7c43", "#ffa600"])

    //stack the data?
    var stackedData = d3.stack()
        .offset(d3.stackOffsetSilhouette)
        .keys(keys)
        (reducedData)

    var minY = 10000000;
    var maxY = -100000000;

    stackedData.forEach(function(d,i) {
        d.forEach(function(p, idx) {
            var tmp_minY = Math.min(...p)
            var tmp_maxY = Math.max(...p)

            if (tmp_minY < minY) {
                minY = tmp_minY
            }

            if (tmp_maxY > maxY) {
                maxY = tmp_maxY
            }
        })
    })

    console.log(minY, maxY)

    // Add Y axis
    var yDomain = d3.extent(reducedData, function (d) {return d.decile;})
    var y = d3.scaleLinear()
        //TODO
        .domain([minY-2, maxY+2])
        .range([height, 0]);

    // create a tooltip
    var Tooltip = svg
        .append("text")
        .attr("x", 0)
        .attr("y", 70)
        .style("opacity", 0)
        .style("font-size", 17)
        .style("fill","white");


    // Three function that change the tooltip when user hover / move / leave a cell
    var mouseover = function (d) {
        Tooltip.style("opacity", 1)
        d3.selectAll(".myArea").style("opacity", .2)
        d3.select(this)
            .style("stroke", "black")
            .style("opacity", 1)
    }
    var mousemove = function (d, i) {
        grp = keys[i]
        Tooltip.text(grp)

    }
    var mouseleave = function (d) {
        Tooltip.style("opacity", 0)
        d3.selectAll(".myArea").style("opacity", 1).style("stroke", "none")
    }

    var area = d3.area()
        .x(function (d, i) {
            return x(d.data.decile);
        })
        .y0(function (d, i) {
            return y(d[0]);
        })
        .y1(function (d,i) {
            return y(d[1]);
        })
        .curve(d3.curveMonotoneX);


    // Show the areas
    svg
        .selectAll("mylayers")
        .data(stackedData)
        .enter()
        .append("path")
        .attr("class", "myArea")
        .style("fill", function (d) {
            return color(d.key);
        })
        .attr("d", area)
        .on("mouseover", mouseover)
        .on("mousemove", mousemove)
        .on("mouseleave", mouseleave)

}
