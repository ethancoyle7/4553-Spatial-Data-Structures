//////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                              //
//                               Authors: Ethan Coyle and Buddy Smith                           //
//                               Class- Spatial Data Structures                                 //
//                               Date: 10/31/2019                                               //
//                               Instructor: Dr. Griffin                                        //
//                               Assignment: P06 Create Worldle Like Game                       //
//////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                              //
// The purpose of this assignement is creating a web base javascript application that will      //
// allow the user to play a guessing game. The user will be able to select a country from a     //
// dropdown list and the application will then randomly select a country from the list and      //
// after selecting a country from the drop down list, the polygon for that country will be      //
// displayed on the map for the user to see and they will be PolyGonColor coded based on the    //
// distance if the user guesses the correct country, then the polygon will be colored green.    //
// After the correct country is guessed, then the user will be able to reload the local host    //
// and play again.                                                                              //
//////////////////////////////////////////////////////////////////////////////////////////////////

//first we need to initilize what happens on the windows load page event
window.onload = function () 
{
    loadCountryList();//go to the function ccalled loadCountryList
};
//initialize the api call to get the list of countrys for the dropdown list and then set the initial states to null
let CountryToGuess = null // country list not initialized yet until the list is loaded
var guesses = []// create empty list for the guesses

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// █████╗ ██████╗ ██╗     ██████╗ █████╗ ██╗     ██╗         ███████╗██╗   ██╗███╗   ██╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗  //
// ██╔══██╗██╔══██╗██║    ██╔════╝██╔══██╗██║     ██║         ██╔════╝██║   ██║████╗  ██║██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝ //
// ███████║██████╔╝██║    ██║     ███████║██║     ██║         █████╗  ██║   ██║██╔██╗ ██║██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗ //
// ██╔══██║██╔═══╝ ██║    ██║     ██╔══██║██║     ██║         ██╔══╝  ██║   ██║██║╚██╗██║██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║ //
// ██║  ██║██║     ██║    ╚██████╗██║  ██║███████╗███████╗    ██║     ╚██████╔╝██║ ╚████║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║ //
// ╚═╝  ╚═╝╚═╝     ╚═╝     ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ //
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
             

///////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                               //
// ██████╗ ██████╗ ██╗   ██╗███╗   ██╗████████╗██████╗ ██╗   ██╗    ██╗     ██╗███████╗████████╗ //
// ██╔════╝██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝██╔══██╗╚██╗ ██╔╝    ██║     ██║██╔════╝╚══██╔══╝//
// ██║     ██║   ██║██║   ██║██╔██╗ ██║   ██║   ██████╔╝ ╚████╔╝     ██║     ██║███████╗   ██║   //
// ██║     ██║   ██║██║   ██║██║╚██╗██║   ██║   ██╔══██╗  ╚██╔╝      ██║     ██║╚════██║   ██║   //
// ╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║   ██║   ██║  ██║   ██║       ███████╗██║███████║   ██║   //
//  ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝       ╚══════╝╚═╝╚══════╝   ╚═╝   //
//                                                                                               //
///////////////////////////////////////////////////////////////////////////////////////////////////
                                                                                              
