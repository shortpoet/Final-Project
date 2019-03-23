
glass_endpoint = 'svgs'
recipe_glass_endpoint = 'cocktails'

var chartDiv = document.getElementById("glasses");
var width = 720;
var height = 960;
// var width = chartDiv.clientWidth;
// var height = chartDiv.clientHeight;
// var glass = 'collins'
// var svg_file_path = '/static/res/' + glass + '.svg'

// Define SVG area dimensions
var svgWidth = 720;
var svgHeight = 960;
console.log(svgWidth)
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



// Append a group area, then set its margins

  // .attr("transform", `translate(${margin.left}, ${margin.top})`);




function drawInput(glass_endpoint) {
	d3.json(glass_endpoint).then(function(svgs) {
    console.log(svgs)
    var dropdownDiv = d3.select('#glassesSelect').append('div').classed('form-group', true).append('label')
      .attr('for', 'glassSelect')
      .text('Select Glass');
    var dropdown = dropdownDiv.append('select').classed('form-control', true).attr('id', 'glassSelect');
    var dropdownOptions = dropdown.selectAll('option').data(svgs).enter()
      .append('option')
      .text(d => d.glass_type)
      .attr('value', d => d.glass_type)
      .attr('id', d => d.glass_type)
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
    console.log(svgs)
    console.log(chosenGlass)
    var glass = svgs.filter(datum => datum.glass_type == chosenGlass)
    console.log(glass)
    // var glassSvg = d3.select('div#glasses').append('svg')
    //   .attr('id', 'svg')
    //   .attr('width', width)
    //   .attr('height', height)
    //   // .attr('viewBox', '0 0 ' + width + ' ' + height)
    //   .attr('viewBox', '0 0 90 120')
    var boundBox = document.getElementById('svg').getBoundingClientRect()
    console.log(boundBox)  
    
    var defs = svg.append('defs')
      // .append('g')
      .attr('id', 'def')

    var clip = defs.append('clipPath').attr('id', 'clip')
      .selectAll('path').data(glass)
      .enter()
      .append('path')
      .attr('d', d => d.mask)
      
    
    var glassGroup = svg.append("g").attr('id', 'glass_group')

    var glassPath = glassGroup.selectAll('path').data(glass)
      .enter()
      .append('path')
      .attr('d', d => d.path)
      .attr('height', height)
      .attr('width', width)
      .attr('fill', 'none')
      .attr('stroke', '#000')
      .attr('stroke-width', '.265')

    // var ingrRectGroup = glassGroup.append('g')

    var ingrRect = glassGroup.selectAll('rect').data(glass)
      .enter()
      .append('rect')
      .attr('x', 13)
      // .attr('y', 20)
      .attr('y', d => d.maskTopMargin)
      .attr('height', d => d.maskHeight)
      // .attr('height', 30)
      .attr('width', 30)
      .attr('clip-path', 'url(#clip)')
      .style('fill', 'green')

    // var ingrRect = ingrRectGroup.append('use')
    //   .attr('class', 'ingredient')
    //   .attr('xlink:href', '#def')
    
    // var maskPath = glassGroup.selectAll('path').data(glass)
    //   .enter()
    //   .append('path')
    //   .attr('d', d => d.mask)
    //   .attr('id', 'clip-Path')
    //   .attr('height', height)
    //   .attr('width', width)
    

    
	})
}	
var chosenGlass = 'cocktail_xl_margarita'
drawGlass(glass_endpoint, chosenGlass)

