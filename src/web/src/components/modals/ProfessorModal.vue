<script setup lang="ts">
import { defineProps, defineEmits } from "vue";
import GenericModal from "@/components/modals/GenericModal.vue";
import { type Professor } from "@/api/professor";

defineProps<{
  prof: Professor;
}>();

const emit = defineEmits<{
  close: [];
}>();

</script>

<template>
  <GenericModal 
    :open="true" 
    @close="emit('close')"
  >
    <template #default="{ close }">
      <div class="p-5 bg-on-primary-dark text-primary rounded shadow-lg">
        <h2 class="text-3xl font-bold mb-1">
          {{ prof.name }}
        </h2>
        <h2 v-if="prof.title" class="text-xl font-bold mb-1">
          {{ prof.title }}
        </h2>
        <p class="mt-4 mb-2">
          <strong>Email:</strong> {{ prof.email }}
        </p>
        <p v-if="prof.phone_number" class="mb-2">
          <strong>Phone:</strong> {{ prof.phone_number }}
        </p>
        <p v-if="prof.department" class="mb-2">
          <strong>Department:</strong> {{ prof.department }}
        </p>
        <p v-if="prof.portfolio_page" class="mb-2">
          <strong>School:</strong> {{ prof.portfolio_page }}
        </p>
        <p v-if="prof.profile_page" class="mb-2">
          <strong>Profile: </strong>
          <a
            :href="prof.profile_page"
            class="text-blue-500 hover:underline"
            target="_blank"
          >
            {{ prof.profile_page }}
          </a>
        </p>
        <button
          class="mt-4 rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
          @click="close()"
        >
          Close
        </button>
      </div>
    </template>
  </GenericModal>
</template>
