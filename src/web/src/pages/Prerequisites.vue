<!--
  look at newCourse Scheduler
-->











<template>
  <p class = "Prerequisites"> Prerequisites {{ Prerequisites }}</p>
  <b-tab
    title = "Department"
    active
  >
  <CourseList
                  v-if="!loading"
                  @addCourse="addCourse"
                  @removeCourse="removeCourse"
                  @showCourseInfo="showCourseInfo"
                  class="w-100"
                />
</template>

<script>
import CourseListComponent from "@/components/CourseList";
export default {
    name:"Prerequisites",
    components : {
      CourseList: CourseListComponent,
    },
    data() {
    return {
      Prerequisites: 'Select your classes from the menu below'
    }
  }
};
</script>

<style>
.Prerequisites{
    color: blue;
  
}

</style> 


