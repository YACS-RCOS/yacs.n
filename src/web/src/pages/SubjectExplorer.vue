<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <div v-if="ready" class="gridContainer w-100 mb-4">
      <b-row>
        <!-- The subject title should be depending on the input parameter from subjectList.vue -->
        <h3 class="subjectBox">{{ subject }}</h3>
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
              <span class="d-inline">
                {{ course.department }}
                {{ course.level }}
              </span>
              <course-sections-open-badge :course="course" />
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
              <span class="d-inline">
                {{ course.department }}
                {{ course.level }}
              </span>
              <course-sections-open-badge :course="course" />
            </b-button>
          </b-col>
        </b-row>
      </b-col>
    </div>
    <CenterSpinner
      v-else
      :height="80"
      :fontSize="1.4"
      loadingMessage="Courses"
      :topSpacing="30"
    />
  </b-container>
</template>

<script>
import { getCourses } from "../services/YacsService";
import { getDefaultSemester } from "@/services/AdminService";
import CenterSpinnerComponent from "../components/CenterSpinner";
import CourseSectionsOpenBadge from "../components/CourseSectionsOpenBadge.vue";

export default {
  name: "SubjectExplorer",
  components: {
    CenterSpinner: CenterSpinnerComponent,
    CourseSectionsOpenBadge,
  },
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
      breadcrumbNav: [
        {
          text: "YACS",
          to: "/",
        },
        {
          text: "Explore",
          to: "/explore",
        },
        {
          text: this.$route.params.subject,
          to: "/explore/" + this.$route.params.subject,
        },
      ],
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
  metaInfo() {
    return {
      title: this.subject,
      titleTemplate: "%s | YACS",
      meta: [
        { charset: 'utf-8' },
        { name: 'description', content: "RPI " + this.subject},
        { name: 'keywords', content: "RPI, YACS, Rensselaer Polytechnic Institute, " + this.subject},
        { property: 'og:title', content: "RPI - YACS Course Scheduler"},
        { property: 'og:site_name', content: 'YACS'},
        { property: 'og:type', content: 'website'}
      ]
    }
  },
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
