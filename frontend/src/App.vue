<template>
      <!-- <HelloWorld msg="The Vizzards"/> -->
    <v-toolbar class="bg-blue-lighten-5" density="compact">
    <v-toolbar-title>Item Labeling: Apartment Ratings in Zurich</v-toolbar-title>
    <v-spacer ></v-spacer><v-spacer ></v-spacer>
    <v-btn icon
    hover="Rate me!">
        <v-icon>mdi-heart</v-icon>
      </v-btn>
    </v-toolbar>
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
    showVisualization: false
    
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
