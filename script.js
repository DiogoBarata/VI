const options = {
  Classes: [
    "Artificer",
    "Barbarian",
    "Bard",
    "Cleric",
    "Custom",
    "Druid",
    "Fighter",
    "Monk",
    "Paladin",
    "Ranger",
    "Rogue",
    "Sorcerer",
    "Warlock",
    "Wizard",
  ],
  Races: [
    "Aarakocra",
    "Aasimar",
    "Bugbear",
    "Centaur",
    "Changeling",
    "Custom",
    "Dragonborn",
    "Dwarf",
    "Eladrin",
    "Elf",
    "Firbolg",
    "Genasi",
    "Gith",
    "Gnome",
    "Goblin",
    "Goliath",
    "Half-Elf",
    "Half-Orc",
    "Halfling",
    "Hobgoblin",
    "Human",
    "Kalashtar",
    "Kenku",
    "Kobold",
    "Leonin",
    "Lizardfolk",
    "Loxodon",
    "Minotaur",
    "Orc",
    "Satyr",
    "Shifter",
    "Simic hybrid",
    "Tabaxi",
    "Tiefling",
    "Triton",
    "Turtle",
    "Vedalken",
    "Warforged",
    "Yaun-Ti",
  ],
  Skills: [
    "Arcana",
    "Religion",
    "Intimidation",
    "History",
    "Insight",
    "Perception",
    "Persuasion",
    "Athletics",
    "Survival",
    "Acrobatics",
    "Sleight of Hand",
    "Deception",
    "Performance",
    "Stealth",
    "Investigation",
    "Nature",
    "Animal Handling",
    "Medicine",
  ],
  Countries: [
    "All",
    "Canada",
    "United States",
    "Brazil",
    "Australia",
    "England",
    "Italy",
    "Germany",
    "Others",
  ],
  Country_Codes: ["All", "CA", "US", "BR", "AU", "GB", "IT", "DE", "Other"],
};

// Init global variables
var dateHisto = "All";
var net_relation = "class_alignment";
var radar_option = "class";

var class_name = "Fighter";
var race_name = "Human";
var skill_name = "Arcana";
var country_name = "All";
var combo_name = "Fighter_Human";

function init() {
  createVis1(".vis1");
  createVis2(".vis2");
  //Vis3 is being created by the initiallization of the buttons
  radioFilter("class_filter", options["Classes"], "Classes:");
  radioFilter("race_filter", options["Races"], "Races:");
  radioFilter("skill_filter", options["Skills"], "Skills:");
  radioFilter("country_filter", options["Countries"], "Countries:");
  initRadioBtts();
  // createVis3('.vis3','class_alignment',class_name)
  createOriginal();
}

function initRadioBtts() {
  radiobtn = document.getElementById("class_filter_" + class_name);
  radiobtn.checked = true;
  radiobtn = document.getElementById("race_filter_" + race_name);
  radiobtn.checked = true;
  radiobtn = document.getElementById("skill_filter_" + skill_name);
  radiobtn.checked = true;
  radiobtn = document.getElementById("country_filter_" + country_name);
  radiobtn.checked = true;
  radiobtn = document.getElementById("r_class");
  radiobtn.checked = true;
  radiobtn = document.getElementById("fc_class");
  radiobtn.checked = true;
  radiobtn = document.getElementById("fr_alignment");
  radiobtn.checked = true;
  disableChartRadioButton("relation", "class", "alignment");
}

