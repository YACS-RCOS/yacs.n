import { getCourses, getDepartments } from "@/api/class";
import { getSemesters } from "@/api/semester";
import { computedAsync, StorageSerializers, useAsyncState, useLocalStorage } from "@vueuse/core";
import { defineStore } from "pinia";
import { computed } from "vue";

const useClassInfoStorePrivate = defineStore("class-info-private", () => {
  const semesters = useAsyncState(getSemesters(), null).state;
  const departments = useAsyncState(getDepartments(), null).state;

  const courses = computed(() =>
    Object.fromEntries(
      (semesters.value ?? []).map((sem) => {
        const thing = computedAsync(async () => await getCourses(sem), null, { lazy: true });
        return [sem, thing as typeof thing | undefined];
      })
    )
  );

  return {
    semesters,
    courses,
    departments
  };
});

export const useClassInfoStore = defineStore("class-info", () => {
  const readOnlyState = useClassInfoStorePrivate();

  const selectedSemester = useLocalStorage<string | null>("classinfo/selected_semester", null, {
    serializer: StorageSerializers.string
  });
  const semesters = computed(() => readOnlyState.semesters);
  const courses = computed(() => readOnlyState.courses);
  const departments = computed(() => readOnlyState.departments);
  const current_courses = computed(() =>
    selectedSemester.value ? courses.value[selectedSemester.value]?.value : null
  );

  return {
    selectedSemester,
    semesters,
    courses,
    current_courses,
    departments
  };
});
