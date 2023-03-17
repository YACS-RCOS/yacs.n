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
      <button>Open modal</button>
      <div class="modal" id="modal">
        <div class="modal-header">
          <div class="title">Select the day of the week you would like your class to be</div>
          <button class="close-button">&times;</button>
        </div>
        <div class="modal-body">
          <b-row>
            <b-col>
              <b-form-group label="M">
              <b-form-checkbox v-model="isChecked" 
                name="Monday" 
                value="Monday" 
                id="Monday">
              </b-form-checkbox>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group label="T">
              <b-form-checkbox v-model="isChecked" 
                name="Tuesday" 
                value="Tuesday" 
                id="Tuesday">
              </b-form-checkbox>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group label="M">
              <b-form-checkbox v-model="isChecked" 
                name="Wednesday" 
                value="Wednesday" 
                id="Wednesday">
              </b-form-checkbox>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group label="R">
              <b-form-checkbox v-model="isChecked" 
                name="Thursday" 
                value="Thursday" 
                id="Thursday">
              </b-form-checkbox>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group label="F">
              <b-form-checkbox v-model="isChecked" 
                name="Friday" 
                value="Friday" 
                id="Friday">
              </b-form-checkbox>
              </b-form-group>
            </b-col>
          </b-row>
        </div>
      </div>
      <div class="active" id="overlay"></div>
      <b-row>
        <b-col>
          <b-form-group label="Begin Time" label-for="btime">
            <b-form-input
            id="btime"
            v-model="begintime"
            :debounce="debounceTime"
            trim
            placeholder="00:00"
            ></b-form-input>
            <input type="text" pattern="^([01]\d|2[0-3]):([0-5]\d)$" title="Please enter a valid 24-hour time in the format HH:mm">  
          </b-form-group>
        </b-col>>
        <b-col>
          <b-form-group label="End Time" label-for="etime">
            <b-form-input
            id="etime"
            v-model="begintime"
            :debounce="debounceTime"
            trim
            placeholder="24:00"
            ></b-form-input>
            <input type="text" pattern="^([01]\d|2[0-3]):([0-5]\d)$" title="Please enter a valid 24-hour time in the format HH:mm"> 
          </b-form-group>
        </b-col>>
      </b-row>
      <!-- <b-row>
        <button type="button" class="open-button" onclick="openPop()">Open Pop</button>
        <div class="form-modal" id="myPop">
        <form action="/action_page.php" class="pop-container"> 
            
        <button type="button" class="btn cancel" onclick="closePop()">Close</button>
        </form>
        </div>  
      </b-row> -->
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
    getTimes().then(() => {
      this.TimeOptions.push(...times.map((t) => t.times));
    })
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
//       /filterSession(courseList)
          // for(loop through courseList){
          //   if (courseList[i].session[i] collide condition){
          //     return false
          //   }
          // }
          // return true
          // }
          // const find2 = filtered.find(
          //   (course) =>

          // );
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
    // function openPop() {
    //   document.getElementById("myPop").style.display = "block";
    // };

    // function closePop() {
    //   document.getElementById("myPop").style.display = "none";
    // };
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

/* .open-button {
  background-color: #555;
  color: white;
  padding: 16px 20px;
  border: none;
  cursor: pointer;
  opacity: 0.8;
  position: fixed;
  bottom: 23px;
  right: 28px;
  width: 280px;
} */

/*.form-modal {
  display: none;
  position: fixed;
  bottom: 0;
  border: 3px solid #f1f1f1;
}

.form-container {
  max-width: 50px;
  padding: 5px;
  background-color: white;
}*/
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translated(-50%, -50%) scale(0);
  transition: 200ms ease-in-out;
  border: 1px solid black;
  border-radius: 10px;
  background-color: white;
  width: 500px;
  max-width: 80%;
}

.modal{
  transform: translate(-50%, -50%) scale(0);
}
.modal-header{
  padding: 10px 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid black;
}

.modal-header .title{
  font-size: 1.25rem;
  font-weight: bold;
}

.modal-header .close{
  cursor: pointer;
  border: none;
  outline: none;
  font-size: 1.25rem;
  font-weight: bold;
}

.modal-body{
  padding: 10px 15px;
  
}

#overlay{
  position: fixed;
  opacity: 0;
  transition: 200ms ease-in-out;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0,0,0,0.5);
  pointer-events: none;
}

#overlay.active {
  pointer-events: none;
  opacity: 1;
}
 
</style>
