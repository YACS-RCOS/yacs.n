<script lang="ts" setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import YacsHeader from "./components/YACSHeader.vue"
import { courseList, selectionInfo } from "./store"
</script>

<template>
  <yacs-header></yacs-header>
  <div class="yacs-content">
    <router-view></router-view>
  </div>
</template>

<style>
body {
  margin: 0;
}

.yacs-content {

}
</style>