function loadCountryList() 
{
    //initialize the api call to get the list of countrys for the dropdown list
    let url = "http://127.0.0.1:8080/CountryList/";
    fetch(url)
        .then(function (response) 
        {
            return response.json();// with the response back from the server, return the json data
        })
        .then(function (data) 
        {
            var CountryNameList = document.getElementById("country");//each element is gained from the html page

            names = data['countries'].sort();// sort the data by the country name

            CountryNameList.innerHTML = "";// these options will populate the dropdown list

            for (var i = 0; i < names.length; i++) //for loop to loop through the names array
            {
                var Option = data['countries'][i];
                var DropDownElement = document.createElement("option");
                DropDownElement.textContent = Option;
                DropDownElement.value = Option;
                CountryNameList.appendChild(DropDownElement);// append all the eleemnts to the dropdown list
            }

            CountryToGuess = names[Math.floor(Math.random() * names.length)] // CountryNameList a random country for the user to guess
        });
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ██████╗ ██╗███████╗██████╗ ██╗      █████╗ ██╗   ██╗     ██████╗ ██████╗ ██╗   ██╗███╗   ██╗████████╗██████╗ ██╗   ██╗ //
// ██╔══██╗██║██╔════╝██╔══██╗██║     ██╔══██╗╚██╗ ██╔╝    ██╔════╝██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝██╔══██╗╚██╗ ██╔╝ //
// ██║  ██║██║███████╗██████╔╝██║     ███████║ ╚████╔╝     ██║     ██║   ██║██║   ██║██╔██╗ ██║   ██║   ██████╔╝ ╚████╔╝  //
// ██║  ██║██║╚════██║██╔═══╝ ██║     ██╔══██║  ╚██╔╝      ██║     ██║   ██║██║   ██║██║╚██╗██║   ██║   ██╔══██╗  ╚██╔╝   //
// ██████╔╝██║███████║██║     ███████╗██║  ██║   ██║       ╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║   ██║   ██║  ██║   ██║    //
// ╚═════╝ ╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝        ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝    //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                                                                                                                      
function DisplayPoly() // now to actually display the country from the guesses
{
    var e = document.getElementById("country");
    var name = e.options[e.selectedIndex].text;
    var PolyGonColor = null
    

    if(name == CountryToGuess)// if the correct country is guessed,change the PolyGonColor of the country to green
    {
        PolyGonColor = '#00FF00'//default PolyGonColor
        document.getElementById("country").disabled = true;//disable the dropdown list so the user can't guess again
        document.getElementById("submit").disabled = true; //disable the submit button so the user can't guess again
        guesses.push([name, 0])
        
    }
    else
    {
        //get the api call for the distance between the two countries
        fetch('http://127.0.0.1:8080/FindDistance/{FirstCountry},{SecondCountry}?FirstPoly=' + name + '&SecondPoly=' + CountryToGuess)
        .then(function (response) 
        {
            return response.json();//grab the url response
        })
        .then(function (data) 
        {
            CountryDistance = Math.floor(data['distance'] /1000)
            console.log(data)
            console.log(CountryDistance)

            if(CountryDistance < 5)
            {
                if(CountryDistance < 1)
                {
                    CountryDistance = 1   
                }
                PolyGonColor = "#66FFFF"
            }
            else if(CountryDistance < 10)
            {
                PolyGonColor = "CCFFCC"// getting even lighter green
            }
            else if(CountryDistance < 20)
            {
                PolyGonColor = "#FFFF66"// getting even lighter yellow
            }
            else if(CountryDistance < 40)
            {
                PolyGonColor = "#0000FF"// getting even lighter blue
            }
            else if(CountryDistance < 60)
            {
                PolyGonColor = "#FF00FF"// getting even lighter purple
            }
            else if(CountryDistance < 80)
            {
                PolyGonColor = "#FF0000"// getting even lighter red
            }
            else if(CountryDistance < 100)
            {
                PolyGonColor = "#6600CC" // displaying purple
            }
            else if(CountryDistance < 140)
            {
                PolyGonColor = "FF8000"// displaying oragne
            }
            else 
            {
                PolyGonColor = "#FF0000"// red is the farthst away
            }
            

            guesses.push([name, CountryDistance])
        });

        ////////////////////////////////////////////////////////////////////////
        // ██████╗ ██╗██████╗ ███████╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗ //
        // ██╔══██╗██║██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║ //
        // ██║  ██║██║██████╔╝█████╗  ██║        ██║   ██║██║   ██║██╔██╗ ██║ //
        // ██║  ██║██║██╔══██╗██╔══╝  ██║        ██║   ██║██║   ██║██║╚██╗██║ //
        // ██████╔╝██║██║  ██║███████╗╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║ //
        // ╚═════╝ ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ //
        ////////////////////////////////////////////////////////////////////////
                                                                          
        //read the api call and get the distance between the two countries based on the url
        fetch('http://127.0.0.1:8080/FindDirection/{Country1},{Country2}?CountryNo1=' + CountryToGuess + '&CountryNo2=' + name)
        .then(function (response) 
        {
            return response.json();//get the json response
        })
        .then(function (data) // with the data returned process it
        {
            let text = null// at the end of the function, this will be the text that will be displayed

            // after finding the distance we need to use our compass
            // which will be the direction from the first country to the second
            
            if(data['CountryDirection'] == 'North')// northern direction
            {
                text = '⬆️'// display the north arrow
            }
            else if(data['CountryDirection'] == 'South')// south direction
            {
                text = '⬇️'// display the south arrow
            }
            else if(data['CountryDirection'] == 'East')//eastern direction
            {
                text = '➡️'// display the east arrow
            }
            else if(data['CountryDirection'] == 'West')// western direction
            {
                text = '⬅️'// display the west arrow
            }
            if(data['CountryDirection'] == 'NorthWest')//northwestern direction
            {
                text = '↖️'// display the north west arrow
            }
            else if(data['CountryDirection'] == 'SouthWest')// to the southwest
            {
                text = '↙️'// display the south west arrow
            }
            else if(data['CountryDirection'] == 'SouthEast')// or the southeeast direction
            {
                text = '↘️'//    display the south east arrow
            }
            else // if none of these are true, then will be in the northeast direction
            {
                text = '↗️' // northeastern direction
            }
            

            document.getElementById("dir").textContent = text;// diaplying the actual direction icon in the html
        });
    }
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // ██████╗ ██╗███████╗██████╗ ██╗      █████╗ ██╗   ██╗     ██████╗ ██████╗ ██╗   ██╗███╗   ██╗████████╗██████╗ ██╗   ██╗ //
    // ██╔══██╗██║██╔════╝██╔══██╗██║     ██╔══██╗╚██╗ ██╔╝    ██╔════╝██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝██╔══██╗╚██╗ ██╔╝ //
    // ██║  ██║██║███████╗██████╔╝██║     ███████║ ╚████╔╝     ██║     ██║   ██║██║   ██║██╔██╗ ██║   ██║   ██████╔╝ ╚████╔╝  //
    // ██║  ██║██║╚════██║██╔═══╝ ██║     ██╔══██║  ╚██╔╝      ██║     ██║   ██║██║   ██║██║╚██╗██║   ██║   ██╔══██╗  ╚██╔╝   //
    // ██████╔╝██║███████║██║     ███████╗██║  ██║   ██║       ╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║   ██║   ██║  ██║   ██║    //
    // ╚═════╝ ╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝        ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝    //
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                                                                                                                          
    let url = "http://127.0.0.1:8080/Geojson/" + name; // get the url of the geojson api call to get the country choice polygon

    fetch(url)
        .then(function (response) 
        {
            return response.json();//wait for the response to return
        })
        .then(function (data) // with the data returned process it
        {
            console.log(data)// see the data returned is correct
            result = data // the result is the geojson of the country choice
            console.log(result) // see if what the api call returns is correct
            let defaultStyle = 
            {
                fillColor: PolyGonColor,
                weight: 2,
                opacity: 1,
                PolyGonColor: 'black',
                fillOpacity: 1
            }

            //add this to the layers of the map inside of the loccal host
            L.geoJSON(result, {style: defaultStyle}).addTo(layers);
            //sorting the list in the order of closest to furthest
            guesses.sort(([a, b], [c, d]) => b - d);
            //these will be displayed inside of the inner html over to the right of the map
            document.getElementById("guesses").innerHTML = "";

            for(i = 0; i < guesses.length; i++)
            {
                var CountryNameList = document.getElementById("guesses");
                var DropDownElement = document.createElement("li");
                DropDownElement.textContent = guesses[i][0];
                DropDownElement.value = guesses[i][0];
                CountryNameList.appendChild(DropDownElement);
            }
            //the following will be displayed in the inner html over to the left of the map
            //and once the country is selected the options will be removed
            selectbox = document.getElementById("country")
            var i;
            for(i=0; i < selectbox.options.length; i++)
            {
                if(selectbox.options[i].selected)
                {
                    selectbox.remove(i);
                }
            }
        });
}
/////////////////////////////////////////////////////////////////////////////////////
// ███╗   ███╗ █████╗ ██╗███╗   ██╗    ██████╗ ██████╗ ██╗██╗   ██╗███████╗██████╗ //    
// ████╗ ████║██╔══██╗██║████╗  ██║    ██╔══██╗██╔══██╗██║██║   ██║██╔════╝██╔══██╗//    
// ██╔████╔██║███████║██║██╔██╗ ██║    ██║  ██║██████╔╝██║██║   ██║█████╗  ██████╔╝//    
// ██║╚██╔╝██║██╔══██║██║██║╚██╗██║    ██║  ██║██╔══██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗//    
// ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║    ██████╔╝██║  ██║██║ ╚████╔╝ ███████╗██║  ██║//    
// ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝//
/////////////////////////////////////////////////////////////////////////////////////    
                                                                                    
let bound = [[[90, 180], [-90, -180]]] // get the bounding box of the map
// let the map fall within the bounds of the box iteself
let map = L.map("map", {maxBounds: bound, maxBoundsViscosity: 1.0}).setView([0, 0], 0);
//initialize the level of zoom inside of the map
map.setMinZoom(3)
map.setMaxZoom(8)
// we need to add a tile layer to our map so that something actually shows up
L.tileLayer(
    "https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_nolabels/{z}/{x}/{y}.png",
    {
        attribution:// this is the attribution of the map using the openstreetmap and cartodb without labels
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attribution/">CartoDB</a>',
        subdomains: "abcd", // get the subdomains of the tile layer
        maxZoom: 19,
    }
).addTo(map);
//on the submit button for the guesses, we need to add event listener to the button
//when the button is clicked, we need to get the value of the country and the PolyGonColor
//and then we need to call the function to get the polygon
let layers = L.layerGroup().addTo(map);
document.getElementById("submit").addEventListener("click", DisplayPoly);