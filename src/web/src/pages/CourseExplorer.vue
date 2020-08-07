<template>
  <div v-if="ready" class="gridContainer w-100 mb-4">
    <b-row>
      <b-col>
        <b-row v-for="n in 2" :key="n" class="departmentBox border m-2 mb-4">
          <b-col>
            <b-row class="school-name">
              <h2 class="m-2 ml-3">{{ schoolOrder[n - 1] }}</h2>
            </b-row>
            <b-row>
              <DepartmentList
                :majors="coursesChunked[n - 1]"
                :deptClassDict="deptClassDict"
                :selectedSemester="selectedSemester"
                :id="n"
                v-on:showCourseInfo="showCourseInfo($event)"
              ></DepartmentList>
            </b-row>
          </b-col>
        </b-row>
      </b-col>
      <b-col>
        <b-row v-for="n in 4" :key="n" class="departmentBox border m-2 mb-4">
          <b-col>
            <b-row class="school-name">
              <h2 class="m-2 ml-3">{{ schoolOrder[n + 1] }}</h2>
            </b-row>
            <b-row>
              <DepartmentList
                :majors="coursesChunked[n + 1]"
                :deptClassDict="deptClassDict"
                :selectedSemester="selectedSemester"
                :id="n + 3"
                v-on:showCourseInfo="showCourseInfo($event)"
              ></DepartmentList>
            </b-row>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
    <b-modal
      id="courseInfoModal"
      v-if="courseInfoModalCourse"
      v-model="showCourseInfoModal"
      :title="courseInfoModalCourse.name + ' ' + courseInfoModalCourse.title"
      hide-footer
    >
      <span v-if="courseInfoModalCourse.frequency">
        Offered: {{ courseInfoModalCourse.frequency }}
        <br />
        <br />
      </span>
      <span>
        {{
          generateRequirementsText(
            courseInfoModalCourse.prerequisites,
            courseInfoModalCourse.corequisites,
            courseInfoModalCourse.raw_precoreqs
          )
        }}
      </span>
      <span v-if="courseInfoModalCourse.description">
        <br />
        <br />
        {{ courseInfoModalCourse.description }}
      </span>
      <span v-else>
        <br />
        <br />
        {{ "No course description found" }}
      </span>
      <br />
      <br />
      <b-button
        class="ml-2"
        variant="danger"
        @click="showCourseInfoModal = !showCourseInfoModal"
      >
        Close
      </b-button>
    </b-modal>
  </div>
  <div v-else>
    <b-spinner></b-spinner>
    <strong class="m-2">Loading courses...</strong>
  </div>
</template>

<script>
import { getCourses } from "../services/YacsService";
import DepartmentListComponenet from "@/components/DepartmentList";
import { generateRequirementsText } from "@/utils";

export default {
  name: "CourseExplorer",
  components: {
    DepartmentList: DepartmentListComponenet,
  },
  props: {
    selectedSemester: String,
  },
  data() {
    return {
      //an object with keys being the dept, and values a list of courses
      deptClassDict: {},
      schoolsMajorDict: {},
      ready: false,

      /*
       *Used to define the order that the schools are placed into the two main
       *columns. This could be implemented generically, but making the columns
       *more or less "even" is NP-Hard so its more convenient to just define
       *manually
       */
      schoolOrder: [
        "Engineering",
        "Science",
        "Humanities, Arts and Social Sciences",
        "Architecture",
        "Business Management",
        "Other",
      ],
      courseInfoModalCourse: null,
      showCourseInfoModal: false,
    };
  },
  async created() {
    getCourses(this.selectedSemester).then((courses) => {
      for (const c of courses) {
        if (!this.schoolsMajorDict[c.school]) {
          this.schoolsMajorDict[c.school] = [c.department];
        } else {
          if (!this.schoolsMajorDict[c.school].includes(c.department)) {
            this.schoolsMajorDict[c.school].push(c.department);
          }
        }
        if (this.deptClassDict[c.department]) {
          this.deptClassDict[c.department].push(c);
        } else {
          this.deptClassDict[c.department] = [c];
        }
      }
      this.ready = true;
    });
  },
  methods: {
    generateRequirementsText,
    showCourseInfo(course) {
      this.courseInfoModalCourse = course;
      this.showCourseInfoModal = true;
    },
  },
  computed: {
    //Used to define the placement of each department into the two main columns
    coursesChunked() {
      const chunkedArr = [];
      for (var i = 0; i < 6; i++) {
        chunkedArr.push(this.schoolsMajorDict[this.schoolOrder[i]]);
      }
      return chunkedArr;
    },
  },
};
</script>

<style>
.gridContainer {
  display: inline-grid;
  grid-template-columns: auto auto;
  justify-content: center;
  align-content: center;
}

.departmentBox {
  width: 30rem;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: center;
}

.school-name {
  background: rgba(108, 90, 90, 0.15);
  border-bottom: rgba(108, 90, 90, 0.1), solid, 1px;
}
</style>