function createOriginal() {
  var legend = d3.select("#lgnOrgn");
  legend.text(class_name + "&" + race_name + " Originality");
  d3.json(
    "https://raw.githubusercontent.com/DiogoBarata/VI/main/resources/datasets/originality_data.json"
  ).then(function (data) {
    minO = data[dateHisto][country_name]["Min"];
    maxO = data[dateHisto][country_name]["Max"];
    valueO = Math.round(
      (data[dateHisto][country_name][combo_name] * 100) / maxO
    );
    var element = document.getElementById("orgnBar");
    element.style.width = valueO + "%";
    element.innerHTML = valueO + "%";
  });
}
function updateOrign() {
  d3.json(
    "https://raw.githubusercontent.com/DiogoBarata/VI/main/resources/datasets/originality_data.json"
  ).then(function (data) {
    maxO = data[dateHisto][country_name]["Max"];
    valueO = Math.round(
      (data[dateHisto][country_name][combo_name] * 100) / maxO
    );
	console.log(data[dateHisto][country_name][combo_name],maxO)
    var element = document.getElementById("orgnBar");
    element.style.width = valueO + "%";
    element.innerHTML = valueO + "%";
  });
}

function createVis1(id) {
  radar_color = "#e41a1c";
  // set the dimensions and margins of the graph
  const el = document.querySelector(".vis1");
  const margin = { top: 60, right: 30, bottom: 45, left: 30 };
  const width = el.clientWidth - 60;
  const height = el.clientHeight - 105;
  // width = 460 - margin.left - margin.right,
  // height = 400 - margin.top - margin.bottom;
  d3.json(
    "https://raw.githubusercontent.com/DiogoBarata/VI/main/resources/datasets/radar_data.json"
  ).then(function (data) {
    centreNode = getCentreNode();
    radar_selected = data[radar_option][dateHisto][country_name][centreNode];
    radar_mean = data[radar_option][dateHisto][country_name]["Mean"];
    // Remove HP because it behaves like an outlier
    radar_selected["axes"].shift();
    var radar_data = [radar_selected];
    var radarChartOptions = {
      w: width,
      h: height,
      margin: margin,
      maxValue: 20,
      levels: 6,
      roundStrokes: false,
      format: ".0f",
    };
    // Draw the chart, get a reference the created svg element :
    let svg_radar2 = RadarChart(id, radar_data, radarChartOptions);
  });
}

