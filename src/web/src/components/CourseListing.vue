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
        <button class="btn" @click="toggleCourse(course)">
          <font-awesome-icon v-if="course.selected" :icon="faTimes" />
          <font-awesome-icon v-else :icon="faPlus" />
        </button>
        <slot name="toggleCollapseButton" :course="course" :toggleCollapse="toggleCollapse">
          <button class="btn" @click="toggleCollapse()" :disabled="!course.sections.length">
            <font-awesome-icon :icon="faChevronDown" />
          </button>
        </slot>
      </div>
    </div>
    <b-collapse v-if="loaded || !lazyLoadCollapse" v-model="showCollapse" :id="course.id">
      <slot name="collapseContent" :course="course">
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
      </slot>
    </b-collapse>
  </div>
</template>

<script>
import '@/typedef';

import { DAY_SHORTNAMES, readableTime, readableDate } from '@/utils';

import { getBackgroundColor, getBorderColor } from '@/services/ColorService';

import { faTimes, faPlus, faChevronDown } from '@fortawesome/free-solid-svg-icons';

// Course Listing by default is a collapsible display of a course and its
// sections and sessions
// However, there are slots available to customize the information displayed
// So far there are two slots with the corresponding scoped props
// 1) toggleCollapseButton { course, toggleCollapse() }
// 2) collapseContent { course }
export default {
  name: 'CourseListing',
  props: {
    course: Object,

    // If true, collapse is open when created
    // If lazyLoadCollapse is true, this is ignored
    openInitial: {
      type: Boolean,
      default: false
    },
    // If true, do not render/add collapse content to the DOM
    // until collapse is opened
    // default false
    lazyLoadCollapse: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      faTimes,
      faPlus,
      faChevronDown,
      DAY_SHORTNAMES,

      // v-model with collapse
      // true or false for open or close respectively collapse
      showCollapse: !this.lazyLoadCollapse && this.openInitial,

      // initially false, set to true on first collapse toggle
      // Used for lazy loading
      loaded: false
    };
  },
  methods: {
    readableTime,
    readableDate,
    getBackgroundColor,
    getBorderColor,
    /**
     * Toggle collapse state
     * @param {boolean} collapse If provided, set collapse state
     */
    toggleCollapse(collapse) {
      if (!this.loaded) {
        this.loaded = true;
      }

      this.showCollapse = collapse !== undefined ? collapse : !this.showCollapse;
    },

    /**
     * Toggle course selected state
     * Emits removeCourse and addCourse events
     * @param {Course} course
     */
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
</style>
