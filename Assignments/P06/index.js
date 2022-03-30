//-----------------------------------------------------------------------------------------------------------------------------------------------------
//                                                              On load
//-----------------------------------------------------------------------------------------------------------------------------------------------------
window.onload = function () {
    loadCountryNames();
};

let correct = null

reds = ['#FF2D00', '#FF3F17', '#FF502D', '#FF6244', '#FF745B', '#FF8571', '#FF9788', '#FFA99F', '#FFBAB5', '#FFCCCC']

var guesses = []

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// █████╗ ██████╗ ██╗     ██████╗ █████╗ ██╗     ██╗         ███████╗██╗   ██╗███╗   ██╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗  //
// ██╔══██╗██╔══██╗██║    ██╔════╝██╔══██╗██║     ██║         ██╔════╝██║   ██║████╗  ██║██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝ //
// ███████║██████╔╝██║    ██║     ███████║██║     ██║         █████╗  ██║   ██║██╔██╗ ██║██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗ //
// ██╔══██║██╔═══╝ ██║    ██║     ██╔══██║██║     ██║         ██╔══╝  ██║   ██║██║╚██╗██║██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║ //
// ██║  ██║██║     ██║    ╚██████╗██║  ██║███████╗███████╗    ██║     ╚██████╔╝██║ ╚████║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║ //
// ╚═╝  ╚═╝╚═╝     ╚═╝     ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ //
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                                                                                                                                     
function loadCountryNames() {
    let url = "http://127.0.0.1:8080/CountryList/";
    fetch(url)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            var select = document.getElementById("country");

            names = data['countries'].sort();

            select.innerHTML = "";

            for (var i = 0; i < names.length; i++) {
                var opt = data['countries'][i];
                var el = document.createElement("option");
                el.textContent = opt;
                el.value = opt;
                select.appendChild(el);
            }

            correct = names[Math.floor(Math.random() * names.length)]
        });
}

function showCountry() {
    var e = document.getElementById("country");
    var name = e.options[e.selectedIndex].text;
    var color = null
    

    if(name == correct)
    {
        color = '#00FF00'
        document.getElementById("country").disabled = true;
        document.getElementById("submit").disabled = true;
        guesses.push([name, 0])
        
    }
    else
    {
        fetch('http://127.0.0.1:8080/FindDistance/{FirstCountry},{SecondCountry}?FirstPoly=' + name + '&SecondPoly=' + correct)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) 
        {
            dis = Math.floor(data['distance'] /1000)
            console.log(data)
            console.log(dis)

            if(dis < 5)
            {
                if(dis < 1)
                {
                    dis = 1   
                }
                color = reds[0]
            }
            else if(dis < 10)
            {
                color = reds[1]
            }
            else if(dis < 20)
            {
                color = reds[2]
            }
            else if(dis < 40)
            {
                color = reds[3]
            }
            else if(dis < 60)
            {
                color = reds[4]
            }
            else if(dis < 80)
            {
                color = reds[5]
            }
            else if(dis < 100)
            {
                color = reds[6]
            }
            else if(dis < 140)
            {
                color = reds[7]
            }
            else if(dis < 180)
            {
                color = reds[8]
            }
            else
            {
                color = reds[9]
            }

            guesses.push([name, dis])
        });

        fetch('http://127.0.0.1:8080/FindDirection/{Country1},{Country2}?CountryNo1=' + correct + '&CountryNo2=' + name)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            let text = null

            if(data['CountryDirection'] == 'NorthWest')
            {
                text = '↖️'
            }
            else if(data['CountryDirection'] == 'SouthWest')
            {
                text = '↙️'
            }
            else if(data['CountryDirection'] == 'SouthEast')
            {
                text = '↘️'
            }
            else if(data['CountryDirection'] == 'NorthEast')
            {
                text = '↗️'
            }
            else if(data['CountryDirection'] == 'North')   
            {
                text = '⬆️'
            }
            else if(data['CountryDirection'] == 'South')
            {
                text = '⬇️'
            }
            else if(data['CountryDirection'] == 'East')
            {
                text = '➡️'
            }
            else
            {
                text = '⬅️'
            }

            document.getElementById("dir").textContent = text;
        });
    }

    let url = "http://127.0.0.1:8080/FindPolyGon/" + name;

    fetch(url)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log(data)
            result = {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": data                        }
                    }
                ]
            };
            console.log(result)
            let defaultStyle = {
                fillColor: color,
                weight: 2,
                opacity: 1,
                color: 'black',
                fillOpacity: 1
            }

            L.geoJSON(result, {style: defaultStyle}).addTo(layers);
            
            guesses.sort(([a, b], [c, d]) => b - d);

            document.getElementById("guesses").innerHTML = "";

            for(i = 0; i < guesses.length; i++)
            {
                var select = document.getElementById("guesses");
                var el = document.createElement("li");
                el.textContent = guesses[i][0];
                el.value = guesses[i][0];
                select.appendChild(el);
            }
            
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

//-----------------------------------------------------------------------------------------------------------------------------------------------------
//                                                              Code
//-----------------------------------------------------------------------------------------------------------------------------------------------------
let bound = [[[90, 180], [-90, -180]]]

let map = L.map("map", {maxBounds: bound, maxBoundsViscosity: 1.0}).setView([0, 0], 0);

map.setMinZoom(3)
map.setMaxZoom(8)

L.tileLayer(
    "https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_nolabels/{z}/{x}/{y}.png",
    {
        attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attribution/">CartoDB</a>',
        subdomains: "abcd",
        maxZoom: 19,
    }
).addTo(map);

// Add Layer Group
let layers = L.layerGroup().addTo(map);

document.getElementById("submit").addEventListener("click", showCountry);