function RadarChart(parent_selector, data, options) {
  const max = Math.max;
  const sin = Math.sin;
  const cos = Math.cos;
  const HALF_PI = Math.PI / 2;

  //Wraps SVG text - Taken from http://bl.ocks.org/mbostock/7555321
  const wrap = (text, width) => {
    text.each(function () {
      var text = d3.select(this),
        words = text.text().split(/\s+/).reverse(),
        word,
        line = [],
        lineNumber = 0,
        lineHeight = 1.4, // ems
        y = text.attr("y"),
        x = text.attr("x"),
        dy = parseFloat(text.attr("dy")),
        tspan = text
          .text(null)
          .append("tspan")
          .attr("x", x)
          .attr("y", y)
          .attr("dy", dy + "em");

      while ((word = words.pop())) {
        line.push(word);
        tspan.text(line.join(" "));
        if (tspan.node().getComputedTextLength() > width) {
          line.pop();
          tspan.text(line.join(" "));
          line = [word];
          tspan = text
            .append("tspan")
            .attr("x", x)
            .attr("y", y)
            .attr("dy", ++lineNumber * lineHeight + dy + "em")
            .text(word);
        }
      }
    });
  }; //wrap

  const cfg = {
    w: 600, //Width of the circle
    h: 600, //Height of the circle
    margin: { top: 20, right: 20, bottom: 20, left: 20 }, //The margins of the SVG
    levels: 3, //How many levels or inner circles should there be drawn
    maxValue: 0, //What is the value that the biggest circle will represent
    labelFactor: 1.25, //How much farther than the radius of the outer circle should the labels be placed
    wrapWidth: 60, //The number of pixels after which a label needs to be given a new line
    opacityArea: 0.35, //The opacity of the area of the blob
    dotRadius: 4, //The size of the colored circles of each blog
    opacityCircles: 0.05, //The opacity of the circles of each blob
    strokeWidth: 2, //The width of the stroke around each blob
    roundStrokes: false, //If true the area and stroke will follow a round path (cardinal-closed)
    color: d3.scaleOrdinal(d3.schemeCategory10), //Color function,
    format: ".2%",
    unit: "",
    legend: false,
  };

  //Put all of the options into a variable called cfg
  if ("undefined" !== typeof options) {
    for (var i in options) {
      if ("undefined" !== typeof options[i]) {
        cfg[i] = options[i];
      }
    }
  }

  //If the supplied maxValue is smaller than the actual one, replace by the max in the data
  // var maxValue = max(cfg.maxValue, d3.max(data, function(i){return d3.max(i.map(function(o){return o.value;}))}));
  let maxValue = 0;
  for (let j = 0; j < data.length; j++) {
    for (let i = 0; i < data[j].axes.length; i++) {
      data[j].axes[i]["id"] = data[j].name;
      if (data[j].axes[i]["value"] > maxValue) {
        maxValue = data[j].axes[i]["value"];
      }
    }
  }
  maxValue = max(cfg.maxValue, maxValue);

  const allAxis = data[0].axes.map((i, j) => i.axis), //Names of each axis
    total = allAxis.length, //The number of different axes
    radius = Math.min(cfg.w / 2, cfg.h / 2), //Radius of the outermost circle
    Format = d3.format(cfg.format), //Formatting
    angleSlice = (Math.PI * 2) / total; //The width in radians of each "slice"

  //Scale for the radius
  const rScale = d3.scaleLinear().range([0, radius]).domain([0, maxValue]);

  /////////////////////////////////////////////////////////
  //////////// Create the container SVG and g /////////////
  /////////////////////////////////////////////////////////
  const parent = d3.select(parent_selector);

  //Remove whatever chart with the same id/class was present before
  parent.select("svg").remove();

  //Initiate the radar chart SVG
  let svg = parent
    .append("svg")
    .attr("width", cfg.w + cfg.margin.left + cfg.margin.right)
    .attr("height", cfg.h + cfg.margin.top + cfg.margin.bottom)
    .attr("class", "radar");

  //Append a g element
  let g = svg
    .append("g")
    .attr(
      "transform",
      "translate(" +
        (cfg.w / 2 + cfg.margin.left) +
        "," +
        (cfg.h / 2 + cfg.margin.top) +
        ")"
    );

  /////////////////////////////////////////////////////////
  ////////// Glow filter for some extra ///////////////////
  /////////////////////////////////////////////////////////

  //Filter for the outside glow
  let filter = g.append("defs").append("filter").attr("id", "glow"),
    feGaussianBlur = filter
      .append("feGaussianBlur")
      .attr("stdDeviation", "2.5")
      .attr("result", "coloredBlur"),
    feMerge = filter.append("feMerge"),
    feMergeNode_1 = feMerge.append("feMergeNode").attr("in", "coloredBlur"),
    feMergeNode_2 = feMerge.append("feMergeNode").attr("in", "SourceGraphic");

  /////////////////////////////////////////////////////////
  /////////////// Draw the Circular grid //////////////////
  /////////////////////////////////////////////////////////

  //Wrapper for the grid & axes
  let axisGrid = g.append("g").attr("class", "axisWrapper");

  //Draw the background circles
  axisGrid
    .selectAll(".levels")
    .data(d3.range(1, cfg.levels + 1).reverse())
    .enter()
    .append("circle")
    .attr("class", "gridCircle")
    .attr("r", (d) => (radius / cfg.levels) * d)
    .style("fill", "#e41a1c")
    .style("stroke", "#e41a1c")
    .style("fill-opacity", cfg.opacityCircles)
    .style("filter", "url(#glow)");

  //Text indicating at what % each level is
  axisGrid
    .selectAll(".axisLabel")
    .data(d3.range(1, cfg.levels + 1).reverse())
    .enter()
    .append("text")
    .attr("class", "axisLabel")
    .attr("x", 4)
    .attr("y", (d) => (-d * radius) / cfg.levels)
    .attr("dy", "0.4em")
    .style("font-size", "18px")
    .attr("fill", "#000000")
    .text((d) => Format((maxValue * d) / cfg.levels) + cfg.unit);

  /////////////////////////////////////////////////////////
  //////////////////// Draw the axes //////////////////////
  /////////////////////////////////////////////////////////

  //Create the straight lines radiating outward from the center
  var axis = axisGrid
    .selectAll(".axis")
    .data(allAxis)
    .enter()
    .append("g")
    .attr("class", "axis");
  //Append the lines
  axis
    .append("line")
    .attr("x1", 0)
    .attr("y1", 0)
    .attr(
      "x2",
      (d, i) => rScale(maxValue * 1.1) * cos(angleSlice * i - HALF_PI)
    )
    .attr(
      "y2",
      (d, i) => rScale(maxValue * 1.1) * sin(angleSlice * i - HALF_PI)
    )
    .attr("class", "line")
    .style("stroke", "#5d0f02")
    .style("stroke-width", "2px");

  //Append the labels at each axis
  // axis.append('button')
  // .style('background','none')
  // .style('border', 'none')
  axis
    .append("text")
    .attr("class", "legend")
    .style("font-size", "16px")
    .attr("text-anchor", "middle")
    .attr("dy", "0.35em")
    .attr(
      "x",
      (d, i) =>
        rScale(maxValue * cfg.labelFactor) * cos(angleSlice * i - HALF_PI)
    )
    .attr(
      "y",
      (d, i) =>
        rScale(maxValue * cfg.labelFactor) * sin(angleSlice * i - HALF_PI)
    )
    .text((d) => d)
    .call(wrap, cfg.wrapWidth)
    .on("click", function (event, d) {
      d3.json(
        "https://raw.githubusercontent.com/DiogoBarata/VI/main/resources/datasets/radar_data_min_max.json"
      ).then(function (data) {
        new_name = data[radar_option][dateHisto][country_name]["max"][d];
        aux = d3.selectAll(".axis");
        updates(new_name);
      });
      // RADAR CLICK ME
    })
    .on("mouseover", function (d) {
      d3.select(this).style("cursor", "pointer");
    })
    .on("mouseout", function (d) {
      d3.select(this).style("cursor", "default");
    });

  function updates(new_name) {
    if (radar_option == "class") {
      class_name = new_name;
      radiobtn = document.getElementById("class_filter_" + class_name);
      radiobtn.checked = true;
    }
    if (radar_option == "race") {
      race_name = new_name;
      radiobtn = document.getElementById("race_filter_" + race_name);
      radiobtn.checked = true;
    }
    if (radar_option == "skill") {
      radiobtn = document.getElementById("skill_filter_" + skill_name);
      radiobtn.checked = true;
      skill_name = new_name;
    }
    if (radar_option == "combo") {
      console.log(combo_name);
      combo_name = new_name;
      str_split = new_name.split("_");

      console.log(combo_name);
      radiobtn = document.getElementById("class_filter_" + str_split[0]);
      radiobtn.checked = true;
      radiobtn = document.getElementById("race_filter_" + str_split[1]);
      radiobtn.checked = true;
    }
    updateNet();
    updateRadar();
  }
  /////////////////////////////////////////////////////////
  ///////////// Draw the radar chart blobs ////////////////
  /////////////////////////////////////////////////////////

  //The radial line function
  const radarLine = d3
    .radialLine()
    .curve(d3.curveLinearClosed)
    .radius((d) => rScale(d.value))
    .angle((d, i) => i * angleSlice);

  if (cfg.roundStrokes) {
    radarLine.curve(d3.curveCardinalClosed);
  }

  //Create a wrapper for the blobs
  const blobWrapper = g
    .selectAll(".radarWrapper")
    .data(data)
    .enter()
    .append("g")
    .attr("class", "radarWrapper");

  //Append the backgrounds
  blobWrapper
    .append("path")
    .attr("class", "radarArea")
    .attr("d", (d) => radarLine(d.axes))
    .style("fill", i.color)
    .style("fill-opacity", cfg.opacityArea)
    .on("mouseover", function (d, i) {
      //Dim all blobs
      parent
        .selectAll(".radarArea")
        .transition()
        .duration(200)
        .style("fill-opacity", 0.1);
      //Bring back the hovered over blob
      d3.select(this).transition().duration(200).style("fill-opacity", 0.7);
    })
    .on("mouseout", () => {
      //Bring back all blobs
      parent
        .selectAll(".radarArea")
        .transition()
        .duration(200)
        .style("fill-opacity", cfg.opacityArea);
    });

  //Create the outlines
  blobWrapper
    .append("path")
    .attr("class", "radarStroke")
    .attr("d", function (d, i) {
      return radarLine(d.axes);
    })
    .style("stroke-width", cfg.strokeWidth + "px")
    .style("stroke", "#cad10a")
    .style("fill", "none")
    .style("filter", "url(#glow)");

  //Append the circles
  // blobWrapper.selectAll(".radarCircle")
  // 	.data(d => d.axes)
  // 	.enter()
  // 	.append("circle")
  // 	.attr("class", "radarCircle")
  // 	.attr("r", cfg.dotRadius)
  // 	.attr("cx", (d,i) => rScale(d.value) * cos(angleSlice * i - HALF_PI))
  // 	.attr("cy", (d,i) => rScale(d.value) * sin(angleSlice * i - HALF_PI))
  // 	.style("fill", "#1f1e1d")
  // 	.style("fill-opacity", 0.8);

  /////////////////////////////////////////////////////////
  //////// Append invisible circles for tooltip ///////////
  /////////////////////////////////////////////////////////

  //Wrapper for the invisible circles on top
  const blobCircleWrapper = g
    .selectAll(".radarCircleWrapper")
    .data(data)
    .enter()
    .append("g")
    .attr("class", "radarCircleWrapper");

  //Append a set of invisible circles on top for the mouseover pop-up
  blobCircleWrapper
    .selectAll(".radarInvisibleCircle")
    .data((d) => d.axes)
    .enter()
    .append("circle")
    .attr("class", "radarInvisibleCircle")
    .attr("r", cfg.dotRadius * 1.5)
    .attr("cx", (d, i) => rScale(d.value) * cos(angleSlice * i - HALF_PI))
    .attr("cy", (d, i) => rScale(d.value) * sin(angleSlice * i - HALF_PI))
    .style("fill", "none")
    .style("pointer-events", "all")
    .on("mouseover", function (d, i) {
      tooltip
        .attr("x", this.cx.baseVal.value - 10)
        .attr("y", this.cy.baseVal.value - 10)
        .transition()
        .style("display", "block")
        .style("font-size", "16px")
        .text(i.value);
    })
    .on("mouseout", function () {
      tooltip.transition().style("display", "none").text("");
    });

  const tooltip = g
    .append("text")
    .attr("class", "tooltip")
    .attr("x", 0)
    .attr("y", 0)
    .style("font-size", "12px")
    .style("display", "none")
    .attr("text-anchor", "middle")
    .attr("dy", "0.35em");

  if (cfg.legend !== false && typeof cfg.legend === "object") {
    let legendZone = svg.append("g");
    let names = data.map((el) => el.name);
    if (cfg.legend.title) {
      let title = legendZone
        .append("text")
        .attr("class", "title")
        .attr(
          "transform",
          `translate(${cfg.legend.translateX},${cfg.legend.translateY})`
        )
        .attr("x", cfg.w - 70)
        .attr("y", 10)
        .attr("font-size", "12px")
        .attr("fill", "#404040")
        .text(cfg.legend.title);
    }
    let legend = legendZone
      .append("g")
      .attr("class", "legend")
      .attr("height", 100)
      .attr("width", 200)
      .attr(
        "transform",
        `translate(${cfg.legend.translateX},${cfg.legend.translateY + 20})`
      );
    // Create rectangles markers
    legend
      .selectAll("rect")
      .data(names)
      .enter()
      .append("rect")
      .attr("x", cfg.w - 65)
      .attr("y", (d, i) => i * 20)
      .attr("width", 10)
      .attr("height", 10)
      .style("fill", (d, i) => cfg.color(i));
    // Create labels
    legend
      .selectAll("text")
      .data(names)
      .enter()
      .append("text")
      .attr("x", cfg.w - 52)
      .attr("y", (d, i) => i * 20 + 9)
      .attr("font-size", "11px")
      .attr("fill", "#737373")
      .text((d) => d);
  }
  return svg;
}

