<template>
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
          v-if="scheduler.scheduleSubsemesters.length > 1"
          v-model="selectedScheduleSubsemester"
          :options="scheduler.scheduleSubsemesters"
          text-field="display_string"
          value-field="display_string"
        ></b-form-select>

<<<<<<< HEAD
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
</template>
=======
                <div class="course-search">
                    <b-form-group
                        label="Search"
                        label-for="search"
                    >
                        <b-form-input id="search" v-model="textSearch" trim placeholder="Intro to College - COLG 1030 - 5/2"></b-form-input>
                    </b-form-group>
                <!-- <div class="form-group">
                    <label for="search">Search</label>
                    <input type="text" v-model='textSearch' class="form-control" id="search" placeholder="Intro to College - COLG 1030">
                </div> -->
                    <b-form-group
                        label="Filter Sub-Semester"
                        for="sub-semester"
                    >
                        <b-form-select v-model="selectedSubsemester" :options="subsemesterOptions"></b-form-select>
                    </b-form-group>
<!--
                <div class="form-group">
                    <label for="sub-semester">Filter Sub-Semester</label>
                    <select id='sub-semester' v-model='selectedSubsemester' class="form-control">
                    <option value="" selected>All</option>
                    <option ng-value="subsemester" ng-repeat='subsemester in subsemesters'>
                        {{subsemester.date_start_display}} - {{subsemester.date_end_display}}
                    </option>
                    </select>
                </div> -->
                    <b-form-group
                        label="Filter Department"
                        for="department"
                    >
                        <b-form-select v-model="selectedDepartment" :options="departmentOptions"></b-form-select>
                    </b-form-group>
                <!-- <div class="form-group">
                    <label for="department">Filter Department</label>
                    <select id='department' ng-model='departmentSearch' class="form-control">
                    <option value="" selected>All</option>
                    <option ng-value="department" ng-repeat='department in departments'>
                        {{department}}
                    </option>
                    </select>
                </div> -->
                </div>
>>>>>>> origin

<script>
import NotificationsMixin from '@/mixins/NotificationsMixin';

<<<<<<< HEAD
import ScheduleComponent from '@/components/Schedule';
import SelectedCoursesComponent from '@/components/SelectedCourses';
import CourseListComponent from '@/components/CourseList';
=======
                <b-list-group flush>
                    <b-list-group-item
                        v-for="course in filteredCourses"
                        :key="course.name + course.date_end + course.date_start"
                        class="course-list-item"
                        @click="addCourse(course)"
                    >
                        <b>{{ course.name }}</b> ({{ readableDate(course.date_start) }} - {{ readableDate(course.date_end) }}) <br>
                        {{ course.title }}
                    </b-list-group-item>
                </b-list-group>
>>>>>>> origin

import SubSemesterScheduler from '@/controllers/SubSemesterScheduler';

<<<<<<< HEAD
import { getSubSemesters, getCourses } from '@/services/YacsService';
=======
            </b-col>
            <b-col md='8'>

                <!-- <h3 class="text-center">Schedule</h3>
                <hr> -->
                <Schedule :courses="selectedCourses"></Schedule>
            </b-col>
>>>>>>> origin

import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';

export default {
  name: 'MainPage',
  mixins: [NotificationsMixin],
  components: {
    Schedule: ScheduleComponent,
    SelectedCourses: SelectedCoursesComponent,
    CourseList: CourseListComponent
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
<<<<<<< HEAD
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
=======
    methods: {
        readableDate (date) {
            return `${date.getMonth() + 1}/${date.getDay() + 1}`;
        },
        addCourse (course) {
            console.log(`Adding ${course.title} to selected courses`);
            console.log(course);
            this.selectedCourses.push(course);
        }
    },
    computed: {
        filteredCourses () {
            return this.courses.filter(({date_start, date_end, department, str}) => {
                return (!this.selectedSubsemester ||
                        (this.selectedSubsemester.date_start.getTime() === date_start.getTime() &&
                        this.selectedSubsemester.date_end.getTime() === date_end.getTime()))
                        && (!this.selectedDepartment ||
                            this.selectedDepartment === department)
                        && (!this.textSearch || str.includes(this.textSearch.toUpperCase()));
            });
>>>>>>> origin
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
