function drawGraph(data) {
  var links = data;
  var nodes = {};
  var nlinks=[];
  var counts = {};

  links.forEach(function(link) {
    if(link.source<link.target) {nlinks.push(link.source+";"+link.target)}
    else nlinks.push(link.target+";"+link.source)
  });

  var distinct_keywords=[ new Set(links.map(x=>x.keyword))];
  distinct_keywords=Array.from(distinct_keywords[0]);
  nlinks.forEach(function(x) { counts[x] = (counts[x] || 0)+1; })
  // compute the distinct nodes from the links.
  links.forEach(function(link) {
      link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
      link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});
  });

  var width = 695,
      height = 440;

  var force = d3.forceSimulation()
      .nodes(d3.values(nodes))
      .force("link", d3.forceLink(links).distance(100))
      .force('center', d3.forceCenter(width / 2, (height) / 2))
      .force("x", d3.forceX())
      .force("y", d3.forceY())
      .force("charge", d3.forceManyBody().strength(-5050))
      .alphaTarget(0.1)
      .on("tick", tick);

  var svg = d3.select("#graph").append("svg")
      .attr("width", width)
      .attr("height", height);
var colors_keywords=["#003f5c","#2f4b7c","#665191","#a05195","#d45087", "#f95d6a", "#ff7c43", "#ffa600"]
  // add the links
  var path = svg.append("g")
      .selectAll("path")
      .data(links)
      .enter()
      .append("path")
      .attr("class", function(d) { return "link " + d.keyword; })
      .style("stroke",  function(d, idx){
        if (idx >= colors_keywords.length) {
          idx = idx - colors_keywords.length
        }
        return  colors_keywords[distinct_keywords.findIndex((element) => element ==d.keyword)]
      })
      .style("stroke-width",  function(d){return 5 })

;

;

  // define the nodes
  var node = svg.selectAll(".node")
      .data(force.nodes())
      .enter().append("g")
      .attr("class", "node")
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended))
          .on("dblclick",function(d){ d.fixed=false;d.fx = null;
          d.fy = null;
          svg.selectAll("circle")
             .filter(function(k) {return k.fixed == false; })
.style('stroke-width', 1).style("fill",d3.rgb("#1f394a"));
if(document.getElementById("select-book").value ==d.name){
if (document.getElementById(d.name+"div").style.display=="none"
) {
  document.getElementById(d.name+"div").style.display="block";
  if (d.x<width/2){
         document.getElementById(d.name+"div").style.left = Math.max(d.x-50-document.getElementById(d.name+"div").offsetWidth,0)+'px';}
         else {
           document.getElementById(d.name+"div").style.left = Math.min((d.x+50),width-document.getElementById(d.name+"div").offsetWidth)+'px';
         }
  if (d.y<height/2){
                document.getElementById(d.name+"div").style.top = Math.max(d.y+50-document.getElementById(d.name+"div").offsetHeight,0)+'px';}
                else {
                  document.getElementById(d.name+"div").style.top = Math.max(Math.min((d.y-50),height-document.getElementById(d.name+"div").offsetHeight),0)+'px';
                }

}
else{document.getElementById(d.name+"div").style.display="none";
}
}
else {
  for (var i=0; i<document.getElementById('select-book').options.length; i++)
          {
           if (document.getElementById('select-book').options[i].text == d.name) 
           {
             document.getElementById("select-book").value =d.name;
             visualize(d.name);
            break;
           }
      }

}

 })

  node.append("circle")
  .attr("r", function(d) {
     d.weight = path.filter(function(l) {
       return l.source.index == d.index || l.target.index == d.index
     }).size();
     var minRadius = 15;
     return minRadius + (d.weight * 3)
   }).attr("id",function(d) {d.name}).style("fill",d3.rgb("#1f394a")) ;
  node.append("text")
          .attr("dx", function(d){return +10})
          .attr("dy", function(d){return -5})
          .style("font-weight","bold")
          .style("fill","white")
          .style("font-size", "12px")
          .text(function(d){return d.name});
  // add the curvy lines
  function tick() {
    var plotcount={};sweep_flag={}
      path.attr("d", function(d) {
        var comboname=d.target.name<d.source.name ? d.target.name+";"+d.source.name : d.source.name+";"+d.target.name;
        if(comboname in plotcount){
          plotcount[comboname]=plotcount[comboname]+1
          sweep_flag[comboname]=sweep_flag[comboname]

        } else {plotcount[comboname]=1,sweep_flag[comboname]=1}
        var linkcount= 0.0+counts[d.target.name<d.source.name ? d.target.name+";"+d.source.name : d.source.name+";"+d.target.name];
// console.log(linkcount);
          var dx = d.target.x - d.source.x,
              dy = d.target.y - d.source.y,
              dr = Math.sqrt(dx * dx + dy * dy)/(2-(plotcount[comboname]*(1/linkcount)));
          return "M" +
              d.source.x + "," +
              d.source.y + "A" +
              dr + "," + dr + " 0 0,"+ sweep_flag[comboname]+" "+
              d.target.x + "," +
              d.target.y;
      });

      node.attr("transform", function(d) {
          return "translate(" + d.x + "," + d.y + ")";
      });
  };

  function dragstarted(d) {
      if (!d3.event.active) force.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
  };

  function dragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
  };

  function dragended(d) {
    d.fixed=true;
    svg.selectAll("circle")
       .filter(function(l) {return l.fixed == true; })
       .style('fill', '#CA2D2B').style('stroke-width', 3);

      if (!d3.event.active) force.alphaTarget(0);
      if (d.fixed == true) {
          d.fx = d.x;
          d.fy = d.y;
      }
      else {
          d.fx = null;
          d.fy = null;
      }


  };
  var temp;
  for ( temp = 0; temp < distinct_keywords.length; temp++) {


    svg.append("rect").attr("x",width-155).attr("y",height-12-temp*15).attr("width", 30).attr("height", 6).style("fill", colors_keywords[temp]);
    svg.append("text").attr("x", width-120).attr("y", height-7-temp*15).text(distinct_keywords[temp]).style("font-size", "15px").style("fill","white").attr("alignment-baseline","middle")
}

  function showhideline(){
    d3.selectAll("."+this.name).style("opacity", 1-d3.selectAll("."+this.name).style("opacity"));

  }

}

