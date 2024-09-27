<script setup lang="ts">
import { useClassInfoStore } from "@/stores/classinfo";
import Multiselect from "@vueform/multiselect";
import "@vueform/multiselect/themes/tailwind.css";
import { storeToRefs } from "pinia";

const selected_semeter = null;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const { semesters } = storeToRefs(useClassInfoStore());
</script>

<template>
  <Multiselect
    v-model="selected_semeter"
    :options="['Batman', 'Robin', 'Joker']"
    mode="single"
    :can-clear="false"
    :can-deselect="false"
    :classes="{
      container:
        'multiselect !bg-on-primary-dark !border !border-link !rounded-md !text-link !w-28',
      dropdown: 'multiselect-dropdown !bg-on-primary-dark',
      singleLabel: 'multiselect-single-label !max-w-[initial]',
      option: 'flex flex-col p-0 m-0 list-none hover:bg-gray-700',
      optionSelected: 'dark:bg-blue-600 dark:text-white'
    }"
  >
    <template #clear><div /></template>
  </Multiselect>
  <!-- <select class="text-lin rounded-sm border border-link bg-transparent p-1">
    <template v-if="semesters.length > 0">
      <option
        v-for="sem of semesters"
        :key="sem"
        :value="sem.toLowerCase()"
        class="bg-on-primary-dark hover:bg-primary"
      >
        {{ sem }}
      </option>
    </template>
    <option
      v-else
      :value="null"
      selected
      disabled
      class="bg-on-primary-dark"
    >
      Loading...
    </option>
  </select> -->
</template>
