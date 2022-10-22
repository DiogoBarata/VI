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
	selectFilter('class_filter', options['Classes'],'Classes:');
	selectFilter('race_filter', options['Races'], 'Races:');
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
    
    d3.json("https://raw.githubusercontent.com/DiogoBarata/VI/main/network_all_data.json").then(function(data) {
		const linkObject = data[relation][centre].links;
        const nodeObject = data[relation][centre].nodes;
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

        // Initialize the network
        const simulation = d3.forceSimulation(nodeObject)           // Force algorithm is applied to nodes
            .force("link", d3.forceLink()                           // This force provides links between nodes
                .distance(linkDistance)      
                .id(function(d) { return d.id; })                   // This provide  the id of a node
                .links(linkObject)                                  // and this the list of links
            )
            .force("charge", d3.forceManyBody().strength(-1000))    // This adds repulsion between nodes
            .force("center", d3.forceCenter(width / 2, height / 2)) // This force attracts nodes to the center of the svg area
            .on("end", ticked);
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

function selectFilter(filterId, data,legend){
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

function radioFilter(filterId, data,legend){
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
		radioFilter('class_filter', options['Classes'], 'Classes:');
		selectFilter('race_filter', options['Races'], 'Races:');
		if(prevCentreSel =='Race'){centreNode='';}
		prevCentreSel = 'Class'
	}
	else if(sel1=='Race'){
		radioFilter('race_filter', options['Races'], 'Races:');
		selectFilter('class_filter', options['Classes'],'Classes:');
		if(prevCentreSel =='Class'){centreNode='';}
		prevCentreSel = 'Race'
	}
	updateNet(sel_relation,centreNode)
});
$selects.eq(0).trigger('change');
