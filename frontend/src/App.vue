<template>
      <!-- <HelloWorld msg="The Vizzards"/> -->
    <v-toolbar class="bg-blue-lighten-5" density="compact">
    <v-toolbar-title>Item Labeling: Apartment Ratings in Zurich</v-toolbar-title>
    <v-spacer ></v-spacer><v-spacer ></v-spacer>
    <!-- <template v-slot:activator="{ props }"> -->
    <v-btn variant="text" icon="mdi-filter" @click="dialog = true"></v-btn>
    <v-btn icon  @click="this.$router.push('/')">
        <v-icon>mdi-heart</v-icon>
      </v-btn>
    <!-- </template> -->
    </v-toolbar>
    <v-dialog
      v-model="dialog"
      width="800"
    >
      <v-card>
        <v-card-title>
          <span class="text-h5">Filters</span>
        </v-card-title>
            <v-select style="width:70%;margin-left: 20px;"
      label="Select Room Type"
      :items="['Private room', 'Entire home/apt', 'Hotel room']"
      @update:modelValue="selectedRoomType"
    ></v-select>
    <v-select style="width:70%;margin-left: 20px;"
      label="Select Neighbourhood Group"
      :items="['Kreis 1', 'Kreis 2', 'Kreis 3', 'Kreis 4','Kreis 5', 'Kreis 6', 'Kreis 7', 'Kreis 8','Kreis 9', 'Kreis 10', 'Kreis 11', 'Kreis 12']"
      @update:modelValue="selectedNeighbourhoodGroup"
    ></v-select>
    <v-text-field style="width:70%;margin-left: 20px;" clearable 
    label="Maximum Nights" variant="outlined" @update:modelValue="selectedMaximumNights"></v-text-field>
    <!-- <v-range-slider style="width:70%;margin-left: 20px;"
    v-model="value"
    step="10"
    thumb-label="always"
  ></v-range-slider> -->
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            class="bg-green-darken-1"
            variant="text"
            @click="save"
          >
            Save
          </v-btn>
          <v-btn
            class="bg-red-darken-1"
            variant="text"
            @click="dialog = false"
          >
            Reset
          </v-btn>
          <v-btn
          class="bg-grey-lighten-2"
            variant="text"
            @click="dialog = false"
          >
            close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  <div>
    <!-- <router-view ></router-view> -->
    <RouterView v-slot="{ Component }">
  <component
    :is="Component"
    :dialogs="dialog"
    :availability="availability" :roomType="roomType" :neighbourhoodGroup="neighbourhoodGroup" inheritAttrs: false
   />
</RouterView>
  </div>
</template>

<script>
// import LabelizeRatings from './components/LabelizeRatings.vue'
// import DataVisualization from './components/DataVisualization.vue'
// import Vue from 'vue';

// export const EventBus = new Vue();

export default {
  name: 'App',
  components: {
},
  data: () => ({
    dialog: false,
    roomType: '',
    neighbourhoodGroup: '',
    availability: '',
    bufferRoomType: '',
    bufferAvailability: '',
    bufferNeighbourhoodGroup: ''
    
  }),
  methods: {
    selectedRoomType(props) {
      this.bufferRoomType = props
    },
    selectedMaximumNights(props) {
      this.bufferAvailability = props
    },
    selectedNeighbourhoodGroup(props) {
      this.bufferNeighbourhoodGroup = props
    },
    save() {
      this.roomType = this.bufferRoomType
      this.neighbourhoodGroup = this.bufferNeighbourhoodGroup
      this.availability = this.bufferAvailability
      this.dialog = false
}
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
  font-family: cursive;
}
</style>
