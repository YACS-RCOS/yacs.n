<template>
  <div
    class="schedule"
    :style="{ height: totalHeight + 'px' }"
    data-cy="schedule"
  >
    <div class="schedule-legend">
      <div
        v-for="(hour, index) of hours"
        :key="hour"
        class="hour-label"
        :style="{ height: hourHeight + '%' }"
      >
        <div v-if="index != 0">{{ hour }}</div>
      </div>
    </div>

    <div class="schedule-grid">
      <div
        v-for="(day, index) of days"
        :key="day.longname"
        class="grid-day"
        :style="{ width: dayWidth + '%' }"
      >
        <div class="day-label">{{ day.longname }}</div>
        <ScheduleEvent
          v-for="courseSession in courseSessionsPerDay[index]"
          :key="courseSession.crn + courseSession.time_start"
          :crn="courseSession.crn"
          :section="courseSession.section"
          :semester="courseSession.semester"
          :name="`${courseSession.course.department}-${courseSession.course.level}`"
          :title="courseSession.course.title"
          :style="{
            'margin-top': eventPosition(courseSession) + 'px',
            height: eventHeight(courseSession) + 'px',
            backgroundColor: getBackgroundColor(courseSession.course.id),
            borderColor: getBorderColor(courseSession.course.id),
            color: getTextColor(courseSession.course.id),
            width: dayWidth + '%',
          }"
        ></ScheduleEvent>
        <div
          v-for="hour of hours"
          :key="hour"
          class="grid-hour"
          :style="{ height: hourHeight + '%' }"
        ></div>
      </div>
    </div>
  </div>
</template>
<script>
import { DAY_LONGNAMES, DAY_SHORTNAMES, hourName, toMinutes } from "@/utils";

import { COLOR_NAMESPACE } from "@/store/modules/color";
import { mapGetters } from "vuex";

// import {
//   getBackgroundColor,
//   getBorderColor,
//   getTextColor,
// } from "@/services/ColorService";

import ScheduleEventComponent from "@/components/ScheduleEvent";

const START_DAY = 1;
const END_DAY = 5;
const START_TIME = 480;
const END_TIME = 1320;
const TOTAL_HEIGHT = 600;

export default {
  name: "Schedule",
  components: {
    ScheduleEvent: ScheduleEventComponent,
  },
  props: {
    /** @type {import("vue").PropType<import("@/typedef").CourseSection[]>} */
    courseSections: {
      type: Array,
      default: () => [],
    },
  },

  data() {
    return {
      totalHeight: TOTAL_HEIGHT,
    };
  },
  computed: {
    ...mapGetters(COLOR_NAMESPACE, [
      "getBackgroundColor",
      "getTextColor",
      "getBorderColor",
    ]),
    courseSessionsPerDay() {
      const courseSessionsPerDay = Array.from({
        length: this.numDays,
      }).map(() => []);

      this.courseSessions.forEach((courseSession) => {
        courseSessionsPerDay[courseSession.day_of_week].push(courseSession);
      });

      courseSessionsPerDay.forEach((courseSessions) =>
        courseSessions.sort(
          (session1, session2) => session2.time_start - session1.time_start
        )
      );

      return courseSessionsPerDay;
    },
    /**
     * @returns {import("@/typedef").CourseSession[]}
     */
    courseSessions() {
      return this.courseSections.map((section) => section.sessions).flat();
    },
    /**
     * Returns the number of days in this schedule
     */
    numDays() {
      return END_DAY - START_DAY + 1;
    },
    /**
     * Returns the total number of minutes in one day for this schedule
     */
    numMinutes() {
      return END_TIME - START_TIME;
    },
    /**
     * Returns a list of hour breakpoints for the schedule legend
     */
    hours() {
      const hours = [];
      for (let time = START_TIME; time < END_TIME; time += 60) {
        hours.push(hourName(time));
      }
      return hours;
    },
    /**
     * Returns a list of names for days of the week
     *
     * @returns {{longname: string, shortname: string}[]}
     */
    days() {
      const days = [];
      for (let day = START_DAY; day <= END_DAY; ++day) {
        days.push({
          longname: DAY_LONGNAMES[day],
          shortname: DAY_SHORTNAMES[day],
        });
      }
      return days;
    },
    /**
     * Return % width for each column
     */
    dayWidth() {
      return 100 / this.numDays;
    },
    /**
     * Return % height for each hour row
     */
    hourHeight() {
      return (60 * 100) / this.numMinutes;
    },
  },
  methods: {
    // getBackgroundColor,
    // getBorderColor,
    // getTextColor,
    /**
     * Calculate the height of the schedule block for `courseSession`
     * Returns the px height
     *
     * @param {CourseSession} courseSession
     * @returns {number}
     */
    eventHeight(courseSession) {
      const eventDuration =
        toMinutes(courseSession.time_end) - toMinutes(courseSession.time_start);
      return TOTAL_HEIGHT * (eventDuration / this.numMinutes);
    },
    /**
     * Calculate the position of the schedule block for `courseSession`
     * Returns the px margin-top
     *
     * @param {CourseSession} courseSession
     * @returns {number}
     */
    eventPosition(courseSession) {
      const eventStart = toMinutes(courseSession.time_start);
      return TOTAL_HEIGHT * ((eventStart - START_TIME) / this.numMinutes);
    },
    // /**
    //  * Returns the `CourseSession`s in the given dayOfWeek
    //  *
    //  * @param {number} dayOfWeek
    //  * @returns {CourseSession[]}
    //  */
    // courseSessionsOnDay(dayOfWeek) {
    //   return this.schedule.dailySessions[dayOfWeek];
    // },
  },
};
</script>

<style scoped lang="scss">
$labelOffset: 0.35em;
$hourFontSize: 0.5em;

.schedule {
  margin-top: 10px;
  margin-right: 15px;
  position: relative; /* so the overlay will position properly */
  // margin-bottom: 15px;
  margin-bottom: 30px;
}

.schedule-legend {
  position: absolute;
  height: 100%;
  left: $labelOffset;
  top: 0.7em;
}

.hour-label {
  color: #777777;
  font-size: $hourFontSize;
  text-align: right;
  font-variant: small-caps;
}

.schedule-grid {
  position: absolute;
  width: calc(100% - #{$hourFontSize + $labelOffset + 1.75em});
  height: 100%;
  left: 2.5em;
}

.day-label {
  color: #777777;
  display: block;
  margin: 0 auto;
  margin-bottom: 3px;
  text-align: center;
  font-size: 0.8em;
  font-variant: small-caps;
}

.grid-day {
  height: 100%;
  float: left;
}

.grid-hour {
  display: block;
  box-sizing: border-box;
  border-top: 1px solid #e7e7e7;
  border-right: 1px solid #e7e7e7;
}

.grid-day:last-of-type .grid-hour {
  border-right: none;
}
</style>
