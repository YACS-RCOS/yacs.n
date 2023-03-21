<template>
<div>
  <b-tabs
    active-nav-item-class="font-weight-bold text-uppercase text-danger"  
    content-class="mt-3"
    fill
  >
    <b-tab title="Syllabus"><p align="center">Please contact the YACS team if you have the syllabus associated with this class</p></b-tab>
    <b-tab title="Course FAQ"><p align="center">Coming Soon</p></b-tab>
    <b-tab title="Sections">
      <p><CourseListing :course="course" :showAddButton = "false"/></p>
    </b-tab>
  </b-tabs>
</div>
</template>

<script>
import CourseListingComponent from "@/components/CourseListing";

export default {
  name: "CourseInfo",
  components: {
    CourseListing: CourseListingComponent,
  },
  props: {
    course: Object,
  },
};
</script>