<script setup lang="ts">
import GenericModal from "@/components/modals/GenericModal.vue";
import { useRouter } from "vue-router/auto";

const router = useRouter();
</script>
<template>
  <GenericModal
    :open="true"
    @close="router.back()"
  />
</template>
