## property-prices
Code for property price mapping using leaflet and python
(Data sources not committed to GitHub)

## Using TopoJSON
Geo-JSON file from realestate-analysis.py will need to be converted to TopoJSON format to reduce size and provide useable load times

Install via NPM:
npm install -g topojson

Run following code to quantize and simplify Geo-JSON file
geo2topo < input > output
topoquantize 1e5 < input > output
toposimplify -p 5e-8 (or 1e-8) < input > output

Rename output to data.js for use with HTML Leaflet script
