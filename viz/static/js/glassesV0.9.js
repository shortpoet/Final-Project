
var endpoint = 'cocktails'
var glass_endpoint = 'svgs'


var chartDiv = document.getElementById("glasses");
var width = 720;
var height = 720;
// var width = chartDiv.clientWidth;
// var height = chartDiv.clientHeight;

// Define SVG area dimensions
var svgWidth = 720;
var svgHeight = 720;
// Define the chart's margins as an object
var margin = {
  top: 5,
  right: 5,
  bottom: 5,
  left: 5
};

// Define dimensions of the chart area
var glassWidth = svgWidth - margin.left - margin.right;
var glassHeight = svgHeight - margin.top - margin.bottom;

// Select body, append SVG area to it, and set its dimensions
var svg = d3.select("#glasses")
  .append("svg")
  .attr('id', 'svg')
  .attr("width", glassWidth)
  .attr("height", glassHeight)
  .attr('viewBox', '0 -5 110 911')

function drawInput(endpoint) {
  d3.json(endpoint).then(function(cocktails) {
    var recipeNames = cocktails.map(x => x.name);
    var recipeSet = new Set(recipeNames);
    var recipeArr = [...recipeSet]
    var recipeSorted = recipeArr.sort((a,b) => a > b ? 1 : a === b ? 0 : -1);
    // console.log(recipeSorted)
    var recSearchBox = d3.select('#recipesSearch').append('div').classed('form-group', true).append('label')
      .attr('for', 'recipeSearch')
      .text('Search for Recipe')
    var recSearchInput = recSearchBox.append('input').classed('form-control', true)
      .attr('id', 'recipeSearch')
      .attr('type', 'text')
      .attr('placeholder', 'Search for Recipe')
      .attr('aria-label', 'Search for Recipe (autocomplete)')
    var chosenRecipe = 'Adam and Eve'
    // drawGlass(endpoint, chosenRecipe)
    autocomplete(document.getElementById('recipeSearch'), recipeSorted);
    var recSubmit = recSearchBox.append('button')
      .attr('type', 'submit')
      .attr('class', 'btn btn-default')
      .attr('id', 'recSubmitSearch')
      .text('Search')
      .on('click', function(d, i){
        d3.select('table').remove()
        var chosenRecipe = document.getElementById('recipeSearch').value
        console.log(chosenIngred)
        drawTable(endpoint, chosenRecipe, 'recipe')
        svg.remove()
        svg = d3.select("#glasses")
          .append("svg")
          .attr('id', 'svg')
          .attr("width", svgWidth)
          .attr("height", svgHeight)
          .attr('viewBox', '0 -5 110 110')
        var chosenRecipe = document.getElementById('recipeSearch').value
        console.log(chosenRecipe)
        drawGlass(endpoint, chosenRecipe)
      })
    var ingSearchBox = d3.select('#ingrSearch').append('div').classed('form-group', true).append('label')
      .attr('for', 'ingredSearch')
      .text('Search for Ingredient')
    var ingSearchInput = ingSearchBox.append('input').classed('form-control', true)
      .attr('id', 'ingredSearch')
      .attr('type', 'text')
      .attr('placeholder', 'Search for Ingredient')
      .attr('aria-label', 'Search for Ingredient (autocomplete)')
    var ingSubmit = ingSearchBox.append('button')
      .attr('type', 'submit')
      .attr('class', 'btn btn-default')
      .attr('id', 'submitSearch')
      .text('Search')
      .on('click', function(d, i){
        d3.select('table').remove()
        var chosenIngred = document.getElementById('ingredSearch').value
        console.log(chosenIngred)
        drawTable(endpoint, chosenIngred, 'ingredient')
      })
    var generate = d3.select('#generate').append('button')
      .attr('type', 'submit')
      .attr('class', 'btn btn-default')
      .attr('id', 'generateButton')
      .text('Generate')
  })
}
drawInput(endpoint)

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

