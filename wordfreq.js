// ==================================================================================================
//
// wordfreq.js
// Version 1 03/11/2018
//
// Script that draws a line plot + scatter plot
// It is designed for d3 v3
//
// ==================================================================================================

// Get size of the window from the size of the HTML element and adapt for
// margins
//
// ==================================================================================================
//

/// log(frequency)
function drawplot(dataset)
{
  document.getElementById("wordfreq").innerHTML = "";

  var margin = {top: 40, right: 40, bottom: 40, left: 120};
  var width = parseInt(document.getElementById("wordfreq").style.width,10)-margin.right -margin.left;
  var height = parseInt(document.getElementById("wordfreq").style.height,10)-margin.top-margin.bottom;

  // ==================================================================================================
  //
  // set the ranges and parse dates
  //
  // ==================================================================================================

  var parseDate = d3.time.format(" %Y-%m-%d").parse;

  var x = d3.time.scale().range([0, width]);
  var y = d3.scale.linear().range([height, 0]);

  var c = function(d) { return d.y;};
  var color = d3.scale.category10().domain(d3.range(10));

  // ==================================================================================================
  //
  // append the svg object to the container with the id "wordfreq" in the html page
  // appends a 'group' element to 'svg'
  // moves the 'group' element to the top left margin
  //
  // ==================================================================================================

  var svg = d3.select("#wordfreq").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

  // ==================================================================================================
  //
  // Get the data from the Json file whose name was read from calling html
  //
  // ==================================================================================================

  var temp= JSON.parse(dataset);
  var data = [];
  console.log(temp.length);
  for (var i =0; i < temp.length; i++)
  {
    if (temp[i]['frequency'] != 0){
      data.push(temp[i]);
    }
  }
  console.log(data.length);

  // ==================================================================================================
  //
  // format the data
  //
  // ==================================================================================================

  data.forEach(function(d) {
    d.date = parseDate(d.date);
    d.frequency = +d.frequency;
  });

  // ==================================================================================================
  //
  // Scale the range of the data
  //
  // ==================================================================================================

  x.domain(d3.extent(data, function(d) { return d.date; }));
  //y.domain([d3.min(data, function(d) { return d.frequency; }), d3.max(data, function(d) { return d.frequency; })]);
  y.domain([-7, 0]);

  // ==================================================================================================
  //
  // Add the X Axis with text label
  //
  // ==================================================================================================

  xAxis = d3.svg.axis().scale(x).orient("bottom");
  yAxis = d3.svg.axis().scale(y).orient("left");

  var axisX = svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
    .style("font-size","16px")
    .style("stroke", "black")
    .style("stroke-width", 1.0);
  axisX.selectAll("line").attr("fill","none");
  axisX.selectAll("path").attr("fill","none");

  svg.append("text")             
    .attr("transform",
        "translate(" + (0.85*width) + " ," + 
        (height + margin.top ) + ")")
    .style("text-anchor", "middle")
    .text("Year")
    .style("font-style","Italic")
    .style("font-size","18px")
    .style("font-weight","Bold");

  // ==================================================================================================
  //
  // Add the Y Axis
  //
  // ==================================================================================================

  var axisY = svg.append("g")
    .call(yAxis)
    .style("font-style","Italic")
    .style("font-size","14px")
    .style("font-weight","Bold")
    .style("stroke", "black")
    .style("stroke-width", 1.0);
  axisY.selectAll("line").attr("fill","none");
  axisY.selectAll("path").attr("fill","none");

  svg.append("text")             
    .attr("class", "y label")
    .attr("text-anchor", "end")
    .attr("y", -margin.left / 2)
    .attr("dy", "0.75em")
    .attr("transform", "rotate(-90)")
    .text("Frequency")
    .style("font-style","Italic")
    .style("font-size","18px")
    .style("font-weight","Bold");

  // ==================================================================================================
  //
  // Define and add the line
  //
  // ==================================================================================================

  var valueline = d3.svg.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.frequency); });

  svg.append("path")
    .attr("class", "line")
    .style("stroke", "blue")
    .style("stroke-width", 1.0)
    .attr("fill","none")
    .attr("d", valueline(data));

  // ==================================================================================================
  //
  // Add the scatterplot
  //
  // ==================================================================================================

  svg.selectAll("dot")
    .data(data)
    .enter().append("circle")
    .attr("fill","red")
    .attr("r", 3.5)
    .attr("cx", function(d) { return x(d.date); })
    .attr("cy", function(d) { return y(d.frequency); });

}

