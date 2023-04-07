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
            <font-awesome-icon v-if="!showCollapse" :icon="faChevronDown" />
            <font-awesome-icon v-else :icon="faChevronUp" />
          </button>
        </slot>
        <button v-show="showAdd" class="btn" @click.stop="toggleCourse()">
          <font-awesome-icon v-if="course.selected" :icon="faTimes" />
          <font-awesome-icon v-else :icon="faPlus" />
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
            v-for="section in sortedSections"
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
                {{ section.crn }} - {{ section.sessions[0].section }} -
                {{ getInstructor(section.sessions) }}
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
      console.log("course obj below");
        console.log(this.course);
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
    getInstructor(sessions) {
      for (let i = 0; i < sessions.length; i++) {
        if (sessions[i].instructor !== "Staff") {
          return sessions[i].instructor;
        }
      }
    },
  },
  computed: {
    sortedSections() {
      return this.course.sections
        .slice()
        .sort((a, b) => a.sessions[0].section - b.sessions[0].section);
    },
  },
};
</script>

<style>
.click-me {
  cursor: pointer;
}
</style>
