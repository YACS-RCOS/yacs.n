<template>
  <div v-if="ready" class="gridContainer w-100 mb-4">
    <b-row>
      <!-- The subject title should be depending on the input parameter from subjectList.vue -->
      <h3 class="subjectBox">{{ subject }}</h3>
      <b-col>
        <b-button class="k-primary" to="/explore">Back</b-button>
      </b-col>
      <h2 class="headerLine"></h2>
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

  <div v-else>
    <b-spinner></b-spinner>
    <strong class="m-2">Loading courses...</strong>
  </div>
</template>

<script>
import { getCourses } from "../services/YacsService";

export default {
  name: "SubjectExplorer",
  components: {},
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
    getCourses(this.selectedSemester).then((courses) => {
      this.rightColumnCourses = courses.filter(
        (c) => c.department === this.subject
      );
      this.leftColumnCourses = this.rightColumnCourses.splice(
        0,
        Math.ceil(this.rightColumnCourses.length / 2)
      );
      this.rightColumnCourses.splice(0, 0);

<<<<<<< Updated upstream
      this.ready = true;
    });
=======
    for (let k = 0; k < allTempData.length - 1; k += 2) {
      this.leftColumnCourses.push(allTempData[k]);
      this.rightColumnCourses.push(allTempData[k + 1]);
    }
    console.log(
      "Total course number of " + this.subject + ": " + allTempData.length
    );
    this.ready = true;
>>>>>>> Stashed changes
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

.headerLine {
  width: 100%;
  margin: 0 auto;
  border: 0;
  height: 8px;
  background: #333;
  background-image: linear-gradient(to right, red, #333, rgb(9, 206, 91));
}

.subjectBox {
  border: 3px solid black;
  height: 3rem;
  width: 15rem;

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
