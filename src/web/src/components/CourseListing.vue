<template>
  <!-- <b-list-group flush>
  <b-list-group-item v-for="course in courses" :key="course.id">-->
  <div>
    <div class="d-flex w-100 justify-content-between">
      <div>
        <b>{{ course.name }}</b>
        ({{ readableDate(course.date_start) }} - {{ readableDate(course.date_end) }})
        <br />
        {{ course.title }}
      </div>
      <div>
        <button v-if="actions.add || actions.remove" class="btn" @click="toggleCourse(course.id)">
          <font-awesome-icon v-if="course.selected" :icon="faTimes" />
          <font-awesome-icon v-else :icon="faPlus" />
        </button>
        <button
          v-if="actions.collapse"
          class="btn"
          @click="toggleShowSection()"
          :disabled="!course.sectionIds.length"
        >
          <font-awesome-icon :icon="faChevronDown" />
        </button>
      </div>
    </div>
    <b-collapse v-if="showSectionsInitial || loaded" v-model="showSections">
      <b-list-group flush>
        <b-list-group-item
          button
          v-for="section in getCourseSections(course.sectionIds)"
          :key="section.id"
          @click.stop="toggleCourseSection(section.id)"
          :style="{
            'border-left': section.selected ? `4px solid ${getBorderColor(section)}` : 'none',
            'background-color': section.selected ? `${getBackgroundColor(section)}` : 'white'
          }"
        >
          {{ section.crn }} - {{ getCourseSession(section.sessionIds[0]).section }}
          <br />

          <span
            v-for="courseSession in getCourseSessions(section.sessionIds)"
            :key="courseSession.id"
          >
            {{ DAY_SHORTNAMES[courseSession.day_of_week + 1] }}:
            {{ readableTime(courseSession.time_start) }} -
            {{ readableTime(courseSession.time_end) }}
            <br />
          </span>
        </b-list-group-item>
      </b-list-group>
    </b-collapse>
  </div>
  <!-- </b-list-group-item>
  </b-list-group>-->
</template>

<script>
import '@/typedef';

import {
  SELECT_COURSE_SECTION,
  UNSELECT_COURSE_SECTION,
  SELECT_COURSE,
  UNSELECT_COURSE,
  ADD_COURSE_SECTION,
  REMOVE_COURSE_SECTION
} from '@/store/mutations';
import { mapGetters } from 'vuex';

import { DAY_SHORTNAMES, readableTime, readableDate } from '@/utils';

import { getBackgroundColor, getBorderColor } from '@/services/ColorService';

import { faTimes, faPlus, faChevronDown } from '@fortawesome/free-solid-svg-icons';
import { SCHEDULE_CONFLICT_ERROR } from '@/controllers/Schedule';

export default {
  name: 'CourseListing',
  props: {
    // courses: Array,
    course: Object,
    actions: Object,
    showSectionsInitial: Boolean
  },
  data() {
    return {
      faTimes,
      faPlus,
      faChevronDown,
      DAY_SHORTNAMES,

      showSections: this.showSectionsInitial,
      loaded: false
    };
  },
  methods: {
    readableTime,
    readableDate,
    getBackgroundColor,
    getBorderColor,
    toggleShowSection() {
      if (!this.loaded && !this.showSections) {
        this.loaded = true;
      }
      this.showSections = !this.showSections;
    },
    toggleCourse(courseId) {
      if (this.getCourse(courseId).selected) {
        this.$store.commit(UNSELECT_COURSE, { courseId });
        this.$store.commit(REMOVE_COURSE_SECTION, { courseId });
      } else {
        this.$store.commit(SELECT_COURSE, { courseId });
      }
    },
    /**
     * Toggle use selection of course section
     * If a user is clicking on course section for the first time,
     * add course section to schedules
     * If the course section had already been clicked
     * remove course section from schedules
     * @param {number} sectionId
     */
    toggleCourseSection(sectionId) {
      if (this.getCourseSection(sectionId).selected) {
        this.$store.commit(UNSELECT_COURSE_SECTION, { sectionId });
        this.$store.commit(REMOVE_COURSE_SECTION, { sectionId });
      } else {
        try {
          this.$store.commit(ADD_COURSE_SECTION, { sectionId });
          this.$store.commit(SELECT_COURSE_SECTION, { sectionId });
        } catch (err) {
          if (err.type === SCHEDULE_CONFLICT_ERROR) {
            this.notifyScheduleConflict(
              this.getCourse(err.addingSession.courseId),
              err.existingSession,
              err.subsemester
            );
          }
          console.error(err.message ?? err);
        }
      }
    },
    /**
     * Generates a Bootstrap Toast notification of a schedule conflict
     * using the provided information
     * @param {Course} course
     * @param {CourseSession} conflictSession
     * @param {Subsemester} subsemester
     */
    notifyScheduleConflict(course, conflictSession, subsemester) {
      const vNodesMsg = this.$createElement('p', { class: ['mb-0'] }, [
        `${subsemester.display_string}: Conflict with ${conflictSession.crn} - ${conflictSession.section} `,
        this.$createElement('div', {
          style: `
            background-color:${getBackgroundColor(conflictSession)};
            border:1px solid ${getBorderColor(conflictSession)};
            width:13px;
            height:13px;
            display:inline-block;`
        })
      ]);
      this.$bvToast.toast(vNodesMsg, {
        title: `Cannot add ${course.title}`,
        variant: 'danger',
        noAutoHide: true
      });
    }
  },
  computed: {
    ...mapGetters([
      'getCourse',
      'getCourseSection',
      'getCourseSections',
      'getCourseSession',
      'getCourseSessions'
    ])
    // courseSections() {
    //   return this.getCourseSections(this.course.sectionIds);
    // }
  }
};
</script>

<style></style>
