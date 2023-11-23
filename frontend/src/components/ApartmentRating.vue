<template>
  <star-rating @update:rating ="setRating"/>
</template>

<script>
import StarRating from 'vue-star-rating'
export default {
  name: 'ApartmentRating',
  components: {
    StarRating
  },
  methods: {
    async setRating(rating){
      this.rating=rating;
      fetch("http://127.0.0.1:5000/model-train",
                              {method: "PUT",
                              headers: {
                                        'Content-Type': 'application/json'
                              }, 
                              body: JSON.stringify({rating: rating}),
                              })


    }
    
  },
}
</script>

<style scoped>

</style>