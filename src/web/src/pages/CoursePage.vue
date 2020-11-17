<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <div v-if="ready" class="w-90 ml-4 mb-4">
      <b-row>
        <b-col>
          <h1 class="mt-4">{{ courseTitle }}</h1>
          <h4 class="mb-1">{{ courseName }}</h4>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          {{
            generateRequirementsText(
              courseObj.prerequisites,
              courseObj.corequisites,
              courseObj.raw_precoreqs
            )
          }}
        </b-col>
      </b-row>
      <b-row>
        <b-col class="mb-4">
          <br />
          {{ courseObj.description }}
        </b-col>
      </b-row>
      <b-button :to="backRoute">Back</b-button>
    </div>
    <div v-else>
      <b-spinner></b-spinner>
      <strong class="m-2">Loading Course...</strong>
    </div>
  </b-container>
</template>

<script>
import { getCourses } from "../services/YacsService";
import { getDefaultSemester } from "@/services/AdminService";
import { generateRequirementsText } from "@/utils";


export default {
  name: "CoursePage",
  data() {
    return {
      ready: false,
      courseName: this.$route.params.course,
      courseTitle: String,
      courseObj: {},
      allCoursePreReqs: {},
      selectedSemester: String,
      backRoute: String,
      breadcrumbNav: [{
        text: 'YACS',
        to: '/'
      },
      {
        text: 'Explore',
        to: '/explore'
      },
      {
        text: this.$route.params.subject,
        to: '/explore/' + this.$route.params.subject
      },
      {
        text: this.$route.params.course,
      }]
    };
  },
  methods: {
    generateRequirementsText,
  },
  async created() {
    const querySemester = this.$route.query.semester;
    console.log(this.$route)
    this.selectedSemester =
      querySemester && querySemester != "null"
        ? querySemester
        : await getDefaultSemester();
    const courses = await getCourses(this.selectedSemester);
    for (const c of courses) {
      this.allCoursePreReqs[c.name] = c.prerequisites;
      if (c.name === this.courseName) {
        this.courseTitle = c.title;
        this.courseObj = c;
      }
    }
    this.backRoute = "/explore/" + this.courseObj.department;
    this.ready = true;
  },
  computed: {
    prereqTree() {
      let treeData = {};
      treeData.name = this.courseName;
      return treeData;
    },
  },
};
</script>
