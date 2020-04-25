<template>
  <div>
    <div @click="actions.add ? toggleCourse(course) : toggleShowSection()" class="d-flex w-100 justify-content-between click-me">
      <div>
        <b>{{ course.name }}</b>
        ({{ readableDate(course.date_start) }} - {{ readableDate(course.date_end) }})
        <br />
        {{ course.title }}
      </div>
      <div>
        <button
          v-if="actions.add || actions.remove"
          class="btn"
          @click="toggleCourse(course)"
        >
          <font-awesome-icon v-if="course.selected" :icon="faTimes" />
          <font-awesome-icon v-else :icon="faPlus" />
        </button>
        <button
          v-if="actions.collapse"
          class="btn"
          @click="toggleShowSection()"
          :disabled="!course.sections.length"
        >
          <font-awesome-icon v-if="!this.showSections" :icon="faChevronDown" />
          <font-awesome-icon v-else :icon="faChevronUp" />
        </button>
      </div>
    </div>
    <b-collapse v-if="showSectionsInitial || loaded" v-model="showSections" :id="course.id">
      <b-list-group flush>
        <b-list-group-item
          button
          v-for="section in course.sections"
          :key="section.crn"
          @click.stop="toggleCourseSection(course, section)"
          :style="{
                'border-left': section.selected
                  ? `4px solid ${getBorderColor(section)}`
                  : 'none',
                'background-color': section.selected
                  ? `${getBackgroundColor(section)}`
                  : 'white'
              }"
        >
          {{ section.crn }} - {{ section.sessions[0].section }}
          <br />

          <span
            v-for="courseSession in section.sessions"
            :key="courseSession.crn + courseSession.day_of_week + courseSession.time_start"
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

import { DAY_SHORTNAMES, readableTime, readableDate } from '@/utils';

import { getBackgroundColor, getBorderColor } from '@/services/ColorService';

import { faTimes, faPlus, faChevronDown, faChevronUp } from '@fortawesome/free-solid-svg-icons';

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
      faChevronUp,
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
        this.$emit('removeCourse', course);
      } else {
        this.$emit('addCourse', course);
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
        this.$emit('removeCourseSection', section);
      } else {
        this.$emit('addCourseSection', course, section);
      }
    }
  }
};
</script>

<style>
.click-me{
  cursor: pointer;
}
  

</style>
