<template>
  <v-card  v-for="(item, index) in CurrentApartment" :key="index" 
    class="mx-auto"
    max-width="500"
  >
    <v-card-title class="text-h6 font-weight-regular justify-space-between">
      <v-progress-linear
      :model-value='progress'
      height="10"
      striped
      color="deep-orange"
    ></v-progress-linear>
    </v-card-title>

    <v-window  v-model="step">
      <v-window-item :value="1">
        <v-card :loading="loading" class="mx-auto my-12" max-width="500">
    <template v-slot:loader="{ isActive }">
      <v-progress-linear
        :active="isActive"
        color="deep-purple"
        height="4"
        indeterminate
      ></v-progress-linear>
    </template>

    <v-img v-if="item.room_type === 'Private room'"
      cover
      height="400"
      src="1-room.jpg"
    ></v-img>
    <v-img v-if="item.room_type === 'Entire home/apt'"
      cover
      height="400"
      src="whole-apartment.jpg"
    ></v-img>
    <v-img v-if="item.room_type === 'Hotel room'"
      cover
      height="400"
      src="hotel-room.jpg"
    ></v-img>

    <v-card-item>
      <v-card-title>{{ item.name }} </v-card-title>

      <v-card-subtitle>
        <span class="me-1">{{ item.room_type }}</span>

        <v-icon color="error" icon="mdi-fire-circle" size="small"></v-icon>
      </v-card-subtitle>
    </v-card-item>

    <v-card-text>
      <div><span style="color: #8D6E63;">Address:</span> {{ item.neighbourhood }} , {{ item.neighbourhood_group }}</div>
      <div><span style="color: #8D6E63;">Minimum Nights:</span> {{ item.minimum_nights }} , <span style="color: #8D6E63;">Availability:</span> {{ item.availability_365 }}</div>
      <div><span style="color: #8D6E63;">Hosted By: </span>{{ item.host_name }} , <span style="color: #8D6E63;">Listings:</span> {{ item.calculated_host_listings_count }}</div>
      <div><span style="color: #8D6E63;">Reviews:</span> {{ item.number_of_reviews }} , <span style="color: #8D6E63;">Last Reviewed:</span> {{ item.last_review }}</div>

      <div class="my-4 text-subtitle-1">$ • {{ item.price }} CHF</div>
    </v-card-text>

    <v-divider class="mx-4 mb-1"></v-divider>

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
    <v-spacer></v-spacer>
      <v-btn
        v-if="showSubmit === true"
        color="green"
        variant="flat"
        @click="goToVisualization"
      >
        Submit
      </v-btn>
    </v-card-actions>
  </v-card>
      </v-window-item>
    </v-window>
  </v-card>
</template>

<script>

  export default {
  name: 'LabelizeRatings',
  props: {
    msg: String,
    switchComponent: Function,
    availability: String,
    roomType: String,
    neighbourhoodGroup: String
  },
  data: () => ({
      step: 1,
      loading: false,
      ApartmentData: [],
      rating: 0,
      progress: 0,
      CurrentApartment: [],
      showSubmit: false,
      predictedData: []
    }),

  mounted() {
    this.fetchData()
  },

  methods: {
    async fetchData() {
      var reqUrl = 'http://127.0.0.1:5000/apartments'
      console.log("ReqURL " + reqUrl)
      const response = await fetch(reqUrl)
      const responseData = await response.json();
      responseData.forEach((apartment) => {
        this.ApartmentData.push(apartment)
      })
      this.CurrentApartment.push(this.ApartmentData[0])
      this.rating = this.CurrentApartment[0].rating
    },
    
    updateInput(props) {
      this.rating = props
      this.progress = this.progress + 10
      this.trainData(this.CurrentApartment[0].id, this.rating) 
      if (this.progress >= 100){
        this.showSubmit = true
        this.progress == 100
        this.CurrentApartment =[]
        this.CurrentApartment.push(this.ApartmentData[9])
      }else{
    
      this.CurrentApartment =[]
      this.CurrentApartment.push(this.ApartmentData[this.progress/10 ])
      this.rating = this.CurrentApartment[0].rating
      }
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