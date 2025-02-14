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

  <main class="flex h-full w-full flex-col overflow-auto bg-on-primary font-sans">
    <RouterView v-slot="{ Component }">
      <template v-if="Component">
        <!-- <Transition mode="out-in"> -->
        <!-- <KeepAlive> -->
        <Suspense timeout="0">
          <!-- main content -->
          <component :is="Component" />

          <!-- loading state -->
          <template #fallback>
            <div
              class="absolute top-1/4 mx-auto aspect-square h-2/5 animate-spin self-center justify-self-center bg-primary mask-image-multiselect-spinner"
            >
              Loading...
            </div>
          </template>
        </Suspense>
        <!-- </KeepAlive> -->
        <!-- </Transition> -->
      </template>
    </RouterView>
  </main>

  <AppFooter />
</template>
