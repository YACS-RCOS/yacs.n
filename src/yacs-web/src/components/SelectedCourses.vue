<template>
  <b-row>
    <b-col cols="auto">
      <h5>CRNs: {{ selectedCrns }}</h5>
    </b-col>
    <button class="col-auto btn btn-success ml-auto mb-2 mr-2 d-block" @click="exportScheduleToIcs">
      <font-awesome-icon :icon="exportIcon" />Export to ICS
    </button>
    <b-col cols="12">
      <b-card-group no-body columns>
        <b-card
          v-for="course of courses"
          :key="course.name"
          :title="course.name"
          :sub-title="course.title"
          class="selected-course-card"
        >
          <button type="button" class="close text-muted" @click="removeCourse(course)">
            <span>&times;</span>
          </button>
          {{ readableDate(course.date_start) }}-{{ readableDate(course.date_end) }}
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
        </b-card>
      </b-card-group>
    </b-col>
  </b-row>
</template>

<script>
import '@/typedef';

import { DAY_SHORTNAMES, readableTime, readableDate } from '@/utils';

import { getBackgroundColor, getBorderColor } from '@/services/ColorService';

import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';

export default {
  name: 'SelectedCourses',
  props: {
    courses: Object
  },
  data() {
    return {
      DAY_SHORTNAMES,
      exportIcon: faPaperPlane,
      ICS_DAY_SHORTNAMES: ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
    };
  },
  methods: {
    readableTime,
    readableDate,
    getBackgroundColor,
    getBorderColor,
    /**
     * Remove a course from `selectedCourses` and remove all its sections from all schedules
     * @param {Course} course
     */
    removeCourse(course) {
      this.$emit('removeCourse', course);
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
    /**
     * Returns list of CRNs for all selected sections
     * @returns {string[]}
     */
    selectedCrns() {
      return Object.values(this.courses)
        .map(c => c.sections.filter(s => s.selected))
        .flat()
        .map(s => s.crn)
        .join(', ');
    }
  }
};
</script>

<style lang="scss">
.selected-course-card {
  max-width: 270px;
  min-width: 270px;

  .close {
    position: absolute;
    top: 10px;
    right: 15px;
  }
}
</style>
