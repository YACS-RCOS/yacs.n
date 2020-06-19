<template>
  <div>Hi im the course explorer with {{ this.courses.length }} courses</div>
</template>

<script>
import { getCourses } from "../services/YacsService";
export default {
  name: "CourseExplorer",
  props: {
    selectedSemester: String,
  },
  data() {
    return {
      courses: [],
    };
  },
  async created() {
    this.courses = await getCourses(this.selectedSemester);
  },
};
</script>

<style></style>
