<template>
    <b-container fluid class="pt-3">
        <b-row>
            <b-col md="4">
                <h3>YACS</h3>
                <hr>

                <CourseList
                    @addCourse="addCourse"
                />

            </b-col>
            <b-col md='8'>
                <b-form-select v-model="selectedScheduleIndex" :options="selectedScheduleOptions"></b-form-select>

                <template v-if="scheduler.schedules.length">
                    <Schedule
                        v-for="(schedule, index) in scheduler.schedules"
                        :key="index"
                        :schedule="schedule"
                        v-show="selectedScheduleIndex === index"
                    />
                </template>

                <SelectedCourses
                    :courses="selectedCourses"
                    @removeCourse="removeCourse"
                    @removeCourseSection="removeCourseSection"
                    @addCourseSection="addCourseSection"
                    @removeAllCourseSections="removeAllCourseSections"
                />

            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import {
    TimeDateMixin,
    Notifications
} from '@/mixins';

import {
    ScheduleComponent,
    SelectedCoursesComponent,
    CourseListComponent
} from '@/components';

import {
    getSubSemesters,
    SubSemesterScheduler
} from '@/services';

export default {
    name: 'MainPage',
    mixins: [
        TimeDateMixin,
        Notifications
    ],
    components: {
        Schedule: ScheduleComponent,
        SelectedCourses: SelectedCoursesComponent,
        CourseList: CourseListComponent
    },
    data () {
        return {
            selectedCourses: {},
            selectedScheduleIndex: null,
            selectedScheduleOptions: [],

            scheduler: new SubSemesterScheduler()
        }
    },
    created () {
        getSubSemesters().then(subsemesters => {
            subsemesters.forEach(subsemester => {
                this.selectedScheduleOptions.push({text: subsemester.text, value: this.selectedScheduleOptions.length });
                this.scheduler.addSubSemester(subsemester);
            });
            if (this.selectedScheduleOptions.length > 0) {
                this.selectedScheduleIndex = this.selectedScheduleOptions[0].value;
            }
        });
    },
    methods: {
        _getCourseIdentifier(courseObj) {
            return `${courseObj.department}${courseObj.level}${courseObj.date_start.getMonth() + 1}${courseObj.date_start.getDay() + 1}${courseObj.date_start.getFullYear()}${courseObj.date_end.getMonth() + 1}${courseObj.date_end.getDay() + 1}${courseObj.date_end.getFullYear()}`;
        },
        addCourse (course) {
            console.log(`Adding ${course.title} to selected courses`);
            console.log(course);
            course.selected = true;
            // This must be vm.set since we're adding a property onto an object
            this.$set(this.selectedCourses, this._getCourseIdentifier(course), course);
        },

        addCourseSection (course, section) {
            try {
                this.scheduler.addCourseSection(course, section);
            } catch (err) {
                if (err.type === 'Schedule Conflict') {
                    this.notifyScheduleConflict(course, err.existingSession, err.subsemester);
                }
            }
        },
        removeCourse (course) {
            this.$delete(this.selectedCourses, this._getCourseIdentifier(course));
            course.selected = false;
            this.scheduler.removeAllCourseSections(course);
        },
        removeCourseSection (section) {
            this.scheduler.removeCourseSection(section);
        },

        removeAllCourseSections (course) {
            this.scheduler.removeAllCourseSections(course);
        }

    }
}
</script>

<style scoped lang="scss">

</style>
