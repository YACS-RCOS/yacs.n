<template>
  <div class="d-flex flex-column flex-grow-1">
    <div class="course-search">
      <b-form-group label="Search" label-for="search">
        <b-form-input
          id="search"
          v-model="textSearch"
          :debounce="debounceTime"
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
      </b-row>

      <div class="subject-filter" v-if="subjectSelectionReady">
        <div class="subject-group" :style="arrayToHSL('backgroundColor', subjectGroupColors[subject_group.title.toLowerCase()])" v-for="(subject_group, subject_group_index) in subjectGroups" :key="subject_group_index">
          {{ extractTitle(subject_group.title) }}<br>
          <button class="subject-buttons" :style="getSubjectButtonColor(subject)" type="button" v-for="(subject, subject_index) in subject_group.elements" :key="subject_index" @click="filterCoursesBySubject(subject)">
            {{ extractTitle(subject) }}
          </button>
          <br>
        </div>
      </div>

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
                    <font-awesome-icon :icon="faInfoCircle" />
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

import { getCourses, getDepartments } from "@/services/YacsService";

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

      subjectGroups: [],
      subjectColors: {},
      subjectGroupColors: {},
      subjectSelectionReady: false,
    };
  },
  async created() {
    getDepartments().then((departments) => {
      this.departmentOptions.push(...departments.map((d) => d.department));
    });
    await this.fetchSubjectGroups();
    this.computeSubjectColors();
    this.subjectSelectionReady = true;
  },
  methods: {
    filterCoursesBySubject(subject) {
      if (this.selectedDepartment == null || this.selectedDepartment != subject) {
        this.selectedDepartment = subject;
      }      
      else {
        this.selectedDepartment = null;
      }
    },
    getSubjectButtonColor(subject) {
      const colors = this.subjectColors[subject];
      console.log("colors: " + colors)
      if (this.selectedDepartment != null && this.selectedDepartment == subject) {
        return this.makeHSL('backgroundColor',colors[0] + 10, colors[1] + 30, colors[2] + 30)
      }
      return this.arrayToHSL('backgroundColor', colors)
    },

    extractColorHSL(element) {
      if (element.includes("#")) {
        return element.split("#")[1].split(",")
      }
      return []
    },

    extractTitle(element) {
      return element.split('#')[0]
    },

    arrayToHSL(property, array) {
      if (array.length == 4) {
        return {
          [property]: `hsla(${array[0]}, ${array[1]}%, ${array[2]}%, ${array[3]})`
        };
      }
      return {
        [property]: `hsl(${array[0]}, ${array[1]}%, ${array[2]}%)`
      };
    },

    makeHSL(property, hue, saturation, lightness, alpha = -1) {
      if (alpha != -1) {
        return {
          [property]: `hsla(${hue}, ${saturation}%, ${lightness}%, ${alpha})`
        };
      }
      // console.log("hue: " + hue + " sat:" + saturation + " light: " + lightness);
      return {
        [property]: `hsl(${hue}, ${saturation}%, ${lightness}%)`
      };
    },

    colorTextExtract(element, hue_offset = 0, saturation_offset = 0, lightness_offset = 0, alpha = 1, index = -1) {
      let colors = this.extractColorHSL(element);
      if (colors.length == 3) {
        return [(colors[0] + hue_offset) % 360, (colors[1] + saturation_offset), (colors[2] + lightness_offset), alpha]
      }
      if (index != -1) {
        return [(index * 360 + hue_offset) % 360, saturation_offset, lightness_offset, alpha]
      }
      else {
        return [hue_offset % 360, saturation_offset, lightness_offset, alpha]
      }
    },    
    
    async fetchSubjectGroups() {
      const response = await fetch('/api/dp/subjectgroups');
      this.subjectGroups = await response.json();
    },

    computeSubjectColors() {
      for (let i = 0; i < this.subjectGroups.length; ++i) {
        let group = this.subjectGroups[i];
        this.subjectGroupColors[group.title.toLowerCase()] = this.colorTextExtract(group.title, 0, 15, 70, 0.7, i / this.subjectGroups.length);
        for (let j = 0; j < group.elements.length; ++j) {
          this.subjectColors[group.elements[j]] = this.colorTextExtract(group.title, j, 12 - j * 0.25, 70 - 5 + j * 0.2, 1, i / this.subjectGroups.length)
        }
      }
      console.log(JSON.stringify(this.subjectGroupColors))
      console.log(JSON.stringify(this.subjectColors))
      console.log(JSON.stringify(this.subjectGroups))
    },



    courseInfoModalToggle(course) {
      this.$emit("showCourseInfo", course);
    },
    /* wrapper for querying with search */
    // todo: get courses should be changed
    //text parameter comes from watch
    updateCourseList() {
      getCourses(this.selectedSemester, this.textSearch, false).then(
        (course_list) => {
          this.courseList = course_list;
        }
      );
    },
    checkFunction(courseInput, textSearch) {
      const text = textSearch
        .trim()
        .replace(/[ !+=_;:'?.>,<|)(*&^%$#@~`-]+/g, "")
        .toUpperCase();
      const input = courseInput
        .trim()
        .replace(/[ !+=_;:'?.>,<|)(*&^%$#@~`-]+/g, "");
      if (input.includes(text)) {
        return true;
      }
      return false;
    },
    filterSection(courses) {
      return courses.filter(
        (course) =>
          (!this.selectedDepartment ||
            course.department === this.selectedDepartment) &&
          (!this.selectedSubsemester ||
            (this.selectedSubsemester.date_start.getTime() ===
              course.date_start.getTime() &&
              this.selectedSubsemester.date_end.getTime() ===
                course.date_end.getTime()))
      );
    },
  },
  watch: {
    /* This value gets debounced */
    textSearch: function () {
      //store in temp to conserve textSearch in input box on screen but removes extra characters for comparing
      this.updateCourseList();
    },
  },
  computed: {
    ...mapState(["selectedSemester", "subsemesters", "departments"]),
    fullList() {
      return this.$store.getters.courses;
    },
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
    filterCourses: function () {
      const courses =
        this.courseList !== null
          ? this.courseList
          : this.$store.getters.courses;

      const filtered = this.filterSection(courses);

      //returns exact match, if not found, then department filtered list
      const find = filtered.find(
        (course) =>
          (course.full_title &&
            course.full_title.toUpperCase() ===
              this.textSearch.toUpperCase()) ||
          course.title.toUpperCase() === this.textSearch.toUpperCase()
      );

      const fullListFiltered = this.filterSection(this.fullList);
      const containString = fullListFiltered.filter(
        (course) =>
          this.checkFunction(course.title, this.textSearch) ||
          this.checkFunction(course.department + course.level, this.textSearch)
      );

      if (find) {
        return [find];
      } else {
        return containString;
      }
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

.subject-filter {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 4px;
  margin-top: 4px;
  margin-bottom: 4px;
  position: relative;
}

.subject-group {
  font-weight: 700;
  font-size: 15px;
  color: #141415;
  border-radius: 4px;
  padding: 6px;
  padding-top: 4px;
  padding-bottom: 2px;
}

.subject-buttons {
  border: none;
  border-radius: 4px;
  font-size: 11px;
  width: 43px;
  padding: 0px;
  font-weight: 600;
  margin-bottom: 0px;
  margin-top: 0px;
  margin-left: 2px;
  margin-right: 2px;
  color: #141415;
  background-color:#141415;
  transition: background-color 0.15s ease;
  text-align: center;
}
.subject-buttons:hover {
  background-color: rgb(80, 85, 87);
}
</style>
