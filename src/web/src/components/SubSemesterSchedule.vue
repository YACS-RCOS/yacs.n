<template>
  <div>
    <b-form-select
      v-model="selectedScheduleSubsemester"
      :options="subSemesters"
      text-field="display_string"
      value-field="display_string"
    ></b-form-select>
    {{ selectedScheduleSubsemester }}
    <Schedule
      v-for="(schedule, index) in scheduler.schedules"
      :key="index"
      :schedule="schedule"
      v-show="
        subSemesters[index].display_string === selectedScheduleSubsemester
      "
    ></Schedule>
  </div>
</template>

<script>
import "@/typedef";

import { withinDuration } from "@/utils";

import SubSemesterScheduler from "@/controllers/SubSemesterScheduler";

import Schedule from "./Schedule";

export default {
  name: "SubSemesterSchedule",
  components: {
    Schedule,
  },
  props: {
    /** @type {import('vue').PropOptions<SubSemesterScheduler>} */
    scheduler: {
      type: SubSemesterScheduler,
      default: () => new SubsemesterScheduler(),
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      selectedScheduleSubsemester: this.subSemesters[0],
    };
  },
  computed: {
    subSemesters() {
      return this.scheduler.subSemesters.filter(
        (s, i, arr) =>
          arr.length == 1 ||
          !arr.every((o, oi) => oi == i || withinDuration(s, o))
      );
    },
  },
};
</script>

<style></style>
