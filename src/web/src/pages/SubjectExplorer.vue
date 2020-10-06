<template>
  <div v-if="ready" class="gridContainer w-100 mb-4">
    <!-- 
      - Department Title
      - mb: margin button  
    -->
    <b-row>
      <b-col class="school-name">
        <h3 class="m-5">{{ schoolOrder[0] }}</h3>
      </b-col>
      <b-col>
        <!-- Course slide bar section -->
        <b-button v-b-toggle.courseSidebar-1>Course Sidebar</b-button>
        <b-button to="/explore">Back</b-button>

        <b-sidebar id="courseSidebar-1" title="Department/Subject name" shadow>
          <div class="px-3 py-2">
            <p>Department description</p>
            <b-img
              src="https://science.rpi.edu/sites/default/files/cs_spotlight_v1.jpg"
              fluid
              thumbnail
            ></b-img>
          </div>
        </b-sidebar>
      </b-col>
    </b-row>
  </div>

  <!-- Loading course display -->
  <div v-else>
    <b-spinner></b-spinner>
    <strong class="m-2">Loading courses...</strong>
  </div>
</template>

<script>
import { getCourses } from "../services/YacsService";
// import DepartmentListComponenet from "@/components/DepartmentList";
import { generateRequirementsText } from "@/utils";

export default {
  name: "SubjectExplorer",
  components: {
    // DepartmentList: DepartmentListComponenet,
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
          this.schoolsMajorDict[c.school] = new Set();
        }
        this.schoolsMajorDict[c.school].add(c.department);
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
