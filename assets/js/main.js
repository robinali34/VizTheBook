function removeVisualizations() {
    var div = document.getElementById("imagecloud");

    while (div.hasChildNodes()) {
        div.removeChild(div.lastChild);
    }

    div = document.getElementById("streamgraph-svg");

    while (div.hasChildNodes()) {
      div.removeChild(div.lastChild);
    }

    div = document.getElementById("graph");

    while (div.hasChildNodes()) {
        div.removeChild(div.lastChild);
    }

    if (mapCircles.length > 0) {
      mapCircles.forEach(function(c) {
        mymap.removeLayer(c);
      });
      mapCircles = [];
    }

}
function visualize(name= "American Men of Action"){
  var title = name;
  removeVisualizations();

  fetch('http://localhost:5000/image?title=' + title, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json'},
  })
  .then(function(response) {
      return response.json();
  })
  .then(function(data) {
      data = data.data;
      draw(data);
  });

  fetch('http://localhost:5000/map?title=' + title, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json'}
  })
  .then(function(response) {
      return response.json();
  })
  .then(function(data) {
      drawMapLocations(data)
  });

  fetch('http://localhost:5000/graphkey?title=' + title, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json'}
  })
  .then(function(response) {
      return response.json();
  })
  .then(function(data) {
    var keywords = [];
    data["data"].forEach(function(d) {
      if (!keywords.includes(d.keyword)) {
        keywords.push(d.keyword)
      }
    })
    createdivs(data["data"],keywords);

  });

  fetch('http://localhost:5000/graphrel?title=' + title, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json'}
  })
  .then(function(response) {
      return response.json();
  })
  .then(function(data) {
    data = data.data;
    drawGraph(data);
  });

  fetch('http://localhost:5000/streamgraph?title=' + title, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json'}
  })
  .then(function(response) {
      return response.json();
  })
  .then(data => {
      data = data["keyword_score"];
      drawStreamgraph(data);
  });
}

fetch('http://localhost:5000/books', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json'}
})
.then(function(response) {
    return response.json();
})
.then(data => {
    data = data.data;
    visualize();
    var select = document.getElementById("select-book");
    for(var i = 0; i < data.length; i++) {
        var opt = data[i];
        var el = document.createElement("option");
        el.textContent = opt;
        el.value = opt;
        // el.onclick = function(e) {
        //   visualize(e.target.text);
        // }
        select.appendChild(el);
    }
});
