<template>
  <div class="d-flex flex-column flex-grow-1">
    <div class="course-search">
      <b-form-group label="Search" label-for="search">
        <b-form-input
          id="search"
          v-model="textSearch"
          trim
          placeholder="Intro to College - COLG 1030"
          list="list-id"
        ></b-form-input>
        <b-form-datalist
          id="list-id"
          :options="mapCourseNames"
          :select-size="10"
        ></b-form-datalist>
      </b-form-group>

      <b-row>
        <!-- >2 b/c default ALL option always present -->
        <b-col v-if="subsemesterOptions.length > 2">
          <b-form-group label="Filter Sub-Semester" for="sub-semester">
            <b-form-select
              v-model="selectedSubsemester"
              :options="subsemesterOptions"
            ></b-form-select>
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group label="Filter Department" for="department">
            <b-form-select
              v-model="selectedDepartment"
              :options="departmentOptions"
            ></b-form-select>
          </b-form-group>
        </b-col>
      </b-row>
    </div>

    <hr />
    <div id="scroll-box">
      <recycle-scroller
        class="scroller"
        :items="filterCourses"
        :item-size="100"
        typeField="vscrl_type"
        v-slot="{ item: course }"
      >
        <div class="course-listing" :class="{ 'bg-light': course.selected }">
          <CourseListing
            :course="course"
            defaultAction="toggleCourse"
            v-on="$listeners"
            lazyLoadCollapse
          >
            <template #toggleCollapseButton="{ course }">
              <button
                v-show="
                  course.corequisites ||
                  course.prerequisites ||
                  course.raw_precoreqs
                "
                class="btn"
                @click.stop="courseInfoModalToggle(course)"
              >
                <font-awesome-icon :icon="faInfoCircle" />
              </button>
            </template>
            <template #collapseContent>
              {{ null }}
            </template>
          </CourseListing>
        </div>
      </recycle-scroller>
    </div>
  </div>
</template>

<script>
import "@/typedef";

import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";

import { DAY_SHORTNAMES } from "@/utils";

import { getDepartments, getCourses } from "@/services/YacsService";

import CourseListingComponent from "@/components/CourseListing";

import { RecycleScroller } from "vue-virtual-scroller";

export default {
  name: "CourseList",
  components: {
    CourseListing: CourseListingComponent,
    RecycleScroller,
  },
  props: {
    courses: Array,
    subsemesters: Array,
    selectedSemester: null,
  },
  data() {
    return {
      faInfoCircle,
      DAY_SHORTNAMES,
      textSearch: "",
      selectedSubsemester: null,
      selectedDepartment: null,
      departmentOptions: [{ text: "All", value: null }],
      courseList: this.courses,
      courseUpdate: _.debounce(this.updateCourseList, 350),
    };
  },
  created() {
    getDepartments().then((departments) => {
      this.departmentOptions.push(...departments.map((d) => d.department));
    });
  },
  methods: {
    courseInfoModalToggle(course) {
      this.$emit("showCourseInfo", course);
    },
    // wrapper for querying with search
    updateCourseList() {
      getCourses(this.selectedSemester, this.textSearch).then((course_list) => {
        this.courseList = course_list;
      });
    },
    /**
     * Given a function and time in ms, will not execute function until it stops being called.
     * @param func: Function to be called
     * @param wait: timeout in ms
     */
    debounce(func, wait) {
      let timerId;
      return function (...args) {
        if (timerId) {
          clearTimeout(timerId);
        }
        timerId = setTimeout(() => {
          func(...args);
          timerId = null;
        }, wait);
      };
    },
  },
  watch: {
    textSearch: function (newSearch) {
      // default list if no input
      if (newSearch.length === 0) {
        this.courseList = this.courses;
        return;
      }

      // debounce query for courses
      this.courseUpdate();
    },
  },
  computed: {
    subsemesterOptions() {
      let options = [{ text: "All", value: null }];
      options.push(
        ...this.subsemesters.map((subsemester) => {
          return { text: subsemester.display_string, value: subsemester };
        })
      );
      // Once we get new data for the <select>, v-model will retain its old value.
      // Need to update this value after receving new data to keep values consistent.
      // eslint-disable-next-line
      this.selectedSubsemester = options[0].value;
      return options;
    },
    // returns exact match if possible.
    // if no exact match exists, returns similar options.
    filterCourses() {
      // filter by selected department
      const filtered = this.courseList.filter(
        (course) =>
          !this.selectedDepartment ||
          course.department === this.selectedDepartment
      );

      // returns exact match, if not found, then department filtered list
      const find = filtered.find(
        (course) =>
          (course.full_title &&
            course.full_title.toUpperCase() ===
              this.textSearch.toUpperCase()) ||
          course.title.toUpperCase() === this.textSearch.toUpperCase()
      );

      if (find) return [find];
      else return filtered;
    },
    // return a list of the titles of each course.
    mapCourseNames() {
      return this.filterCourses.map((course) => {
        return course.full_title || course.title;
      });
    },
  },
};
</script>

<style scoped lang="scss">
#scroll-box {
  // overflow-y: scroll !important;
  // overflow-x: hidden;
  flex-grow: 1;
  flex-basis: 0px; // allows flex and scroll combo
  // flex-grow will set height during runtime
  min-height: 200px; // fix for when at breakpoint <= md. Height isn't filling for some reason.
}

.scroller {
  height: 100%;
  overflow-x: hidden;
}

.course-listing {
  height: 100px;
  padding-top: 10px;
  border-bottom: 1px solid #e9ecef;
}
</style>
