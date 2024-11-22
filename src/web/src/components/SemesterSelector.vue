<script setup lang="ts">
import { useClassInfoStore } from "@/stores/classinfo";
import Multiselect from "@vueform/multiselect";
import "@vueform/multiselect/themes/tailwind.css";
import { until } from "@vueuse/core";
import { storeToRefs } from "pinia";

const { semesters, selectedSemester } = storeToRefs(useClassInfoStore());

void until(semesters)
  .toBeTruthy()
  .then((v) => {
    selectedSemester.value = v[0];
  });
</script>

<template>
  <Multiselect
    v-model="selectedSemester"
    :options="semesters ?? []"
    :loading="!semesters"
    :disabled="!semesters"
    mode="single"
    :can-clear="false"
    :can-deselect="false"
    :classes="{
      container:
        'multiselect !bg-on-primary-dark !border !border-primary !rounded-md !text-link !w-max',
      containerActive: 'ring ring-opacity-30 ring-primary',
      wrapper:
        'relative mx-auto w-full h-full flex items-center justify-end box-border cursor-pointer outline-none',
      dropdown: 'multiselect-dropdown !bg-on-primary-dark',
      spinner:
        ' mask-image-multiselect-spinner w-8 mx-8 aspect-square animate-spin bg-primary bg-center bg-no-repeat self-center ',
      singleLabel: 'multiselect-single-label !min-w-max !static !px-2',
      option: 'flex flex-col p-0 m-0 list-none',
      optionSelected: 'bg-primary bg-opacity-15',
      optionPointed: 'bg-primary bg-opacity-10',
      optionSelectedPointed: 'bg-primary bg-opacity-20',
      caret: 'multiselect-caret mask-image-multiselect-caret !bg-primary !bg-none'
    }"
  />
</template>
