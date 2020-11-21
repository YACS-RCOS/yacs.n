<template>
  <div v-if="ready" class="w-90 ml-4 mb-4">
    <b-row>
      <b-col>
        <h1 class="mt-4">{{ courseTitle }}</h1>
        <h4 class="mb-1">{{ courseName }}</h4>
        <h6 class="mb-1">{{getCredits}} Credits</h6>
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
    };
  },
  methods: {
    generateRequirementsText,
  },
  async created() {
    const querySemester = this.$route.query.semester;
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
    getCredits() {
      var credits;
      if (this.courseObj.min_credits != this.courseObj.max_credits){
        credits = [this.courseObj.min_credits,this.courseObj.max_credits].join("-");
      } else{
        credits = this.courseObj.min_credits;
      }
      return credits;
    },
  },
};
</script>
