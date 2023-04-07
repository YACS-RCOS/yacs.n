<!--
  look at newCourse Scheduler
-->
<template>
  <b-container fluid class="py-3 h-100 main-body">
    <b-row class="h-100">
      <b-col md="4" class="d-flex flex-column">
        <b-tabs card class="h-100 d-flex flex-column flex-grow-1">
          <b-tab
            title = Prerequisites
            active
            class="flex-grow-1 w-100"
            data-cy="course-search-tab"
          >

            <b-card-text class="d-flex flex-grow-1 w-100">
              <CenterSpinner
                v-if="loading"
                class="d-flex flex-grow-1 flex-column w-100 justify-content-center align-items-center"
                :height="60"
                :fontSize="1"
                loadingMessage="Prerequisites"
                :topSpacing="0"
              />

                <CourseList
                  v-if="!loading"
                  @addCourse="addCourse"
                  @removeCourse="removeCourse"
                  @showCourseInfo="showCourseInfo"
                  class="w-100"
                />
            </b-card-text>
        </b-tab>
        </b-tabs>
      </b-col>
    </b-row>
  </b-container>
</template>


<script>

</script>






<!-- 
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

 -->
