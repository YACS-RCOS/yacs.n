<template>
  <h1>{{ courseName }}</h1>
</template>

<script>
export default {
  name: "CoursePage",
  data() {
    return {
      courseName: this.$route.params.course,
    };
  },
};
</script>
