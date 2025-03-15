<script setup lang="ts">
import { defineProps, ref } from 'vue'
import Multiselect from '@vueform/multiselect'
import "@vueform/multiselect/themes/tailwind.css"

const props = defineProps<{
  departments: string[]
}>()

// Track the single selected department
const selectedDepartment = ref<string | null>(null)
</script>

<template>
  <div class="my-4 w-64 text-black">
    <Multiselect
      v-model="selectedDepartment"
      :options="props.departments"
      placeholder="Search by department"
      :searchable="true"
    />
  </div>
</template>
