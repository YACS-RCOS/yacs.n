<template>
  <div class="schedule" :style="{ height: totalHeight + 'px' }">
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
        <ScheduleEvent
          v-for="courseSession in courseSessionsOnDay(index)"
          :key="courseSession.crn + courseSession.day_of_week + courseSession.time_start"
          :crn="courseSession.crn"
          :section="courseSession.section"
          :semester="courseSession.semester"
          :style="{
            'margin-top': eventPosition(courseSession) + 'px',
            height: eventHeight(courseSession) + 'px',
            backgroundColor: ColorService.getBackgroundColor(courseSession),
            borderColor: ColorService.getBorderColor(courseSession),
            color: ColorService.getTextColor(courseSession),
            width: dayWidth + '%'
          }"
          class="schedule-event"
        ></ScheduleEvent>
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
/**
 * @typedef {import('@/index').CourseSession} CourseSession
 */
import { DAY_LONGNAMES, DAY_SHORTNAMES, hourName, toMinutes } from '@/utils';

import ColorService from '@/services/ColorService';
import Schedule from '@/services/ScheduleService';

import ScheduleEventComponent from '@/components/ScheduleEvent';

export default {
  name: 'Schedule',
  components: {
    ScheduleEvent: ScheduleEventComponent
  },
  props: {
    schedule: Schedule
  },
  data() {
    return {
      startDay: 1,
      endDay: 5,
      startTime: 480,
      endTime: 1320,
      totalHeight: 600,

      ColorService
    };
  },
  methods: {
    /**
     * Calculate the height of the schedule block for `courseSession`
     * Returns the px height
     * @param {CourseSession} courseSession
     * @returns {number}
     */
    eventHeight(courseSession) {
      const eventDuration = toMinutes(courseSession.time_end) - toMinutes(courseSession.time_start);
      return this.totalHeight * (eventDuration / this.numMinutes);
    },
    /**
     * Calculate the position of the schedule block for `courseSession`
     * Returns the px margin-top
     * @param {CourseSession} courseSession
     * @returns {number}
     */
    eventPosition(courseSession) {
      const eventStart = toMinutes(courseSession.time_start);
      return this.totalHeight * ((eventStart - this.startTime) / this.numMinutes);
    },
    /**
     * Returns the `CourseSession`s in the given dayOfWeek
     * @param {number} dayOfWeek
     * @return {CourseSession[]}
     */
    courseSessionsOnDay(dayOfWeek) {
      return this.schedule.dailySessions[dayOfWeek];
    }
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
        days.push({ longname: DAY_LONGNAMES[day], shortname: DAY_SHORTNAMES[day] });
      }
      return days;
    },
    /**
     * Return % width for each column
     */
    dayWidth() {
      return 100 / this.numDays - 1;
    },
    /**
     * Return % height for each hour row
     */
    hourHeight() {
      return (60 * 100) / this.numMinutes;
    }
  }
};
</script>

<style scoped lang="scss">
.schedule {
  margin-right: 15px;
  margin-top: 10px;
  position: relative; /* so the overlay will position properly */
  margin-bottom: 15px;
}

.schedule-legend {
  position: absolute;
  height: 100%;
  left: 0.35em;
  top: 0.7em;
}

.hour-label {
  color: #777777;
  font-size: 0.5em;
  text-align: right;
  font-variant: small-caps;
}

.schedule-grid {
  position: absolute;
  width: 100%;
  height: 100%;
  left: 2.5em;
}

.day-label {
  color: #777777;
  display: block;
  margin: 0 auto;
  text-align: center;
  font-size: 0.8em;
  font-variant: small-caps;
}

.grid-day {
  //width: 1000;
  height: 100%;
  float: left;
}

.grid-hour {
  display: block;
  box-sizing: border-box;
  border-top: 1px solid #e7e7e7;
  border-right: 1px solid #e7e7e7;
  //position: relative;
}

.grid-day:last-of-type .grid-hour {
  border-right: none;
}
</style>
