<template>
  <b-list-group class="selected-course-list" flush>
    <b-list-group-item v-for="course of courses" :key="course.id">
      <CourseListing
        :course="course"
        :actions="{remove:true}"
        showSectionsInitial
        v-on="$listeners"
      />
    </b-list-group-item>
  </b-list-group>
</template>

<script>
import '@/typedef';

import CourseListingComponent from '@/components/CourseListing';

export default {
  name: 'SelectedCourses',
  components: {
    CourseListing: CourseListingComponent
  },
  props: {
    courses: Object
  }
};
</script>

<style lang="scss">
</style>
