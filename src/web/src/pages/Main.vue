<template>
  <div>
    <Header></Header>
    <b-container fluid class="py-3 h-100">
      <b-row class="h-100">
        <b-col md="4" class="d-flex flex-column">
          <b-card no-body class="h-100">
            <b-tabs card class="h-100 d-flex flex-column flex-grow-1">
              <b-tab title="Course Search" active class="flex-grow-1">
                <b-card-text class="d-flex flex-grow-1">
                  <CourseList class="w-100" />
                </b-card-text>
              </b-tab>
              <b-tab class="flex-grow-1">
                <template v-slot:title>
                  <div class="text-center">
                    Selected Courses
                    <b-badge variant="light">{{ numSelectedCourses }}</b-badge>
                  </div>
                </template>
                <b-card-text class="w-100 d-flex flex-grow-1 flex-column">
                  <SelectedCourses />
                </b-card-text>
              </b-tab>
            </b-tabs>
          </b-card>
        </b-col>
        <b-col md="8" class="d-flex flex-column">
          <!-- :options="scheduler.scheduleSubsemesters" -->
          <b-form-select
            v-model="selectedScheduleSubsemester"
            :options="scheduleSubsemesterOptions"
            text-field="display_string"
            value-field="display_string"
          ></b-form-select>
          <!-- v-for="(schedule, index) in scheduler.schedules" -->
          <Schedule
            v-for="(scheduleId, index) in scheduleIds"
            :key="index"
            :schedule="$store.getters.getSchedule(scheduleId)"
            v-show="selectedScheduleIndex === index"
          />
          <b-row>
            <b-col>
              <h5>CRNs: {{ selectedCrns }}</h5>
            </b-col>

            <b-col md="4">
              <button
                id="export-ics-button"
                class="col-auto btn-sm btn btn-primary ml-auto mb-2 mr-5 mt-1 d-block"
                @click="exportScheduleToIcs"
              >
                <font-awesome-icon :icon="exportIcon" />Export to ICS
              </button>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
    <Footer></Footer>
  </div>
</template>

<script>
// import NotificationsMixin from '@/mixins/NotificationsMixin';

import ScheduleComponent from '@/components/Schedule';
import SelectedCoursesComponent from '@/components/SelectedCourses';
import CourseListComponent from '@/components/CourseList';
import Footer from '@/components/Footer';

import SubSemesterScheduler from '@/controllers/SubSemesterScheduler';

import {
  getSubSemesters
  // getCourses
} from '@/services/YacsService';

import { LOAD_CLASSES } from '@/store/actions';

import HeaderComponent from '@/components/Header';

import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';
import {
  // SELECT_COURSE_SECTION,
  // UNSELECT_COURSE_SECTION,
  // SELECT_COURSE,
  // UNSELECT_COURSE,
  INIT_SELECTED_COURSES,
  // ADD_COURSE_SECTION,
  // REMOVE_COURSE_SECTION,
  ADD_SCHEDULE
} from '@/store/mutations';

import { generateScheduleId } from '@/store/helpers';

