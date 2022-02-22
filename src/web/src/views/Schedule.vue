<script setup>
// import {semesters} from "../utils/core/semester";
import {currentSchedule, scheduleIndex, currentSchedules} from "../utils/core/scheduler";
import {computed} from "vue";

const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
const hours = ['8am', '9am', '10am', '11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm']

const getStyleBySession = (session, color) => {
  console.log(color)
  return {
    boxSizing: 'border-box',
    overflow: 'hidden',
    height: ((session.time.duration - 1 / 6) * 100 / 28) + '%',
    width: '20%',
    display: 'inline-block',
    top: (session.time.start * 100 / 28) + '%',
    left: (session['day_of_week'] * 20) + '%',
    position: 'absolute',
    background: `hsl(${color.color[0]}, ${color.color[1]}%, ${color.color[2]}%)`,
    color: `hsl(${color.text[0]}, ${color.text[1]}%, ${color.text[2]}%)`,
    borderLeft: `4px solid hsl(${color.border[0]}, ${color.border[1]}%, ${color.border[2]}%)`
  }
}

const handler = (step) => {
  if (scheduleIndex.value + step > currentSchedules.value.length - 1) {
    scheduleIndex.value = 0
  } else if (scheduleIndex.value + step < 0) {
    scheduleIndex.value = currentSchedules.value.length - 1
  } else {
    scheduleIndex.value += step
  }
}

const title = computed(() => {
  if (currentSchedule.value && Object.keys(currentSchedule.value.info).length === 0)
    return 'please select a course to start'
  else if (currentSchedules.value && currentSchedules.value.length)
    return (scheduleIndex.value + 1) + '/' + currentSchedules.value.length
  return 'conflict'
})
</script>

<template>
  <div>
    <div>{{ title }}</div>
    <div @click="handler(1)">NEXT</div>
    <div @click="handler(-1)">PREV</div>
    <div class="yacs-schedule-table">
      <div v-for="(day, index) in days" class="yacs-schedule-column" :style="{zIndex: 6 - index}">
        <div class="yacs-schedule__day">{{ day }}</div>
        <div v-for="(hour, index) in hours" class="yacs-schedule-cell">
          <div class="yacs-schedule__hour">{{ hour }}</div>
        </div>
      </div>
      <div v-if="currentSchedule" style="position: absolute; inset: 0; z-index: 1000;">
        <div v-for="({course, section}, courseName) in currentSchedule.info">
          <div v-for="session in section.sessions" :style="getStyleBySession(session, course.color)">
            {{ course.name }}
            {{ course.title }}
            {{ section.crn }} - {{ section.index }}
          </div>
        </div>
      </div>
      <div v-else></div>
    </div>
  </div>
</template>

<style scoped>
.yacs-schedule-table {
  display: flex;
  flex-wrap: nowrap;
  justify-content: space-evenly;
  align-items: flex-start;
  height: 900px;
  margin: 25px 0 0 30px;
  position: relative;
}

.yacs-schedule-column {
  position: relative;
  border-right: 1px solid black;
  flex: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  background: white;
}

.yacs-schedule-column > .yacs-schedule-cell {
  /*border-top: 1px solid black;*/
  border-bottom: 1px solid black;
  flex: 1;
  position: relative;
}

.yacs-schedule-column > .yacs-schedule-cell:nth-child(2) {
  border-top: 1px solid black;
}

.yacs-schedule-column > .yacs-schedule-cell:last-child {
  border-bottom: none;
}

.yacs-schedule-column:nth-last-child(2) {
  border: none;
}

.yacs-schedule__day {
  position: absolute;
  top: 0;
  transform: translateY(-100%);
  width: 100%;
  text-align: center;
  background: white;
}
.yacs-schedule__hour {
  position: absolute;
  top: 0;
  left: 0;
  transform: translate(-100%, -60%);
  font-size: 8px;
}
</style>