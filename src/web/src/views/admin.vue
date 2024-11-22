<script setup lang="ts">
import type { RouteNamedMap } from "unplugin-vue-router/types";
import { RouterLink } from "vue-router/auto";

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
      class="rounded bg-action p-1"
      >{{ title }}
    </RouterLink>

    <RouterView v-slot="{ Component }">
      <Transition>
        <component
          :is="Component"
          class="duration-1000 [&.v-enter-active]:transition-opacity [&.v-enter-from]:opacity-0 [&.v-leave-active]:transition-opacity [&.v-leave-to]:opacity-0"
        />
      </Transition>
    </RouterView>

    <div class="flex-grow" />

    <RouterLink
      to="/"
      class="rounded bg-secondary p-1"
      >Go home
    </RouterLink>
  </div>
</template>
