<template>
  <b-list-group id="selected-course-list" flush data-cy="selected-courses">
    <div v-if="Object.keys(courses).length == 0" class="no-courses">
      Oops! It looks like you haven't selected anything!
      <br />
      Please select some courses from the "Course Search" tab!
    </div>
    <b-list-group-item
      class="selected"
      v-for="course of courses"
      :key="course.id"
    >
      <CourseListing :course="course" v-on="$listeners" />
    </b-list-group-item>
  </b-list-group>
</template>

<script>
import "@/typedef";

import CourseListingComponent from "@/components/CourseListing";

export default {
  name: "SelectedCourses",
  components: {
    CourseListing: CourseListingComponent,
  },
  props: {
    courses: Object,
  },
};
</script>

<style scoped lang="scss">
#selected-course-list {
  overflow-y: scroll !important;
  overflow-x: auto;
  min-height: 200px;
  flex-grow: 1;
  flex-basis: 0px; // allows flex and scroll combo
  border-bottom: 1px solid #dbdbdc;
}
.no-courses {
  margin-right: 20px;
  border-style: solid;
  border-width: 2px;
  border-color: rgb(0, 0, 0, 0.05);
  font-size: 16px;
  padding: 20px;
}
</style>
