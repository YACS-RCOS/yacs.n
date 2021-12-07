<template>
  <div data-cy="course-listing">
    <div
      @click="callDefaultAction()"
      class="d-flex w-100 justify-content-between click-me"
    >
      <div>
        <b data-cy="name">{{ course.name }}</b>
        ({{ readableDate(course.date_start) }} -
        {{ readableDate(course.date_end) }})

        <br />
        {{ course.title }}
        <br />
        <course-sections-open-badge :course="course" />
      </div>
      <div class="d-flex">
        <slot
          name="toggleCollapseButton"
          :course="course"
          :toggleCollapse="toggleCollapse"
        >
          <button
            class="btn"
            v-if="course.sections.length"
            @click.stop="toggleCollapse()"
          >
            <svg v-if="!this.showCollapse"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
              focusable="false" 
              data-prefix="fas" 
              data-icon="chevron-down" 
              class="svg-inline--fa fa-chevron-down fa-w-14 toggle-icon" 
              role="img"  
              viewBox="0 0 448 512">
              <title> "Expand course"</title>
              <path fill="currentColor" d="M207.029 381.476L12.686 187.132c-9.373-9.373-9.373-24.569 0-33.941l22.667-22.667c9.357-9.357 24.522-9.375 33.901-.04L224 284.505l154.745-154.021c9.379-9.335 24.544-9.317 33.901.04l22.667 22.667c9.373 9.373 9.373 24.569 0 33.941L240.971 381.476c-9.373 9.372-24.569 9.372-33.942 0z"></path>
            </svg>

            <svg v-else
              xmlns="http://www.w3.org/2000/svg" 
              aria-hidden="true"
              focusable="false"
              data-prefix="fas" 
              data-icon="chevron-up" 
              class="svg-inline--fa fa-chevron-up fa-w-14 toggle-icon" 
              role="img" viewBox="0 0 448 512">
              <title> "collapse course" </title>
              <path fill="currentColor" d="M240.971 130.524l194.343 194.343c9.373 9.373 9.373 24.569 0 33.941l-22.667 22.667c-9.357 9.357-24.522 9.375-33.901.04L224 227.495 69.255 381.516c-9.379 9.335-24.544 9.317-33.901-.04l-22.667-22.667c-9.373-9.373-9.373-24.569 0-33.941L207.03 130.525c9.372-9.373 24.568-9.373 33.941-.001z"></path>
            </svg>
          </button>
        </slot>
        <button v-show="showAdd" class="btn" @click.stop="toggleCourse()">
          <svg v-if="course.selected"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
            focusable="false" 
            data-prefix="fas" 
            data-icon="times" 
            class="svg-inline--fa fa-times fa-w-11 toggle-icon" 
            role="img"  
            viewBox="0 0 352 512">
            <title>"Toggle course off"</title>
            <path fill="currentColor" d="M242.72 256l100.07-100.07c12.28-12.28 12.28-32.19 0-44.48l-22.24-22.24c-12.28-12.28-32.19-12.28-44.48 0L176 189.28 75.93 89.21c-12.28-12.28-32.19-12.28-44.48 0L9.21 111.45c-12.28 12.28-12.28 32.19 0 44.48L109.28 256 9.21 356.07c-12.28 12.28-12.28 32.19 0 44.48l22.24 22.24c12.28 12.28 32.2 12.28 44.48 0L176 322.72l100.07 100.07c12.28 12.28 32.2 12.28 44.48 0l22.24-22.24c12.28-12.28 12.28-32.19 0-44.48L242.72 256z"></path>
          </svg>

          <svg v-else
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
            focusable="false"
            data-prefix="fas"
            data-icon="plus"
            class="svg-inline--fa fa-plus fa-w-14 toggle-icon"
            role="img" 
            viewBox="0 0 448 512">
            <title>"Toggle course on"</title>
            <path fill="currentColor" d="M416 208H272V64c0-17.67-14.33-32-32-32h-32c-17.67 0-32 14.33-32 32v144H32c-17.67 0-32 14.33-32 32v32c0 17.67 14.33 32 32 32h144v144c0 17.67 14.33 32 32 32h32c17.67 0 32-14.33 32-32V304h144c17.67 0 32-14.33 32-32v-32c0-17.67-14.33-32-32-32z"></path>
          </svg>
        </button>
      </div>
    </div>
    <b-collapse
      v-if="loaded || !lazyLoadCollapse"
      v-model="showCollapse"
      :id="course.id"
    >
      <slot name="collapseContent" :course="course">
        <b-list-group flush>
          <b-list-group-item
            class="selected"
            button
            v-for="section in course.sections"
            :key="section.crn"
            @click.stop="toggleCourseSection(section)"
            :style="{
              'border-left': section.selected
                ? `4px solid ${getBorderColor(course.name)}`
                : 'none',
              'background-color': section.selected
                ? `${getBackgroundColor(course.name)} !important`
                : $store.state.darkMode
                ? 'var(--dark-primary)'
                : 'white',
              color: section.selected
                ? 'black'
                : $store.state.darkMode
                ? 'var(--dark-primary-text)'
                : 'black',
            }"
          >
            <b-row class="mb-2" align-h="between">
              <b-col cols="auto">
                {{ section.crn }} - {{ section.sessions[0].section }}
              </b-col>
              <b-col v-if="section.seats_total > 0" cols="auto">
                <course-section-seats-badge
                  :seatsOpen="section.seats_open"
                  :seatsFilled="section.seats_filled"
                  :seatsTotal="section.seats_total"
                />
              </b-col>
            </b-row>

            <span
              v-for="courseSession in section.sessions"
              :key="
                courseSession.crn +
                courseSession.day_of_week +
                courseSession.time_start
              "
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
import "@/typedef";

