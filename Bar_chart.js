
// set the dimensions and margins of the graph
const margin = {top: 30, right: 30, bottom: 70, left: 60},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
const svg = d3.select("#my_dataviz")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Parse the Data
d3.csv("years.csv").then( function(data) {

// X axis
const x = d3.scaleBand()
  .range([ 0, width ])
  .domain(data.map(d => d.Year))
  .padding(0.2);
svg.append("g")
  .attr("transform", `translate(0, ${height})`)
  .call(d3.axisBottom(x))
  .selectAll("text")
    .attr("transform", "translate(-10,0)rotate(-45)")
    .style("text-anchor", "end");

// Add Y axis
const y = d3.scaleLinear()
  .domain([0, 2500])
  .range([ height, 0]);
svg.append("g")
  .call(d3.axisLeft(y));

// Bars
svg.selectAll("mybar")
  .data(data)
  .join("rect")
    .attr("x", d => x(d.Year))
    .attr("y", d => y(d.Players))
    .attr("width", x.bandwidth())
    .attr("height", d => height - y(d.Players))
    .attr("fill", "#69b3a2")
    .on("mouseover", function(event, d){

      console.log(d3.select(this.Year))

      // Reduce opacity of all rect to 0.2
      d3.selectAll(".myRect").style("opacity", 0.2)

      // Highlight all rects of this subgroup with opacity 1. It is possible to select them since they have a specific class = their name.
      d3.selectAll(this).style("opacity",1)      

      tooltip
        .transition()
        .duration(100)
        .style("opacity", 1)
      tooltip
        .html("Range: " + d.x0 + " - " + d.x1)
        .style("left", (d3.mouse(this)[0]+20) + "px")
        .style("top", (d3.mouse(this)[1]) + "px")
    })
    .on("mouseleave", function (event,d) { // When user do not hover anymore

      // Back to normal opacity: 1
      d3.selectAll(".myRect")
      .style("opacity",1)
    })
    .on("click", selectYear)

var tooltip = d3.select("#my_dataviz")
.append("div")
.style("opacity", 0)
.attr("class", "tooltip")
.style("background-color", "black")
.style("color", "white")
.style("border-radius", "5px")
.style("padding", "10px")

var selectYear = function(d){
//TODO
}

})
