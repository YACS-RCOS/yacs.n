<template>
  <div>
    <b-form-select
      v-model="selectedScheduleSubsemester"
      :options="subsemesterOptions"
    ></b-form-select>
    <Schedule
      v-for="({ subsemester, scheduleCourseSections },
      index) of courseSectionsPerSubsemester"
      v-show="subsemesterOptions[index].value === selectedScheduleSubsemester"
      :key="subsemester.display_string"
      :course-sections="scheduleCourseSections"
    ></Schedule>
  </div>
</template>

<script>
import { withinDuration, withinCourseDuration } from "@/utils";

// import SubsemesterScheduler from "@/controllers/SubsemesterScheduler";

import Schedule from "./Schedule";

export default {
  name: "SubsemesterSchedule",
  components: {
    Schedule,
  },
  props: {
    // /** @type {import('vue').PropOptions<SubSemesterScheduler>} */
    // scheduler: {
    //   type: SubsemesterScheduler,
    //   default: () => new SubsemesterScheduler(),
    // },
    // loading: {
    //   type: Boolean,
    //   default: false,
    // },
    /** @type {import("vue").PropType<import("@/typedef").CourseSection[]>} */
    courseSections: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      selectedScheduleSubsemester: null,
    };
  },
  computed: {
    /** @returns {import("@/typedef").Subsemester[]} */
    subsemesters() {
      return this.$store.state.subsemesters.filter(
        (s, i, arr) =>
          arr.length == 1 ||
          !arr.every((o, oi) => oi == i || withinDuration(s, o))
      );
    },
    subsemesterOptions() {
      return this.subsemesters.map((subsemester, index) => ({
        text: subsemester.display_string,
        value: index === 0 ? null : subsemester.display_string,
      }));
    },
    courseSectionsPerSubsemester() {
      const courseSectionsPerSubsemester = this.subsemesters.map(
        (subsemester) => ({
          subsemester,
          scheduleCourseSections: [],
        })
      );

      for (const courseSection of this.courseSections) {
        for (const schedule of courseSectionsPerSubsemester) {
          if (
            withinCourseDuration(courseSection.course, schedule.subsemester)
          ) {
            schedule.scheduleCourseSections.push(courseSection);
          }
        }
      }

      return courseSectionsPerSubsemester;
    },
  },
};
</script>

<style></style>
