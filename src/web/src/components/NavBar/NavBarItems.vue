<script lang="ts">
export type NavItems = [route: keyof RouteNamedMap, path: string, icon?: FunctionalComponent][];
</script>

<script setup lang="ts">
import type { FunctionalComponent } from "vue";
import type { RouteNamedMap } from "vue-router/auto-routes";

defineProps<{
  items: NavItems;
}>();
</script>

<template>
  <RouterLink
    v-for="[link, name, icon] of items"
    :key="link"
    :to="link"
    class="flex justify-center gap-x-0.5 rounded-md border-4 border-primary border-opacity-0 bg-primary bg-opacity-0 p-1 text-primary hover:bg-opacity-5 focus:bg-opacity-5 active:bg-opacity-10 motion-safe:transition-all motion-safe:duration-75 [&.router-link-active]:border-opacity-100"
  >
    <template v-if="icon">
      <component
        :is="icon"
        class="aspect-square h-6"
      />
    </template>
    <p>
      {{ name }}
    </p>
  </RouterLink>
</template>
