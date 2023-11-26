<template>
  <v-container width="200%">
   <v-row class="bg-grey-lighten-2">
     <v-col cols="8">
       <v-sheet class="pa-2 ma-2" height="720px" id="mapContainer"> Level 1: .v-col-8 </v-sheet>
     </v-col>
     <v-col cols="4">
       <v-row no-gutters>
         <v-col cols="12">
           <v-sheet class="pa-2 ma-2" height="233px"> Level 1: .v-col-12 </v-sheet>
         </v-col>
       </v-row>
       <v-row no-gutters >
         <v-col cols="12">
           <v-sheet class="pa-2 ma-2" height="233px"> Level 2: .v-col-12 </v-sheet>
         </v-col>
       </v-row>
       <v-row no-gutters >
         <v-col cols="12">
           <v-sheet class="pa-2 ma-2" height="233px"> Level 3: .v-col-12 </v-sheet>
         </v-col>
       </v-row>
     </v-col>
   </v-row>
 </v-container>
 </template>
 
 <script>
   // Import Leaflet for map visualization
   import "leaflet/dist/leaflet.css";
   import L from 'leaflet';

   import Plotly from 'plotly.js/dist/plotly';

   //import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet"

   //Vue.component('l-map', LMap);
   //Vue.component('l-tile-layer', LTileLayer);
   //Vue.component('l-marker', LMarker);
   delete L.Icon.Default.prototype._getIconUrl;

   L.Icon.Default.mergeOptions({
     iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
     iconUrl: require('leaflet/dist/images/marker-icon.png'),
     shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
   });
 
   export default {
   name: 'DataVisualization',
   props: {
     msg: String
   },
   data: () => ({
       loading: false,
       elevations: [0, 4, 8, 12, 16, 20],
       predictedData: [],

     }),
 
   mounted() {
     this.fetchData()

     this.map = L.map("mapContainer").setView([47.37, 8.55], 12);

     L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
       attribution:
         '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
     }).addTo(this.map);
     //use a mix of renderers
     var customPane = this.map.createPane("customPane");
     //var canvasRenderer = L.canvas({ pane: "customPane" });
     customPane.style.zIndex = 399; // put just behind the standard overlay pane which is at 400

     // Dummy data values, change once dataloading is done

     var apt_list = [[47.37,8.55],[47.37374,8.51],[47.3738,8.81],[47.37171,8.41],[47.37324,8.23]];
     var price_list = [1200,900,200,300,500]
     var rank_list = [0,3,6,9,30]
     var titles = ["Cozy apartment in zurich","Shitty apartment","Apt3","Apt4","Apt5"]
     var max_rank = Math.max(...rank_list)
     
     
     var i;
     for(i=0;i<apt_list.length;i++)
     {
       var marker = L.marker(apt_list[i],{title :`${price_list[i]} CHF`}).addTo(this.map);
       marker.bindPopup(`<b> ${titles[i]} </b><br>Price: <b>${price_list[i]} CHF</b><br>Rank: <b>${rank_list[i]}</b>`);
     
       var hue_rotate_val = 250-100*(rank_list[i]/max_rank);
       marker._icon.style.filter = `hue-rotate(${hue_rotate_val}deg)`
     }

     this.map.on('moveend', () => {
       const bounds = this.map.getBounds().toBBoxString();
       /* now send your bounds to the server, requesting only the visible markers */
       console.log(bounds)
     })
     },
    methods: {
      async fetchData() {
        const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      };
        const response =  await fetch("http://127.0.0.1:5000/model-predict", requestOptions)
        const responseData =  await response.json();
        responseData.forEach((apartment) => {
            this.predictedData.push(apartment)
      })
      console.log(this.predictedData)
      }
    }
    }
  
  }
 
 </script>

 <!-- Add "scoped" attribute to limit CSS to this component only -->
 <style scoped>
 h3 {
   margin: 40px 0 0;
 }
 ul {
   list-style-type: none;
   padding: 0;
 }
 li {
   display: inline-block;
   margin: 0 10px;
 }
 a {
   color: #42b983;
 }
 </style>