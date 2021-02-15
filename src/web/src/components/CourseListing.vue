<template>
  <div
    data-cy="course-listing"
    class="pl-3 py-3"
    style="border-top: 3px solid lightgrey;"
    :style="{
      'background-color': $store.state.schedule.selectedCoursesById[course.id]
        ? `${getBackgroundColor(course.id)} !important`
        : $store.state.darkMode
        ? 'var(--dark-primary)'
        : undefined,
      color: $store.state.darkMode ? 'var(--dark-primary)' : undefined,
    }"
  >
    <b-row
      style="cursor: pointer; flex-direction: column;"
      @click="toggleCourse()"
    >
      <b-col>
        <b-row align-h="between">
          <b-col cols="auto">
            <strong>{{ course.name }}</strong>
            ({{ readableDate(course.date_start) }} -
            {{ readableDate(course.date_end) }})
            <br />
            {{ course.title }}
          </b-col>
          <b-col cols="auto" class="mr-2">
            <button class="btn" @click.stop="toggleCourse()">
              <font-awesome-icon
                v-if="$store.state.schedule.selectedCoursesById[course.id]"
                :icon="faTimes"
              />
              <font-awesome-icon v-else :icon="faPlus" />
            </button>
          </b-col>
        </b-row>
      </b-col>
      <b-col>
        <b-row align-h="between">
          <b-col cols="auto">
            <course-sections-open-badge :course="course" />
          </b-col>
          <b-col cols="auto">
            <b-button-group>
              <button
                v-if="course.description || course.raw_precoreqs"
                class="btn"
                data-cy="course-info-button"
              >
                <router-link
                  :to="`/explore/${course.department}/${course.name}`"
                >
                  <font-awesome-icon :icon="faInfoCircle" />
                </router-link>
              </button>

              <button
                v-if="course.sections.length"
                class="btn"
                @click.stop="toggleCollapse()"
              >
                <font-awesome-icon v-if="!showCollapse" :icon="faChevronDown" />
                <font-awesome-icon v-else :icon="faChevronUp" />
              </button>
            </b-button-group>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
    <b-collapse
      :id="course.id"
      v-model="showCollapse"
      :style="{
        color: $store.state.darkMode ? 'var(--dark-text-primary)' : undefined,
      }"
    >
      <b-list-group
        flush
        style="
          border-top: 1px solid lightgrey;
          border-bottom: 1px solid lightgrey;
        "
      >
        <b-list-group-item
          v-for="section in course.sections"
          :key="section.crn"
          button
          :style="{
            'margin-left': activeCourseSectionsByCrn[section.crn]
              ? '8px'
              : undefined,
            'border-left': activeCourseSectionsByCrn[section.crn]
              ? `8px solid ${getBorderColor(course.id)}`
              : '1px solid lightgrey',
            'background-color': $store.state.schedule
              .selectedCourseSectionsByCrn[section.crn]
              ? `${getBackgroundColor(course.id)} !important`
              : $store.state.darkMode
              ? 'var(--dark-primary)'
              : undefined,
            color: $store.state.schedule.selectedCourseSectionsByCrn[
              section.crn
            ]
              ? 'black'
              : $store.state.darkMode
              ? 'var(--dark-primary-text)'
              : undefined,
          }"
          @click.stop="toggleCourseSection(section)"
        >
          <b-row class="mb-2" align-h="between">
            <b-col cols="auto">
              {{ section.crn }} - {{ section.sessions[0].section }}
            </b-col>
            <b-col v-if="section.seats_total > 0" cols="auto">
              <course-section-seats-badge
                :seats-open="section.seats_open"
                :seats-filled="section.seats_filled"
                :seats-total="section.seats_total"
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
    </b-collapse>
  </div>
</template>

<script>
import { DAY_SHORTNAMES, readableTime, readableDate } from "@/utils";
import { COLOR_NAMESPACE } from "@/store/modules/color";
import { mapGetters } from "vuex";

// import { getBackgroundColor, getBorderColor } from "@/services/ColorService";

import {
  faTimes,
  faPlus,
  faChevronDown,
  faChevronUp,
  faInfoCircle,
} from "@fortawesome/free-solid-svg-icons";

import CourseSectionSeatsBadge from "./CourseSectionSeatsBadge.vue";
import CourseSectionsOpenBadge from "./CourseSectionsOpenBadge.vue";