function drawGlass(endpoint, chosenRecipe) {
	d3.json(endpoint).then(function(cocktails) {
      // console.log(cocktails)
      // console.log(chosenRecipe)
      var recipe = cocktails.filter(datum => datum.name == chosenRecipe)
      console.log(recipe)
      var boundBox = document.getElementById('svg').getBoundingClientRect()
      // console.log(boundBox)  
      
      var defs = svg.append('defs')
        // .append('g')
        .attr('id', 'def')

      var clip = defs.append('clipPath').attr('id', 'clip')
        .selectAll('path').data(recipe)
        .enter()
        .append('path')
        .attr('d', d => d.mask)

      var starDef = svg.append('defs')
        .append('g')
        .attr('id', 'starDef')
      // glassGroup
        .append('svg')
        .attr('height', 25)
        .attr('width', 23)
        .attr('viewBox', '0 0 26 26')
        .attr('class', 'star rating')
        .append('polygon')
        .attr('class', 'star')
        .attr('points', "9.9, 1.1, 3.3, 21.78, 19.8, 8.58, 0, 8.58, 16.5, 21.78")
        .style('fill-rule', 'nonzero')
        // .style('fill', 'yellow')
        
      // Append a group area, then set its margins
      var glassGroup = svg.append("g").attr('id', 'glass_group')
        .attr("transform", `translate(${margin.left - 3}, ${margin.top})`);

      var glassPath = glassGroup.selectAll('path').data(recipe)
        .enter()
        .append('path')
        .attr('d', d => d.path)
        // .attr('height', .5 * glassHeight)
        // .attr('width', .5 * glassWidth)
        .attr('fill', 'none')
        .attr('stroke', '#000')
        .attr('stroke-width', '.265')

      var ingrRectGroup = glassGroup.append('g')
        .attr('id', 'ingrRectGroup')

      var maskTopMargin = recipe[0]['maskTopMargin']
      var maskHeight = recipe[0]['maskHeight']
      var ings = recipe[0]['ingredients'].map(x=>x)
      var ingVals = recipe[0]['ingredients'].map(x=>x.replace(/[A-Za-z]/g, '').trim())
      // console.log(maskTopMargin, maskHeight, ings)
      var volume = recipe[0]['total_volume']
      var y = 0
      var ingrRect = ingrRectGroup.selectAll('rect').data(ingVals)
        .enter()
        .append('rect')
        .attr('x', 0)
        .attr('y', maskTopMargin)
        .attr('height', (d,i) => {
          // console.log(y)
          this_arr = ingVals.slice(0, ingVals.length + y)
          // console.log(this_arr)
          this_arr = this_arr.map(x=>x/volume*maskHeight)
          // console.log(this_arr)
          y -= 1
          return this_arr.reduce((a,b)=> a + b, 0)
        })
        .attr('width', 60)
        .attr('clip-path', 'url(#clip)') 
        .style('fill', (d,i) => `rgb(100, ${(i+1)*60}, 100)`)
      var ingrTextGroup = ingrRectGroup.append('g')
        .attr('id', 'ingrTextGroup')
        .attr("transform", `translate(${margin.left + 50}, ${margin.top})`);
        // .attr("transform", `translate(10, 0)`);
      var k = 0
      var rectHeights = d3.selectAll('rect').nodes().map(x=>x.getBBox().height).reverse()

      // console.log(rectHeights)
      var ingrText = ingrTextGroup.selectAll('text').data(ings)
        .enter()
        .append('text')
        .attr('x', 0)
        .attr('y', (d,i) => {
          while (i < rectHeights.length) {
            if (i == 0) {
              // console.log(rectHeights[i])
              return (rectHeights[i]/2)
            }
            else {
              // console.log(rectHeights[i])
              return ((rectHeights[i] - rectHeights[i-1]) / 2) + rectHeights[i-1]
            }
          }
        })
        .text(d => d)  
        .style('font-size', 2)
        .style('fill', 'black')
        .style('text-align', 'center')
        .classed('ingrText', true)

      var borderPath = glassGroup.append("rect")
        .attr("x", 0)
        .attr("y", -5)
        .attr("height", 75)
        .attr("width", 105)
        .style("stroke", 'black')
        .style("fill", "none")
        .style("stroke-width", .75);
    
      var instructions = recipe[0]['instructions']
      // console.log(instructions)
      instructions = instructions.split('.').slice(0, -1)
      // console.log(instructions)

      var instrDiv = d3.select('#instructions')
        .style('border', '5px solid black')
        // .style('height', 480 +'px')
        .append('ul')
        .selectAll('li')
        .data(instructions)
        .enter()
        .append('li')
        .text(d=>d)
        .style('font-size', 2)
        .style('color', 'green')
        .style('text-align', 'center')
        .classed('instrText', true)
        .append('hr')
        .append('br')

      var ratingGroup = glassGroup.append('g')
        .attr('transform', 'translate(2.5, 0)')
        // .append('div')
        .attr('class', 'stars')
        .attr('data-stars', 1)
        
      
      // var dataStars1 = ratingGroup.append('use')
      //   .attr('transform', 'translate(0, 75)')
      //   .attr('data-rating', 1)
      //   .attr('id', 'data-stars1')
      //   .attr("xlink:href","#starDef")
      // var dataStars2 = ratingGroup.append('use')
      //   .attr('transform', 'translate(20, 75)')
      //   .attr('data-rating', 2)
      //   .attr('id', 'data-stars2')
      //   .attr("xlink:href","#starDef")
      // var dataStars3 = ratingGroup.append('use')
      //   .attr('transform', 'translate(40, 75)')
      //   .attr('data-rating', 3)
      //   .attr('id', 'data-stars3')
      //   .attr("xlink:href","#starDef")
      // var dataStars4 = ratingGroup.append('use')
      //   .attr('transform', 'translate(60, 75)')
      //   .attr('data-rating', 4)
      //   .attr('id', 'data-stars4')
      //   .attr("xlink:href","#starDef")
      // var dataStars5 = ratingGroup.append('use')
      //   .attr('transform', 'translate(80, 75)')
      //   .attr('data-rating', 5)
      //   .attr('id', 'data-stars5')
      //   .attr("xlink:href","#starDef")
      
      // var dataStars1 = ratingGroup.append('g')
      //   .attr('transform', 'translate(0, 75)')
      //   .append('svg')
      //   .attr('data-rating', 1)
      //   .attr('id', 'data-stars1')
      //   .attr('height', 25)
      //   .attr('width', 23)
      //   .attr('viewBox', '0 0 26 26')
      //   .attr('class', 'star rating')
      //   .append('polygon')
      //   .attr('points', "9.9, 1.1, 3.3, 21.78, 19.8, 8.58, 0, 8.58, 16.5, 21.78")
      //   .style('fill-rule', 'nonzero')
      // var dataStars2 = ratingGroup.append('g')
      //   .attr('transform', 'translate(20, 75)')
      //   .append('svg')
      //   .attr('data-rating', 2)
      //   .attr('id', 'data-stars2')
      //   .attr('height', 25)
      //   .attr('width', 23)
      //   .attr('viewBox', '0 0 26 26')
      //   .attr('class', 'star rating')
      //   .append('polygon')
      //   .attr('points', "9.9, 1.1, 3.3, 21.78, 19.8, 8.58, 0, 8.58, 16.5, 21.78")
      //   .style('fill-rule', 'nonzero')      
      // var dataStars3 = ratingGroup.append('g')
      //   .attr('transform', 'translate(40, 75)')
      //   .append('svg')
      //   .attr('data-rating', 3)
      //   .attr('id', 'data-stars3')
      //   .attr('height', 25)
      //   .attr('width', 23)
      //   .attr('viewBox', '0 0 26 26')
      //   .attr('class', 'star rating')
      //   .append('polygon')
      //   .attr('points', "9.9, 1.1, 3.3, 21.78, 19.8, 8.58, 0, 8.58, 16.5, 21.78")
      //   .style('fill-rule', 'nonzero')      
      // var dataStars4 = ratingGroup.append('g')
      //   .attr('transform', 'translate(60, 75)')
      //   .append('svg')
      //   .attr('data-rating', 4)
      //   .attr('id', 'data-stars4')
      //   .attr('height', 25)
      //   .attr('width', 23)
      //   .attr('viewBox', '0 0 26 26')
      //   .attr('class', 'star rating')
      //   .append('polygon')
      //   .attr('points', "9.9, 1.1, 3.3, 21.78, 19.8, 8.58, 0, 8.58, 16.5, 21.78")
      //   .style('fill-rule', 'nonzero')
      // var dataStars5 = ratingGroup.append('g')
      //   .attr('transform', 'translate(80, 75)')
      //   .append('svg')
      //   .attr('data-rating', 5)
      //   .attr('id', 'data-stars5')
      //   .attr("xlink:href","#starDef")
      //   .attr('height', 25)
      //   .attr('width', 23)
      //   .attr('viewBox', '0 0 26 26')
      //   .attr('class', 'star rating')
      //   .append('polygon')
      //   .attr('points', "9.9, 1.1, 3.3, 21.78, 19.8, 8.58, 0, 8.58, 16.5, 21.78")
      //   .style('fill-rule', 'nonzero')


      var ratingDiv = d3.select('#glasses').append('div')
        .attr("transform", `translate(0, -25)`)
        .attr('class', 'stars')
        .attr('data-stars', 1)
        .append('text')
        .text('Hello World!')
      var dataStars1 = ratingDiv
        .append('svg')
        .attr('data-rating', 1)
        .attr('id', 'data-stars1')
        .attr('height', 25)
        .attr('width', 23)
        .attr('viewBox', '0 0 26 26')
        .attr('class', 'star rating')
        .append('polygon')
        .attr('points', "9.9, 1.1, 3.3, 21.78, 19.8, 8.58, 0, 8.58, 16.5, 21.78")
        .style('fill-rule', 'nonzero')
      var dataStars2 = ratingDiv
        .append('svg')
        .attr('data-rating', 2)
        .attr('id', 'data-stars2')
        .attr('height', 25)
        .attr('width', 23)
        .attr('viewBox', '0 0 26 26')
        .attr('class', 'star rating')
        .append('polygon')
        .attr('points', "9.9, 1.1, 3.3, 21.78, 19.8, 8.58, 0, 8.58, 16.5, 21.78")
        .style('fill-rule', 'nonzero')      
      var dataStars3 = ratingDiv
        .append('svg')
        .attr('data-rating', 3)
        .attr('id', 'data-stars3')
        .attr('height', 25)
        .attr('width', 23)
        .attr('viewBox', '0 0 26 26')
        .attr('class', 'star rating')
        .append('polygon')
        .attr('points', "9.9, 1.1, 3.3, 21.78, 19.8, 8.58, 0, 8.58, 16.5, 21.78")
        .style('fill-rule', 'nonzero')      
      var dataStars4 = ratingDiv
        .append('svg')
        .attr('data-rating', 4)
        .attr('id', 'data-stars4')
        .attr('height', 25)
        .attr('width', 23)
        .attr('viewBox', '0 0 26 26')
        .attr('class', 'star rating')
        .append('polygon')
        .attr('points', "9.9, 1.1, 3.3, 21.78, 19.8, 8.58, 0, 8.58, 16.5, 21.78")
        .style('fill-rule', 'nonzero')
      var dataStars5 = ratingDiv
        .append('svg')
        .attr('data-rating', 5)
        .attr('id', 'data-stars5')
        .attr("xlink:href","#starDef")
        .attr('height', 25)
        .attr('width', 23)
        .attr('viewBox', '0 0 26 26')
        .attr('class', 'star rating')
        .append('polygon')
        .attr('points', "9.9, 1.1, 3.3, 21.78, 19.8, 8.58, 0, 8.58, 16.5, 21.78")
        .style('fill-rule', 'nonzero')

    })
}	
// var chosenRecipe = 'Adam and Eve'
// drawGlass(endpoint, chosenRecipe)

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
function drawTable(endpoint, chosenParam, paramType) {
	// console.log(endpoint)
	d3.json(endpoint).then(function(recipe_dump) {
    
    var chosenRecipes = []
    if (paramType === 'ingredient') {
      var recipeFilter = recipe_dump.filter(recipe => {
        recipe['ingredients'].forEach(ingredient => {
          // console.log(ingredient)
          // if (ingredient !== undefined && ingredient.indexOf(chosenIngred) !== -1) {
          if (ingredient.includes(chosenParam)) {
            chosenRecipes.push(recipe)
            return true;
          }
      })
    })
    }
    else if (paramType === 'recipe') {
      var chosenRecipes = recipe_dump.filter(datum => datum.name == chosenParam)
      // chosenRecipes.push(recipe)
      // console.log(recipe)  
    }
    
		// console.log(endpoint)
    console.log(chosenRecipes)
		var headers = d3.keys(recipe_dump[0])
		// console.log(headers)
		headers = headers.slice(9,10).concat(headers.slice(2,6))
		// console.log(headers)
		var dataTable = d3.select('#table').append('table').attr('class', 'datatable table table-striped');
		var header = dataTable.append('thead').selectAll('th').data(headers).enter()
			.append('th')
			.attr('class', 'sortable')
			.attr('value', d => d)
			.attr('id', d => `${d}-header`)
			.text(d => d)
		var tbody = dataTable.append('tbody')
		var content = tbody.selectAll('tr').data(chosenRecipes).enter()
			.append('tr')
			.html((data, i) => (`
			  <td class="col_0 row_${i + 1}">${data.name}</td><td class="col_1 row_${i + 1}">${data.glass_size}</td>
				<td class="col_2 row_${i + 1}">${data.glass_type}</td><td class="col_3 row_${i + 1}">${data.ingredients}</td>
				<td class="col_4 row_${i + 1}">${data.instructions}</td>
				`
			))
			.on('mouseover', function(d, i) {
				d3.select(this).style('background-color', 'rgb(0, 14, 142').style('color', 'silver')
			})
			.on('mouseout', function(d, i) {
				d3.select(this).style('background-color', null).style('color', null)
				d3.select('.data').append('table').classed('table table-striped table-sortable', true)
      })
      .on('click', function(d, i) {
        svg.remove()
        svg = d3.select("#glasses")
          .append("svg")
          .attr('id', 'svg')
          .attr("width", svgWidth)
          .attr("height", svgHeight)
          .attr('viewBox', '0 -5 110 110')
        var chosenRecipe = this.__data__.name
        console.log(this)
        drawGlass(endpoint, chosenRecipe)
        document.getElementById('glasses').scrollIntoView()      
      })
		var sortAscending = true
		header.on('click',function(d, i) {
			var sort_value = d3.select(this).attr('value')
			var numeric = headers.slice(1, 8)
			console.log(headers)
			console.log(numeric)
			if (sortAscending === true) {
				if (numeric.includes(sort_value)) {
					content.sort((a,b) => d3.ascending(parseFloat(a[sort_value]), parseFloat(b[sort_value])))
				}
				else {
					content.sort((a,b) => d3.ascending(a[sort_value].toLowerCase().replace(/\s/g, ''), b[sort_value].toLowerCase().replace(/\s/g, '')))
				}
				sortAscending = false
				d3.select(this).attr('class', 'asc')
			} else {
				if (numeric.includes(sort_value)) {
					content.sort((a,b) => d3.descending(parseFloat(a[sort_value]), parseFloat(b[sort_value])))
				}
				else {
					content.sort((a,b) => d3.descending(a[sort_value].toLowerCase().replace(/\s/g, ''), b[sort_value].toLowerCase().replace(/\s/g, '')))
				}
				sortAscending = true
				d3.select(this).attr('class', 'desc')
			}
		})
	})
}
var chosenIngred = 'rum'
var paramType = 'ingredient'
drawTable(endpoint, chosenIngred, paramType)