function createVis2(id) {
  const el = document.querySelector(".vis2");
  const margin = { top: 60, right: 30, bottom: 45, left: 50 };
  const width = el.clientWidth - 80;
  const height = el.clientHeight - 105;

  console.log(margin, width, height);

  // append the svg object to the body of the page
  const svg = d3
    .select(id)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // Parse the Data
  d3.csv(
    "https://raw.githubusercontent.com/DiogoBarata/VI/main/resources/datasets/years.csv"
  ).then(function (data) {
    // X axis
    const x = d3
      .scaleBand()
      .range([0, width])
      .domain(data.map((d) => d.Year))
      .padding(0.2);
    svg
      .append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(d3.axisBottom(x))
      .selectAll("text")
      .attr("transform", "translate(12,0)")
      .style("text-anchor", "end");

    // Add Y axis
    const y = d3.scaleLinear().domain([0, 4000]).range([height, 0]);
    svg.append("g").call(d3.axisLeft(y));

    svg.append("text").attr("x", 85).text("Number of Players along the Years").style("font-weight", "bold").style("text-decoration", "underline");

    // Add Tooltip
    var tooltip = d3
      .select(id)
      .append("div")
      .style("opacity", 0)
      .attr("class", "tooltip")
      .style("background-color", "black")
      .style("color", "white")
      .style("border-radius", "5px")
      .style("padding", "10px");

    // Bars
    svg
      .selectAll("mybar")
      .data(data)
      .join("rect")
      .attr("class", "allbars")
      .attr("x", (d) => x(d.Year))
      .attr("y", (d) => y(d.Players))
      .attr("width", x.bandwidth())
      .attr("height", (d) => height - y(d.Players))
      .attr("fill", "#e41a1c")
      .on("mouseover", function (event, d) {
        console.log(event);
        tooltip.transition().duration(100).style("opacity", 1);
        tooltip
          .html("IRL event: " + d.IRL)
          .style("left", event.offsetX / 2 + "px")
          .style("top", event.offsetY / 2 + "px");
      })
      .on("mouseleave", function (event, d) {
        d3.selectAll(".myRect").style("opacity", 1);
        tooltip.transition().duration(100).style("opacity", 0);
      })
      .on("mousemove", function (event, d) {
        tooltip
          .style("left", event.offsetX / 2 + "px")
          .style("top", event.offsetY / 2 + "px");
      })
      .on("click", function (event, d) {
        // Select and deselect a bars
        if (!d3.select(this).classed("selected")) {
          d3.select(this).classed("selected", true);
          d3.selectAll(".allbars").style("fill", "#e41a1c");
          d3.select(this).style("fill", "#5d0f02");
          dateHisto = d.Year;
          updateNet();
          updateRadar();
        } else {
          d3.select(this).classed("selected", false);
          d3.selectAll(".allbars").style("fill", "#e41a1c");
          d3.select(this).style("fill", "#e41a1c");
          dateHisto = "All";
          updateNet();
          updateRadar();
        }
      });
  });
}

