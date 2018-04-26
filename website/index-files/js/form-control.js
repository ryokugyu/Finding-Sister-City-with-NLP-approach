var items = "climate culture demographics economy politics proximity".split(" ")
var sliders = items.map( item => {return document.getElementById(item + "-slider")} )
var outputs = items.map( item => {return document.getElementById(item + "-value")} )
var submit_button = document.getElementById("submit-button")
var city_input = document.getElementById("city-input")


// Autocomplete function for the input search bar
$( function() {
    city_names = ['Chicago', 'New York', 'Los Angeles', "San Francisco"]
    var limit = 5
    $( "#city-input" ).autocomplete({
        // source: city_names
        source: function(request, response) {
            var results = $.ui.autocomplete.filter(city_names, request.term)
            response(results.slice(0, limit))
        }
    })
})

// Function to initialize the sliders
init_slider = function (slider, output) {
    slider.oninput = function() {
        output.innerHTML = slider.value
        // console.log( slider.value )
        // console.log( output.innerHTML)
    }
}

// Initialize the sliders
for (var i = 0; i < items.length; i++) {
    init_slider( sliders[i], outputs[i] );
}

// Get and submit values on button click
submit_button.onclick = function() {
    submit_vals = [ city_input.value, sliders.map( slider => {return (slider.value - 50) / 50.0} ) ]
    console.log( submit_vals )
}
