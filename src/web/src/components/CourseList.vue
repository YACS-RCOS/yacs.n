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
      <b-row>
        <!-- > time filter -->
        <!-- <div class="course-filter"
        :class="{ 'time-filter' : course.selected}"> -->
        <div>
          <button class="show-grid-button" @click="showGrid = true">Open Time Filter</button>
          <div v-if="showGrid">
            <button class="close-grid-button" @click="showGrid = false">Collapse</button>
            <p></p>
            <div v-for="(row, rowIndex) in grid" :key="rowIndex" class="grid-row">
              <div v-for="(box, boxIndex) in row" :key="boxIndex"
                  class="grid-box badge-light"
                  :style="{ backgroundColor: box.color }"
                  @click="handleBoxClick(rowIndex, boxIndex)">
                {{ box.label }}
              </div>
            </div>
          </div>
        </div>
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
      showGrid: false,
      //grid is the time filter box check which box is clicked
      grid: [
      [
        { label: ' 7:00-7:59', value: true, color: 'white'},
        { label: ' 7:00-7:59', value: true, color: 'white'},
        { label: ' 7:00-7:59', value: true, color: 'white'},
        { label: ' 7:00-7:59', value: true, color: 'white'},
        { label: ' 7:00-7:59', value: true, color: 'white'},
      ],
      [
        { label: ' 8:00-8:59', value: true, color: 'white'},
        { label: ' 8:00-8:59', value: true, color: 'white'},
        { label: ' 8:00-8:59', value: true, color: 'white'},
        { label: ' 8:00-8:59', value: true, color: 'white'},
        { label: ' 8:00-8:59', value: true, color: 'white'},
      ],
      [
        { label: ' 9:00-9:59', value: true, color: 'white'},
        { label: ' 9:00-9:59', value: true, color: 'white'},
        { label: ' 9:00-9:59', value: true, color: 'white'},
        { label: ' 9:00-9:59', value: true, color: 'white'},
        { label: ' 9:00-9:59', value: true, color: 'white'},
      ],
      [
        { label: '10:00-10:59', value: true, color: 'white'},          
        { label: '10:00-10:59', value: true, color: 'white'},
        { label: '10:00-10:59', value: true, color: 'white'},
        { label: '10:00-10:59', value: true, color: 'white'},
        { label: '10:00-10:59', value: true, color: 'white'},
      ],
      [
        { label: '11:00-11:59', value: true, color: 'white'},
        { label: '11:00-11:59', value: true, color: 'white'},
        { label: '11:00-11:59', value: true, color: 'white'},
        { label: '11:00-11:59', value: true, color: 'white'},
        { label: '11:00-11:59', value: true, color: 'white'},
      ],
      [
        { label: '12:00-12:59', value: true, color: 'white'},
        { label: '12:00-12:59', value: true, color: 'white'},
        { label: '12:00-12:59', value: true, color: 'white'},
        { label: '12:00-12:59', value: true, color: 'white'},
        { label: '12:00-12:59', value: true, color: 'white'},
      ],
      [
        { label: '13:00-13:59', value: true, color: 'white'},
        { label: '13:00-13:59', value: true, color: 'white'},
        { label: '13:00-13:59', value: true, color: 'white'},
        { label: '13:00-13:59', value: true, color: 'white'},
        { label: '13:00-13:59', value: true, color: 'white'},
      ],
      [
        { label: '14:00-14:59', value: true, color: 'white'},
        { label: '14:00-14:59', value: true, color: 'white'},
        { label: '14:00-14:59', value: true, color: 'white'},
        { label: '14:00-14:59', value: true, color: 'white'},
        { label: '14:00-14:59', value: true, color: 'white'},
      ],
      [
        { label: '15:00-15:59', value: true, color: 'white'},
        { label: '15:00-15:59', value: true, color: 'white'},
        { label: '15:00-15:59', value: true, color: 'white'},
        { label: '15:00-15:59', value: true, color: 'white'},
        { label: '15:00-15:59', value: true, color: 'white'},
      ],
      [
        { label: '16:00-16:59', value: true, color: 'white'},
        { label: '16:00-16:59', value: true, color: 'white'},
        { label: '16:00-16:59', value: true, color: 'white'},
        { label: '16:00-16:59', value: true, color: 'white'},
        { label: '16:00-16:59', value: true, color: 'white'},
      ],
      [
        { label: '17:00-17:59', value: true, color: 'white'},
        { label: '17:00-17:59', value: true, color: 'white'},
        { label: '17:00-17:59', value: true, color: 'white'},
        { label: '17:00-17:59', value: true, color: 'white'},
        { label: '17:00-17:59', value: true, color: 'white'},
      ],
      [
        { label: '18:00-18:59', value: true, color: 'white'},
        { label: '18:00-18:59', value: true, color: 'white'},
        { label: '18:00-18:59', value: true, color: 'white'},
        { label: '18:00-18:59', value: true, color: 'white'},
        { label: '18:00-18:59', value: true, color: 'white'},
      ],
      [
        { label: '19:00-19:59', value: true, color: 'white'},
        { label: '19:00-19:59', value: true, color: 'white'},
        { label: '19:00-19:59', value: true, color: 'white'},
        { label: '19:00-19:59', value: true, color: 'white'},
        { label: '19:00-19:59', value: true, color: 'white'},
      ],
      [
        { label: '20:00-20:59', value: true, color: 'white'},
        { label: '20:00-20:59', value: true, color: 'white'},
        { label: '20:00-20:59', value: true, color: 'white'},
        { label: '20:00-20:59', value: true, color: 'white'},
        { label: '20:00-20:59', value: true, color: 'white'},
      ],
      [
        { label: '21:00-21:59', value: true, color: 'white'},
        { label: '21:00-21:59', value: true, color: 'white'},
        { label: '21:00-21:59', value: true, color: 'white'},
        { label: '21:00-21:59', value: true, color: 'white'},
        { label: '21:00-21:59', value: true, color: 'white'},
      ],
      [
        { label: '22:00-22:59', value: true, color: 'white'},
        { label: '22:00-22:59', value: true, color: 'white'},
        { label: '22:00-22:59', value: true, color: 'white'},
        { label: '22:00-22:59', value: true, color: 'white'},
        { label: '22:00-22:59', value: true, color: 'white'},
      ],
      ],
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
    //time filter
    handleBoxClick(row, col) {
      this.grid[row][col].value = !this.grid[row][col].value
      if(this.grid[row][col].color == "lightgreen"){
        this.grid[row][col].color = 'white';
      }else{
        this.grid[row][col].color = 'lightgreen';
      }
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

      let time_filter = find ? find : filtered;
      let sample = find ? find : filtered;
      for (let course_index=sample.length-1; course_index >=0 ; course_index--){
        let course_section = sample[course_index]["sections"];
        for(let section_index = course_section.length-1; section_index >= 0; section_index--){
          let section_session = course_section[section_index]["sessions"];
          let Avaliable = true;//boolean that check if this section course can fit all time selected on the schedule_arr
          for(let session_index=section_session.length-1; session_index >= 0; session_index--){
            let day = parseInt(section_session[session_index]["day_of_week"]);
            let st = section_session[session_index]["time_start"];
            let en = section_session[session_index]["time_end"];
            if(st==null || en==null){break;}
            let start = parseInt(st.substring(0, 2));
            let end = parseInt(en.substring(0, 2));
            start -= 7;
            end -=7;
            for( let i=start; i<=end; i++){
              if(this.grid[i][day].value == false){
                Avaliable = false;
                break;
              }
            }
          }
          if(!Avaliable){
            time_filter[course_index]["sections"].splice(section_index,1);
            if(time_filter[course_index]["sections"].length==0){
              time_filter.splice(course_index,1);
            }
          }
        }
      }
      return time_filter;
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

.grid-row {
  display: flex;
  flex-direction: row;
  padding:0px;
}

.grid-box {
  width: 6vw;
  height: 4vh;
  margin-right: 0px;
  border: 1px solid black;
  text-align: center;
  text-size-adjust: 8px;
  margin: 0px;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  display: block;
  font-size: 1vw;
  font-weight: 400;
  line-height: 1.5;
  color: #495057;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
}

.show-grid-button{
  text-align: center;
  display: block;
  height: 4vh;
  font-size: 1vw;
  font-weight: 400;
  line-height: 1.5;
  color: #495057;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  width: 10vw;
}

.show-grid-button:active{
  background-color: lightgreen;
}

.close-grid-button{
  text-align: center;
  display: block;
  height: 4vh;
  font-size: 1vw;
  font-weight: 400;
  line-height: 1.5;
  color: #495057;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  width: 10vw;
}

.close-grid-button:active{
  background-color: lightgreen;
}
</style>
