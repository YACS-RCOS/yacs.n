<template>
  <div class="d-flex flex-column flex-grow-1">
    <div class="course-search">
      <b-form-group label="Search" label-for="search">
        <b-form-input
          id="search"
          v-model="textSearch"
          :debounce="debounceTime"
          trim
          placeholder="Intro to College - COLG 1030"
          list="list-id"
        ></b-form-input>
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
    <!-- Start of Dynamic Scrolling Rendering To Account For Varying Course Data. > -->
    <hr />
    <div id="scroll-box" data-cy="course-list">
      <div v-if="filterCourses.length == 0" class="no-courses">
        Oops, no results!
      </div>
      <DynamicScroller
        class="scroller"
        :items="filterCourses"
        :min-item-size="10"
        typeField="vscrl_type"
      >
        <template v-slot="{ item: course, index, active }">
          <DynamicScrollerItem
            :item="course"
            :active="active"
            :size-dependencies="[course.title]"
            :data-index="index"
            :emitResize="true"
          >
            <div
              class="course-listing"
              :class="{ 'bg-light': course.selected }"
            >
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
                    data-cy="course-info-button"
                  >
                    <svg 
                      xmlns="http://www.w3.org/2000/svg"
                      aria-hidden="true" 
                      focusable="false" 
                      data-prefix="fas" 
                      data-icon="info-circle" 
                      class="svg-inline--fa fa-info-circle fa-w-16 nfo-icon" 
                      role="img"  viewBox="0 0 512 512">
                      <title> "Course info"</title>
                      <path fill="currentColor" d="M256 8C119.043 8 8 119.083 8 256c0 136.997 111.043 248 248 248s248-111.003 248-248C504 119.083 392.957 8 256 8zm0 110c23.196 0 42 18.804 42 42s-18.804 42-42 42-42-18.804-42-42 18.804-42 42-42zm56 254c0 6.627-5.373 12-12 12h-88c-6.627 0-12-5.373-12-12v-24c0-6.627 5.373-12 12-12h12v-64h-12c-6.627 0-12-5.373-12-12v-24c0-6.627 5.373-12 12-12h64c6.627 0 12 5.373 12 12v100h12c6.627 0 12 5.373 12 12v24z"></path>
                    </svg>
                  </button>
                </template>
                <template #collapseContent>
                  {{ null }}
                </template>
              </CourseListing>
            </div>
          </DynamicScrollerItem>
        </template>
      </DynamicScroller>
    </div>
  </div>
</template>

<script>
import "@/typedef";
import { mapState } from "vuex";
import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";

import { DAY_SHORTNAMES } from "@/utils";

import { getDepartments, getCourses } from "@/services/YacsService";

import CourseListingComponent from "@/components/CourseListing";

import { DynamicScroller, DynamicScrollerItem } from "vue-virtual-scroller";

export default {
  name: "CourseList",
  components: {
    CourseListing: CourseListingComponent,
    DynamicScroller,
    DynamicScrollerItem,
  },
  data() {
    return {
      faInfoCircle,
      DAY_SHORTNAMES,
      textSearch: "",
      selectedSubsemester: null,
      selectedDepartment: null,
      courseList: null,
      debounceTime: 300,
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
    /* wrapper for querying with search */
    updateCourseList() {
      getCourses(this.selectedSemester, this.textSearch, false).then(
        (course_list) => {
          this.courseList = course_list;
        }
      );
    },
  },
  watch: {
    /* This value gets debounced */
    textSearch: function () {
      this.updateCourseList();
    },
  },
  computed: {
    ...mapState(["selectedSemester", "subsemesters", "departments"]),

    departmentOptions() {
      return [{ text: "All", value: null }].concat(
        ...this.departments.map(({ department }) => department)
      );
    },

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
      const courses =
        this.courseList !== null
          ? this.courseList
          : this.$store.getters.courses;

      // filter by selected department
      const filtered = courses.filter(
        (course) =>
          (!this.selectedDepartment ||
            course.department === this.selectedDepartment) &&
          (!this.selectedSubsemester ||
            (this.selectedSubsemester.date_start.getTime() ===
              course.date_start.getTime() &&
              this.selectedSubsemester.date_end.getTime() ===
                course.date_end.getTime()))
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

.form-group {
  font-size: 16px;
}
.course-listing {
  padding: 10px;
  border-bottom: 1px solid #dbdbdc;
}

.no-courses {
  border-style: solid;
  border-width: 2px;
  border-color: rgb(0, 0, 0, 0.05);
  font-size: 17px;
  padding: 20px;
}

.info-icon{
  width: 1em;
  height: 1em;
}
</style>