function createdivs(divdata,keywords){
  // divdata.forEach(function (item2,index) {
      var listring='',tabstring='';
      divdata.forEach(function (item,index) {
        if (listring==''){
          listring=listring+'\
            <li class="nav-item" role="presentation">\
              <a class="nav-link active" id="book'+index+'keyword'+item.keyword+'-tab" data-toggle="tab" href="#book'+index+'keyword'+item.keyword+'" role="tab" aria-controls="book'+index+'keyword'+item.keyword+'" aria-selected="true">'+item.keyword+'</a>\
            </li>'
            tabstring=tabstring+'    <div class="tab-pane fade show active" id="book'+index+'keyword'+item.keyword+'" role="tabpanel" aria-labelledby="book'+index+'keyword'+item.keyword+'-tab" ><p class="popup">'+item.section+'</p></div>'

        }
        else {
          listring=listring+'\
            <li class="nav-item" role="presentation">\
              <a class="nav-link" id="book'+index+'keyword'+item.keyword+'-tab" data-toggle="tab" href="#book'+index+'keyword'+item.keyword+'" role="tab" aria-controls="book'+index+'keyword'+item.keyword+'" aria-selected="false" style="color:black;">'+item.keyword+'</a>\
            </li>'
            tabstring=tabstring+'    <div class="tab-pane fade" id="book'+index+'keyword'+item.keyword+'" role="tabpanel" aria-labelledby="book'+index+'keyword'+item.keyword+'-tab"  ><p class="popup">'+item.section+'</p></div>'

        }

    });
    var bookname=divdata[0].title;
    var bookdiff="medium";
    var bookreadtime="5 hrs";

      document.body.insertAdjacentHTML( 'afterbegin', '\
      <div class="row" >\
        <div class="col-3 popup-div" id="'+bookname+'div" >\
          <p style="margin:0"  class="popup-header" id="'+bookname+'divheader"> '+bookname+' <span id="close" style="cursor: pointer;float:right;line-height:20px;font-size:13px" onclick="closediv(this)" onmouseover="mouseoverclose(this)" onmouseout="mouseoutclose(this)"><u>Close</u></span></p>\
          <p style="margin:0;font-size:14px;" class="popup"><span >Dificulty Level:'+bookdiff+'</span><span style="float:right"> Reading Time : '+bookreadtime+'<span> </p>\
          <ul class="nav nav-tabs" id="myTab" role="tablist" style="font-size:14px">'+

    listring
          +'</ul>\
          <div class="tab-content" id="myTabContent" style="font-size:12px">\
              '+tabstring+'</div>\
      </div>\
      </div>\
      ' );
    dragElement(document.getElementById(bookname+"div"));


}

function closediv(a){
  document.getElementById(a.parentElement.parentElement.id).style.display="none";
}
function mouseoverclose(a){
      a.style.color = 'blue';
}
function mouseoutclose(a){
  a.style.color = '';
};


function dragElement(elmnt) {
  var pos1 , pos2 , pos3 , pos4;
  if (document.getElementById(elmnt.id + "header")) {
    /* if present, the header is where you move the DIV from:*/
    document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
  } else {
    /* otherwise, move the DIV from anywhere inside the DIV:*/
    elmnt.onmousedown = dragMouseDown;
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    console.log({ elmntoffsetTop : elmnt.offsetTop, pos2 : pos2 ,pos4:pos4});
    console.log({ elmntoffsetLeft : elmnt.offsetLeft, pos1 : pos1 ,pos3:pos3});

    // set the element's new position:
    elmnt.style.top = (elmnt.offsetTop-5 - pos2) + "px";
    elmnt.style.left = (elmnt.offsetLeft -5- pos1) + "px";
  }

  function closeDragElement() {
    /* stop moving when mouse button is released:*/
    document.onmouseup = null;
    document.onmousemove = null;
  }
}
