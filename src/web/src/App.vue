<script setup lang="ts">
import { watchEffect } from "vue";
import { RouterView, useRoute } from "vue-router/auto";
import AppFooter from "./components/AppFooter.vue";
import NavBar from "./components/NavBar.vue";
import { useThemeStore } from "./stores/theme";

const themeStore = useThemeStore();

const route = useRoute();

watchEffect(() => {
  themeStore.applyTheme();
});
</script>

<template>
  <header v-if="route.matched.length > 0 && route.matched[0].name != '/admin'">
    <NavBar />
  </header>

  <main class="h-full w-full bg-on-primary font-sans">
    <RouterView />
  </main>

  <AppFooter />
</template>
