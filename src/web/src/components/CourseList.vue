<template>
  <div class="d-flex flex-column flex-grow-1">
    <div class="course-search">
      <b-form-group label="Search" label-for="search">
        <b-form-input
          id="search"
          v-model="textSearch"
          trim
          placeholder="Intro to College - COLG 1030"
        ></b-form-input>
      </b-form-group>

      <b-row>
        <!-- >2 b/c default ALL option always present -->
        <b-col v-if="subsemesterOptions.length > 2">
          <b-form-group label="Filter Sub-Semester" for="sub-semester">
            <b-form-select v-model="selectedSubsemester" :options="subsemesterOptions"></b-form-select>
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Filter Department" for="department">
            <b-form-select v-model="selectedDepartment" :options="departmentOptions"></b-form-select>
          </b-form-group>
        </b-col>
      </b-row>
    </div>

    <hr />

    <b-list-group id="scroll-box" class="mb-2 mb-sm-0 flex-grow-1" flush>
      <b-list-group-item
        v-for="course in filteredCourses"
        :key="course.id"
        :class="{'bg-light': course.selected}"
      >
        <CourseListing :course="course" defaultAction="toggleCourse" v-on="$listeners">
          <template #toggleCollapseButton="{ course }">
            <button
              v-show="course.corequisites || course.prerequisites || course.raw_precoreqs"
              class="btn"
              @click.stop="courseInfoModalToggle(course)"
            >
              <font-awesome-icon :icon="faInfoCircle" />
            </button>
          </template>
          <template
            #collapseContent="{ course: {corequisites, prerequisites, raw_precoreqs, frequency, description} }"
          >
            <b-modal :id="course.name" :title="course.name  + ' ' + course.title" hide-footer>
              <span v-if="frequency">
                Offered: {{frequency}}
                <br />
                <br />
              </span>
              <span>{{generateRequirementsText(prerequisites, corequisites, raw_precoreqs)}}</span>
              <span v-if="description">
                <br />
                <br />
                {{description}}
              </span>
              <br />
              <br />
              <b-button
                variant="primary"
                @click="toggleCourse(course);courseInfoModalToggle(course)"
              >{{course.selected ? 'Remove from schedule' : 'Add to schedule'}}</b-button>
              <b-button class="ml-2" variant="danger" @click="courseInfoModalToggle(course)">Close</b-button>
            </b-modal>
          </template>
        </CourseListing>
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
import '@/typedef';

import { faInfoCircle } from '@fortawesome/free-solid-svg-icons';

import { DAY_SHORTNAMES } from '@/utils';

import { getDepartments } from '@/services/YacsService';

import CourseListingComponent from '@/components/CourseListing';

export default {
  name: 'CourseList',
  components: {
    CourseListing: CourseListingComponent
  },
  props: {
    courses: Array,
    subsemesters: Array,
    selectedSemester: null
  },
  data() {
    return {
      faInfoCircle,
      DAY_SHORTNAMES,
      textSearch: null,
      selectedSubsemester: null,
      selectedDepartment: null,
      departmentOptions: [{ text: 'All', value: null }]
    };
  },
  created() {
    getDepartments().then(departments => {
      this.departmentOptions.push(...departments.map(d => d.department));
    });
  },
  methods: {
    /**
     * Toggle course selected state
     * Emits removeCourse and addCourse events
     */
    toggleCourse(course) {
      if (course.selected) {
        this.$emit('removeCourse', course);
      } else {
        this.$emit('addCourse', course);
      }
    },
    courseInfoModalToggle(course) {
      this.$root.$emit('bv::toggle::modal', course.name);
    },
    generateRequirementsText(prereqs, coreqs, raw) {
      let text = [];
      if (prereqs || coreqs) {
        const same = JSON.stringify(prereqs) == JSON.stringify(coreqs);

        text.push('Requires');

        if (prereqs) {
          text.push('completion of');

          if (!same) text.push(prereqs.join(', '));
        }

        if (prereqs && coreqs) text.push(same ? 'or' : 'and');

        if (coreqs) {
          text.push('concurrent enrollment in');

          text.push(coreqs.join(', '));
        }
      } else {
        text.push('Requirements:', raw);
      }

      return text.join(' ');
    }
  },
  computed: {
    subsemesterOptions() {
      let options = [{ text: 'All', value: null }];
      options.push(
        ...this.subsemesters.map(subsemester => {
          return { text: subsemester.display_string, value: subsemester };
        })
      );
      // Once we get new data for the <select>, v-model will retain its old value.
      // Need to update this value after receving new data to keep values consistent.
      // eslint-disable-next-line
      this.selectedSubsemester = options[0].value;
      return options;
    },
    /**
     * Returns a list of courses that match the selected filters
     * @returns {Course[]}
     */
    filteredCourses() {
      return this.courses.filter(({ date_start, date_end, department, title, semester }) => {
        return (
          (!this.selectedSubsemester ||
            (this.selectedSubsemester.date_start.getTime() === date_start.getTime() &&
              this.selectedSubsemester.date_end.getTime() === date_end.getTime())) &&
          (!this.selectedDepartment || this.selectedDepartment === department) &&
          (!this.textSearch || title.includes(this.textSearch.toUpperCase())) &&
          this.selectedSemester === semester
        );
      });
    }
  }
};
</script>

<style scoped lang="scss">
#scroll-box {
  overflow-y: scroll !important;
  overflow-x: hidden;
  flex-basis: 0px; // allows flex and scroll combo
  // flex-grow will set height during runtime
  min-height: 200px; // fix for when at breakpoint <= md. Height isn't filling for some reason.
}
</style>
