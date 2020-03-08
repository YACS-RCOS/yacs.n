<template>
    <b-row>
        <b-col cols="12">
            <div class="schedule" :style="{ height: totalHeight + 'px' }">
                <div class="schedule-legend">
                    <div class="hour-label" v-for="(hour, index) of hours" :key="hour" :style="{ height: hourHeight + '%' }">
                    <div v-if="index != 0">{{ hour }}</div>
                    </div>
                </div>

                <div class="schedule-grid">
                    <div class="grid-day" v-for="(day, index) of days" :key="day.longname" :style="{ width: dayWidth + '%' }">
                        <div class="day-label">{{ day.longname }}</div>
                        <!-- <ng-container > -->
                            <!-- <schedule-event *ngFor="let period of periodsOnDay(day)"
                                [style.margin-top.px] = "eventPosition(period)"
                                [style.backgroundColor] = "getBackgroundColor(period)"
                                [style.borderColor] = "getBorderColor(period)"
                                [style.color] = "getTextColor(period)"
                                [normalHeight] = "eventHeight(period)"
                                [period] = "period">
                            </schedule-event>  -->
                            <ScheduleEvent
                                v-for="courseSession in courseSessionsOnDay(index)"
                                :key="courseSession.crn + courseSession.day_of_week + courseSession.time_start"
                                :crn="courseSession.crn"
                                :section="courseSession.section"
                                :semester="courseSession.semester"
                                :style="{
                                    'margin-top': eventPosition(courseSession) + 'px',
                                    height: eventHeight(courseSession) + 'px',
                                    backgroundColor: getBackgroundColor(courseSession),
                                    borderColor: getBorderColor(courseSession),
                                    color: getTextColor(courseSession),
                                    width: dayWidth + '%'
                                }"
                                class="schedule-event"
                            >
                            </ScheduleEvent>
                            <div class="grid-hour" v-for="hour of hours" :key="hour" :style="{ height: hourHeight + '%' }"></div>
                        <!-- </ng-container> -->
                    </div>
                </div>
            </div>
        </b-col>
        <b-col>
            <h5>Selected Courses:</h5>
        </b-col>
        <b-col cols='12'>
            <b-card-group deck>
                <b-card
                    v-for="course in courses"
                    :key="course.name + course.date_end + course.date_start"
                    :sub-title="course.title"
                    class="selected-course-card"
                >
                <button type="button" class="close text-muted" @click="$emit('unselectCourse', course)">
                    <span>&times;</span>
                </button>
                    <!-- <b-card-header>
                        {{course.name}}
                    </b-card-header> -->
                    <!-- <b-card-body> -->
                        <!-- <b-card-sub-title>{{course.title}}</b-card-sub-title> -->
                    <!-- </b-card-body> -->
                    <b-list-group flush>
                        <b-list-group-item
                            v-for="(section, index) in course.sections"
                            :key="section.crn"
                            @click.stop="addCourseSection(course, index)"
                            class="course-section-item"
                        >
                            {{section.crn}} <br>

                            <span
                                v-for="courseSession in section.sessions"
                                :key="courseSession.crn + courseSession.day_of_week + courseSession.time_start"
                            >
                                {{DAY_SHORTNAMES[courseSession.day_of_week + 1]}}: {{readableTime(courseSession.time_start)}} - {{readableTime(courseSession.time_end)}}
                                <br>
                            </span>

                        </b-list-group-item>
                    </b-list-group>
                </b-card>
            </b-card-group>
        </b-col>
    </b-row>
</template>
<script>
import moment from 'moment';
import ColorService from '../services/ColorService';
import ScheduleEvent from './ScheduleEvent';

export default {
    name: 'Schedule',
    components: {
        ScheduleEvent
    },
    props: {
        courses: Array
    },
    data () {
        return {
            startDay: 1,
            endDay: 5,
            startTime: 480,
            endTime: 1320,
            totalHeight: 600,

            DAY_SHORTNAMES: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
            DAY_LONGNAMES: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],

            colorService: new ColorService(),

            courseSessions: [],
        }
    },
    methods: {
        hourName (minutes) {
            const hour = minutes / 60;
            if (hour === 0) {
                return '12 AM';
            } else if (hour < 12) {
                return hour + ' AM';
            } else if (hour === 12) {
                return 'Noon';
            } else {
                return (hour - 12) + ' PM';
            }
        },
        toMinutes (timeString) {
            // let timeInt = parseInt(timeString);
            // return (Math.floor(timeInt / 100) * 60) + (timeInt % 100);
            const mmt = moment(timeString, 'kk:mm:ss');
            return mmt.hours() * 60 + mmt.minutes();
        },
        eventHeight (courseSession) {
            const eventDuration = this.toMinutes(courseSession.time_end) - this.toMinutes(courseSession.time_start);
            // console.log(this.toMinutes(courseSession.time_end));
            // console.log(this.toMinutes(courseSession.time_start));
            // console.log(eventDuration);
            return (this.totalHeight  * (eventDuration / this.numMinutes));
        },
        eventPosition (courseSession) {
            const eventStart = this.toMinutes(courseSession.time_start);
            return (this.totalHeight * ((eventStart - this.startTime) / this.numMinutes));
        },
        getBackgroundColor (courseSession) {
            return this.colorService.getColor(courseSession.crn).primary;
        },
        getBorderColor (courseSession) {
            return this.colorService.getColor(courseSession.crn).border;
        },
        getTextColor (courseSession) {
            return this.colorService.getColor(courseSession.crn).text;
        },
        readableTime (timeString) {
            return moment(timeString, 'kk:mm:ss').format('h:mma');
        },
        courseSessionsOnDay(dayOfWeek) {
            return this.courseSessions.filter(cs => cs.day_of_week === dayOfWeek);
        },
        addCourseSection (course, sectionIndex) {
            console.log(`ADDING ${course.title} - ${sectionIndex}: ${course.sections[sectionIndex].sessions.length}`);
            this.courseSessions.push(...course.sections[sectionIndex].sessions);
        }
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

.foo {
  //width: 1000;
  height: 3.5%;
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

.schedule-event {
  display: block;
  box-sizing: border-box;
  border-top: 1px solid #e7e7e7!important; //temp fix for the borders not showing
  border-right: 1px solid #e7e7e7 !important;
  position: absolute;
  //height: 20%;
//   width: 20%;
}

.selected-course-card {
    max-width: 270px;
    min-width: 270px;

    .close {
        position: absolute;
        top: 10px;
        right: 15px;
    }
}

.course-section-item {
    cursor: pointer;
}
</style>