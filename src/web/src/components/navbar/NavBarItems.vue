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
    class="[&.router-link-active]:border-primary text-primary flex justify-center gap-x-0.5 rounded-md border-4 border-transparent p-1 hover:backdrop-brightness-150 active:backdrop-brightness-200 motion-safe:transition-all motion-safe:duration-75"
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
