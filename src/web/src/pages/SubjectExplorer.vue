<template>
  <div v-if="ready" class="gridContainer w-100 mb-4">
    <b-row>
      <!-- The subject title should be depending on the input parameter from subjectList.vue -->
      <h1 class="subjectBox">{{ subject }}</h1>
      <b-col>
        <b-button class="k-primary" to="/explore">Back</b-button>
      </b-col>
    </b-row>

    <br />

    <!-- left column of courses -->
    <b-col>
      <b-row
        v-for="course in this.leftColumnCourses"
        v-bind:key="course.level + course.department"
      >
        <!-- Navigates to course page by click on the course button  -->
        <b-col class="m-1 ml-0">
          <b-button
            variant="light"
            class="courseBox border m-2"
            :to="{
              name: 'CoursePage',
              params: {
                course: course.name,
                subject: course.department,
              },
            }"
          >
            {{ course.title }}
            <br />
            {{ course.department }}
            {{ course.level }}
            <br />
          </b-button>
        </b-col>
      </b-row>
    </b-col>

    <!-- right column of courses -->
    <b-col>
      <b-row
        v-for="course in this.rightColumnCourses"
        :key="course.level + course.department"
      >
        <!-- Navigates to course page by click on the course button  -->
        <b-col class="m-1 ml-2">
          <b-button
            variant="light"
            class="courseBox border m-2"
            :to="{
              name: 'CoursePage',
              params: {
                course: course.name,
                subject: course.department,
              },
            }"
          >
            {{ course.title }}
            <br />
            {{ course.department }}
            {{ course.level }}
            <br />
          </b-button>
        </b-col>
      </b-row>
    </b-col>
  </div>

  <div id="spinnerWrapper" v-else>
    <CenterSpinner/>
  </div>
</template>

<script>
import { getCourses } from "../services/YacsService";
import { getDefaultSemester } from "@/services/AdminService";
import CenterSpinner from "../components/CenterSpinner";

export default {
  name: "SubjectExplorer",
  components: {CenterSpinner},
  props: {
    selectedSemester: String,
  },
  data() {
    return {
      subjectCourseArr: [], // array of courses for the selected subject
      leftColumnCourses: [],
      rightColumnCourses: [],
      subject: this.$route.params.subject, // subject object from CourseExplorer
      // split the total course number to half, left column rounds up
      leftColumnCourseNum: Number,
      rightColumnCourseNum: Number,
      ready: false,
    };
  },

  /**
   * created function calls automatically once the page is access/ object is created
   * Loop through all courses in data base
   * Only store the courses within the same subject/major into an array
   * subjectCourseArr is an array of course objects
   */
  async created() {
    const querySemester = this.$route.query.semester;
    this.selectedSemester =
      querySemester && querySemester != "null"
        ? querySemester
        : await getDefaultSemester();
    const courses = await getCourses(this.selectedSemester);
    //Obtain All Courses Such That Department Matches The Subject Name.
    const allTempData = courses.filter((c) => c.department === this.subject);
    for (let k = 0; k < allTempData.length; k++) {
      if (k % 2 == 0) this.leftColumnCourses.push(allTempData[k]);
      else this.rightColumnCourses.push(allTempData[k]);
    }
    this.ready = true;
  },
  methods: {},
  computed: {},
};
</script>

<style scope>
.gridContainer {
  display: inline-grid;
  grid-template-columns: auto auto;
  justify-content: center;
  align-content: center;
}

.subjectBox {
  /* border: 3px solid black; */
  margin-bottom: 20px;
  height: 2.5rem;
  width: 15rem;
  font-size: xx-large;
  font-weight: 600;
  text-align: center;
}

.courseBox {
  height: 5rem;
  width: 30rem;
  text-align: left;
}

.major-courseBox:hover {
  background: rgba(108, 90, 90, 0.15);
}
</style>
