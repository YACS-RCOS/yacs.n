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
  </div>
  <div v-else>
    <b-spinner></b-spinner>
    <strong class="m-2">Loading courses...</strong>
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
        if (c.name === this.courseName) {
          this.courseObj = c;
          console.log(this.courseObj);
        }
      }
      this.ready = true;
    });
  },
};
</script>

<style>
.container {
  text-align: center;
  margin: ;
}
</style>
