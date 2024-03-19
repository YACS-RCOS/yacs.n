<script setup lang="ts">
import { watchEffect } from "vue";
import { RouterView } from "vue-router/auto";
import AppFooter from "./components/AppFooter.vue";
import NavBar from "./components/NavBar.vue";
import { useThemeStore } from "./stores/theme";

const themeStore = useThemeStore();

watchEffect(() => {
  themeStore.applyTheme();
});
</script>

<template>
  <header>
    <NavBar />
  </header>

  <RouterView />

  <AppFooter />
</template>