// linear
function drawlinearplot(dataset)
{
  document.getElementById("wordfreq").innerHTML = "";

  var margin = {top: 40, right: 40, bottom: 40, left: 140};
  var width = parseInt(document.getElementById("wordfreq").style.width,10)-margin.right -margin.left;
  var height = parseInt(document.getElementById("wordfreq").style.height,10)-margin.top-margin.bottom;

  // ==================================================================================================
  //
  // set the ranges and parse dates
  //
  // ==================================================================================================

  var parseDate = d3.time.format(" %Y-%m-%d").parse;

  var x = d3.time.scale().range([0, width]);
  var y = d3.scale.linear().range([height, 0]);

  var c = function(d) { return d.y;};
  var color = d3.scale.category10().domain(d3.range(10));

  // ==================================================================================================
  //
  // append the svg object to the container with the id "wordfreq" in the html page
  // appends a 'group' element to 'svg'
  // moves the 'group' element to the top left margin
  //
  // ==================================================================================================

  var svg = d3.select("#wordfreq").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

  // ==================================================================================================
  //
  // Get the data from the Json file whose name was read from calling html
  //
  // ==================================================================================================

  var temp= JSON.parse(dataset);
  var data = [];
  console.log(temp.length);
  j = 0
  for (var i =0; i < temp.length; i++)
  {
    if (temp[i]['frequency'] != 0){
      data.push(temp[i]);
      data[j]['frequency'] = Math.pow(10, temp[i]['frequency']) * 100;
      j = j + 1
    }
    else {
      data.push(temp[i]);
      j = j + 1;
    }
  }
  console.log(data.length);
  console.log(data);

  // ==================================================================================================
  //
  // format the data
  //
  // ==================================================================================================

  data.forEach(function(d) {
    d.date = parseDate(d.date);
    d.frequency = +d.frequency;
  });

  // ==================================================================================================
  //
  // Scale the range of the data
  //
  // ==================================================================================================

  x.domain(d3.extent(data, function(d) { return d.date; }));
  y.domain([0, d3.max(data, function(d) { return d.frequency; })]);
  //y.domain([-7, 0]);

  // ==================================================================================================
  //
  // Add the X Axis with text label
  //
  // ==================================================================================================

  xAxis = d3.svg.axis().scale(x).orient("bottom");
  yAxis = d3.svg.axis().scale(y).orient("left");

  var axisX = svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
    .style("font-size","16px")
    .style("font-famliy","sans-serif")
    .style("stroke", "black")
    .style("stroke-width", 1.0);
  axisX.selectAll("line").attr("fill","none");
  axisX.selectAll("path").attr("fill","none");

  svg.append("text")             
    .attr("transform",
        "translate(" + (0.85*width) + " ," + 
        (height + margin.top ) + ")")
    .style("text-anchor", "middle")
    .text("Year")
    //.style("font-style","Italic")
    .style("font-size","18px")
    .style("font-famliy","sans-serif")
    //.style("font-weight","Bold");

  // ==================================================================================================
  //
  // Add the Y Axis
  //
  // ==================================================================================================

  var axisY = svg.append("g")
    .call(yAxis)
    //.style("font-style","Italic")
    .style("font-famliy","sans-serif")
    .style("font-size","14px")
    //.style("font-weight","Bold")
    .style("stroke", "black")
    .style("stroke-width", 1.0);
  axisY.selectAll("line").attr("fill","none");
  axisY.selectAll("path").attr("fill","none");

  svg.append("text")             
    .attr("class", "y label")
    .attr("text-anchor", "end")
    .attr("y", -margin.left / 2)
    .attr("dy", "0.75em")
    .attr("transform", "rotate(-90)")
    .text("Frequency as % of all words")
    //.style("font-style","Italic")
    .style("font-famliy","sans-serif")
    .style("font-size","18px")
    //.style("font-weight","Bold");

  // ==================================================================================================
  //
  // Define and add the line
  //
  // ==================================================================================================

  var valueline = d3.svg.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.frequency); });

  svg.append("path")
    .attr("class", "line")
    .style("stroke", "blue")
    .style("stroke-width", 1.0)
    .attr("fill","none")
    .attr("d", valueline(data));

  // ==================================================================================================
  //
  // Add the scatterplot
  //
  // ==================================================================================================

  svg.selectAll("dot")
    .data(data)
    .enter().append("circle")
    .attr("fill","red")
    .attr("r", 3.5)
    .attr("cx", function(d) { return x(d.date); })
    .attr("cy", function(d) { return y(d.frequency); });

}
