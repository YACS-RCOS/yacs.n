<script setup lang="ts">
import YacsNav from "../components/YacsNav.vue";
import { courseList, selectionInfo } from "../store";

console.log(selectionInfo);
</script>

<template>
  <div>
    <yacs-nav></yacs-nav>
  </div>
  <div>{{ courseList }}</div>
  <div>hi</div>
  <div>there</div>
</template>


<style scoped>

</style>