function createVis3(id, relation, centre) {
  const el = document.querySelector(".vis3");
  const margin = { top: 10, right: 30, bottom: 10, left: 30 };
  const width = el.clientWidth - 60;
  const height = el.clientHeight - 20;
  // Append the svg object to the body of the page
  const svg = d3
    .select(id)
    .append("svg")
    .attr("id", "netVis")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("class", "network")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

  d3.json(
    "https://raw.githubusercontent.com/DiogoBarata/VI/main/resources/datasets/network_data.json"
  ).then(function (data) {
    const linkObject = data[relation][dateHisto][country_name][centre].links;
    const nodeObject = data[relation][dateHisto][country_name][centre].nodes;
    // Initialize the links
    var link = svg
      .selectAll("line")
      .data(linkObject)
      .join("line")
      .style("stroke", "#aaa");
    link.append("text").text(function (d) {
      return d.distance;
    });
    // Initialize the nodes
    var node = svg
      .selectAll(".node")
      .data(nodeObject)
      .enter()
      .append("g")
      .attr("class", "node")
      .on("click", function (event, d) {
        updates(d.name);
      })
      .on("mouseover", function (d) {
        d3.select(this).style("cursor", "pointer");
      })
      .on("mouseout", function (d) {
        d3.select(this).style("cursor", "default");
      });
    // TODO position the text inside the box
    img_width = 80;
    img_height = 50;
    node
      .append("svg:image")
      .attr("width", img_width + "px")
      .attr("height", img_height + "px")
      .attr("xlink:href", "resources/imgs/dice.png");
    node
      .append("text")
      .text(function (d) {
        return d.name;
      })
      .style("font-family", "Copperplate, Papyrus, fantasy")
      .style("font-size", "16px")
      .style("font-weight", "bold")
      .attr("y", 28)
      .attr("x", 30);

    function linkDistance(d) {
      calcDist = 15 * (1 / d.distance) + 1;
      return calcDist;
    }
    // This function is run at each iteration of the force algorithm
    // Updating the nodes position.
    function ticked() {
      link
        .attr("x1", (d) => d.source.x + img_width / 2)
        .attr("y1", (d) => d.source.y + img_height / 2)
        .attr("x2", (d) => d.target.x + img_width / 2)
        .attr("y2", (d) => d.target.y + img_height / 2);
      node.attr("transform", (d) => `translate(${d.x},${d.y})`);
    }
    // Initialize the network
    const simulation = d3
      .forceSimulation(nodeObject) // Force algorithm is applied to nodes
      .force(
        "link",
        d3
          .forceLink() // This force provides links between nodes
          .id(function (d) {
            return d.id;
          }) // This provide  the id of a node
          .links(linkObject) // and this the list of links
          .distance(linkDistance)
          .strength(0.005)
      )
      .force("charge", d3.forceManyBody()) // This adds repulsion between nodes
      .force("center", d3.forceCenter(width / 2, height / 2)) // This force attracts nodes to the center of the svg area
      .on("end", ticked);
  });

  function updates(new_name) {
    rel_node = net_relation.split("_")[1];
    // Change rel and centre?
    // if(rel_node == 'class'){
    // 	class_name = new_name
    // 	radiobtn = document.getElementById("class_filter_"+class_name);
    // 	radiobtn.checked = true;
    // };
    // if(rel_node == 'race'){
    // 	race_name = new_name
    // 	radiobtn = document.getElementById("race_filter_"+race_name);
    // 	radiobtn.checked = true;
    // };
    // if(rel_node == 'skill'){
    // 	radiobtn = document.getElementById("skill_filter_"+skill_name);
    // 	radiobtn.checked = true;
    // 	skill_name = new_name
    // };
    // if(rel_node == 'combo'){
    // 	console.log(combo_name)
    // 	combo_name = new_name
    // 	str_split = new_name.split('_')

    // 	console.log(combo_name)
    // 	radiobtn = document.getElementById("class_filter_"+str_split[0]);
    // 	radiobtn.checked = true;
    // 	radiobtn = document.getElementById("race_filter_"+str_split[1]);
    // 	radiobtn.checked = true;
    // };
    // updateNet()
    // updateRadar()
  }
}

