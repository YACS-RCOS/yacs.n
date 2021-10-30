<template>
  <div
    class="schedule"
    :style="{ height: totalVHeight + 'vh', 'min-height': minHeight + 'px' }"
    data-cy="schedule"
  >
    <div class="schedule-legend">
      <div
        class="hour-label"
        v-for="(hour, index) of hours"
        :key="hour"
        :style="{ height: hourHeight + '%' }"
      >
        <div v-if="index != 0">{{ hour }}</div>
      </div>
    </div>

    <div class="schedule-grid">
      <div
        class="grid-day"
        v-for="(day, index) of days"
        :key="day.longname"
        :style="{ width: dayWidth + '%' }"
      >
        <div class="day-label">{{ day.longname }}</div>
        <div v-for="(section, k) in temp.sections" :key="k" class="section-overlay">
          <ScheduleEvent
            v-for="(session, j) in getSessionsOfDay(section, index)" :key="j"

            :crn="session.crn"
            :section="session.section"
            :semester="session.semester"
            :name="section.department + ' ' + section.level"
            :title="section.title"
            :style="{
              'margin-top':
                'max(' +
                eventPosition(session) +
                'vh,' +
                eventPosition(session, minHeight) +
                'px)',
              height: eventHeight(session) + 'vh',
              'min-height': eventHeight(session, minHeight) + 'px',
              backgroundColor: getBackgroundColor(session),
              borderColor: getBorderColor(session),
              color: getTextColor(session),
              width: '100%'
            }"
          ></ScheduleEvent>
        </div>
        <div
          class="grid-hour"
          v-for="hour of hours"
          :key="hour"
          :style="{ height: hourHeight + '%' }"
        ></div>
      </div>
    </div>
  </div>
</template>
<script>
import "@/typedef";

import { DAY_LONGNAMES, DAY_SHORTNAMES, hourName, toMinutes } from "@/utils";

import {
  getBackgroundColor,
  getBorderColor,
  getTextColor,
} from "@/services/ColorService";

import ScheduleEventComponent from "@/components/ScheduleEvent";

export default {
  name: "Schedule",
  components: {
    ScheduleEvent: ScheduleEventComponent,
  },
  props: {
    possibility: {
      default: () => []
    },
  },
  data() {
    return {
      startDay: 1,
      endDay: 5,
      startTime: 480,
      endTime: 1320,
      totalVHeight: 70,
      minHeight: 600,
      temp: this.possibility
    };
  },
  methods: {
    getBackgroundColor,
    getBorderColor,
    getTextColor,
    /**
     * Calculate the height of the schedule block for `courseSession`
     * Returns normalized height, i.e. height * duration_percentage
     * @param {CourseSession} courseSession
     * @param {number} totalHeight totalVHeight as default
     * @returns {number}
     */
    eventHeight(courseSession, totalHeight = this.totalVHeight) {
      const eventDuration =
        toMinutes(courseSession.time_end) - toMinutes(courseSession.time_start);
      return totalHeight * (eventDuration / this.numMinutes);
    },
    /**
     * Calculate the position of the schedule block for `courseSession`
     * Returns normalized position, i.e. height * before_percentage
     * @param {CourseSession} courseSession
     * @param {number} totalHeight totalVHeight as default
     * @returns {number}
     */
    eventPosition(courseSession, totalHeight = this.totalVHeight) {
      const eventStart = toMinutes(courseSession.time_start);
      return totalHeight * ((eventStart - this.startTime) / this.numMinutes);
    },
    /**
     * Returns the `CourseSession`s in the given dayOfWeek
     * @param {number} dayOfWeek
     * @return {CourseSession[]}
     */
    
    getSessionsOfDay(section, day) {
      return section.sessions.filter(session => session.day_of_week === day)
    },
  },
  computed: {
    /**
     * Returns the number of days in this schedule
     */
    numDays() {
      return this.endDay - this.startDay + 1;
    },
    /**
     * Returns the total number of minutes in one day for this schedule
     */
    numMinutes() {
      return this.endTime - this.startTime;
    },
    /**
     * Returns a list of hour breakpoints for the schedule legend
     */
    hours() {
      const hours = [];
      for (let time = this.startTime; time < this.endTime; time += 60) {
        hours.push(hourName(time));
      }
      return hours;
    },
    /**
     * Returns a list of names for days of the week
     */
    days() {
      const days = [];
      for (let day = this.startDay; day <= this.endDay; ++day) {
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
  watch: {
    possibility(val) {
      this.temp = val
    }
  }
};
</script>

<style scoped lang="scss">
$labelOffset: 0.35em;
$hourFontSize: 0.5em;

.schedule {
  margin-top: 10px;
  margin-right: 15px;
  position: relative; /* so the overlay will position properly */
  margin-bottom: 15px;
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

.section-overlay {
  position: absolute;
  width: 20%;
  height: 100%;
}
</style>
