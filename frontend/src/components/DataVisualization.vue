<template>
  <v-app>
  <v-container width="200%">
   <v-row class="bg-grey-lighten-2">
     <v-col cols="8">
       <v-sheet class="pa-2 ma-2" height="720px" id="mapContainer"  @click:map="update_map"></v-sheet>
     </v-col>
     <v-col cols="4">
       <v-row no-gutters>
         <v-col cols="12">
          <v-card class="pa-2 ma-2" height="180px" id="histContainer1"> Price </v-card>
          <v-range-slider 
            id="price_slider" 
            color="green" 
            v-model="price_minmax" 
            thumb-label
            :max=max_price
            :min=0
            @update:modelValue="update_data">
          </v-range-slider>
         </v-col>
       </v-row>
       <v-row no-gutters >
         <v-col cols="12">
           <v-card class="pa-2 ma-2" height="180px" id="histContainer2"> No of reviews
           </v-card>
           
           <v-range-slider 
            id="review_slider" 
            color="blue" 
            v-model="review_minmax" 
            thumb-label
            :max=max_reviews
            :min=0
            @update:modelValue="update_data"
            >
          </v-range-slider>
         </v-col>
       </v-row>
       <v-row no-gutters >
         <v-col cols="12">
           <v-card class="pa-2 ma-2" height="180px" id="histContainer3"> Min no of days </v-card>
           <v-range-slider 
            id="minnights_slider" 
            color="orange"
            v-model="minnights_minmax" 
            thumb-label
            :max=max_minnights
            :min=0
            @update:modelValue="update_data">
          </v-range-slider>
         </v-col>
       </v-row>
     </v-col>
   </v-row>
  </v-container>
  </v-app>
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
        filteredData: [],
        number_of_reviews: [],
        minimum_nights: [],
        price: [],
        max_price: 0,
        max_minnights: 0,
        max_reviews: 0,
        price_minmax: [0,100],
        review_minmax: [0,100],
        minnights_minmax: [0,100],
        availabilitys: '',
        roomTypes: '',
        neighbourhoodGroups: '',


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
      this.layerGroup = L.layerGroup().addTo(this.map);
      L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
        attribution:
          '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(this.map);
      //use a mix of renderers
      var customPane = this.map.createPane("customPane");
      //var canvasRenderer = L.canvas({ pane: "customPane" });
      customPane.style.zIndex = 399; // put just behind the standard overlay pane which is at 400
      
      //this.map.on('moveend', () => {
        //const bounds = this.map.getBounds().toBBoxString();
        /* now send your bounds to the server, requesting only the visible markers */
        //console.log(bounds)
      //})
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

            if(apartment["number_of_reviews"] > this.max_reviews)
              this.max_reviews = apartment["number_of_reviews"];
            if(apartment["price"] > this.max_price)
              this.max_price= apartment["price"];
            if(apartment["minimum_nights"] > this.max_minnights)
              this.max_minnights = apartment["minimum_nights"];

            this.number_of_reviews.push(apartment["number_of_reviews"]);
            this.minimum_nights.push(apartment["minimum_nights"]);
            this.price.push(apartment["price"]);
            
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

        //sort based on rating
        this.predictedData.sort(function(a,b) {
          return b.rating - a.rating
        });

        this.predictedData = this.predictedData.slice(0,100)


      
        this.filteredData = this.predictedData.slice()

        //console.log(this.filteredData)

        this.price_minmax[1] = this.max_price;
        this.minnights_minmax[1] = this.max_minnights;
        this.review_minmax[1] = this.max_reviews;



        //console.log(this.predictedData.length)
        this.update_map();
        this.update_data();
      },

      reset_filters()
      {
        this.filteredData = this.predictedData.slice()
      },

      update_data()
      {
        this.reset_filters();
        //console.log("Before-after")
        //console.log(this.filteredData.length)
        for(var i=this.predictedData.length-1;i>=0;i--)
        {
          //myArray.splice(index, 1);
          if(this.predictedData[i]["price"] <= this.price_minmax[0] || this.predictedData[i]["price"] >= this.price_minmax[1])
          {
            this.filteredData.splice(i,1)
          }
          if(this.predictedData[i]["number_of_reviews"] <= this.review_minmax[0] || this.predictedData[i]["number_of_reviews"] >= this.review_minmax[1])
          {
            this.filteredData.splice(i,1)
          }
          if(this.predictedData[i]["minimum_nights"] <= this.minnights_minmax[0] || this.predictedData[i]["minimum_nights"] >= this.minnights_minmax[1])
          {
            this.filteredData.splice(i,1)
          }
        }
        //console.log(this.filteredData.length)
        this.update_map();
        this.drawHistogramPlot("histContainer1",this.price, "green", this.price_minmax);
        this.drawHistogramPlot("histContainer2",this.number_of_reviews, "blue", this.review_minmax);
        this.drawHistogramPlot("histContainer3",this.minimum_nights, "orange", this.minnights_minmax);
      },

      update_map() {

        //console.log(props)
        var max_rank = this.filteredData.length
        
      
        var i;

        
        //console.log("Predicted data:")
        //console.log(this.predictedData)
        //console.log(this.predictedData.length)

        
        this.layerGroup.clearLayers()
        for(i=0;i<max_rank;i++)
        {
          var price = this.filteredData[i]["price"]
          var latitude = this.filteredData[i]["latitude"]
          var longitude = this.filteredData[i]["longitude"]
          var title = this.filteredData[i]["name"]
          var rank = i

          //console.log(this.filteredData[i]["rating"])
          var marker = L.marker([latitude,longitude],{title :`${price} CHF`}).addTo(this.layerGroup);
          //this.markers.push(marker)
          marker.bindPopup(`<b> ${title} </b><br>Price: <b>${price} CHF</b><br>Rank: <b>${rank}</b>`);
        
          var hue_rotate_val = 250-100*(rank/max_rank);
          marker._icon.style.filter = `hue-rotate(${hue_rotate_val}deg)`
          //marker._icon.style.filter = `saturate(${1 - rank/max_rank})`
          //marker._icon.style.filter = `opacity(${1 - rank/max_rank})`
        }

      },

      drawHistogramPlot(id,hist_data,hist_color,minmax) {

        var data_within_range = [];
        var data_outside_range = [];
        
        for(var i=0;i<hist_data.length;i++)
        {
          if(hist_data[i]<=minmax[1] && hist_data[i]>=minmax[0])
          {
            data_within_range.push(hist_data[i]);
          }
          else
          {
            data_outside_range.push(hist_data[i]);
          }
        }

        var trace1 = {
          x: data_within_range,
          type: 'histogram',
          title: id,
          nbinsx: 100,
          marker: {
            color:hist_color
          }

        };

        var trace2 = {
          x: data_outside_range,
          type: 'histogram',
          title: id,
          nbinsx: 100,
          marker: {
            color:"grey"
          }

        };
        var data = [trace1,trace2];
        var layout = {
          barmode: "overlay",
          showlegend: false,
          autosize: true,
          //width: 300,
          //height: 300,
          margin: {
            l: 40,
            r: 20,
            b: 40,
            t: 10,
            pad: 2
          },
        }
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