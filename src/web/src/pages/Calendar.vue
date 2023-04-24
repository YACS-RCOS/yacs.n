<template>
  <div
    class="schedule"
    :style="{ height: totalVHeight + 'vh', 'min-height': minHeight + 'px' }"
    data-cy="schedule"
  >
    <div class="schedule-legend">
      <div
        class="hour-label"
        v-for="hour of hours"
        :key="hour"
        :style="{ height: hourHeight + '%' }"
      >
        <div>{{ hour }}</div>
      </div>
    </div>
    <div class="schedule-grid">
      <div
        class="grid-day"
        v-for="day of days"
        :key="day.longname"
        :style="{ width: dayWidth + '%' }"
      >
        <div class="day-label">{{ day.longname }}</div>
        <ScheduleEvent
          v-for="exam in filteredExams"
          :key="exam.id"
          :day="exam.dayOfWeek"
          :startTime="exam.time_start.split('T')[1].split(':').slice(0, 2).join(':')"
          :endTime="exam.time_end.split('T')[1].split(':').slice(0, 2).join(':')"
          :section="exam.section"
          :name="exam.course"
          :location="exam.room"
          :title="exam.course + ' - ' + exam.section"
          :style="{
            'margin-top':
              'max(calc(' +
              eventPosition(exam) +
              'vh + 1px),' +
              eventPosition(exam, minHeight) +
              1 +
              'px)',
            height: 'calc(' + eventHeight(exam) + 'vh - 1px)',
            'min-height': eventHeight(exam, minHeight) - 1 + 'px',
            backgroundColor: getEventColor(exam),
            borderColor: getBorderColor(exam.course),
            color: getTextColor(exam.course),
            width: 'calc(100% - 1px)',
          }"
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
import "@/typedef";

import { DAY_LONGNAMES, DAY_SHORTNAMES, hourName, toMinutes } from "@/utils";

import {
  getBackgroundColor,
  getBorderColor,
  getTextColor,
} from "@/services/ColorService";

import ScheduleEventComponent from "./CalendarEvent.vue";


export default {
  name: "Schedule",
  components: {
    ScheduleEvent: ScheduleEventComponent,
  },
  props: {
    possibility: {
      default: () => [],
    },
    examDetails: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      startDay: 1,
      endDay: 5,
      startTime: 480,
      endTime: 1320,
      totalVHeight: 80,
      minHeight: 600,
      sessionTypes: {
        LEC: "Lecture",
        REC: "Recitation",
        LAB: "Lab",
        TES: "Test",
        STU: "Studio",
        null: "No Type",
      },
    };
  },
  methods: {
    getEventColor(session) {
      if (session.department === "CSCI") {
        return "#ff7f50";
      } else if (session.department === "ARTS") {
        return "#6495ed";
      }
      return "#3a3";
    },
    getBackgroundColor,
    getBorderColor,
    getTextColor,

    eventPosition(exam, minHeight, totalHeight = this.totalVHeight) {
      const dayIndex = this.days.findIndex(day => day.longname === exam.dayOfWeek);
      const startMinutes = toMinutes(exam.startTime);
      const dayStartMinutes = this.startTime + (dayIndex * this.numMinutes);
      const minutesFromStartOfDay = startMinutes - dayStartMinutes;
      const positionPercent = (minutesFromStartOfDay / this.numMinutes) * 100;
      const positionPixels = (positionPercent / 100) * totalHeight;
      const minHeightPixels = (minHeight / this.numMinutes) * totalHeight;
      return Math.max(minHeightPixels + 1, positionPixels + 1); // add 1px for the border
    },

    eventHeight(exam, minHeight, totalHeight = this.totalVHeight) {
      const startMinutes = toMinutes(exam.startTime);
      const endMinutes = toMinutes(exam.endTime);
      const durationMinutes = endMinutes - startMinutes;
      const durationPercent = (durationMinutes / this.numMinutes) * 100;
      const durationPixels = (durationPercent / 100) * totalHeight;
      const minHeightPixels = (minHeight / this.numMinutes) * totalHeight;
      return Math.max(minHeightPixels - 1, durationPixels - 1); // subtract 1px for the border
    },


    getSessionsOfDay(section, day) {
      return section && section.sessions
        ? section.sessions.filter((session) => session.day_of_week === day)
        : [];
    },

    mapSessionType(type) {
      return this.sessionTypes[type] == null ? type : this.sessionTypes[type];
    },
  },
  computed: {
    filteredExams() {
      return this.examDetails.filter((exam) => {
        const day = this.days.find((day) => day.longname.includes(exam.dayOfWeek));
        return day !== undefined;
      });
    },
    numDays() {
      return this.endDay - this.startDay + 1;
    },

    numMinutes() {
      return this.endTime - this.startTime;
    },

    hours() {
      const hours = [];
      for (let time = this.startTime; time < this.endTime; time += 60) {
        hours.push(hourName(time));
      }
      return hours;
    },

    days() {
      const days = [];
      const startDate = new Date(2023, 4, 1); // Adjust the starting date as needed (Year, Month - 1, Day)

      for (let day = this.startDay; day <= this.endDay; ++day) {
        const currentDate = new Date(startDate);
        currentDate.setDate(startDate.getDate() + (day - this.startDay));
        const formattedDate = currentDate.toLocaleString("en-US", {
          month: "short",
          day: "2-digit",
        });

        days.push({
          longname: DAY_LONGNAMES[day] + " (" + formattedDate + ")",
          shortname: DAY_SHORTNAMES[day],
        });
      }
      return days;
    },


    dayWidth() {
      return 100 / this.numDays;
    },

    hourHeight() {
      return (60 * 100) / this.numMinutes;
    },
  },
  watch: {
    possibility(val) {
      this.temp = val;
      console.log(this.temp);
    },
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
  pointer-events: none;
}
</style>