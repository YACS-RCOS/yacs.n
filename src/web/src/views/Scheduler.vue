<script setup lang="ts">
import YacsNav from "../components/YacsNav.vue";
import { courses } from "../store";
</script>

<template>
  <div>
    <yacs-nav></yacs-nav>
  </div>
  <div v-for="course in courses.courseList">
    {{ course.full_title }}
    <div v-for="(value, key) in course">
      {{ key }}
    </div>
  </div>
</template>


<style scoped>

</style>