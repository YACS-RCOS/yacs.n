import { getSemesters } from "@/api/semester";
import { useAsyncState } from "@vueuse/core";
import { defineStore } from "pinia";
import { computed, ref } from "vue";

const useClassInfoStorePrivate = defineStore("class-info-private", () => {
  const semesters = useAsyncState(getSemesters(), null).state;

  return {
    semesters
  };
});

export const useClassInfoStore = defineStore("class-info", () => {
  const readOnlyState = useClassInfoStorePrivate();

  return {
    selectedSemester: ref<string | null>(null),
    semesters: computed(() => readOnlyState.semesters)
  };
});