import { DAY_SHORTNAMES, readableTime, readableDate } from "@/utils";

import { getBackgroundColor, getBorderColor } from "@/services/ColorService";

import {
  faTimes,
  faPlus,
  faChevronDown,
  faChevronUp,
} from "@fortawesome/free-solid-svg-icons";

import CourseSectionSeatsBadge from "./CourseSectionSeatsBadge.vue";
import CourseSectionsOpenBadge from "./CourseSectionsOpenBadge.vue";

// Course Listing by default is a collapsible display of a course and its
// sections and sessions
// However, there are slots available to customize the information displayed
// So far there are two slots with the corresponding scoped props
// 1) toggleCollapseButton { course, toggleCollapse() }
// 2) collapseContent { course }
export default {
  name: "CourseListing",
  components: {
    CourseSectionSeatsBadge,
    CourseSectionsOpenBadge,
  },
  props: {
    course: Object,

    // If true, collapse is open when created
    // If lazyLoadCollapse is true, this is ignored
    openInitial: {
      type: Boolean,
      default: false,
    },
    // If true, do not render/add collapse content to the DOM
    // until collapse is opened
    // default false
    lazyLoadCollapse: {
      type: Boolean,
      default: false,
    },

    // Method name of default action
    // When body of CourseListing is clicked on, the
    // defaultAction is called
    // Kind of hacky, doesnt allow parameters, but keeps it
    // relatively flexible
    defaultAction: {
      type: String,
      default: "toggleCollapse",
    },

    //if this is false the add course + button wont appear
    //this is useful for the course explorer
    showAddButton: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      faTimes,
      faPlus,
      faChevronDown,
      faChevronUp,
      DAY_SHORTNAMES,

      // v-model with collapse
      // true or false for open or close respectively collapse
      showCollapse: !this.lazyLoadCollapse && this.openInitial,

      // initially false, set to true on first collapse toggle
      // Used for lazy loading
      loaded: false,

      showAdd: this.showAddButton,
    };
  },
  methods: {
    readableTime,
    readableDate,
    getBackgroundColor,
    getBorderColor,

    // Just a wrapper, can't call `[defaultAction]()` in html
    callDefaultAction() {
      this[this.defaultAction]();
    },

    /**
     * Toggle collapse state
     * @param {boolean} collapse If provided, set collapse state
     */
    toggleCollapse(collapse) {
      if (!this.loaded) {
        this.loaded = true;
      }

      this.showCollapse =
        collapse !== undefined ? collapse : !this.showCollapse;
    },

    /**
     * Toggle course selected state
     * Emits removeCourse and addCourse events
     */
    toggleCourse() {
      if (this.course.selected) {
        this.$emit("removeCourse", this.course);
      } else {
        this.$emit("addCourse", this.course);
      }
    },
    /**
     * Toggle use selection of course section
     * If a user is clicking on course section for the first time,
     * add course section to schedules
     * If the course section had already been clicked
     * remove course section from schedules
     * @param {CourseSection} section
     */
    toggleCourseSection(section) {
      if (section.selected) {
        this.$emit("removeCourseSection", section);
      } else {
        this.$emit("addCourseSection", this.course, section);
      }
    },

    //used in the course explorer to show a courses info modal
    showInfoModal() {
      this.$emit("showCourseInfo", this.course);
    },
  },
};
</script>

<style>
.click-me {
  cursor: pointer;
}
.toggle-icon{
  width: 1em;
  height: 1em;
}
.badge-success{
  background-color: #186329;
}

</style>
