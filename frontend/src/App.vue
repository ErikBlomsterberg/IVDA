<template>
      <!-- <HelloWorld msg="The Vizzards"/> -->
    <v-toolbar class="bg-blue-lighten-5" density="compact">
    <v-toolbar-title>Item Labeling: Apartment Ratings in Zurich</v-toolbar-title>
    <v-spacer ></v-spacer><v-spacer ></v-spacer>
    <!-- <template v-slot:activator="{ props }"> -->
    <v-btn variant="text" icon="mdi-filter" @click="dialog = true"></v-btn>
    <v-btn icon  >
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
  <LabelizeRatings v-if="showVisualization === false" @switchComponent="switchComponent($event)" msg="The Vizzards"/>
  <DataVisualization v-if="showVisualization === true" msg="The Vizzards"/>
</template>

<script>
import LabelizeRatings from './components/LabelizeRatings.vue'
import DataVisualization from './components/DataVisualization.vue'

export default {
  name: 'App',
  components: {
    LabelizeRatings,
    DataVisualization
  },
  data: () => ({
    showVisualization: false,
    dialog: false
    
  }),
  methods: {
    switchComponent(value) {
      this.showVisualization = value
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
