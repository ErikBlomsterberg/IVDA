<template>
   <v-container width="200%">
    <v-row class="bg-grey-lighten-2">
      <v-col cols="8">
        <v-sheet class="pa-2 ma-2" height="720px"> Level 1: .v-col-8 </v-sheet>
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
  
    export default {
    name: 'DataVisualization',
    props: {
      msg: String
    },
    data: () => ({
        loading: false,
        predictedData: []
      }),
  
    mounted() {
      this.fetchData()
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