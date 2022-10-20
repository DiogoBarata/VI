const margin = {top: 10, right: 30, bottom: 30, left: 40},
      width = 500 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;
const options = {
    "Classes": [
        {"id": "root"},
        {"id": "Classes", "parent":"root"},
        {"id": "Artificer", "parent": "Classes"},
        {"id": "Barbarian", "parent": "Classes"},
        {"id": "Bard", "parent": "Classes"},
        {"id": "Cleric", "parent": "Classes"},
        {"id": "Druid", "parent": "Classes"},
        {"id": "Fighter", "parent": "Classes"},
        {"id": "Monk", "parent": "Classes"},
        {"id": "Paladin", "parent": "Classes"},
        {"id": "Ranger", "parent": "Classes"},
        {"id": "Rogue", "parent": "Classes"},
        {"id": "Sorcerer", "parent": "Classes"},
        {"id": "Warlock", "parent": "Classes"},
        {"id": "Wizard", "parent": "Classes"}
    ],
    "Races": [
        {"id": "root"},
        {"id": "Races", "parent":"root"},
        {"id":"Aarakocra", "parent":"Races"},
        {"id":"Aasimar", "parent":"Races"},
        {"id":"Bugbear", "parent":"Races"},
        {"id":"Centaur", "parent":"Races"},
        {"id":"Changeling", "parent":"Races"},
        {"id":"Custom", "parent":"Races"},
        {"id":"Dragonborn", "parent":"Races"},
        {"id":"Dwarf", "parent":"Races"},
        {"id":"Eladrin", "parent":"Races"},
        {"id":"Elf", "parent":"Races"},
        {"id":"Firbolg", "parent":"Races"},
        {"id":"Genasi", "parent":"Races"},
        {"id":"Gith", "parent":"Races"},
        {"id":"Gnome", "parent":"Races"},
        {"id":"Goblin", "parent":"Races"},
        {"id":"Goliath", "parent":"Races"},
        {"id":"Half-Elf", "parent":"Races"},
        {"id":"Half-Orc", "parent":"Races"},
        {"id":"Halfling", "parent":"Races"},
        {"id":"Hobgoblin", "parent":"Races"},
        {"id":"Human", "parent":"Races"},
        {"id":"Kalashtar", "parent":"Races"},
        {"id":"Kenku", "parent":"Races"},
        {"id":"Kobold", "parent":"Races"},
        {"id":"Leonin", "parent":"Races"},
        {"id":"Lizardfolk", "parent":"Races"},
        {"id":"Loxodon", "parent":"Races"},
        {"id":"Minotaur", "parent":"Races"},
        {"id":"Orc", "parent":"Races"},
        {"id":"Satyr", "parent":"Races"},
        {"id":"Shifter", "parent":"Races"},
        {"id":"Simic hybrid", "parent":"Races"},
        {"id":"Tabaxi", "parent":"Races"},
        {"id":"Tiefling", "parent":"Races"},
        {"id":"Triton", "parent":"Races"},
        {"id":"Turtle", "parent":"Races"},
        {"id":"Vedalken", "parent":"Races"},
        {"id":"Warforged", "parent":"Races"},
        {"id":"Yaun-Ti", "parent":"Races"}
    ]
}
const optionsNet = {
    'NetFilter':[
        {"id": "root"},
        {"id": "Relation Node", "parent":"root"},
        {"id": "Centre Node", "parent":"root"},
        {"id": "Classes", "parent":"Relation Node"},
        {"id": "Races", "parent":"Relation Node"},
        {"id":"Alignment", "parent":"Relation Node"},
        {"id": "Classes", "parent":"Centre Node"},
        {"id": "Races", "parent":"Centre Node"},
        {"id":"Alignment", "parent":"Centre Node"}
    ]
}

function init(){
    createVis3(".vis3",'Align_Race','LG');
    // someFilter('.class_filter','Classes',options);
    // someFilter('.race_filter','Races',options);
    // netFilter('.country_filter','NetFilter',optionsNet);
}


