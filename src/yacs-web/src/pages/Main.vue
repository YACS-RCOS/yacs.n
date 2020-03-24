<template>
  <div>
    <Header></Header>
    <b-container fluid class="py-3 h-100">
      <b-row class="h-100">
        <b-col md="4" class="d-flex flex-column">
          <h3>YACS</h3>
          <b-card no-body class="h-100">
          <b-tabs card class="h-100 d-flex flex-column flex-grow-1">
            <b-tab title="Course Search" active class="flex-grow-1">
            <b-card-text class="d-flex flex-grow-1">
              <CourseList @addCourse="addCourse" @removeCourse="removeCourse" :courses="courses" />
              </b-card-text>
            </b-tab>
            <b-tab class="flex-grow-1">
              <template v-slot:title>
                <div class="text-center">
                  Selected Courses
                  <b-badge variant="light">{{numSelectedCourses}}</b-badge>
                </div>
              </template>
              <b-card-text class="w-100 d-flex flex-grow-1 flex-column">
            <SelectedCourses
                :courses="selectedCourses"
                @removeCourse="removeCourse"
                @removeCourseSection="removeCourseSection"
                @addCourseSection="addCourseSection"
              />
              </b-card-text>
            </b-tab>
          </b-tabs>
          </b-card>
        </b-col>
        <b-col md="8">
          <b-form-select
            v-model="selectedScheduleSubsemester"
            :options="scheduler.scheduleSubsemesters"
            text-field="display_string"
            value-field="display_string"
          ></b-form-select>

          <template v-if="scheduler.schedules.length">
            <Schedule
              v-for="(schedule, index) in scheduler.schedules"
              :key="index"
              :schedule="schedule"
              v-show="selectedScheduleIndex === index"
            />
          </template>
          <b-row>
            <b-col cols="auto">
              <h5>CRNs: {{ selectedCrns }}</h5>
            </b-col>
            <button
              class="col-auto btn btn-success ml-auto mb-2 mr-2 d-block"
              @click="exportScheduleToIcs"
            >
              <font-awesome-icon :icon="exportIcon" />Export to ICS
            </button>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
  </div>
  
</template>

<script>
import NotificationsMixin from '@/mixins/NotificationsMixin';

import ScheduleComponent from '@/components/Schedule';
import SelectedCoursesComponent from '@/components/SelectedCourses';
import CourseListComponent from '@/components/CourseList';

import SubSemesterScheduler from '@/controllers/SubSemesterScheduler';

import HeaderComponent from '@/components/Header';

import { getSubSemesters, getCourses } from '@/services/YacsService';

import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';

export default {
  name: 'MainPage',
  mixins: [NotificationsMixin],
  components: {
    Schedule: ScheduleComponent,
    SelectedCourses: SelectedCoursesComponent,
    CourseList: CourseListComponent,
    Header: HeaderComponent
  },
  data() {
    return {
      selectedCourses: {},

      selectedScheduleSubsemester: null,

      scheduler: new SubSemesterScheduler(),

      courses: [],

      exportIcon: faPaperPlane,
      ICS_DAY_SHORTNAMES: ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
    };
  },
  created() {
    getSubSemesters().then(subsemesters => {
      subsemesters.forEach(subsemester => {
        this.scheduler.addSubSemester(subsemester);
      });
      if (this.scheduler.scheduleSubsemesters.length > 0) {
        this.selectedScheduleSubsemester = this.scheduler.scheduleSubsemesters[0].display_string;
      }
    });
    getCourses().then(courses => this.courses.push(...courses));
  },
  methods: {
    addCourse(course) {
      console.log(`Adding ${course.title} to selected courses`);
      console.log(course);
      course.selected = true;
      // This must be vm.set since we're adding a property onto an object
      this.$set(this.selectedCourses, course.id, course);
    },

    addCourseSection(course, section) {
      try {
        this.scheduler.addCourseSection(course, section);
        section.selected = true;
      } catch (err) {
        if (err.type === 'Schedule Conflict') {
          this.notifyScheduleConflict(course, err.existingSession, err.subsemester);
        }
      }
    },
    removeCourse(course) {
      this.$delete(this.selectedCourses, course.id);
      course.selected = false;
      this.scheduler.removeAllCourseSections(course);
    },
    removeCourseSection(section) {
      this.scheduler.removeCourseSection(section);
    },
    /**
     * Export all selected course sections to ICS
     */
    exportScheduleToIcs() {
      let calendarBuilder = window.ics();
      let semester;

      for (const course of Object.values(this.courses)) {
        for (const section of course.sections.filter(s => s.selected)) {
          for (const session of section.sessions) {
            semester = session.semester;
            calendarBuilder.addEvent(
              `Class: ${course.title}`,
              'LEC day',
              session.location,
              new Date(`${course.date_start.toDateString()} ${session.time_start}`),
              new Date(`${course.date_start.toDateString()} ${session.time_end}`),
              {
                freq: 'WEEKLY',
                interval: 1,
                until: course.date_end,
                byday: [this.ICS_DAY_SHORTNAMES[session.day_of_week]]
              }
            );
          }
        }
      }
      calendarBuilder.download(
        `${semester.replace(/^(\w)(\w*?)\s?(\d+)/, function(_, semFirstLetter, semRest, year) {
          return semFirstLetter.toUpperCase() + semRest.toLowerCase() + year;
        })}_Schedule`
      );
    }
  },
  computed: {
    selectedScheduleIndex() {
      return this.scheduler.scheduleSubsemesters.findIndex(
        s => s.display_string === this.selectedScheduleSubsemester
      );
    },
    /**
     * Returns list of CRNs for all selected sections
     * @returns {string[]}
     */
    selectedCrns() {
      return Object.values(this.selectedCourses)
        .map(c => c.sections.filter(s => s.selected))
        .flat()
        .map(s => s.crn)
        .join(', ');
    },
    numSelectedCourses() {
      return Object.values(this.selectedCourses).length;
    }
  }
};
</script>

<style lang="scss">
// NOTE!
// for every v-tab a div.tab-content container is generated
// I can't find access to the div so the workaround is to
// apply the css attributes globally to .tab-content
// This means that all v-tabs in this app will have flexbox content
// Hopefully this doesn't screw up someone's debugging later lol
.tab-content {
  display: flex;
  flex-grow: 1;
}
// This makes it so active tabs are display:flex
// The default is display:block
.tab-content > .active {
  display: flex;
}
</style>