import { scheduleTypes } from "@/store/modules/schedule";

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
    /** @type {import("vue").PropType<import("@/typedef").CourseSection[]>} */
    activeCourseSections: {
      type: Array,
      default: () => [],
    },

    // If true, collapse is open when created
    // If lazyLoadCollapse is true, this is ignored
    // openInitial: {
    //   type: Boolean,
    //   default: false,
    // },
    // // If true, do not render/add collapse content to the DOM
    // // until collapse is opened
    // // default false
    // lazyLoadCollapse: {
    //   type: Boolean,
    //   default: false,
    // },

    // // Method name of default action
    // // When body of CourseListing is clicked on, the
    // // defaultAction is called
    // // Kind of hacky, doesnt allow parameters, but keeps it
    // // relatively flexible
    // defaultAction: {
    //   type: String,
    //   default: "toggleCollapse",
    // },

    //if this is false the add course + button wont appear
    //this is useful for the course explorer
    // showAddButton: {
    //   type: Boolean,
    //   default: true,
    // },
  },
  data() {
    return {
      faTimes,
      faPlus,
      faChevronDown,
      faChevronUp,
      faInfoCircle,
      DAY_SHORTNAMES,

      // v-model with collapse
      // true or false for open or close respectively collapse
      // showCollapse: !this.lazyLoadCollapse && this.openInitial,
      showCollapse: true,
      // // initially false, set to true on first collapse toggle
      // // Used for lazy loading
      // loaded: false,

      // showAdd: this.showAddButton,
    };
  },
  computed: {
    ...mapGetters(COLOR_NAMESPACE, ["getBackgroundColor", "getBorderColor"]),
    activeCourseSectionsByCrn() {
      const activeCourseSectionCrns = new Set(
        this.activeCourseSections.map((section) => section.crn)
      );
      return this.course.sections.reduce(
        (obj, section) => ({
          ...obj,
          [section.crn]: activeCourseSectionCrns.has(section.crn),
        }),
        {}
      );
    },
  },
  methods: {
    readableTime,
    readableDate,
    // getBackgroundColor,
    // getBorderColor,

    // Just a wrapper, can't call `[defaultAction]()` in html
    // callDefaultAction() {
    //   this[this.defaultAction]();
    // },

    /**
     * Toggle collapse state
     *
     * @param {boolean} collapse If provided, set collapse state
     */
    toggleCollapse(collapse) {
      this.showCollapse =
        collapse !== undefined ? collapse : !this.showCollapse;
    },

    /**
     * Toggle course selected state
     * Emits removeCourse and addCourse events
     */
    async toggleCourse() {
      if (this.$store.state.schedule.selectedCoursesById[this.course.id]) {
        // if (this.course.selected) {
        // this.$emit("removeCourse", this.course);
        await this.$store.dispatch(scheduleTypes.actions.UNSELECT_COURSE, {
          courseId: this.course.id,
        });
      } else {
        // this.$emit("addCourse", this.course);
        await this.$store.dispatch(scheduleTypes.actions.SELECT_COURSE, {
          courseId: this.course.id,
        });
      }
    },
    /**
     * Toggle use selection of course section
     * If a user is clicking on course section for the first time,
     * add course section to schedules
     * If the course section had already been clicked
     * remove course section from schedules
     *
     * @param {CourseSection} section
     */
    async toggleCourseSection(section) {
      if (this.$store.state.schedule.selectedCourseSectionsByCrn[section.crn]) {
        // if (section.selected) {
        // this.$emit("removeCourseSection", this.course, section);
        await this.$store.dispatch(
          scheduleTypes.actions.UNSELECT_COURSE_SECTION,
          {
            courseId: this.course.id,
            courseSectionCrn: section.crn,
          }
        );
      } else {
        // this.$emit("addCourseSection", this.course, section);
        await this.$store.dispatch(
          scheduleTypes.actions.SELECT_COURSE_SECTION,
          {
            courseId: this.course.id,
            courseSectionCrn: section.crn,
          }
        );
      }
    },

    //used in the course explorer to show a courses info modal
    // showInfoModal() {
    //   this.$emit("showCourseInfo", this.course);
    // },
  },
};
</script>

<style scoped>
.action-button:hover {
  background-color: grey;
}
</style>
