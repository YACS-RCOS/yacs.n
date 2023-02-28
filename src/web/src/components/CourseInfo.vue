<template>
<div>
  <b-tabs
    active-nav-item-class="font-weight-bold text-uppercase text-danger"
    active-tab-class="font-weight-bold text-success"
    content-class="mt-3"
    fill
  >
    <b-tab title="Example Coursework" active><p>Hello</p></b-tab>
    <b-tab title="Syllabus"><p>I'm</p></b-tab>
    <b-tab title="Custom Fields"><p>the</p></b-tab>
    <b-tab title="Course FAQ"><p>file</p></b-tab>
    <b-tab title="Sections">
      <p>{{ course.title }}</p>
      <p>hi</p>
    </b-tab>
  </b-tabs>
</div>
</template>

<script>
//import CourseListingComponent from "@/components/CourseListing";

export default {
  name: "CourseInfo",
  //components: {
  //  CourseListing: CourseListingComponent,
  //},
  props: {
    course: Object,
  },
};
</script>