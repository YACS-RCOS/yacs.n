<template>
    <b-row>
        <b-col cols="12">
            <div class="schedule" :style="{ height: totalHeight + 'px' }">
                <div class="schedule-legend">
                    <div class="hour-label" v-for="(hour, index) of hours" :key="hour" :style="{ height: hourHeight + '%' }">
                    <div v-if="index != 0">{{ hour }}</div>
                    </div>
                </div>

                <button class="btn btn-success ml-auto mb-2 d-block" @click="exportScheduleToIcs">
                    <font-awesome-icon :icon="exportIcon" /> Export to ICS
                </button>

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
                                    backgroundColor: getBackgroundColor(courseSession),
                                    borderColor: getBorderColor(courseSession),
                                    color: getTextColor(courseSession),
                                    width: dayWidth + '%'
                                }"
                                class="schedule-event"
                            >
                            </ScheduleEvent>
                            <div class="grid-hour" v-for="hour of hours" :key="hour" :style="{ height: hourHeight + '%' }"></div>
                    </div>
                </div>
            </div>
        </b-col>
        <b-col>
            <h5>Selected Courses:</h5>
        </b-col>
        <b-col cols='12'>
            <b-card-group no-body columns>
                <b-card
                    v-for="course in courses"
                    :key="course.name"
                    :title="course.name"
                    :sub-title="course.title"
                    class="selected-course-card"
                >
                    <button type="button" class="close text-muted" @click="removeCourse(course)">
                        <span>&times;</span>
                    </button>

                    <b-list-group flush>
                        <b-list-group-item
                            button
                            v-for="section in course.sections"
                            :key="section.crn"
                            @click.stop="toggleCourseSection(course, section)"
                            :style="{
                                'border-left': section.selected ? `4px solid ${getBorderColor(section)}` : 'none',
                                'background-color': section.selected ? `${getBackgroundColor(section)}` : 'white'
                            }"
                        >
                            {{section.crn}} - {{section.sessions[0].section}}<br>

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
import ScheduleService from '../services/ScheduleService';
import ColorService from '../services/ColorService';
import ScheduleEvent from './ScheduleEvent';
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';

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

            exportIcon: faPaperPlane,

            DAY_SHORTNAMES: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
            DAY_LONGNAMES: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],

            ICS_DAY_SHORTNAMES: ["MO", "TU", "WE", "TH", "FR", "SA", "SU"],

            colorService: new ColorService(),
            schedule: new ScheduleService(),
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
            const mmt = moment(timeString, 'kk:mm:ss');
            return mmt.hours() * 60 + mmt.minutes();
        },
        eventHeight (courseSession) {
            const eventDuration = this.toMinutes(courseSession.time_end) - this.toMinutes(courseSession.time_start);
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
            return this.schedule.dailySessions[dayOfWeek];
        },
        addCourseSection (course, sectionIndex) {
            console.log(`ADDING ${course.title} - ${sectionIndex}: ${course.sections[sectionIndex].sessions.length}`);
            course.sections[sectionIndex].sessions.forEach(session => session.course = course);
            this.courseSessions.push(...course.sections[sectionIndex].sessions);
        },
        exportScheduleToIcs () {
            let calendarBuilder = window.ics()
            // console.log(this.courses);
            // console.log(this.schedule.dailySessions);
            for (const dayArray of this.schedule.dailySessions) {
                for (const session of dayArray) {
                    console.log(session);
                    // console.log(this.courses[this.courseIdentifierFunc(session)]);
                    // Add course type in description when available from DB.
                    calendarBuilder.addEvent(`Class: ${session.course.title}`, "LEC day", session.course.location, new Date(`${session.course.date_start.toDateString()} ${session.time_start}`), new Date(`${session.course.date_start.toDateString()} ${session.time_end}`), {
                        freq: "WEEKLY",
                        interval: 1,
                        until: session.course.date_end,
                        byday: [this.ICS_DAY_SHORTNAMES[session.day_of_week]]
                    });
                }
            }
            calendarBuilder.download();
        },
        removeCourse (course) {
            this.schedule.removeCourse(course);
            this.$emit('unselectCourse', course);
        },
        toggleCourseSection (course, section) {
            if (section.selected) {
                this.schedule.removeCourseSection(section);
            } else {
                try {
                    // Only allow selection of one section per course
                    this.schedule.removeCourse(course);
                    this.schedule.addCourseSection(course, section);
                } catch (err) {
                    if (err.type === 'Schedule Conflict') {
                        const vNodesMsg = this.$createElement(
                            'p',
                            { class: [ 'mb-0', ] },
                            [
                                `Conflict with ${err.existingSession.crn} - ${err.existingSession.section} `,
                                this.$createElement(
                                    'div',
                                    {
                                        style: `
                                            background-color:${this.getBackgroundColor(err.existingSession)};
                                            border:1px solid ${this.getBorderColor(err.existingSession)};
                                            width:13px;
                                            height:13px;
                                            display:inline-block;`
                                    }
                                )
                            ]
                        );
                        this.$bvToast.toast(vNodesMsg, {
                            title: `Cannot add ${section.crn} - ${section.sessions[0].section}`,
                            variant: 'danger',
                            noAutoHide: true,
                        });
                    }
                }
            }
        },
        addCourse(course) {
            this.schedule.addCourse(course);
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
</style>