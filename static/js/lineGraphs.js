
function LineGraph(placeholderName){
  this.placeholderName = placeholderName;

  this.width = $("#"+this.placeholderName).innerWidth()
  this.height = $("#"+this.placeholderName).innerHeight()
  this.points = [];
  var self = this; //for d3
  this.lineGenerator = d3.line();

  this.makeLine = function(){
    var pathData = this.lineGenerator(this.points);
    this.svg = d3.select('.mydiv')
              .append('svg')
    this.path = this.svg.append('path')
                .attr('d', pathData)
                .attr('class', 'line')
  }

  this.addPoint = function(x,y) {
    console.log(x,y)
    this.points.push([y*10,x])
    var pathData = this.lineGenerator(this.points);
    $(this.path.attr('d', pathData))
  }
  this.render = function(){
    console.log(this.placeholderName)
    console.log(this.width)
    // console.log(this.height)
    // this.body = d3.select("#" + this.placeholderName)
    //           .append("svg:svg")
    //           .attr("class", "lineGraph")
    //           .attr("width", this.width)
    //           .attr("height", this.height);
    // this.xScale = d3.scaleLinear()
    //             .domain([1,2,3,4,5])
    //             .range([0, this.width])
    // this.yScale = d3.scaleLinear()
    //             .domain([1,2,3,4,5])
    //             .range([0, this.height])

    // // 7. d3's line generator
    // this.line = d3.line()
    //           .x(function(d, i) { return this.xScale(i); }) // set the x values for the line generator
    //           .y(function(d) { return this.yScale(d.y); }) // set the y values for the line generator 
    //           .curve(d3.curveMonotoneX) // apply smoothing to the line

    // // 8. An array of objects of length N. Each object has key -> value pair, the key being "y" and the value is a random number
    // this.data = d3.range(5).map(function(d) { return {"y": d3.randomUniform(1)() } })
 
    // // 1. Add the SVG to the page and employ #2
    // this.svg = d3.select("#" + this.placeholderName).append("svg")
    //             .attr("width", this.width)
    //             .attr("height", this.height)
    //             .append("g")

    // // 3. Call the x axis in a group tag
    // this.svg.append("g")
    //     .attr("class", "x axis")
    //     .attr("transform", "translate(0," + this.height + ")")
    //     .call(d3.axisBottom(this.xScale)); // Create an axis component with d3.axisBottom

    // // 4. Call the y axis in a group tag
    // this.svg.append("g")
    //     .attr("class", "y axis")
    //     .call(d3.axisLeft(this.yScale)); // Create an axis component with d3.axisLeft

    // // 9. Append the path, bind the data, and call the line generator 
    // this.svg.append("path")
    //     .datum(this.data) // 10. Binds data to the line 
    //     .attr("class", "line") // Assign a class for styling 
    //     .attr("d", this.line); // 11. Calls the line generator 

  }
}




// // 2. Use the margin convention practice 
// var margin = {top: 50, right: 50, bottom: 50, left: 50}
//   , width = window.innerWidth - margin.left - margin.right // Use the window's width 
//   , height = window.innerHeight - margin.top - margin.bottom; // Use the window's height

// // The number of datapoints
// var n = 21;

// // 5. X scale will use the index of our data
// var xScale = d3.scaleLinear()
//     .domain([0, n-1]) // input
//     .range([0, width]); // output

// // 6. Y scale will use the randomly generate number 
// var yScale = d3.scaleLinear()
//     .domain([0, 1]) // input 
//     .range([height, 0]); // output 

// // 7. d3's line generator
// var line = d3.line()
//     .x(function(d, i) { return xScale(i); }) // set the x values for the line generator
//     .y(function(d) { return yScale(d.y); }) // set the y values for the line generator 
//     .curve(d3.curveMonotoneX) // apply smoothing to the line

// // 8. An array of objects of length N. Each object has key -> value pair, the key being "y" and the value is a random number
// var dataset = d3.range(n).map(function(d) { return {"y": d3.randomUniform(1)() } })

// // 1. Add the SVG to the page and employ #2
// var svg = d3.select("body").append("svg")
//     .attr("width", width + margin.left + margin.right)
//     .attr("height", height + margin.top + margin.bottom)
//   .append("g")
//     .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// // 3. Call the x axis in a group tag
// svg.append("g")
//     .attr("class", "x axis")
//     .attr("transform", "translate(0," + height + ")")
//     .call(d3.axisBottom(xScale)); // Create an axis component with d3.axisBottom

// // 4. Call the y axis in a group tag
// svg.append("g")
//     .attr("class", "y axis")
//     .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft

// // 9. Append the path, bind the data, and call the line generator 
// svg.append("path")
//     .datum(dataset) // 10. Binds data to the line 
//     .attr("class", "line") // Assign a class for styling 
//     .attr("d", line); // 11. Calls the line generator 

// // 12. Appends a circle for each datapoint 
// svg.selectAll(".dot")
//     .data(dataset)
//   .enter().append("circle") // Uses the enter().append() method
//     .attr("class", "dot") // Assign a class for styling
//     .attr("cx", function(d, i) { return xScale(i) })
//     .attr("cy", function(d) { return yScale(d.y) })
//     .attr("r", 5)
//       .on("mouseover", function(a, b, c) { 
//   			console.log(a) 
//         this.attr('class', 'focus')
// 		})
//       .on("mouseout", function() {  })
//       .on("mousemove", mousemove);

//   var focus = svg.append("g")
//       .attr("class", "focus")
//       .style("display", "none");

//   focus.append("circle")
//       .attr("r", 4.5);

//   focus.append("text")
//       .attr("x", 9)
//       .attr("dy", ".35em");

//   svg.append("rect")
//       .attr("class", "overlay")
//       .attr("width", width)
//       .attr("height", height)
//       .on("mouseover", function() { focus.style("display", null); })
//       .on("mouseout", function() { focus.style("display", "none"); })
//       .on("mousemove", mousemove);
  
//   function mousemove() {
//     var x0 = x.invert(d3.mouse(this)[0]),
//         i = bisectDate(data, x0, 1),
//         d0 = data[i - 1],
//         d1 = data[i],
//         d = x0 - d0.date > d1.date - x0 ? d1 : d0;
//     focus.attr("transform", "translate(" + x(d.date) + "," + y(d.close) + ")");
//     focus.select("text").text(d);
//   }