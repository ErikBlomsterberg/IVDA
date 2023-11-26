<template>
  <v-container width="200%">
   <v-row class="bg-grey-lighten-2">
     <v-col cols="8">
       <v-sheet class="pa-2 ma-2" height="720px" id="mapContainer"  @click:map="update_map"></v-sheet>
     </v-col>
     <v-col cols="4">
       <v-row no-gutters>
         <v-col cols="12">
           <v-sheet class="pa-2 ma-2" height="233px" id="histContainer1"></v-sheet>
         </v-col>
       </v-row>
       <v-row no-gutters >
         <v-col cols="12">
           <v-sheet class="pa-2 ma-2" height="233px" id="histContainer2"></v-sheet>
         </v-col>
       </v-row>
       <v-row no-gutters >
         <v-col cols="12">
           <v-sheet class="pa-2 ma-2" height="233px" id="histContainer3"></v-sheet>
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

  import Plotly from 'plotly.js-dist';

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
      msg: String,
      availability: String,
      roomType: String,
      neighbourhoodGroup: String
    },
    data: () => ({
        loading: false,
        elevations: [0, 4, 8, 12, 16, 20],
        predictedData: [],
        number_of_reviews: [],
        minimum_nights: [],
        price: [],
        availabilitys: '',
        roomTypes: '',
        neighbourhoodGroups: ''
      }),
  watch: {
    availability(newMyProp) {
      this.availabilitys = newMyProp
      this.fetchData()
    },
    roomType(newMyProp) {
      this.roomTypes = newMyProp
      this.fetchData()
    },
    neighbourhoodGroup(newMyProp) {
      this.neighbourhoodGroups = newMyProp
      this.fetchData()
    },
  },
  
    mounted() {
      console.log("Fetching data")
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


      //var apt_list = [[47.37,8.55],[47.37374,8.51],[47.3738,8.81],[47.37171,8.41],[47.37324,8.23]];
      //var price_list = [1200,900,200,300,500]
      //var rank_list = [0,3,6,9,30]
      //var titles = ["Cozy apartment in zurich","Shitty apartment","Apt3","Apt4","Apt5"]

      
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
            this.predictedData.push(apartment);
            this.number_of_reviews.push(apartment["number_of_reviews"]);
            this.minimum_nights.push(apartment["minimum_nights"]);
            this.price.push(apartment["price"]);
            // if ():
            
      })
      if( this.neighbourhoodGroups.length > 0){
      this.predictedData = this.predictedData.filter(item => item["neighbourhood_group"] === this.neighbourhoodGroups);
      }
      if( this.roomType.length > 0){
      this.predictedData = this.predictedData.filter(item => item["room_type"] === this.neighbourhoodGroups);
      }
      if( this.availability.length > 0){
      this.predictedData = this.predictedData.filter(item => item["availability_365"] <= this.neighbourhoodGroups);
      }
      this.predictedData.forEach((apartment) => {
      this.number_of_reviews.push(apartment["number_of_reviews"]);
            this.minimum_nights.push(apartment["minimum_nights"]);
            this.price.push(apartment["price"]);
      })
        this.update_map();
        this.drawHistogramPlot("histContainer1",this.price);
        this.drawHistogramPlot("histContainer2",this.minimum_nights);
        this.drawHistogramPlot("histContainer3",this.number_of_reviews);
      },
      filterData(){
        this.predictedData = this.predictedData.filter(item => item["neighbourhood_group"] === this.neighbourhoodGroups);
          console.log("test")
          console.log(this.predictedData)
        this.update_map();
        this.drawHistogramPlot("histContainer1",this.price);
        this.drawHistogramPlot("histContainer2",this.minimum_nights);
        this.drawHistogramPlot("histContainer3",this.number_of_reviews);
      },

      update_map() {

        //console.log(props)
        var max_rank = Math.min(this.predictedData.length,100);
      
      
        var i;


        console.log("Predicted data:")
        console.log(this.predictedData)
        console.log(this.predictedData.length)


        for(i=0;i<max_rank;i++)
        {
          var price = this.predictedData[i]["price"]
          var latitude = this.predictedData[i]["latitude"]
          var longitude = this.predictedData[i]["longitude"]
          var title = this.predictedData[i]["name"]
          var rank = i

          console.log(this.predictedData[i]["rating"])
          var marker = L.marker([latitude,longitude],{title :`${price} CHF`}).addTo(this.map);
          marker.bindPopup(`<b> ${title} </b><br>Price: <b>${price} CHF</b><br>Rank: <b>${rank}</b>`);
        
          var hue_rotate_val = 250-100*(rank/max_rank);
          marker._icon.style.filter = `hue-rotate(${hue_rotate_val}deg)`
        }

      },

      drawHistogramPlot(id,hist_data) {
        var trace1 = {
          x: hist_data,
          type: 'histogram',
          //text: this.ScatterPlotData.name,

        };
        var data = [trace1];
        var layout = {}
        var config = {responsive: true}
        Plotly.newPlot(id, data, layout, config);
        //this.clickScatterPlot()
      },
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