function updateNet() {
  centre = getCentreNode();
  aux_relation = net_relation.split("_")[0];
  if (aux_relation == "class") {
    centre = class_name;
  } else if (aux_relation == "race") {
    centre = race_name;
  }

  if (
    centre == "" &&
    !(
      net_relation == "" ||
      net_relation.startsWith("None") ||
      net_relation.endsWith("None")
    )
  ) {
    d3.select("#netVis").remove();
  }
  if (
    centre != "" &&
    !(
      net_relation == "" ||
      net_relation.startsWith("None") ||
      net_relation.endsWith("None")
    )
  ) {
    d3.select("#netVis").remove();
    createVis3(".vis3", net_relation, centre);
  }
}

function updateRadar() {
  createVis1(".vis1");
}

function radioFilter(filterId, data, legend) {
  d3.select(".div_" + filterId).remove();
  var filter = d3
    .select("." + filterId)
    .append("div")
    .attr("class", "div_" + filterId);
  filter.append("legend").text(legend);
  filter
    .selectAll("input")
    .data(data)
    .enter()
    .append("label")
    .attr("for", function (d, i) {
      return filterId + "_" + d;
    })
    .text(function (d) {
      return d;
    })
    .append("input")
    .attr("type", "radio")
    .attr("name", "radio" + "_" + filterId)
    .attr("id", function (d, i) {
      return filterId + "_" + d;
    })
    .attr("value", function (d, i) {
      return d;
    })
    .attr("onClick", "changeRadio(this)");
}

