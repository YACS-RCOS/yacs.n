<template>
  <div class="d-flex flex-column flex-grow-1">
    <div class="course-search">
      <b-form-group label="Search" label-for="search">
        <b-form-input
          id="search"
          v-model="textSearch"
          trim
          placeholder="Intro to College - COLG 1030 - 5/2"
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
        <CourseListing :course="course" :actions="{add:true}" v-on="$listeners" />
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
import '@/typedef';

import { DAY_SHORTNAMES } from '@/utils';

import { getDepartments, getSubSemesters } from '@/services/YacsService';

import CourseListingComponent from '@/components/CourseListing';

export default {
  name: 'CourseList',
  components: {
    CourseListing: CourseListingComponent
  },
  // props: {
  //   courses: Array
  // },
  data() {
    return {
      DAY_SHORTNAMES,
      textSearch: null,
      selectedSubsemester: null,
      subsemesterOptions: [{ text: 'All', value: null }],
      selectedDepartment: null,
      departmentOptions: [{ text: 'All', value: null }]
    };
  },
  created() {
    getDepartments().then(departments => {
      this.departmentOptions.push(...departments.map(d => d.department));
    });
    getSubSemesters().then(subsemesters => {
      this.subsemesterOptions.push(
        ...subsemesters.map(subsemester => {
          return { text: subsemester.display_string, value: subsemester };
        })
      );
    });
  },
  computed: {
    /**
     * Returns a list of courses that match the selected filters
     * @returns {Course[]}
     */
    filteredCourses() {
      // return this.courses
      return this.$store.getters.courses
      .filter(({ date_start, date_end, department, title }) => {
        return (
          (!this.selectedSubsemester ||
            (this.selectedSubsemester.date_start.getTime() === date_start.getTime() &&
              this.selectedSubsemester.date_end.getTime() === date_end.getTime())) &&
          (!this.selectedDepartment || this.selectedDepartment === department) &&
          (!this.textSearch || title.includes(this.textSearch.toUpperCase()))
        );
      });
    }
  }
};
</script>

<style scoped lang="scss">
#scroll-box {
  overflow-y: scroll !important;
  overflow-x: auto;
  height: 0px; // allows flex and scroll combo
              // flex-grow will set height during runtime
}
</style>
