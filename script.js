const options = {
	"Classes":['Artificer','Barbarian','Bard','Cleric','Druid','Fighter','Monk','Paladin',
	'Ranger','Rogue','Sorcerer','Warlock','Wizard'],
	"Races":['Aarakocra', 'Aasimar', 'Bugbear', 'Centaur', 'Changeling', 'Custom', 
	'Dragonborn', 'Dwarf', 'Eladrin', 'Elf', 'Firbolg', 'Genasi', 'Gith', 'Gnome', 
	'Goblin', 'Goliath', 'Half-Elf', 'Half-Orc', 'Halfling', 'Hobgoblin', 'Human', 
	'Kalashtar', 'Kenku', 'Kobold', 'Leonin', 'Lizardfolk', 'Loxodon', 'Minotaur', 
	'Orc', 'Satyr', 'Shifter', 'Simic hybrid', 'Tabaxi', 'Tiefling', 'Triton', 
	'Turtle', 'Vedalken', 'Warforged', 'Yaun-Ti']
}

function init(){
	createVis2('.vis2')
	selectFilter('class_filter', options['Classes'],'Classes:');
	selectFilter('race_filter', options['Races'], 'Races:');
}

var dateHisto = 'All';

function createVis2(id){
	// set the dimensions and margins of the graph
	const margin = {top: 30, right: 30, bottom: 70, left: 60},
	width = 460 - margin.left - margin.right,
	height = 400 - margin.top - margin.bottom;

	// append the svg object to the body of the page
	const svg = d3.select(id)
		.append("svg")
			.attr("width", width + margin.left + margin.right)
			.attr("height", height + margin.top + margin.bottom)
		.append("g")
			.attr("transform", `translate(${margin.left},${margin.top})`);

	// Parse the Data
	d3.csv("https://raw.githubusercontent.com/DiogoBarata/VI/main/resources/datasets/years.csv").then( function(data) {
		console.log(data)	
	// X axis
		const x = d3.scaleBand()
			.range([ 0, width ])
			.domain(data.map(d => d.Year))
			.padding(0.2);
		svg.append("g")
			.attr("transform", `translate(0, ${height})`)
			.call(d3.axisBottom(x))
			.selectAll("text")
			.attr("transform", "translate(12,0)")
				.style("text-anchor", "end");

		// Add Y axis
		const y = d3.scaleLinear()
			.domain([0, 4000])
			.range([ height, 0]);
		svg.append("g")
			.call(d3.axisLeft(y));

		svg.append('text')
			.attr('x',85)
			.text('Number of Players along the Years')

		// Add Tooltip
		var tooltip = d3.select(id)
			.append("div")
			.style("opacity", 0)
			.attr("class", "tooltip")
			.style("background-color", "black")
			.style("color", "white")
			.style("border-radius", "5px")
			.style("padding", "10px")
	
		// Bars
		svg.selectAll("mybar")
			.data(data)
			.join("rect")
				.attr('class','allbars')
				.attr("x", d => x(d.Year))
				.attr("y", d => y(d.Players))
				.attr("width", x.bandwidth())
				.attr("height", d => height - y(d.Players))
				.attr("fill", "#2296F3")
			.on("mouseover", function(event, d){
				tooltip
					.transition()
					.duration(100)
					.style("opacity", 1)
				tooltip
					.html("IRL event: " + d.IRL)
					.style("left", (event.x)/2-100 + "px")
					.style("top", (event.y)/2 + "px")
			})
			.on("mouseleave", function (event,d) {
				d3.selectAll(".myRect")
					.style("opacity",1)
				tooltip
					.transition()
					.duration(100)
					.style("opacity", 0)
			})
			.on("mousemove", function (event,d) {
				tooltip
					.style("left", (event.x)/2-100 + "px")
					.style("top", (event.y)/2 + "px")
			})
			.on("click", function (event,d) {
				// Select and deselect a bar
				if (!d3.select(this).classed("selected")){
					d3.select(this).classed("selected",true)
					d3.selectAll('.allbars').style('fill', '#2296F3'); //fill all circles black
					d3.select(this).style("fill", "#012B4E"); //then fill this circle lightcoral
					dateHisto = d.Year
					updateNet(sel_relation,centreNode)
				}else{
					d3.select(this).classed("selected",false)
					d3.selectAll('.allbars').style('fill', '#2296F3'); //fill all circles black
					d3.select(this).style("fill", "#2296F3")
					dateHisto = 'All'
					updateNet(sel_relation,centreNode)
				}
			})
	})
}