function changeRadio(radio_selection) {
  radio_group_name = radio_selection.name.substring(6);
  radio_group_name = radio_group_name.split("_")[0];
  radio_value = radio_selection.value;
  relation_name = net_relation.split("_")[0];
  if (radio_group_name == "class") {
    updateOrign();
    class_name = radio_value;
    combo_name = class_name + "_" + race_name;
  } else if (radio_group_name == "race") {
    updateOrign();
    race_name = radio_value;
    combo_name = class_name + "_" + race_name;
  } else if (radio_group_name == "country") {
    country_name = getCountryCode(radio_value);
  } else if (radio_group_name == "skill") {
    skill = radio_value;
  }

  if (
    radio_group_name == relation_name ||
    radio_group_name == "country" ||
    ((radio_group_name == "class" || radio_group_name == "race") &&
      relation_name == "combo")
  ) {
    updateNet();
    updateRadar();
  }
}

function getCountryCode(countryName) {
  const index = options["Countries"].indexOf(countryName);
  return options["Country_Codes"][index];
}

function getCentreNode() {
  relation_name = net_relation.split("_")[0];
  if (relation_name == "class") {
    return class_name;
  } else if (relation_name == "race") {
    return race_name;
  } else if (relation_name == "combo") {
    return combo_name;
  } else if (relation_name == "skill") {
    return skill_name;
  }
}

