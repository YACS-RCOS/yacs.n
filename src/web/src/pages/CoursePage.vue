<template>
  <h1>{{ courseName }}</h1>
</template>

<script>
import { getCourses } from "../services/YacsService";
import { getDefaultSemester } from "@/services/AdminService";

export default {
  name: "CoursePage",
  data() {
    return {
      courseName: this.$route.params.course,
      courseObj: {},
      selectedSemester: String,
    };
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
