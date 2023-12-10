<template> <v-card class="mx-auto my-12" max-width="350" max-height="600">
  
      <v-img v-if="room_type === 'Private room'"
        cover
        height="220"
        src="1-room.jpg"
      ></v-img>
      <v-img v-if="room_type === 'Entire home/apt'"
        cover
        height="220"
        src="whole-apartment.jpg"
      ></v-img>
      <v-img v-if="room_type === 'Hotel room'"
        cover
        height="220"
        src="hotel-room.jpg"
      ></v-img>
  
      <v-card-item>
        <v-card-title>{{ name }} </v-card-title>
  
        <v-card-subtitle>
          <span class="me-1">{{ room_type }}</span> <span style="width:80%"></span><span style="margin-right: 80%;" class="my-4 text-subtitle-1">Rank: {{ rank }}</span>
  
          <v-icon color="error" icon="mdi-fire-circle" size="small"></v-icon>
        </v-card-subtitle>
      </v-card-item>
  
      <v-card-text>
        <div><span style="color: #8D6E63;">Address:</span> {{ neighbourhood }} , {{ neighbourhood_group }}</div>
        <div><span style="color: #8D6E63;">Minimum Nights:</span> {{ minimum_nights }} , <span style="color: #8D6E63;">Availability:</span> {{ availability_365 }}</div>
        <div><span style="color: #8D6E63;">Hosted By: </span>{{ host_name }} , <span style="color: #8D6E63;">Listings:</span> {{ calculated_host_listings_count }}</div>
        <div><span style="color: #8D6E63;">Reviews:</span> {{ number_of_reviews }} , <span style="color: #8D6E63;">Last Reviewed:</span> {{ last_review }}</div>
  
        <div class="my-4 text-subtitle-1">$ • {{ price }} CHF</div>
      </v-card-text>
  
      <!-- <v-divider class="mx-2 mb-1"></v-divider> -->
      <v-card-actions>
        <v-rating
        hover
        :length="5"
        :size="32"
        :model-value=rating
        active-color="amber"
        @update:modelValue="updateInput"
        @click:modelValue="updateInput"
      />
    </v-card-actions>
    </v-card>
  </template>
  
  <script>

  
    export default {
    name: 'ApartmentDetails',
    props: {
      msg: String,
      room_type: String,
      neighbourhood: String, 
      neighbourhood_group: String,
      minimum_nights: String, 
      availability_365: String,
      host_name: String,
      calculated_host_listings_count: String,
      number_of_reviews: String,
      last_review: String,
      s_rating: String,
      price: String,
      name: String,
      rank: String,
      s_id: String
    },
    data: () => ({
        step: 1,
        loading: false,
        ApartmentData: [],
        progress: 0,
        CurrentApartment: [],
        showSubmit: false,
        predictedData: [],
        snackbar: true,
        rating: 0,
        id: ''

      }),
  watch: {
    s_rating(newValue) {
      // The watcher is triggered whenever the prop value changes
      console.log('Tamanna')
      this.rating = newValue;
      this.updateInput(newValue)
    }
    ,
    s_id(newValue){
        this.id =newValue
    }
  },
  
    mounted() {
        this.rating = this.s_rating
        this.id = this.s_id
    },
  
    methods: {
      updateInput(props) {
        this.rating = props
        this.trainData(this.id, this.rating) 
    },
    trainData(id, rating) {
    const requestOptions = {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: id, rating: rating })
    };
    fetch("http://127.0.0.1:5000/model-train", requestOptions)
      .then(response => response.json())
  },
    async goToVisualization() {
      this.$router.push({name :"DataVisualization"});
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