// d3.xml(svg_file_path).mimeType("image/svg+xml").get(function(error, xml) {
//   if (error) throw error;
//   document.body.appendChild(xml.documentElement);
// });
// var dg = "M14.997 56.882c-.32-.867-.472-3.905-.61-5.866-.812-11.488-1.215-31.785-1.294-34.524l-.13-4.46V9.86c0-1.406.021-2.813 0-4.219-.024-1.684-.05-4.89-.148-5.051-.136-.227-.703-.27-.793-.022-.14.388.035 3.734.042 5.6.005 1.407 0 2.813 0 4.218 0 .725-.012 1.45 0 2.174.021 1.358.094 2.715.129 4.073.057 2.288.07 4.577.129 6.865.05 1.951.12 3.902.193 5.852.077 2.02.259 6.058.259 6.058l.504 14.757.122 4.63.074 2.933c0 .936.387 1.102.827 1.436.501.38 1.828.468 1.828.468H28.85s1.327-.088 1.828-.468c.44-.334.828-.5.828-1.436l.073-2.934.122-4.629.505-14.757s.181-4.038.258-6.058c.074-1.95.143-3.9.193-5.852.06-2.288.072-4.577.13-6.865.034-1.358.107-2.715.129-4.073.011-.725 0-1.45 0-2.174 0-1.405-.006-2.811 0-4.217.006-1.867.182-5.213.041-5.6-.09-.25-.657-.206-.793.02-.097.162-.124 3.368-.148 5.052-.021 1.406 0 2.813 0 4.219v2.173l-.13 4.459c-.079 2.74-.482 23.036-1.294 34.524-.138 1.96-.29 5-.61 5.866-.524.845-5.12.554-7.492.587-2.374-.033-6.968.258-7.493-.587z"
// var dm = "M32.115 1.154c-.032.581-.083 2.991-.1 4.487-.015 1.406-.006 2.813 0 4.219v2.173l-.129 4.459c-.079 2.74-.482 23.036-1.294 34.524-.138 1.96-.29 5-.61 5.866-.524.845-5.12.554-7.492.587-2.374-.033-6.968.258-7.493-.587-.32-.867-.472-3.905-.61-5.866-.812-11.488-1.221-31.785-1.294-34.524l-.13-4.46V9.86c0-1.406.016-2.813 0-4.219-.016-1.5-.05-4.18-.1-4.503 7.1.11 15.605-.022 19.252.016z"
// var glassSvg = d3.select('div#glasses').append('svg')
//   .attr('id', 'svg')
//   .attr('width', width)
//   .attr('height', height)
//   // .attr('viewBox', '0 0 ' + width + ' ' + height)
//   .attr('viewBox', '0 0 90 120')
// var boundBox = document.getElementById('svg').getBoundingClientRect()
// console.log(boundBox)
  

// var glassGroup = glassSvg.append('g')
//   .attr('fill', 'none')
//   .attr('stroke', '#000')
//   .attr('stroke-width', '.265')
// var glassPath = glassGroup.append('path')
//   .attr('d', dg)
//   .attr('height', height)
//   .attr('width', width)
// var maskPath = glassGroup.append('path')
//   .attr('d', dm)
//   .attr('id', 'clip-Path')
//   .attr('height', height)
//   .attr('width', width)

// var clip = glassGroup.append('clipPath')
//   .attr('id', 'clip')
//   .append('path')
//   .attr('d', dm)

// var ingrFill = glassGroup.append('rect')
//   .attr('x', 13)
//   .attr('y', 5)
//   // .attr('x', boundBox.x)
//   // .attr('y', boundBox.y)
//   .attr('clip-path', 'url(#clip)')
//   .style('fill', 'green')
//   .attr('height', 20)
//   .attr('width', 19)
  // .attr('height', boundBox.height)
  // .attr('width', boundBox.width)

  // load the external svg from a file
// d3.xml(svg_file_path).mimeType("image/svg+xml").get(function(error, xml) {
//   //   if (error) throw error;
//   var importedNode = document.importNode(xml.documentElement, true);
  
//   d3.select("svg")
//     .each(function() {
//       this.appendChild(importedNode);
//     })
//     var clipPath = document.getElementById('mask').getAttribute('d')

//     var boundBox = document.getElementById(glass + 'svg').getBoundingClientRect()
//     console.log(clipPath)
//     console.log(boundBox)
//     svg.append('clipPath')
//       .attr('id', 'clip-Path')
//       .append('path')
//       .attr('d', clipPath)
//     svg.append('rect')
//       .attr('x', boundBox.x)
//       .attr('y', boundBox.y)
//       .attr('clip-path', 'url(#clipPath)')
//       .style('fill', 'green')
//       .attr('height', boundBox.height)
//       .attr('width', boundBox.width)
//     // inside of our d3.xml callback, call another function
//     // that styles individual paths inside of our imported svg
//     styleImportedSVG()
// });

// d3.xml(svg_file_path).mimeType("image/svg+xml").get(function(error, xml) {
//   if (error) throw error;
//   document.body.appendChild(xml.documentElement);
//   var importedNode = document.importNode(xml.documentElement, true);
//   d3.select("div#glasses")
//     .each(function() {
//       this.appendChild(importedNode);
//     })
//     // inside of our d3.xml callback, call another function
//     // that styles individual paths inside of our imported svg
//     styleImportedSVG()
  
// });

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