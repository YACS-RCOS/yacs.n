<template>
  <div class="rating">
    <div
      v-for="star in totalStars"
      :key="star"
      @click="rate(star)"
      @mouseover="hoverRating(star)"
      @mouseleave="resetHover"
      :class="{
        'selected': star <= currentRating,
        'hover': star <= hoverRatingValue
      }"
    >
      {{ getStarSymbol(star) }}
    </div>
    <p v-if="showRating">Your Rating: {{ currentRating }}/5</p>
  </div>
</template>

<script>
export default {
  props: {
    initialRating: {
      type: Number,
      default: 0,
    },
    totalStars: {
      type: Number,
      default: 5,
    },
    showRating: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      currentRating: this.initialRating,
      hoverRatingValue: 0,
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
    },
    getStarSymbol(star) {
      return star <= this.currentRating ? '★' : '☆';
    },
  },
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
