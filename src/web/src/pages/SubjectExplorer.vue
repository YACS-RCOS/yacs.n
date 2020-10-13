<template>
  <div v-if="ready" class="gridContainer w-100 mb-4">
    <!-- Subject Title -->
    <b-row>
      <b-col class="school-name">
        <!-- The subject title should be depending on the input parameter from subjectList.vue -->
        <h3 class="m-3">{{ subject }}</h3>
      </b-col>
      <b-col>
        <!-- Subject slide bar section -->
        <b-button v-b-toggle.courseSidebar-1>Subject Sidebar</b-button>
        <b-button to="/explore">Back</b-button>

        <b-sidebar id="courseSidebar-1" title="subject name" shadow>
          <div class="px-3 py-2">
            <p>subject description</p>
            <b-img
              src="https://science.rpi.edu/sites/default/files/cs_spotlight_v1.jpg"
              fluid
              thumbnail
            ></b-img>
          </div>
        </b-sidebar>
      </b-col>
    </b-row>
    <br />

    <!-- left column of courses -->
    <b-col>
      <b-row
        v-for="n in this.leftColumnCourseNum"
        :key="n"
        class="courseBox border m-2 mb-4"
      >
        <!-- Navigates to course page by click on the course button  -->
        <b-col class="m-1 ml-0">
          <b-button
            squared
            variant="light"
            class="course-button m-0 ml-0"
            :to="{
              name: 'CoursePage',

              params: {
                course: subjectCourseArr[n - 1].name,
                subject: subjectCourseArr[n - 1].department,
              },
            }"
          >
            {{ subjectCourseArr[n - 1].title }}
            <br />
            {{ subjectCourseArr[n - 1].department }}
            {{ subjectCourseArr[n - 1].level }}
            <br />
          </b-button>
        </b-col>
      </b-row>
    </b-col>

    <!-- right column of courses -->
    <b-col>
      <b-row
        v-for="n in this.rightColumnCourseNum"
        :key="n"
        class="courseBox border m-2 mb-4"
      >
        <!-- Navigates to course page by click on the course button  -->
        <b-col class="m-1 ml-2">
          <b-button
            squared
            variant="light"
            :to="{
              name: 'CoursePage',
              params: {
                course: subjectCourseArr[n - 1].name,
                subject: subjectCourseArr[n - 1].department,
              },
            }"
          >
            {{ subjectCourseArr[n - 1].title }}
            <br />
            {{ subjectCourseArr[n - 1].department }}
            {{ subjectCourseArr[n - 1].level }}
            <br />
          </b-button>
        </b-col>
      </b-row>
    </b-col>
  </div>

  <!-- Loading course display -->
  <div v-else>
    <b-spinner></b-spinner>
    <strong class="m-2">Loading courses...</strong>
  </div>
</template>

<script>
import { getCourses } from "../services/YacsService";
import { generateRequirementsText } from "@/utils";

export default {
  name: "SubjectExplorer",
  components: {},
  props: {
    selectedSemester: String,
  },
  data() {
    return {
      // subject
      subjectCourseArr: [],
      subject: this.$route.params.subject,
      leftColumnCourseNum: Number,
      rightColumnCourseNum: Number,
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

  /**
   * created function calls automatically once the page is access/ object is created
   * Loop through all courses in data base
   * Only store the courses within the same subject/major into an array
   * subjectCourseArr is an array of course objects
   */
  async created() {
    getCourses(this.selectedSemester).then((courses) => {
      console.log("\nThe page object is created, subject-> " + this.subject);
      for (const c of courses) {
        if (c.department === this.subject) {
          this.subjectCourseArr.push(c);
        }
      }
      this.leftColumnCourseNum = Math.ceil(this.subjectCourseArr.length / 2);
      this.rightColumnCourseNum =
        this.subjectCourseArr.length - this.leftColumnCourseNum;

      console.log("subjectCourseArr is " + this.subjectCourseArr[0].name);
      console.log("subjectCourseArr is " + this.subjectCourseArr[0].title);

      console.log("course size is " + courses.length);
      console.log("subjectCourseArr size is " + this.subjectCourseArr.length);
      console.log("leftColumnCourseNum size is " + this.leftColumnCourseNum);
      console.log("rightColumnCourseNum size is " + this.rightColumnCourseNum);

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
    //Used to define the placement of each subject into the two main columns
    coursesChunked() {
      const chunkedArr = [];
      for (var i = 0; i < 6; i++) {
        chunkedArr.push(this.schoolssubjectDict[this.schoolOrder[i]]);
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

.subjectBox {
  width: 10rem;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: left;
}

#scroll-box {
  flex-grow: 1;
  flex-basis: 0px;
  min-height: 200px;
  border: 1px rgba(108, 90, 90, 0.15) solid;
  padding: 0 1em 0 1em;
}

.scroller {
  max-height: 20em;
  overflow-x: hidden;
  text-align: left;
  list-style: none;
  padding-left: 0;
}

.course-listing {
  height: 100px;
  padding-top: 10px;
  border-top: 1px solid #e9ecef;
  border-bottom: 1px solid #e9ecef;
}
</style>
