<template>
  <div class="feedback-form">
    <textarea v-model="feedback" :placeholder="placeholder"></textarea>
    <div class="character-count">{{ remainingCharacters }} characters remaining</div>
    <button @click="submitFeedback" :disabled="isSubmitting || !isValid">Submit Feedback</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      feedback: '',
      isSubmitting: false,
      maxCharacters: 300,
      placeholder: 'Enter your feedback...'
    };
  },
  computed: {
    remainingCharacters() {
      return this.maxCharacters - this.feedback.length;
    },
    isValid() {
      return this.feedback.trim() !== '' && this.feedback.length <= this.maxCharacters;
    }
  },
  methods: {
    async submitFeedback() {
      if (this.isValid && !this.isSubmitting) {
        this.isSubmitting = true;
        try {
          // Simulate API call or database submission delay
          await new Promise(resolve => setTimeout(resolve, 1000));
          this.$emit('submit', this.feedback);
          this.feedback = '';
        } catch (error) {
          console.error('Error submitting feedback:', error);
        } finally {
          this.isSubmitting = false;
        }
      }
    }
  }
};
</script>

<style scoped>
.feedback-form {
  font-family: Arial, sans-serif;
  max-width: 400px;
  margin: 0 auto;
}

textarea {
  width: 100%;
  height: 150px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.character-count {
  margin-top: 5px;
  color: #888;
  font-size: 12px;
}

button {
  margin-top: 10px;
  padding: 6px 12px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
