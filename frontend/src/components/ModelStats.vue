<template>
  <div>
    <div>Recommendation Accuracy: {{ model_error }}</div>
    <div>Rated Apartments: {{ n_ratings }}</div>
  </div>
</template>

<script>
export default {
  props: {
    // Define a prop named 'message' with type String
    model_error: String,
    // Define a prop named 'info' with type Object
    n_ratings: Object
  }
};
</script>

<style scoped>
/* Add your styling here if needed */
div {
  display: inline-block;
  margin-right: 10px; /* Add margin for spacing between the two text strings */
}
</style>