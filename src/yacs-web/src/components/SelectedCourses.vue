<template>
    <b-row>
        <b-col cols="auto">
            <h5>CRNs: {{selectedCrns}}</h5>
        </b-col>
        <button class="col-auto btn btn-success ml-auto mb-2 mr-2 d-block" @click="exportScheduleToIcs">
            <font-awesome-icon :icon="exportIcon" /> Export to ICS
        </button>
        <b-col cols="12">
            <b-card-group no-body columns>
                <b-card
                    v-for="course of courses"
                    :key="course.name"
                    :title="course.name"
                    :sub-title="course.title"
                    class="selected-course-card"
                >
                    <button type="button" class="close text-muted" @click="removeCourse(course)">
                        <span>&times;</span>
                    </button>
                    {{readableDate(course.date_start)}}-{{readableDate(course.date_end)}}

                    <b-list-group flush>
                        <b-list-group-item
                            button
                            v-for="section in course.sections"
                            :key="section.crn"
                            @click.stop="toggleCourseSection(course, section)"
                            :style="{
                                'border-left': section.selected ? `4px solid ${ColorService.getBorderColor(section)}` : 'none',
                                'background-color': section.selected ? `${ColorService.getBackgroundColor(section)}` : 'white'
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
import { 
    TimeDateMixin 
} from '@/mixins';

import {
    ColorService
} from '@/services';

import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';

export default {
    name: 'SelectedCourses',
    mixins: [
        TimeDateMixin
    ],
    props: {
        courses: Object,
    },
    data () {
        return {
            ColorService,
            exportIcon: faPaperPlane,
            ICS_DAY_SHORTNAMES: ["MO", "TU", "WE", "TH", "FR", "SA", "SU"],
        }
    },
    methods: {
        removeCourse (course) {
            this.$emit('removeCourse', course);
        },
        toggleCourseSection (course, section) {
            if (section.selected) {
                this.$emit('removeCourseSection', section);
            } else {
                this.$emit('addCourseSection', course, section);
            }
        },
        exportScheduleToIcs () {
            let calendarBuilder = window.ics()
            let semester;

            for (const course of Object.values(this.courses)) {
                for (const section of course.sections.filter(s => s.selected)) {
                    for (const session of section.sessions) {
                        semester = session.semester;
                        calendarBuilder.addEvent(
                            `Class: ${course.title}`, 
                            "LEC day",
                            session.location,
                            new Date(`${course.date_start.toDateString()} ${session.time_start}`), 
                            new Date(`${course.date_start.toDateString()} ${session.time_end}`),
                            {
                                freq: "WEEKLY",
                                interval: 1,
                                until: course.date_end,
                                byday: [this.ICS_DAY_SHORTNAMES[session.day_of_week]]
                            }
                        );
                    }
                }
            }

            // for (const dayArray of this.schedule.dailySessions) {
            //     for (const session of dayArray) {
            //         console.log(session);
            //         // Add course type in description when available from DB. Add location of session when available.
            //         let courseInfo = this.courses[session._courseKey];
            //         semester = session.semester;
            //         calendarBuilder.addEvent(`Class: ${courseInfo.title}`, "LEC day", session.location, new Date(`${courseInfo.date_start.toDateString()} ${session.time_start}`), new Date(`${courseInfo.date_start.toDateString()} ${session.time_end}`), {
            //             freq: "WEEKLY",
            //             interval: 1,
            //             until: courseInfo.date_end,
            //             byday: [this.ICS_DAY_SHORTNAMES[session.day_of_week]]
            //         });
            //     }
            // }
            calendarBuilder.download(`${semester.replace(/^(\w)(\w*?)\s?(\d+)/, function (_, semFirstLetter, semRest, year) { return semFirstLetter.toUpperCase() + semRest.toLowerCase() + year })}_Schedule`);
        },
    },
    computed: {
        selectedCrns () {
            return Object.values(this.courses).map(c => c.sections.filter(s => s.selected)).flat().map(s => s.crn).join(", ");
        },
        
    }
}
</script>

<style lang="scss">
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