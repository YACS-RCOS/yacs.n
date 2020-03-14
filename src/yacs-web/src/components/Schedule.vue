<template>
    <div class="schedule" :style="{ height: totalHeight + 'px' }">
        <div class="schedule-legend">
            <div class="hour-label" v-for="(hour, index) of hours" :key="hour" :style="{ height: hourHeight + '%' }">
                <div v-if="index != 0">{{ hour }}</div>
            </div>
        </div>

        <div class="schedule-grid">
            <div class="grid-day" v-for="(day, index) of days" :key="day.longname" :style="{ width: dayWidth + '%' }">
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
                    >
                    </ScheduleEvent>
                    <div class="grid-hour" v-for="hour of hours" :key="hour" :style="{ height: hourHeight + '%' }"></div>
            </div>
        </div>
    </div>
</template>
<script>
import {
    TimeDateMixin
} from '@/mixins';

import {
    ColorService
} from '@/services';

import { 
    ScheduleEventComponent 
} from '@/components';

export default {
    name: 'Schedule',
    mixins: [
        TimeDateMixin
    ],
    components: {
        'ScheduleEvent': ScheduleEventComponent
    },
    props: {
        schedule: Object,
    },
    data () {
        return {
            startDay: 1,
            endDay: 5,
            startTime: 480,
            endTime: 1320,
            totalHeight: 600,

            ColorService,
        }
    },
    methods: {
        eventHeight (courseSession) {
            const eventDuration = this.toMinutes(courseSession.time_end) - this.toMinutes(courseSession.time_start);
            return (this.totalHeight  * (eventDuration / this.numMinutes));
        },
        eventPosition (courseSession) {
            const eventStart = this.toMinutes(courseSession.time_start);
            return (this.totalHeight * ((eventStart - this.startTime) / this.numMinutes));
        },

        courseSessionsOnDay(dayOfWeek) {
            return this.schedule.dailySessions[dayOfWeek];
        },
    },
    computed: {
        numDays () { return (this.endDay - this.startDay) + 1; },
        numMinutes () { return (this.endTime - this.startTime); },
        hours () {
            const hours = [];
            for (let time = this.startTime; time < this.endTime; time += 60) {
                hours.push(this.hourName(time));
            }
            return hours;
        },
        days () {
            const days = [];
            for (let day = this.startDay; day <= this.endDay; ++day) {
                days.push({longname: this.DAY_LONGNAMES[day], shortname: this.DAY_SHORTNAMES[day]});
            }
            return days;
        },
        dayWidth () { return (100 / this.numDays) - 1; },
        hourHeight () { return 60 * 100 / this.numMinutes; },
    }
}
</script>

<style scoped lang="scss">
.schedule {
  margin-right: 15px;
  margin-top: 10px;
  position:relative; /* so the overlay will position properly */
  margin-bottom: 15px;
}

.schedule-legend{
  position: absolute;
  height: 100%;
  left: .35em;
  top:.70em;
}

.hour-label{
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
  display:block;
  margin: 0 auto;
  text-align: center;
  font-size: .8em;
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