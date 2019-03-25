
var endpoint = 'cocktails'
var glass_endpoint = 'svgs'


// var chartDiv = document.getElementById("glasses");
// var width = 720;
// var height = 960;
// var width = chartDiv.clientWidth;
// var height = chartDiv.clientHeight;

// Define SVG area dimensions
var svgWidth = 720;
var svgHeight = 960;
// Define the chart's margins as an object
// var margin = {
//   top: 5,
//   right: 5,
//   bottom: 5,
//   left: 5
// };

var margin = {top: 5, right: 5, bottom: 5, left: 5},
    width = 720 - margin.left - margin.right,
    height = 960 - margin.top - margin.bottom;

// Define dimensions of the chart area
var glassWidth = svgWidth - margin.left - margin.right;
var glassHeight = svgHeight - margin.top - margin.bottom;

// Select body, append SVG area to it, and set its dimensions
var svg = d3.select("#glasses")
  .append("svg")
  .attr('id', 'svg')
  .attr("width", width)
  .attr("height", height)
  .attr('viewBox', '0 0 90 120')

function drawSearch(endpoint) {
  d3.json(endpoint).then(function(cocktails) {
    var recipeNames = cocktails.map(x => x.name);
    var recipeSet = new Set(recipeNames);
    var recipeArr = [...recipeSet]
    var recipeSorted = recipeArr.sort((a,b) => a > b ? 1 : a === b ? 0 : -1);
    console.log(recipeSorted)
    var searchBox = d3.select('#recipesSearch').append('div').classed('form-group', true).append('label')
      .attr('for', 'recipeSearch')
      .text('Search for Recipe')
    var searchInput = searchBox.append('input').classed('form-control', true)
      .attr('id', 'recipeSearch')
      .attr('type', 'text')
      .attr('placeholder', 'Search for Recipe')
      .attr('aria-label', 'Search for Recipe (autocomplete)')
    var chosenRecipe = 'Adam and Eve'
    drawGlass(endpoint, chosenRecipe)
    autocomplete(document.getElementById('recipeSearch'), recipeSorted);
    var submit = searchBox.append('button')
      .attr('type', 'submit')
      .attr('class', 'btn btn-default')
      .attr('id', 'submitSearch')
      .text('Search')
      .on('click', function(d, i){
        svg.remove()
        svg = d3.select("#glasses")
          .append("svg")
          .attr('id', 'svg')
          .attr("width", svgWidth)
          .attr("height", svgHeight)
          .attr('viewBox', '0 0 90 120')
        var chosenRecipe = document.getElementById('recipeSearch').value
        console.log(chosenRecipe)
        drawGlass(endpoint, chosenRecipe)
      })
  })
}
drawSearch(endpoint)

function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
    var a, b, i, val = this.value;
    /*close any already open lists of autocompleted values*/
    closeAllLists();
    if (!val) { return false;}
    currentFocus = -1;
    /*create a DIV element that will contain the items (values):*/
    a = document.createElement("DIV");
    a.setAttribute("id", this.id + "autocomplete-list");
    a.setAttribute("class", "autocomplete-items");
    /*append the DIV element as a child of the autocomplete container:*/
    this.parentNode.appendChild(a);
    /*for each item in the array...*/
    for (i = 0; i < arr.length; i++) {
      /*check if the item starts with the same letters as the text field value:*/
      if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
        /*create a DIV element for each matching element:*/
        b = document.createElement("DIV");
        /*make the matching letters bold:*/
        b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
        b.innerHTML += arr[i].substr(val.length);
        /*insert a input field that will hold the current array item's value:*/
        b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
        /*execute a function when someone clicks on the item value (DIV element):*/
            b.addEventListener("click", function(e) {
            /*insert the value for the autocomplete text field:*/
            inp.value = this.getElementsByTagName("input")[0].value;
            /*close the list of autocompleted values,
            (or any other open lists of autocompleted values:*/
            closeAllLists();
        });
        a.appendChild(b);
      }
    }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
    var x = document.getElementById(this.id + "autocomplete-list");
    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {
      /*If the arrow DOWN key is pressed,
      increase the currentFocus variable:*/
      currentFocus++;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.keyCode == 38) { //up
      /*If the arrow UP key is pressed,
      decrease the currentFocus variable:*/
      currentFocus--;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.keyCode == 13) {
      /*If the ENTER key is pressed, prevent the form from being submitted,*/
      e.preventDefault();
      if (currentFocus > -1) {
        /*and simulate a click on the "active" item:*/
        if (x) x[currentFocus].click();
      }
    }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
    closeAllLists(e.target);
  });
}

