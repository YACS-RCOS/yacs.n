<template>
  <div v-if="ready" class="container w-100 mb-4">
    <b-row>
      <b-col>
        <h1>{{ courseName }}</h1>
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
      <b-col>
        <br />
        {{ courseObj.description }}
      </b-col>
    </b-row>
    <b-button to="/explore">Back</b-button>
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
      courseObj: {},
      allCoursePreReqs: {},
      treeData: {},
      selectedSemester: String,
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
    getCourses(this.selectedSemester).then((courses) => {
      for (const c of courses) {
        this.allCoursePreReqs[c.name] = c.prerequisites;
        if (c.name === this.courseName) {
          this.courseObj = c;
        }
      }
      this.treeData = this.prereqTree;
      console.log("logging:");
      console.log(this.treeData);
      this.ready = true;
    });
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

<style>
.container {
  text-align: center;
  /* margin: ; */
}
</style>
