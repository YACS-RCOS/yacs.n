<template>
  <div>
    <div class="d-flex w-100 justify-content-between">
      <div>
        <b>{{ course.name }}</b>
        ({{ readableDate(course.date_start) }} - {{ readableDate(course.date_end) }})
        <br />
        {{ course.title }}
      </div>
      <div>
        <button v-if="actions.add || actions.remove" class="btn" @click="toggleCourse(course)">
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
          v-for="section in courseSections"
          :key="section.crn"
          @click.stop="toggleCourseSection(course, section)"
          :style="{
            'border-left': section.selected ? `4px solid ${getBorderColor(section)}` : 'none',
            'background-color': section.selected ? `${getBackgroundColor(section)}` : 'white'
          }"
        >
          {{ section.crn }} - {{ $store.getters.getSession(section.sessionIds[0]).section }}
          <br />

          <span
            v-for="courseSession in $store.getters.getSessions(section.sessionIds)"
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

import { DAY_SHORTNAMES, readableTime, readableDate } from '@/utils';

import { getBackgroundColor, getBorderColor } from '@/services/ColorService';

import { faTimes, faPlus, faChevronDown } from '@fortawesome/free-solid-svg-icons';
import { SCHEDULE_CONFLICT_ERROR } from '@/controllers/Schedule';

export default {
  name: 'CourseListing',
  props: {
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
    toggleCourse(course) {
      if (course.selected) {
        // this.$emit('removeCourse', course);
        this.$store.commit(UNSELECT_COURSE, { id: course.id });
        this.$store.commit(REMOVE_COURSE_SECTION, { courseId: course.id });
      } else {
        // this.$emit('addCourse', course);
        this.$store.commit(SELECT_COURSE, { id: course.id });
      }
    },
    /**
     * Toggle use selection of course section
     * If a user is clicking on course section for the first time,
     * add course section to schedules
     * If the course section had already been clicked
     * remove course section from schedules
     * @param {Course} course
     * @param {CourseSection} section
     */
    toggleCourseSection(course, section) {
      if (section.selected) {
        // this.$emit('removeCourseSection', section);
        this.$store.commit(UNSELECT_COURSE_SECTION, { id: section.id });
        this.$store.commit(REMOVE_COURSE_SECTION, { sectionId: section.id });
      } else {
        try {
          // this.$emit('addCourseSection', course, section);
          this.$store.commit(ADD_COURSE_SECTION, { sectionId: section.id });
          this.$store.commit(SELECT_COURSE_SECTION, { id: section.id });
        } catch (err) {
          if (err.type === SCHEDULE_CONFLICT_ERROR) {
            this.notifyScheduleConflict(course, err.existingSession, err.subsemester);
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
        // title: `Cannot add ${section.crn} - ${section.sessions[0].section}`,
        title: `Cannot add ${course.title}`,
        variant: 'danger',
        noAutoHide: true
      });
    }
  },
  computed: {
    courseSections() {
      return this.$store.getters.getSections(this.course.sectionIds);
    }
  }
};
</script>

<style></style>
