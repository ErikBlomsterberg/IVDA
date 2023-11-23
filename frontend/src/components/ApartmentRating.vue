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
      const response = await fetch("http://127.0.0.1:5000/model-predict",
                              {method: "POST",
                              headers: {
                                        'Content-Type': 'application/json'
                              }, 
                              body: JSON.stringify({rating: rating}),
                              })
      const data = await response.json()
      console.log(data)

    }
    
  },
}
</script>

<style scoped>

</style>