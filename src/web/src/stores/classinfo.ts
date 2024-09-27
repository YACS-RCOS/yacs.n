import { getSemesters } from "@/api/semester";
import { useAsyncState } from "@vueuse/core";
import { defineStore } from "pinia";
import { computed } from "vue";

const useClassInfoStorePrivate = defineStore("class-info-private", () => {
  const semesters = useAsyncState(getSemesters(), []).state;

  return {
    semesters
  };
});

export const useClassInfoStore = defineStore("class-info", () => {
  const readOnlyState = useClassInfoStorePrivate();

  return {
    semesters: computed(() => readOnlyState.semesters)
  };
});
