<script setup lang="ts">
import { useClassInfoStore } from "@/stores/classinfo";
import Multiselect from "@vueform/multiselect";
// import "@vueform/multiselect/themes/tailwind.css";
import { until } from "@vueuse/core";
import { storeToRefs } from "pinia";

const { semesters, selectedSemester } = storeToRefs(useClassInfoStore());

void until(semesters)
  .toBeTruthy()
  .then((v) => {
    if (v.length > 0) {
      selectedSemester.value ??= v[v.length - 1];
    }
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
    class=""
    :classes="{
      container: 'multiselect bg-transparent! border! border-primary! rounded-md!',
      containerActive: 'ring-2 ring-primary/50',
      wrapper:
        'relative mx-auto w-full h-full flex items-center justify-end box-border cursor-pointer outline-hidden',
      dropdown: 'multiselect-dropdown bg-on-primary-dark! min-w-max!',
      spinner:
        'mask-image-multiselect-spinner w-7 mx-8 my-0 aspect-square animate-spin bg-primary bg-center bg-no-repeat self-center',
      singleLabel: 'multiselect-single-label min-w-max! px-2! static!',
      option: ' flex flex-col py-0 px-2 m-0 list-none',
      optionSelected: ' bg-primary/15',
      optionPointed: ' bg-primary/10',
      optionSelectedPointed: ' bg-primary/20',
      caret: ' multiselect-caret mask-image-multiselect-caret bg-primary! bg-none!'
    }"
  />
</template>

<!-- todo: remove this once https://github.com/vueform/multiselect/pull/442 is merged  -->
<!-- eslint-disable-next-line vue/no-restricted-block -->
<style>
@reference "../assets/main.css";

.multiselect {
  @apply relative mx-auto box-border flex w-full cursor-pointer items-center justify-end rounded-sm border border-gray-300 bg-white text-base leading-snug outline-hidden;
}
.multiselect.is-disabled {
  @apply cursor-default bg-gray-100;
}
.multiselect.is-open {
  @apply rounded-b-none;
}
.multiselect.is-open-top {
  @apply rounded-t-none;
}
.multiselect.is-active {
  @apply ring-3 ring-green-500/30;
}

.multiselect-wrapper {
  @apply relative mx-auto box-border flex w-full cursor-pointer items-center justify-end outline-hidden;
}

.multiselect-single-label {
  @apply pointer-events-none absolute top-0 left-0 box-border flex h-full max-w-full items-center bg-transparent pr-16 pl-3.5 leading-snug rtl:right-0 rtl:left-auto rtl:pr-3.5 rtl:pl-0;
}

.multiselect-single-label-text {
  @apply block max-w-full overflow-hidden text-ellipsis whitespace-nowrap;
}

.multiselect-multiple-label {
  @apply pointer-events-none absolute top-0 left-0 flex h-full items-center bg-transparent pl-3.5 leading-snug rtl:right-0 rtl:left-auto rtl:pr-3.5 rtl:pl-0;
}

.multiselect-search {
  @apply absolute inset-0 box-border w-full appearance-none rounded-sm border-0 bg-white pl-3.5 font-sans text-base outline-hidden focus:ring-0 rtl:pr-3.5 rtl:pl-0;
}

.multiselect-tags {
  @apply mt-1 flex min-w-0 shrink grow flex-wrap items-center pl-2 rtl:pr-2 rtl:pl-0;
}

.multiselect-tag {
  @apply mr-1 mb-1 flex min-w-0 items-center rounded-sm bg-green-500 py-0.5 pl-2 text-sm font-semibold whitespace-nowrap text-white rtl:mr-0 rtl:ml-1 rtl:pr-2 rtl:pl-0;
}
.multiselect-tag.is-disabled {
  @apply pr-2 opacity-50 rtl:pl-2;
}

.multiselect-tag-wrapper {
  @apply overflow-hidden text-ellipsis whitespace-nowrap;
}

.multiselect-tag-wrapper-break {
  @apply break-all whitespace-normal;
}

.multiselect-tag-remove {
  @apply mx-0.5 flex items-center justify-center rounded-xs p-1 hover:bg-black/10;
}

.multiselect-tag-remove-icon {
  @apply bg-multiselect-remove inline-block h-3 w-3 bg-center bg-no-repeat opacity-30;
}

.multiselect-tag-remove:hover .multiselect-tag-remove-icon {
  @apply opacity-60;
}

.multiselect-tags-search-wrapper {
  @apply relative mx-1 mb-1 inline-block h-full shrink grow;
}

.multiselect-tags-search {
  @apply absolute inset-0 box-border w-full appearance-none border-0 p-0 font-sans text-base outline-hidden focus:ring-0;
}

.multiselect-tags-search-copy {
  @apply invisible inline-block h-px whitespace-pre-wrap;
}

.multiselect-placeholder {
  @apply pointer-events-none absolute top-0 left-0 flex h-full items-center bg-transparent pl-3.5 leading-snug text-gray-400 rtl:right-0 rtl:left-auto rtl:pr-3.5 rtl:pl-0;
}

.multiselect-caret {
  @apply bg-multiselect-caret pointer-events-none relative z-10 mr-3.5 box-content h-4 w-2.5 shrink-0 grow-0 transform bg-center bg-no-repeat py-px opacity-40 transition-transform rtl:mr-0 rtl:ml-3.5;
}
.multiselect-caret.is-open {
  @apply pointer-events-auto rotate-180;
}

.multiselect-clear {
  @apply relative z-10 flex shrink-0 grow-0 pr-3.5 opacity-40 transition duration-300 hover:opacity-80 rtl:pr-0 rtl:pl-3.5;
}

.multiselect-clear-icon {
  @apply bg-multiselect-remove box-content inline-block h-4 w-2.5 bg-center bg-no-repeat py-px;
}

.multiselect-spinner {
  @apply bg-multiselect-spinner z-10 mr-3.5 h-4 w-4 shrink-0 grow-0 animate-spin bg-center bg-no-repeat rtl:mr-0 rtl:ml-3.5;
}

.multiselect-inifite {
  @apply flex w-full items-center justify-center;
}

.multiselect-inifite-spinner {
  @apply bg-multiselect-spinner z-10 m-3.5 h-4 w-4 shrink-0 grow-0 animate-spin bg-center bg-no-repeat;
}

.multiselect-dropdown {
  @apply absolute -right-px bottom-0 -left-px z-50 -mt-px flex max-h-60 translate-y-full transform flex-col overflow-y-scroll rounded-b-sm border border-gray-300 bg-white;
}
.multiselect-dropdown.is-top {
  @apply top-px bottom-auto -translate-y-full rounded-t-sm rounded-b-none;
}
.multiselect-dropdown.is-hidden {
  @apply hidden;
}

.multiselect-options {
  @apply m-0 flex list-none flex-col p-0;
}

.multiselect-group {
  @apply m-0 p-0;
}

.multiselect-group-label {
  @apply box-border flex cursor-default items-center justify-start bg-gray-200 px-3 py-1 text-left text-sm leading-normal font-semibold;
}
.multiselect-group-label.is-pointable {
  @apply cursor-pointer;
}
.multiselect-group-label.is-pointed {
  @apply bg-gray-300 text-gray-700;
}
.multiselect-group-label.is-selected {
  @apply bg-green-600 text-white;
}
.multiselect-group-label.is-disabled {
  @apply cursor-not-allowed bg-gray-100 text-gray-300;
}
.multiselect-group-label.is-selected.is-pointed {
  @apply bg-green-600 text-white opacity-90;
}
.multiselect-group-label.is-selected.is-disabled {
  @apply cursor-not-allowed bg-green-600/50 text-green-100;
}

.multiselect-group-options {
  @apply m-0 p-0;
}

.multiselect-option {
  @apply box-border flex cursor-pointer items-center justify-start px-3 py-2 text-left text-base leading-snug;
}
.multiselect-option.is-pointed {
  @apply bg-gray-100 text-gray-800;
}
.multiselect-option.is-selected {
  @apply bg-green-500 text-white;
}
.multiselect-option.is-disabled {
  @apply cursor-not-allowed text-gray-300;
}
.multiselect-option.is-selected.is-pointed {
  @apply bg-green-500 text-white opacity-90;
}
.multiselect-option.is-selected.is-disabled {
  @apply cursor-not-allowed bg-green-500/50 text-green-100;
}

.multiselect-no-options {
  @apply bg-white px-3 py-2 text-left text-gray-600 rtl:text-right;
}

.multiselect-no-results {
  @apply bg-white px-3 py-2 text-left text-gray-600 rtl:text-right;
}

.multiselect-fake-input {
  @apply absolute right-0 -bottom-px left-0 h-px w-full appearance-none border-0 bg-transparent p-0 text-transparent outline-hidden;
}

.multiselect-assistive-text {
  @apply absolute -m-px h-px w-px overflow-hidden;
  clip: rect(0 0 0 0);
}

.multiselect-spacer {
  @apply box-content h-9 py-px;
}
</style>