function createVis3(id,relation,centre){
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
            .attr("stroke", "green")
            .style("fill", "green")
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
            .force("center", d3.forceCenter(width / 1.5, height / 1.5)) // This force attracts nodes to the center of the svg area
            .on("end", ticked);
        function linkDistance(d) {
            calcDist = 10*(1/d.distance) + 1 
            console.log(calcDist, d.target)
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
    d3.select("#netVis").remove();
    createVis3(".vis3",relation,centre);
}

function someFilter(filterId,filterType,data){
    // Node content
	function renderNode(selection, rcd) {
		selection.append('input')
    		.attr('type', 'checkbox')
    		.on('change', function () {
      			d3.select('#selected')
				.text(checkboxValues(d3.select(filterId)));
    		});
		selection.append('span')
    		.text(rcd.id);
	}
	// Return array of ids that is checked
	function checkboxValues(selection) {
		console.log(selection.select('.body')
			.selectAll('input:checked').data().map(d => d.id));
		return selection.select('.body')
			.selectAll('input:checked').data().map(d => d.id);
	}
	// Recursively append child nodes
	function nextLevel(selection, node) {
		const label = selection.append('span');
		const arrow = label.append('span').classed('arrow', true);
		label.call(renderNode, node.data);
		if (!node.hasOwnProperty('children')) return;
		const items = selection.append('ul')
			.style('list-style-type', 'none')
			.selectAll('li')
			.data(node.children, d => d.id);
		items.exit().remove();
		items.enter()
			.append('li').merge(items)
			.each(function (d) {
				d3.select(this).call(nextLevel, d);
			});
		label.select('.arrow')
			.text('▼ ')
			.on('click', function () {  // Collapse on click
				const childList = selection.select('ul');
				if (!childList.size()) return;
				const expanded = childList.style('display') !== 'none';
				d3.select(this).text(expanded ? '▶ ' : '▼ ');
				childList.style('display', expanded ? 'none' : 'inherit');
			});
	}
	// Generate tree view
	function tree(selection) {
		selection
			.classed('viewport', true)
			.style('overflow-y', 'scroll')
			.style('height', '500px')
			.append('div')
			.classed('body', true)
			.style('transform', 'scale(1.5)')
			.style('transform-origin', 'top left');
	}
	// Update tree data
	function updateTree(selection, items) {
		const root = d3.stratify()
			.id(d => d.id)
			.parentId(d => d.parent)(items);
		selection.select('.body')
			.call(nextLevel, root);
		// Remove dummy root node
		selection.select('.body > span').remove();
		selection.select('.body > ul').style('padding-left', 0);
	}
	
	// Render
	d3.select(filterId + ' div').remove();
	d3.select(filterId).append('div')
		.call(tree)
		.call(updateTree, data[filterType]);

}

function netFilter(filterId,filterType,data){
    // Node content
	function renderNode(selection, rcd) {
		selection.append('input')
    		.attr('type', 'checkbox')
    		.on('change', function () {
      			d3.select('#selected')
				.text(checkboxValues(d3.select(filterId)));
    		});
		selection.append('span')
    		.text(rcd.id);
	}
	// Return array of ids that is checked
	function checkboxValues(selection) {
		var selectedNetFilters = (selection.select('.body')
			.selectAll('input:checked').data().map(d => d.id));
        console.log(selectedNetFilters)
	}
	// Recursively append child nodes
	function nextLevel(selection, node) {
		const label = selection.append('span');
		const arrow = label.append('span').classed('arrow', true);
		label.call(renderNode, node.data);
		if (!node.hasOwnProperty('children')) return;
		const items = selection.append('ul')
			.style('list-style-type', 'none')
			.selectAll('li')
			.data(node.children, d => d.id);
		items.exit().remove();
		items.enter()
			.append('li').merge(items)
			.each(function (d) {
				d3.select(this).call(nextLevel, d);
			});
		label.select('.arrow')
			.text('▼ ')
			.on('click', function () {  // Collapse on click
				const childList = selection.select('ul');
				if (!childList.size()) return;
				const expanded = childList.style('display') !== 'none';
				d3.select(this).text(expanded ? '▶ ' : '▼ ');
				childList.style('display', expanded ? 'none' : 'inherit');
			});
	}
	// Generate tree view
	function tree(selection) {
		selection
			.classed('viewport', true)
			.style('overflow-y', 'scroll')
			.style('height', '500px')
			.append('div')
			.classed('body', true)
			.style('transform', 'scale(1.5)')
			.style('transform-origin', 'top left');
	}
	// Update tree data
	function updateTree(selection, items) {
		const root = d3.stratify()
			.id(d => d.id)
			.parentId(d => d.parent)(items);
		selection.select('.body')
			.call(nextLevel, root);
		// Remove dummy root node
		selection.select('.body > span').remove();
		selection.select('.body > ul').style('padding-left', 0);
	}
	
	// Render
	d3.select(filterId + ' div').remove();
	d3.select(filterId).append('div')
		.call(tree)
		.call(updateTree, data[filterType]);

}