function createVis3(id,relation,centre){
	const margin = {top: 10, right: 30, bottom: 30, left: 40},
      width = 700 - margin.left - margin.right,
      height = 400 - margin.top - margin.bottom;
    // Append the svg object to the body of the page
    const svg = d3.select(id)
        .append("svg")
        .attr("id","netVis")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("class","node")
        .attr("transform",`translate(${margin.left}, ${margin.top})`);
    
    d3.json("https://raw.githubusercontent.com/DiogoBarata/VI/main/resources/datasets/network_all_data_with_dates.json").then(function(data) {
		console.log(data[relation],relation,dateHisto,centre)
		const linkObject = data[relation][dateHisto][centre].links;
        const nodeObject = data[relation][dateHisto][centre].nodes;
        // Initialize the links
        var link = svg
            .selectAll("line")
            .data(linkObject)
            .join("line")
            .style("stroke", "#aaa");
        // Initialize the nodes
        var node = svg.selectAll(".node")
            .data(nodeObject)
            .enter().append("g")
            .attr("class","node")
        node.append("circle")
            .attr("r",15)
            .attr("stroke", "grey")
            .style("fill", "grey")
        node.append("text")
            .text(function(d){ return d.name;})

		
		function linkDistance(d) {
			calcDist = 10*(1/d.distance) + 1
			return calcDist;
		}
		// This function is run at each iteration of the force algorithm
		// Updating the nodes position.
		function ticked() {
			link
				.attr("x1", d => d.source.x)
				.attr("y1", d => d.source.y)
				.attr("x2", d => d.target.x)
				.attr("y2", d => d.target.y);
			node
				.attr("transform", d => `translate(${d.x},${d.y})`);
			
		}
        // Initialize the network
        const simulation = d3.forceSimulation(nodeObject)           // Force algorithm is applied to nodes
            .force("link", d3.forceLink()                           // This force provides links between nodes  
                .id(function(d) { return d.id; })                   // This provide  the id of a node
                .links(linkObject)                                  // and this the list of links
				.distance(linkDistance)
            )
            .force("charge", d3.forceManyBody().strength(-1000))    // This adds repulsion between nodes
            .force("center", d3.forceCenter(width / 2, height / 2)) // This force attracts nodes to the center of the svg area
            .on("end", ticked);
        
    });    
}

function updateNet(relation,centre){
	if(centre=='' && !(relation == ''|| relation.startsWith('None') || relation.endsWith('None'))){
		d3.select("#netVis").remove();
	}
	if(centre!='' && !(relation == ''|| relation.startsWith('None') || relation.endsWith('None'))){
		d3.select("#netVis").remove();
		createVis3(".vis3",relation,centre);
	}

}

function selectFilter(filterId, data, legend){
	d3.select(".div_"+filterId).remove();
	var filter = d3.select('.'+filterId)
		.append('div')
		.attr('class','div_'+ filterId)
	filter
		.append('legend')
		.text(legend)
	filter
		.selectAll("input")
		.data(data)
		.enter()
		.append('label')
		.attr('for',function(d,i){ return filterId+i; })
		.text(function(d) { return d; })
		.append("input")
		.attr("type", "checkbox")
		.attr("id", function(d,i) { return filterId+i; })
		.attr("onClick", "changeSelect(this)");
}

function radioFilter(filterId, data, legend){
	d3.select(".div_"+filterId).remove();
	var filter = d3.select('.'+filterId)
		.append('div')
		.attr('class','div_'+ filterId)
	filter
		.append('legend')
		.text(legend)
	filter
		.selectAll("input")
		.data(data)
		.enter()
		.append('label')
		.attr('for',function(d,i){ return filterId+i; })
		.text(function(d) { return d; })
		.append("input")
		.attr("type", "radio")
		.attr("name","radio_filter")
		.attr("id", function(d,i) { return filterId+i; })
		.attr("value", function(d,i) { return d; })
		.attr("onClick", "changeRadio(this)");
}

var centreNode=''
var sel_relation = ''

function changeSelect(select_selection){}

function changeRadio(radio_selection){
	centreNode=radio_selection.value;
	updateNet(sel_relation,centreNode)
}

var prevCentreSel = ''
var $selects = $('select');
$selects.on('change', function() {
    $("option", $selects).prop("disabled", false);
    $selects.each(function() {
        var $select = $(this), 
            $options = $selects.not($select).find('option'),
            selectedText = $select.children('option:selected').text();
        $options.each(function() {
            if($(this).text() == selectedText) $(this).prop("disabled", true);
        });
    });
	var sel = document.getElementById('select_1');
	var sel1 = sel.options[sel.selectedIndex].value;
	var sel = document.getElementById('select_2');
	var sel2 = sel.options[sel.selectedIndex].value;
	sel_relation = sel1 + '_' + sel2

	if (sel1=='Class'){
		if(prevCentreSel != 'Class'){
			radioFilter('class_filter', options['Classes'], 'Classes:');
			selectFilter('race_filter', options['Races'], 'Races:');
		}
		if(prevCentreSel =='Race'){centreNode='';}
		prevCentreSel = 'Class'
	}
	else if(sel1=='Race'){
		if(prevCentreSel != 'Race'){
			radioFilter('race_filter', options['Races'], 'Races:');
			selectFilter('class_filter', options['Classes'],'Classes:');
		}
		if(prevCentreSel =='Class'){centreNode='';}
		prevCentreSel = 'Race'
	}
	updateNet(sel_relation,centreNode)
});
$selects.eq(0).trigger('change');
