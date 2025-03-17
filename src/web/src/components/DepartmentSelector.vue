<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import Multiselect from '@vueform/multiselect'
import "@vueform/multiselect/themes/tailwind.css"

const props = defineProps<{
  departments: string[]
}>()

const emit = defineEmits<{
  'update': [selectedOption: string | null]
}>();

function updateDepartment(selectedDepartment: string | null) {
  emit('update', selectedDepartment);
}
</script>

<template>
  <div class="w-64 text-black border border-gray-300 rounded">
    <Multiselect
      :options="props.departments"
      placeholder="Search by department"
      :searchable="true"
      @update:model-value="updateDepartment"
    />
  </div>
</template>
