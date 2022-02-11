<script setup>
import {semesters} from "../store";
const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
const hours = ['8am', '9am', '10am', '11am', '12am', '1pm', '2pm', '3pm', '5pm', '5pm', '6pm', '7pm', '8pm']
</script>

<template>
  <div>
    <div class="yacs-schedule-table">
      <div v-for="(day, index) in days" class="yacs-schedule-column" :style="{zIndex: 6 - index}">
        <div class="yacs-schedule__day">{{ day }}</div>
        <div v-for="(hour, index) in hours" class="yacs-schedule-cell">
          <div class="yacs-schedule__hour">{{ hour }}</div>
        </div>
      </div>
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
  padding: 25px 0 0 30px;
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

.yacs-schedule-column:last-child {
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