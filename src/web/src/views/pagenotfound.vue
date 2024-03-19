<script setup lang="ts">
import { definePage } from "unplugin-vue-router/runtime";
definePage({
  path: "/:path(.*)*"
});
</script>

<template>
  <div>404: Page Not Found</div>
</template>
