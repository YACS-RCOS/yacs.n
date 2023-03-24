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
    <!-- <div>
      <button @click="showModal = true">Time Filter</button>
      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <div v-show="showPopupWindow">
            <h3>Popup Window</h3>
            <table>
              <tbody>
                <tr v-for="(row, rowIndex) in colors" :key="rowIndex">
                  <td v-for="(cell, cellIndex) in row" :key="cellIndex">
                    <button
                      :id="rowIndex + ',' + cellIndex"
                      :class="{ 'color-button': true, 'grey': !cell, 'white': cell }"
                      @click="switchColor(rowIndex, cellIndex)"
                    >
                      {{ rowIndex * 5 + cellIndex + 1 }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <button @click="showModal = false">Cancel</button>
        </div>
      </div>
    </div> -->
    <div>
      <button @click="togglePopupWindow">Show Popup Window</button>
      <div v-show="showPopupWindow">
        <h3>Popup Window</h3>
        <table>
          <tbody>
            <tr v-for="(row, rowIndex) in colors" :key="rowIndex">
              <td v-for="(cell, cellIndex) in row" :key="cellIndex">
                <button
                  :id="rowIndex + ',' + cellIndex"
                  :class="{ 'color-button': true, 'grey': !cell, 'white': cell }"
                  @click="switchColor(rowIndex, cellIndex)"
                >
                {{ times[rowIndex][cellIndex] }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <!-- <div style="float: left;" class="w-10">
      <b-button
        @click="showPopup = !showPopup"
        style="
          margin-top: 0px;
          color: #007bff;
          border: solid #007bff;
          background-color: transparent;
        ">
        Filter by Time
      </b-button>
      <popup-grid v-if="showPopup"></popup-grid>
    </div> -->
    <!-- <div class="popup-grid">
      <table>
        <tbody>
          <tr v-for="(row, rowIndex) in grid" :key="rowIndex">
            <td v-for="(cell, colIndex) in row" :key="colIndex">
              <button @click="toggleCell(rowIndex, colIndex)" :class="{ active: cell }" >
            </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div> -->
    <!-- <div>
      <button @click="showPopup = !showPopup" style="
      margin-top: 10px;
      color: #007bff;
      border: solid #007bff;
      background-color: transparent;
    ">Filter by Time</button>
      <popup-grid v-if="showPopup" :grid="grid" @update-grid="grid = $event"></popup-grid>
    </div> -->
    <!-- Button trigger modal -->
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
      select_start:null,
      select_end :null,
      select_day:null,
      debounceTime: 300,
      colors: [
        [true, true, true, true, true],
        [true, true, true, true, true],
        [true, true, true, true, true],
        [true, true, true, true, true],
        [true, true, true, true, true],
        [true, true, true, true, true],
        [true, true, true, true, true],
        [true, true, true, true, true],
        [true, true, true, true, true],
        [true, true, true, true, true],
        [true, true, true, true, true],
        [true, true, true, true, true],
      ],
      showPopupWindow: false,
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
    // todo: get courses should be changed
    updateCourseList() {
      getCourses(this.selectedSemester, this.textSearch, false).then(
        (course_list) => {
          this.courseList = course_list;
        }
      );
    },
    updateButtons() {
      const buttons = document.getElementsByClassName('color-button');
      for (let i = 0; i < buttons.length; i++) {
        const row = Math.floor(i / 5);
        const col = i % 5;
        buttons[i].style.backgroundColor = this.colors[row][col] ? 'white' : 'grey';
      }
    },
    togglePopupWindow() {
      this.showPopupWindow = !this.showPopupWindow;
      if (this.showPopupWindow) {
        this.updateButtons();
      }
    },
    switchColor(row, col) {
      this.colors[row][col] = !this.colors[row][col];
      this.updateButtons();
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
    times() {
      const startHour = 8;
      const times = [];
      for (let i = 0; i < 12; i++) {
        const hour = startHour + i;
        const ampm = hour >= 12 ? "PM" : "AM";
        const displayHour = hour > 12 ? hour - 12 : hour;
        const row = Array(5).fill(`${displayHour}:00 ${ampm}`);
        times.push(row);
      }
      return times;
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

.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.button-grid {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.button-row {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
}

button {
  width: 50px;
  height: 50px;
  align-items: center;
  border: 1px solid #ccc;
  background-color: #fff;
}

button.active {
  background-color: #007aff;
  color: #fff;
}