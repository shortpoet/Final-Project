
endpoint = 'cocktails'
glass_endpoint = 'svgs'


var chartDiv = document.getElementById("glasses");
var width = 720;
var height = 960;
// var width = chartDiv.clientWidth;
// var height = chartDiv.clientHeight;

// Define SVG area dimensions
var svgWidth = 720;
var svgHeight = 960;
// Define the chart's margins as an object
var margin = {
  top: 60,
  right: 60,
  bottom: 60,
  left: 60
};

// Define dimensions of the chart area
var glassWidth = svgWidth - margin.left - margin.right;
var glassHeight = svgHeight - margin.top - margin.bottom;

// Select body, append SVG area to it, and set its dimensions
var svg = d3.select("#glasses")
  .append("svg")
  .attr('id', 'svg')
  .attr("width", svgWidth)
  .attr("height", svgHeight)
  .attr('viewBox', '0 0 90 120')

function drawSelect(glass_endpoint) {
	d3.json(glass_endpoint).then(function(cocktails) {
    console.log(cocktails)
    var dropdownDiv = d3.select('#glassesSelect').append('div').classed('form-group', true).append('label')
      .attr('for', 'glassSelect')
      .text('Select Glass');
    var dropdown = dropdownDiv.append('select').classed('form-control', true).attr('id', 'glassSelect');
    var dropdownOptions = dropdown.selectAll('option').data(cocktails).enter()
      .append('option')
      .text(d => d.glass_type)
      .attr('value', d => d.glass_type)
      .attr('id', d => d.glass_type)
    dropdownDiv.on('change', function(){
      var sel = document.getElementById('glassSelect')
      var chosenGlass = sel.options[sel.selectedIndex].value
      glassGroup.remove()
      glassGroup = svg.append("g")
      drawGlass(endpoint, chosenGlass)
      })
    d3.select('cocktail_xl_margarita').attr('selected', 'selected')    
	})
}	
drawSelect(glass_endpoint)

function drawSearch(endpoint) {
  d3.json(endpoint).then(function(cocktails) {
    var searchBox = d3.select('#recipesSearch').append('div').classed('form-group').append('label')
      .attr('for', 'recipeSearch')
      .text('Search for Recipe')
    var searchInput = searchBox.append('input').classed('form-control', true)
      .attr('id', 'recipeSearch')
      .attr('type', 'text')
      .attr('placeholder', 'Search for Recipe')
      .attr('aria-label', 'Search for Recipe (autocomplete)')
  })
}

function drawGlass(endpoint, chosenGlass) {
	d3.json(endpoint).then(function(cocktails) {
      console.log(cocktails)
      console.log(chosenGlass)
      var glass = cocktails.filter(datum => datum.glass_type == chosenGlass)
      console.log(glass)
      var boundBox = document.getElementById('svg').getBoundingClientRect()
      console.log(boundBox)  
      
      var defs = svg.append('defs')
        .append('g')
        .attr('id', 'def')

      var clip = defs.append('clipPath').attr('id', 'clip')
        .selectAll('path').data(cocktails)
        .enter()
        .append('path')
        .attr('d', d => d.mask)
        
      // Append a group area, then set its margins
      var glassGroup = svg.append("g").attr('id', 'glass_group')

      // .attr("transform", `translate(${margin.left}, ${margin.top})`);

      var glassPath = glassGroup.selectAll('path').data(cocktails)
        .enter()
        .append('path')
        .attr('d', d => d.path)
        .attr('height', height)
        .attr('width', width)
        .attr('fill', 'none')
        .attr('stroke', '#000')
        .attr('stroke-width', '.265')

      var ingrRectGroup = glassGroup.append('g')

      var ingrRect = ingrRectGroup.selectAll('rect').data(cocktails)
        .enter()
        .append('rect')
        .attr('x', 13)
        .attr('y', d => d.maskTopMargin)
        .attr('height', d => d.maskHeight)
        .attr('width', 30)
        .attr('clip-path', 'url(#clip)')
        .style('fill', 'green')
    })
}	
var chosenGlass = 'cocktail_xl_margarita'
drawGlass(endpoint, chosenGlass)

function styleImportedSVG () {
  d3.select('svg')
    .on('mouseover', function() {
      // console.log('mouseover');
      // console.log('this', this);
      d3.selectAll('path')
        .style({
          'fill-opacity':   0.1,
          'stroke-opacity': 0.3
        })
    })
    .on('mouseout', function() {
      // console.log('mouseout');
      d3.selectAll('path')
        .style({
          'fill-opacity':   1,
          'stroke-opacity': 1
        })
    })
}