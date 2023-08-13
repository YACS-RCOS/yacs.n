<template>
    <div class="rating">
      <div
        v-for="star in 5"
        :key="star"
        @click="rate(star)"
        @mouseover="hoverRating(star)"
        @mouseleave="resetHover"
        :class="{ 'selected': star <= currentRating, 'hover': star <= hoverRatingValue }"
      >
        &#9733;
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      initialRating: {
        type: Number,
        default: 0
      }
    },
    data() {
      return {
        currentRating: this.initialRating,
        hoverRatingValue: 0
      };
    },
    methods: {
      rate(rating) {
        this.currentRating = rating;
        this.$emit('rate', rating);
      },
      hoverRating(rating) {
        this.hoverRatingValue = rating;
      },
      resetHover() {
        this.hoverRatingValue = 0;
      }
    }
  };
  </script>
  
  <style scoped>
  .rating {
    display: inline-block;
  }
  
  .hover {
    color: gold;
    cursor: pointer;
  }
  
  .selected {
    color: gold;
  }
  </style>
  