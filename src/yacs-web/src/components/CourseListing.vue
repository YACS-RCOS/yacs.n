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
        <button
          v-if="actions.add"
          class="btn"
          v-show="!course.selected"
          @click="$emit('addCourse', course)"
        >
          <font-awesome-icon :icon="faPlus" />
        </button>
        <button v-if="actions.remove" class="btn" @click="$emit('removeCourse', course)">
          <font-awesome-icon :icon="faTimes" />
        </button>
        <button class="btn" @click="showSections = !showSections">
          <font-awesome-icon :icon="faChevronDown" />
        </button>
      </div>
    </div>
    <b-collapse v-model="showSections" :id="course.id">
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

import { faTimes, faPlus, faChevronDown } from '@fortawesome/free-solid-svg-icons';

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

      showSections: this.showSectionsInitial
    };
  },
  methods: {
    readableTime,
    readableDate,
    getBackgroundColor,
    getBorderColor,
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