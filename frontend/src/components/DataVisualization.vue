<template>
  <v-app>
    <v-switch
        v-model="colorblind_mode"
        color="primary"
        @update:modelValue="update_data"
        hide-details
        inset
        :label="`Colorblind Mode: ${colorblind_mode.toString()}`">
      </v-switch>

      <v-select
        v-model="filters_selected"
        :items="filters_list"
        chips
        label="Filter by"
        multiple
        @update:modelValue="update_filters"
      ></v-select>
  
  <v-container width="200%">
   <v-row class="bg-grey-lighten-2">
    <ModelStats :model_error=this.model_error :n_ratings=this.n_ratings />
    <v-col cols="2"></v-col>
     <v-col cols="8">
       <v-sheet class="pa-2 ma-2" height="720px" id="mapContainer"  @click:map="update_map"></v-sheet>
       <br>
       <v-slider 
            id="displayed_apartments_slider" 
            label="No of apartments displayed"
            color="blue" 
            thumb-color="dark blue"
            thumb-label
            :max=100
            :min=0
            :step="1"
            v-model="max_displayed_apartments" 
            @update:modelValue="update_data"
            >
          </v-slider>
     </v-col>
     <v-col cols="4">
       <v-row no-gutters>
         <v-col cols="12"  v-if="price_filter==true">
          <v-card-text>Filter by price</v-card-text>
          <v-card class="pa-2 ma-2" height="150px" id="histContainer1"> Price </v-card>
          
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
         <v-col cols="12"  v-if="no_reviews_filter==true">
          <v-card-text>Filter by "No of reviews"</v-card-text>
           <v-card class="pa-2 ma-2" height="150px" id="histContainer2"> No of reviews
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
         <v-col cols="12"  v-if="min_nights_filter==true">
          <v-card-text>Filter by "Min no of days"</v-card-text>
           <v-card class="pa-2 ma-2" height="150px" id="histContainer3"> Min no of days </v-card>
           
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
       <v-row no-gutters>
         <v-col cols="12"  v-if="max_nights_filter==true">
          <v-card-text>Filter by max days</v-card-text>
          <v-card class="pa-2 ma-2" height="150px" id="histContainer4"> Max no of nights </v-card>
          
          <v-range-slider 
            id="max_nights_slider" 
            color="red" 
            v-model="maxnights_minmax" 
            thumb-label
            :max=max_maxnights
            :min=0
            @update:modelValue="update_data">
          </v-range-slider>
         </v-col>
       </v-row>
       <v-row no-gutters>
         <v-col cols="12"  v-if="no_reviews_monthly_filter==true">
          <v-card-text>Filter by reviews per month</v-card-text>
          <v-card class="pa-2 ma-2" height="150px" id="histContainer5"> No of monthly reviews </v-card>
          
          <v-range-slider 
            id="monthly_reviews_slider" 
            color="purple" 
            v-model="monthly_reviews_minmax" 
            thumb-label
            :max=max_monthly_reviews
            :min=0
            @update:modelValue="update_data">
          </v-range-slider>
          
          </v-col>
       </v-row>
     </v-col>
   </v-row>
  </v-container>
  </v-app><v-dialog theme="light" v-model="detailview" scrollable width="auto">
    <ApartmentDetails :room_type="s_room_type" :neighbourhood="s_neighbourhood"  :neighbourhood_group="s_neighbourhood_group" 
    :minimum_nights = "s_minimum_nights" :availability_365="s_availability_365" :host_name="s_host_name" :calculated_host_listings_count="s_calculated_host_listings_count"
      :number_of_reviews="s_number_of_reviews" :last_review="s_last_review" :s_rating="s_rating" :name="s_name" :price="s_price" :rank="s_rank" :s_id="s_id"/>
    </v-dialog>
 </template>
 
 <script>
  // Import Leaflet for map visualization
  import "leaflet/dist/leaflet.css";
  import L from 'leaflet';

  import Plotly from 'plotly.js-dist';

  import ModelStats from './ModelStats.vue';
  import ApartmentDetails from "./ApartmentDetails.vue";
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
      neighbourhoodGroup: String,
      dialogs: Boolean
    },
    components: {
    ModelStats,
    ApartmentDetails
    },
    data: () => ({
        loading: false,
        elevations: [0, 4, 8, 12, 16, 20],
        predictedData: [],
        filteredData: [],
        number_of_reviews: [],
        minimum_nights: [],
        price: [],
        maximum_nights: [],
        number_of_monthly_reviews: [],
        max_price: 0,
        max_minnights: 0,
        max_reviews: 0,
        max_maxnights: 0,
        max_monthly_reviews: 0,
        price_minmax: [0,100],
        review_minmax: [0,100],
        minnights_minmax: [0,100],
        maxnights_minmax: [0,100],
        monthly_reviews_minmax: [0,100],
        availabilitys: '',
        roomTypes: '',
        neighbourhoodGroups: '',
        colorblind_mode: false,
        max_displayed_apartments: 20,
        filters_list: ["price","max_nights","min_nights","no_reviews","no_reviews_monthly"],
        filters_selected: ["price","max_nights","no_reviews_monthly"],
        price_filter:true,
        max_nights_filter:true,
        min_nights_filter:false,
        no_reviews_filter:false,
        no_reviews_monthly_filter:true,

        filter: '',
        model_error: 0,
        n_ratings: 0,
        detailview: false,
        s_room_type: ''
      }),
  watch: {
    availability(newMyProp) {
      this.availabilitys = newMyProp
    },
    roomType(newMyProp) {
      this.roomTypes = newMyProp
    },
    neighbourhoodGroup(newMyProp) {
      this.neighbourhoodGroups = newMyProp
    },
    dialogs(newMyProp) {
      this.filter = newMyProp
      this.fetchModelData()
      this.update_data()
    }
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

        this.fetchModelData()

    },

    methods: {
      async fetchModelData() {
        var res = await fetch("http://127.0.0.1:5000/model-stats")
        var data = await res.json()
        this.model_error = data['error']
        this.n_ratings = data['n_ratings']
      },
      async fetchData() {
        this.test = 'Tamanna'
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
            if(apartment["reviews_per_month"] > this.max_monthly_reviews)
              this.max_monthly_reviews = apartment["reviews_per_month"];
            if(apartment["availability_365"] > this.max_maxnights)
              this.max_maxnights = apartment["availability_365"];
            if(apartment["price"] > this.max_price)
              this.max_price= apartment["price"];
            if(apartment["minimum_nights"] > this.max_minnights)
              this.max_minnights = apartment["minimum_nights"];

            this.number_of_reviews.push(apartment["number_of_reviews"]);
            this.minimum_nights.push(apartment["minimum_nights"]);
            this.price.push(apartment["price"]);
            this.maximum_nights.push(apartment["availability_365"]);
            this.number_of_monthly_reviews.push(apartment["reviews_per_month"]);
            
      })

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


      update_filters()
      {
        console.log("update Filters")
        this.price_filter = false;
        this.min_nights_filter = false;
        this.max_nights_filter = false;
        this.no_reviews_filter = false;
        this.no_reviews_monthly_filter = false;

        for(var i=0;i<this.filters_selected.length;i++)
        {
          if(this.filters_selected[i]=="price")
          {
            this.price_filter=true;
          }
          if(this.filters_selected[i]=="min_nights")
          {
            this.min_nights_filter=true;
          }
            if(this.filters_selected[i]=="max_nights")
          {
            this.max_nights_filter=true;
          }
            if(this.filters_selected[i]=="no_reviews")
          {
            this.no_reviews_filter=true;
          }
            if(this.filters_selected[i]=="no_reviews_monthly")
          {
            this.no_reviews_monthly_filter=true;
          }
        }

        setTimeout(this.update_histograms, 100);

        
      },


      update_data()
      {
        //console.log("Update Data")
        //this.update_filters();
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
          if(this.predictedData[i]["availability_365"] <= this.maxnights_minmax[0] || this.predictedData[i]["availability_365"] >= this.maxnights_minmax[1])
          {
            this.filteredData.splice(i,1)
          }
          if(this.predictedData[i]["reviews_per_month"] <= this.monthly_reviews_minmax[0] || this.predictedData[i]["reviews_per_month"] >= this.monthly_reviews_minmax[1])
          {
            this.filteredData.splice(i,1)
          }
        }
        if( this.neighbourhoodGroups.length > 0) {
        this.filteredData = this.predictedData.filter(item => item["neighbourhood_group"] === this.neighbourhoodGroups);
        }
        if( this.roomType.length > 0){

        this.filteredData = this.predictedData.filter(item => item["room_type"] === this.roomType);
        }
        if( this.availability.length > 0){
        this.filteredData = this.predictedData.filter(item => item["availability_365"] <= this.availability);
        }
        //console.log(this.filteredData.length)
        this.update_map();
        this.update_histograms();
      },

      update_histograms()
      {
        //console.log("Update histograms")
        if(this.price_filter==true)
          this.drawHistogramPlot("histContainer1",this.price, "green", this.price_minmax);
        if(this.no_reviews_filter==true)
          this.drawHistogramPlot("histContainer2",this.number_of_reviews, "blue", this.review_minmax);
        if(this.min_nights_filter==true)
          this.drawHistogramPlot("histContainer3",this.minimum_nights, "orange", this.minnights_minmax);
        if(this.max_nights_filter==true)
          this.drawHistogramPlot("histContainer4",this.maximum_nights, "red", this.maxnights_minmax);
        if(this.no_reviews_monthly_filter==true)
          this.drawHistogramPlot("histContainer5",this.number_of_monthly_reviews, "purple", this.monthly_reviews_minmax);

      },

      marker_click(e)
      {
        console.log("Marker clicked!")
        this.detailview = true
        this.details_data = JSON.parse(JSON.stringify(e.target.id))
        this.s_room_type = this.details_data['_Private room'] == 1 ? 'Private room' : this.details_data['_Hotel room'] == 1 ? 'Hotel room' : this.details_data['_Entire home/apt'] == 1 ? 'Entire home/apt' : ''
        this.s_neighbourhood = this.details_data['neighbourhood']
        this.s_neighbourhood_group = this.details_data['neighbourhood_group']
        this.s_minimum_nights = this.details_data['minimum_nights']
        this.s_availability_365 = this.details_data['availability_365']
        this.s_host_name = this.details_data['host_name']
        this.s_calculated_host_listings_count = this.details_data['calculated_host_listings_count']
        this.s_number_of_reviews = this.details_data['number_of_reviews']
        this.s_last_review = this.details_data['last_review']
        this.s_rating = this.details_data['rating']
        this.s_price = this.details_data['price']
        this.s_name = this.details_data['name']
        this.s_id = this.details_data['id']
        this.s_rank = e.target.rank

    //     :room_type="s_room_type" :neighbourhood="s_neighbourhood"  :neighbourhood_group="s_neighbourhood_group" 
    // :minimum_nights = "s_minimum_nights" :availability_365="s_availability_365" :host_name="s_host_name" :calculated_host_listings_count="s_calculated_host_listings_count"
    //   :number_of_reviews="s_number_of_reviews" :last_review="s_last_review" :s_rating="3"
      },


      update_map() {

        //console.log(props)
        var max_rank = this.filteredData.length

        
        
      
        var i;

        
        //console.log("Predicted data:")
        //console.log(this.predictedData)
        //console.log(this.predictedData.length)

        
        this.layerGroup.clearLayers()
        for(i=0;i<Math.min(max_rank,this.max_displayed_apartments);i++)
        {
          var price = this.filteredData[i]["price"]
          var latitude = this.filteredData[i]["latitude"]
          var longitude = this.filteredData[i]["longitude"]
          var title = this.filteredData[i]["name"]
          var rank = i
          // popupComponent.$mount(test);
          //console.log(this.filteredData[i]["rating"])
          var marker = L.marker([latitude,longitude],{title :`${price} CHF`},{rank})
          marker.on('click', this.marker_click);
          marker.addTo(this.layerGroup);
          marker.id = this.filteredData[i];
          marker.rank = rank;
          //this.markers.push(marker)
          console.log(title,price,rank)
          // marker.bindPopup(`<b> ${title}</b><br>Price: <b>${price} CHF</b><br>Rank: <b>${rank}</b>`);
          
        
          var hue_rotate_val = 250-100*(rank/max_rank);
          if(this.colorblind_mode==true)
          {
            marker._icon.style.filter = `saturate(${1 - rank/max_rank})`
          }
          else
          {
            marker._icon.style.filter = `hue-rotate(${hue_rotate_val}deg)`
          }
          
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