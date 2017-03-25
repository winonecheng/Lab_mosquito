var mymap = L.map('mapid').setView([23, 120.23	], 13);
baseMaps = L.tileLayer('https://api.tiles.mapbox.com/v1/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'jonne260',
    accessToken: 'pk.eyJ1Ijoiam9ubmUyNjAiLCJhIjoiY2owbmFncmdwMDAwMzJxbnZxMm85eDdtYSJ9.WsKUG0wpHZHUJ0oAWJOqLg'
}).addTo(mymap);

heatmap_points1 = addressPoints[1].map(function (p) { return [p[2], p[1]]; });
heatmap_points2 = addressPoints[2].map(function (p) { return [p[1], p[0]]; });
var heat ={
	"1":L.heatLayer(heatmap_points1,{minOpacity:0.6, radius:20, blur:20}),
	"2":L.heatLayer(heatmap_points2,{minOpacity:0.6, radius:20, blur:20})
};
var disease ={
	"1":"登革熱",
	"2":"流感",
	"3":"腸病毒"
};

console.log(addressPoints[2]);
var now_disease = 1;
heat[now_disease].addTo(mymap);
update_other();
update_number(now_disease);
update_area(now_disease);

function switcher() {
    var x = document.getElementById("switcher");
    if (x.className.indexOf("w3-show") == -1) 
        x.className += " w3-show";
    else 
        x.className = x.className.replace(" w3-show", "");
}

function redraw_heatmap(n){
	heat[now_disease].remove();
	heat[n].addTo(mymap);
	now_disease = n;
}

function change_disease(n){
	var x = document.getElementById("switcher_name");
	x.innerHTML = disease[n];
	switcher();
	redraw_heatmap(n);
	update_number(n);
	update_area(n);
}

function update_number(n){
	var x = document.getElementById("number_header");
	x.innerHTML = "<p>累計"+disease[n]+"人數</p>";
	var y = document.getElementById("biggertext");
	y.innerHTML = addressPoints[n].length
}

function update_other(){
	var x = document.getElementById("other");
	for(var i = 1; i <= Object.keys(disease).length; i++){
		var p = document.createElement("p");
		p.style.textAlign = "center";
		p.style.margin = "15px auto";
		var t = document.createTextNode(disease[i]+" "+addressPoints[i].length+"人");
		p.appendChild(t);
		x.appendChild(p);
	}
}

function update_area(n){
	var counts = {};
	var x = document.getElementById("area");
	while (x.firstChild) {
		x.removeChild(x.firstChild);
	}

	var arr = addressPoints[n].map(function(p){ return p[0]; });
	arr.forEach(function(x){ counts[x] = (counts[x]||0)+1; });
	keysSorted = Object.keys(counts).sort(function(a,b){return counts[b]-counts[a];})
	for(var i = 0; i < 3; i++){
		var p = document.createElement("p");
		p.style.textAlign = "center";
		p.style.margin = "10px auto";		
		var t = document.createTextNode(keysSorted[i]+" "+counts[keysSorted[i]]+"人");
		p.appendChild(t);
		x.appendChild(p);

	}		
}