<script setup lang="ts">
import { useRoute } from "vue-router/auto";

const route = useRoute();
</script>

<template>
  <div>{{ route.params }}</div>
</template>
