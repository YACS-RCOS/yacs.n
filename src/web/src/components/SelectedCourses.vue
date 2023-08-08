<template>
  <b-list-group id="selected-course-list" flush>
    <div v-if="Object.keys(courses).length == 0" class="no-courses">
      Oops! It looks like you haven't selected anything!
      <br/>
      Please select some courses from the "Course Search" tab!
    </div>
    <b-list-group-item
        class="selected"
        v-for="course of courses"
        :key="course.id"
    >
      <CourseListing :course="course" v-on="$listeners"/>
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
  // data() {
  //   return {
  //     isSticky: false,
  //   };
  // },
  // mounted() {
  //   window.addEventListener('scroll', this.handleScroll);
  // },
  // beforeDestroy() {
  //   window.removeEventListener('scroll', this.handleScroll);
  // },
  //
  // methods: {
  //   handleScroll() {
  //     console.log("handScroll");
  //     const navbarHeight = 55.5;
  //     const scrollY = window.scrollY;
  //     console.log(navbarHeight + " " + scrollY);
  //     if (scrollY > navbarHeight) {
  //       this.isSticky = true;
  //     } else {
  //       this.isSticky = false;
  //     }
  //   },
  // }
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
//.course-list-sticky {
//  position: sticky;
//  //top: 55.5px;
//  z-index: 1; /* Adjust the z-index as needed */
//  margin-top: 55.5px;
//}

</style>