export default {
  name: 'MainPage',
  // mixins: [NotificationsMixin],
  components: {
    Schedule: ScheduleComponent,
    SelectedCourses: SelectedCoursesComponent,
    CourseList: CourseListComponent,
    Header: HeaderComponent,
    Footer: Footer
  },
  data() {
    return {
      // selectedCourses: {},

      selectedScheduleSubsemester: null,

      // scheduler: new SubSemesterScheduler(),

      // courses: [],

      exportIcon: faPaperPlane,
      ICS_DAY_SHORTNAMES: ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
    };
  },
  created() {
    getSubSemesters().then(subsemesters => {
      this.$store.commit(ADD_SCHEDULE, {
        id: generateScheduleId(),
        schedule: new SubSemesterScheduler(subsemesters)
      });
      const { scheduleSubsemesters } = this.$store.getters.getSchedule();
      if (scheduleSubsemesters.length > 0) {
        this.selectedScheduleSubsemester = scheduleSubsemesters[0].display_string;
      }
      // subsemesters.forEach(subsemester => {
      //   this.scheduler.addSubSemester(subsemester);
      // });
      // this.$store
      //   .dispatch(CREATE_SCHEDULE, { schedule: new SubSemesterScheduler(subsemesters) })
      //   .then(scheduleId => {
      //     const { scheduleSubsemesters } = this.$store.getters.getSchedule(scheduleId);
      //     if (scheduleSubsemesters.length > 0) {
      //       this.selectedScheduleSubsemester = scheduleSubsemesters[0].display_string;
      //     }
      //   });
      // if (this.scheduler.scheduleSubsemesters.length > 0) {
      // this.selectedScheduleSubsemester = this.scheduler.scheduleSubsemesters[0].display_string;
      // }
    });
    // getCourses().then(courses => this.courses.push(...courses));
    this.$store.dispatch(LOAD_CLASSES);
    this.$store.commit(INIT_SELECTED_COURSES);
  },
  methods: {
    // addCourse(course) {
    //   console.log(`Adding ${course.title} to selected courses`);
    //   console.log(course);
    //   // course.selected = true;
    //   // This must be vm.set since we're adding a property onto an object
    //   // this.$set(this.selectedCourses, course.id, course);
    //   this.$store.commit(SELECT_COURSE, { id: course.id });
    // },

    // addCourseSection(course, section) {
    //   try {
    //     this.$store.commit(ADD_COURSE_SECTION, { sectionId: section.id });
    //     // this.scheduler.addCourseSection(course, section);
    //     // section.selected = true;
    //     this.$store.commit(SELECT_COURSE_SECTION, { id: section.id });
    //   } catch (err) {
    //     if (err.type === 'Schedule Conflict') {
    //       this.notifyScheduleConflict(course, err.existingSession, err.subsemester);
    //     }
    //     console.log(err);
    //   }
    // },
    // removeCourse(course) {
    //   // this.$delete(this.selectedCourses, course.id);
    //   // course.selected = false;
    //   this.$store.commit(UNSELECT_COURSE, { id: course.id });
    //   // this.scheduler.removeAllCourseSections(course);
    //   this.$store.commit(REMOVE_COURSE_SECTION, { courseId: course.id });
    // },
    // removeCourseSection(section) {
    //   this.$store.commit(UNSELECT_COURSE_SECTION, { id: section.id });
    //   // this.scheduler.removeCourseSection(section);
    //   this.$store.commit(REMOVE_COURSE_SECTION, { sectionId: section.id });
    // },
    /**
     * Export all selected course sections to ICS
     */
    exportScheduleToIcs() {
      let calendarBuilder = window.ics();
      let semester;

      // for (const course of Object.values(this.courses)) {
      // for (const section of course.sections.filter(s => s.selected)) {
      for (const section of this.$store.getters.selectedCourseSections) {
        const course = this.$store.getters.getCourse(section.courseId);
        for (const session of this.$store.getters.getSessions(section.sessionIds)) {
          // The dates from the DB have no timezone, so when they are
          // cast to a JS date they're by default at time midnight 00:00:00.
          // This will exclude all classes if they're on that final day, so bump
          // the end date by 1 day.
          let exclusive_date_end = new Date(course.date_end);
          exclusive_date_end.setDate(course.date_end.getDate() + 1);
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
              until: exclusive_date_end,
              byday: [this.ICS_DAY_SHORTNAMES[session.day_of_week]]
            }
          );
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
      return this.$store.getters.getSchedule()?.scheduleSubsemesters.findIndex(
        // this.scheduler.scheduleSubsemesters.findIndex(
        s => s.display_string === this.selectedScheduleSubsemester
      );
    },
    /**
     * Returns list of CRNs for all selected sections
     * @returns {string[]}
     */
    selectedCrns() {
      return (
        this.$store.getters.selectedCourseSections
          // Object.values(this.selectedCourses)
          // .map(c => c.sections.filter(s => s.selected))
          // .flat()
          .map(s => s.crn)
          .join(', ')
      );
    },
    numSelectedCourses() {
      return this.$store.getters.selectedCourses.length;
      // return Object.values(this.selectedCourses).length;
    },
    scheduleSubsemesterOptions() {
      return this.$store.getters.getSchedule()?.scheduleSubsemesters ?? [];
    },
    scheduleIds() {
      return this.$store.getters.getSchedule()?.scheduleIds ?? [];
      // return this.$store.getters.getSchedule() ? this.$store.getters.getSchedule().scheduleIds : [];
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

.card {
  border: none !important;

  a:visited {
    color: black;
  }

  .card-header {
    background: white !important;
  }
}

#export-ics-button {
  background: #3d4959 !important;
}
</style>
