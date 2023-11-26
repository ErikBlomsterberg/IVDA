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
    <v-text-field style="width:70%;margin-left: 20px;" clearable 
    label="Minimum Nights" variant="outlined" @update:modelValue="selectedMinimumNights"></v-text-field>
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
            @click="dialog = false"
          >
            Save
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
  <!-- <LabelizeRatings v-if="showVisualization === false" @switchComponent="switchComponent($event)" msg="The Vizzards"/>
  <DataVisualization v-if="showVisualization === true" msg="The Vizzards"/> -->
  <div>
    <router-view></router-view>
  </div>
</template>

<script>
// import LabelizeRatings from './components/LabelizeRatings.vue'
// import DataVisualization from './components/DataVisualization.vue'

export default {
  name: 'App',
  components: {
    // LabelizeRatings,
    // DataVisualization
  },
  data: () => ({
    dialog: false,
    value: [20, 40],
    
  }),
  methods: {
    selectedRoomType(props) {
      console.log(props)
    },
    selectedMinimumNights(props) {
      console.log(props)
    }
  }
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