function disableChartRadioButton(name, centreValue, relationValue) {
  if (name == "relation") {
    value = centreValue;
  }
  if (name == "centre") {
    value = relationValue;
  }
  // fetch all inputs of given name
  // we need to iterate them all to enable those that might have been disabled earlier
  $('input[name="' + name + '"]').each(function (index, radio) {
    // disable the one of same value as the checked value
    if (
      radio.value == value ||
      (value == "combo" && (radio.value == "class" || radio.value == "race")) ||
      (value == "class" && radio.value == "combo") ||
      (value == "race" && radio.value == "combo")
    ) {
      radio.disabled = true;
    } else {
      radio.disabled = false;
    }
  });
  net_relation = centreValue + "_" + relationValue;
  updateNet();
}

function matchRadioButton(id, value) {
  radiobtn = document.getElementById(id + value);
  radiobtn.checked = true;
  relationValue = document.querySelector(
    'input[name="relation"]:checked'
  ).value;
  disableChartRadioButton("relation", value, relationValue);
  radar_option = value;
  updateRadar();
}

//Radio Buttons Filtering Behaviour Monitor
$('input[name="centre"]').change(function () {
  matchRadioButton("r_", $(this).val());
});
$('input[name="relation"]').change(function () {
  centreValue = document.querySelector('input[name="centre"]:checked').value;
  disableChartRadioButton("centre", centreValue, $(this).val());
});
$('input[name="f_radar"]').change(function () {
  matchRadioButton("fc_", $(this).val());
});
