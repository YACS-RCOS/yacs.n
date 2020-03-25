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
            backgroundColor: getBackgroundColor(courseSession),
            borderColor: getBorderColor(courseSession),
            color: getTextColor(courseSession),
            width: dayWidth + '%'
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
import '@/typedef';

<<<<<<< HEAD
import { DAY_LONGNAMES, DAY_SHORTNAMES, hourName, toMinutes } from '@/utils';
=======
                <button class="btn btn-success ml-auto mb-2 d-block" @click="exportScheduleToIcs">
                    <font-awesome-icon :icon="exportIcon" /> Export to ICS
                </button>

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
>>>>>>> origin

import { getBackgroundColor, getBorderColor, getTextColor } from '@/services/ColorService';

<<<<<<< HEAD
import Schedule from '@/controllers/Schedule';

import ScheduleEventComponent from '@/components/ScheduleEvent';
=======
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
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons'
>>>>>>> origin

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
      totalHeight: 600
    };
  },
  methods: {
    getBackgroundColor,
    getBorderColor,
    getTextColor,
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
<<<<<<< HEAD
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
=======
    data () {
        return {
            startDay: 1,
            endDay: 5,
            startTime: 480,
            endTime: 1320,
            totalHeight: 600,

            exportIcon: faPaperPlane,

            DAY_SHORTNAMES: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
            DAY_LONGNAMES: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],

            ICS_DAY_SHORTNAMES: ["MO", "TU", "WE", "TH", "FR", "SA", "SU"],

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
            // The session needs a reference to the course so the exportable schedule can be built
            course.sections[sectionIndex].sessions.map(session => session.course = course);
            this.courseSessions.push(...course.sections[sectionIndex].sessions);
        },
        exportScheduleToIcs () {
            let calendarBuilder = window.ics()
            for (var session of this.courseSessions) {
                // console.log(session);
                // Add course type in description when available from DB.
                calendarBuilder.addEvent(`Class: ${session.course.title}`, "LEC day", session.course.location, new Date(`${session.course.date_start.toDateString()} ${session.time_start}`), new Date(`${session.course.date_start.toDateString()} ${session.time_end}`), {
                    freq: "WEEKLY",
                    interval: 1,
                    until: session.course.date_end,
                    byday: [this.ICS_DAY_SHORTNAMES[session.day_of_week]]
                });
            }
            calendarBuilder.download();
        }
>>>>>>> origin
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
  width: 99%;
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
