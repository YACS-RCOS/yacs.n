<template>
  <b-container fluid class="pt-3">
    <Header class='mb-3'></Header>
    <b-row>
      <b-col md="4">
        <hr />

        <CourseList @addCourse="addCourse" />
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

        <SelectedCourses
          :courses="selectedCourses"
          @removeCourse="removeCourse"
          @removeCourseSection="removeCourseSection"
          @addCourseSection="addCourseSection"
        />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import NotificationsMixin from '@/mixins/NotificationsMixin';

import ScheduleComponent from '@/components/Schedule';
import SelectedCoursesComponent from '@/components/SelectedCourses';
import CourseListComponent from '@/components/CourseList';

import SubSemesterScheduler from '@/controllers/SubSemesterScheduler';

import { getSubSemesters } from '@/services/YacsService';

import Header from '../components/Header';

export default {
  name: 'MainPage',
  mixins: [NotificationsMixin],
  components: {
    Schedule: ScheduleComponent,
    SelectedCourses: SelectedCoursesComponent,
    CourseList: CourseListComponent,
    Header: Header,
  },
  data() {
    return {
      selectedCourses: {},

      selectedScheduleSubsemester: null,

      scheduler: new SubSemesterScheduler(),

      currentSemester: ""

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
    newSemester(sem){
      this.currentSemester = sem;
    }
  },
  computed: {
    selectedScheduleIndex() {
      return this.scheduler.scheduleSubsemesters.findIndex(
        s => s.display_string === this.selectedScheduleSubsemester
      );
    }
  }
};
</script>

<style scoped lang="scss"></style>
