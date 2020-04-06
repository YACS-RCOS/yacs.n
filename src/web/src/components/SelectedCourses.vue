<template>
  <b-list-group id="selected-course-list" class="flex-grow-1" flush>
    <b-list-group-item v-for="course of courses" :key="course.id">
      <CourseListing
        :course="course"
        :actions="{ remove: true, collapse: true }"
        showSectionsInitial
      />
    </b-list-group-item>
  </b-list-group>
  <!-- <CourseListing
    :courses="courses"
    :actions="{ remove: true, collapse: true }"
    showSectionsInitial
    class="flex-grow-1"
  />-->
</template>

<script>
import '@/typedef';

import CourseListingComponent from '@/components/CourseListing';

export default {
  name: 'SelectedCourses',
  components: {
    CourseListing: CourseListingComponent
  },
  computed: {
    courses() {
      return this.$store.getters.selectedCourses;
    }
  }
};
</script>

<style scoped lang="scss">
#selected-course-list {
  overflow-y: scroll !important;
  overflow-x: auto;
  height: 0px;
}
</style>
