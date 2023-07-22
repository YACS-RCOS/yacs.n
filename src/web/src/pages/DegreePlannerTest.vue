<template>
    <div>
      <input v-model="courseName" @input="handleInput" placeholder="Enter course name">
      <ul v-if="showDropdown">
        <li v-for="course in matchingCourses" :key="course.id" @click="selectCourse(course)">
          {{ course.name }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        courseName: '',
        matchingCourses: [],
        showDropdown: false,
      };
    },
    methods: {
      handleInput() {
        // Simulate fetching matching courses from the database (replace this with actual API call).
        this.matchingCourses = this.fetchMatchingCoursesFromDatabase(this.courseName);
        this.showDropdown = this.matchingCourses.length > 0;
      },
      selectCourse(course) {
        this.courseName = course.name;
        this.showDropdown = false;
      },
      fetchMatchingCoursesFromDatabase(input) {
        // Replace this with actual API call to fetch matching courses from the database.
        // For simplicity, using a static array in this example.
        const coursesFromDatabase = [
          { id: 1, name: 'Mathematics' },
          { id: 2, name: 'Computer Science' },
          { id: 3, name: 'Physics' },
          { id: 4, name: 'Chemistry' },
          { id: 5, name: 'Biology' },
        ];
        return coursesFromDatabase.filter(course => course.name.toLowerCase().includes(input.toLowerCase()));
      },
    },
  };
  </script>
  