var y = d3.scale.linear() 
  .rangeRound([height, 0]);

var z = d3.scale.category10();


function drawGlass(endpoint, chosenRecipe) {
	d3.json(endpoint).then(function(cocktails) {
    console.log(cocktails)
    console.log(chosenRecipe)
    var recipe = cocktails.filter(datum => datum.name == chosenRecipe)
    console.log(recipe)
    var boundBox = document.getElementById('svg').getBoundingClientRect()
    console.log(boundBox)  
    
    var defs = svg.append('defs')
      // .append('g')
      .attr('id', 'def')
    var clip = defs.append('clipPath').attr('id', 'clip')
      .selectAll('path').data(recipe)
      .enter()
      .append('path')
      .attr('d', d => d.mask)
      
    // Append a group area, then set its margins
    var glassGroup = svg.append("g").attr('id', 'glass_group')
      .attr("transform", `translate(${margin.left}, ${margin.top})`);
    var glassPath = glassGroup.selectAll('path').data(recipe)
      .enter()
      .append('path')
      .attr('d', d => d.path)
      .attr('height', height)
      .attr('width', width)
      .attr('fill', 'none')
      .attr('stroke', '#000')
      .attr('stroke-width', '.265')
    var ingrRectGroup = glassGroup.append('g')
    var maskTopMargin = recipe[0]['maskTopMargin']
    var maskHeight = recipe[0]['maskHeight']
    var ings = recipe[0]['ingredients'].map(x=>x)
    var ingVals = recipe[0]['ingredients'].map(x=>x.replace(/[A-Za-z]/g, '').trim())
    // console.log(maskTopMargin, maskHeight, ings)

    var volume = recipe[0]['total_volume']
    var j = 0
    var ingrRect = ingrRectGroup.selectAll('rect').data(ingVals)
      .enter()
      .append('rect')
      .attr('x', 0)
      .attr('y', maskTopMargin)
      .attr('height', (d,i) => {
        // console.log(y)
        this_arr = ingVals.slice(0, ingVals.length + j)
        // console.log(this_arr)
        this_arr = this_arr.map(x=>x/volume*maskHeight)
        // console.log(this_arr)
        j -= 1
        return this_arr.reduce((a,b)=> a + b, 0)
      })
      .attr('width', 60)
      .attr('clip-path', 'url(#clip)') 
      .style('fill', (d,i) => `rgb(100, ${(i+1)*60}, 100)`)
    var ingrTextGroup = ingrRectGroup.append('g')
      .attr('id', 'ingrTextGroup')
      .attr("transform", `translate(${margin.left + 30}, ${margin.top})`);
      // .attr("transform", `translate(10, 0)`);
    var k = 0
    
    var ingrText = ingrTextGroup.selectAll('text').data(ings)
      .enter()
      .append('text')
      .attr('x', 0)
      .attr('y', (d,i) => {
        console.log(k)
        this_arr = ingVals.slice(0, ingVals.length + k)
        console.log(this_arr)
        this_arr = this_arr.map(x=>x/volume*maskHeight)
        console.log(this_arr)
        k -= 1
        return this_arr.reduce((a,b)=> (a + b), 0)
      })
      .text(d => d)  
      .style('font-size', 3)
      .style('fill', 'black')
      .style('text-align', 'center')
      .classed('ingrText', true)
    })
}	
var chosenRecipe = 'Adam and Eve'
// drawGlass(endpoint, chosenRecipe)

var layers = d3.layout.stack()(ingVals.map(val => {
  return ings.map(ing => {
    return {x: ing, y: val}
  })
}))
console.log(layers)

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