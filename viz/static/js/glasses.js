
glass_endpoint = 'svgs'
recipe_endpoint = 'cocktails'

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

function drawInput(glass_endpoint) {
	d3.json(glass_endpoint).then(function(svgs) {
    console.log(svgs)
    var dropdownDiv = d3.select('#glassesSelect').append('div').classed('form-group', true).append('label')
      .attr('for', 'glassSelect')
      .text('Select Glass');
    var dropdown = dropdownDiv.append('select').classed('form-control', true).attr('id', 'glassSelect');
    var dropdownOptions = dropdown.selectAll('option').data(svgs).enter()
      .append('option')
      .text(d => d.name)
      .attr('value', d => d.name)
      .attr('id', d => d.name)
    dropdownDiv.on('change', function(){
      var sel = document.getElementById('glassSelect')
      var chosenGlass = sel.options[sel.selectedIndex].value
      glassGroup.remove()
      glassGroup = svg.append("g")
      drawGlass(glass_endpoint, chosenGlass)
      })
    d3.select('cocktail_xl_margarita').attr('selected', 'selected')    
	})
}	
drawInput(glass_endpoint)

function drawGlass(glass_endpoint, chosenGlass) {
	d3.json(glass_endpoint).then(function(svgs) {
    d3.json(recipe_endpoint).then(function(recipes) {
      console.log(svgs)
      console.log(recipes)
      console.log(chosenGlass)
      var glass = svgs.filter(datum => datum.name == chosenGlass)
      console.log(glass)
      var boundBox = document.getElementById('svg').getBoundingClientRect()
      console.log(boundBox)  
      
      var defs = svg.append('defs')
        .append('g')
        .attr('id', 'def')

      var clip = defs.append('clipPath').attr('id', 'clip')
        .selectAll('path').data(glass)
        .enter()
        .append('path')
        .attr('d', d => d.mask)
        
      // Append a group area, then set its margins
      var glassGroup = svg.append("g").attr('id', 'glass_group')

      // .attr("transform", `translate(${margin.left}, ${margin.top})`);

      var glassPath = glassGroup.selectAll('path').data(glass)
        .enter()
        .append('path')
        .attr('d', d => d.path)
        .attr('height', height)
        .attr('width', width)
        .attr('fill', 'none')
        .attr('stroke', '#000')
        .attr('stroke-width', '.265')

      var ingrRectGroup = glassGroup.append('g')

      var ingrRect = ingrRectGroup.selectAll('rect').data(glass)
        .enter()
        .append('rect')
        .attr('x', 13)
        .attr('y', d => d.maskTopMargin)
        .attr('height', d => d.maskHeight)
        .attr('width', 30)
        .attr('clip-path', 'url(#clip)')
        .style('fill', 'green')
    })
	})
}	
var chosenGlass = 'cocktail_xl_margarita'
drawGlass(glass_endpoint, chosenGlass)

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