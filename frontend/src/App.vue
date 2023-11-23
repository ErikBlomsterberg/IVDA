<template>
  <div>
    <HelloWorld msg="The Vizzards"/>
    <ApartmentRating/>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import ApartmentRating from './components/ApartmentRating.vue'


export default {
  name: 'App',
  components: {
    HelloWorld,
    ApartmentRating
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
  margin-top: 60px;
}
</style>
