<script setup lang="ts">
import { RouterLink } from "vue-router/auto";
import type { RouteNamedMap } from "vue-router/auto-routes";

const actions: [keyof RouteNamedMap, string][] = [
  ["/admin/upload_courses", "Upload Courses CSV"],
  ["/admin/upload_finals", "Upload Finals CSV"],
  ["/admin/upload_prof", "Import Professors via JSON"],
  ["/admin/edit_semester", "Edit Semesters"],
  ["/admin/edit_prof", "Edit Professors"]
];
</script>
<template>
  <div class="flex h-full w-full flex-col items-center gap-4 py-10">
    <h1 class="text-5xl font-extrabold">YACS Admin Panel</h1>

    <RouterLink
      v-for="[href, title] of actions"
      :key="href"
      :to="href"
      class="bg-action rounded-sm p-1"
      >{{ title }}
    </RouterLink>

    <RouterView v-slot="{ Component }">
      <Transition>
        <component :is="Component" />
      </Transition>
    </RouterView>

    <div class="grow" />

    <RouterLink
      to="/"
      class="bg-secondary rounded-sm p-1"
      >Go home
    </RouterLink>
  </div>
</template>
