<template>
  <div>
    <div v-if="hasConflict" class="alert alert-danger">
      Can't display because of course conflict!
    </div>
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
            v-for="exam in filteredExams(day)"
            :key="exam.id"
            :day="exam.dayOfWeek"
            :startTime="
              exam.time_start.split('T')[1].split(':').slice(0, 2).join(':')
            "
            :endTime="
              exam.time_end.split('T')[1].split(':').slice(0, 2).join(':')
            "
            :section="exam.section"
            :name="exam.course"
            :location="exam.room"
            :time="exam.time"
            :title="exam.course"
            :style="{
              'margin-top': eventPosition(exam.time) + 'vh',
              height: eventHeight(exam.time) + '%',
              backgroundColor: getBackgroundColor(
                getCourseDepartmentAndLevel(exam.course)
              ),
              borderColor: getBorderColor(
                getCourseDepartmentAndLevel(exam.course)
              ),
              color: getTextColor(getCourseDepartmentAndLevel(exam.course)),
              width: 20 + '%',
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
  </div>
</template>

<script>
import "@/typedef";

import { DAY_LONGNAMES, DAY_SHORTNAMES, hourName } from "@/utils";

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
    getCourseDepartmentAndLevel(course) {
      const [department, , level] = course.split(" ");
      return department + "-" + level;
    },
    getBackgroundColor,
    getBorderColor,
    getTextColor,

    timeToMinutes(time) {
      const [, hours, minutes, ampm] = time.match(/(\d+):(\d+)(AM|PM)/);
      let hours24 = parseInt(hours, 10);
      if (ampm === "PM" && hours24 !== 12) hours24 += 12;
      if (ampm === "AM" && hours24 === 12) hours24 = 0;
      return hours24 * 60 + parseInt(minutes, 10);
    },

    eventPosition(timeRange) {
      const timeString = timeRange.split("-")[0];
      const eventStart = this.timeToMinutes(timeString);
      const timeOffSet = eventStart - 8 * 60;
      return (timeOffSet * 80) / 14 / 60;
    },

    eventHeight(timeRange) {
      const timeStart = timeRange.split("-")[0];
      const timeEnd = timeRange.split("-")[1];
      const eventStart = this.timeToMinutes(timeStart);
      const eventEnd = this.timeToMinutes(timeEnd);
      const diff = eventEnd - eventStart;
      return (diff * 7.14286) / 60;
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
    hasConflict() {
      const conflicts = new Set();
      for (const exam1 of this.examDetails) {
        for (const exam2 of this.examDetails) {
          if (
            exam1 !== exam2 &&
            exam1.course !== exam2.course &&
            exam1.day === exam2.day &&
            exam1.time === exam2.time
          ) {
            conflicts.add(exam1);
            conflicts.add(exam2);
          }
        }
      }
      return conflicts.size > 0;
    },
    filteredExams() {
      return (day) => {
        if (this.hasConflict) {
          return [];
        }
        const examsWithoutDuplicates = [];
        const seenExams = new Set();

        for (const exam of this.examDetails.filter((exam) => {
          return exam.dayOfWeek === day.longname.split(" ")[0];
        })) {
          const identifier = exam.course + "-" + exam.time;

          if (!seenExams.has(identifier)) {
            seenExams.add(identifier);
            examsWithoutDuplicates.push(exam);
          } else {
            const existingExam = examsWithoutDuplicates.find(
              (e) => e.course === exam.course && e.time === exam.time
            );
            const existingRooms = existingExam.room
              .split(", ")
              .concat(exam.room.split(", "));
            const uniqueRooms = [...new Set(existingRooms)];
            existingExam.room = uniqueRooms.join(", ");
          }
        }
        return examsWithoutDuplicates;
      };
    },
    uniqueExams() {
      const examsWithoutDuplicates = [];
      const seenExams = new Set();

      for (const exam of this.examDetails) {
        const identifier = exam.course + "-" + exam.time;

        if (!seenExams.has(identifier)) {
          seenExams.add(identifier);
          examsWithoutDuplicates.push(exam);
        } else {
          const existingExam = examsWithoutDuplicates.find(
            (e) => e.course === exam.course && e.time === exam.time
          );
          const existingRooms = existingExam.room
            .split(", ")
            .concat(exam.room.split(", "));
          const uniqueRooms = [...new Set(existingRooms)];
          existingExam.room = uniqueRooms.join(", ");
        }
      }
      return examsWithoutDuplicates;
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
      const startDate = new Date(2023, 4, 1);

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
  position: relative;
  margin-bottom: 15px;
  margin-bottom: 50px;
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
  font-size: 0.85vw;
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

.section- {
  position: absolute;
  width: 20%;
  height: 100%;
  pointer-events: none;
}
</style>
