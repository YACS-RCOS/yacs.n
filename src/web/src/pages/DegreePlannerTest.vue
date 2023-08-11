<template>
  <div class="search-container">
    <!-- Input field for course search -->
    <input
      v-model="courseName"
      @input="debouncedHandleInput"
      placeholder="Enter course name"
      class="search-input"
    >
    <!-- Dropdown for displaying matching courses -->
    <ul v-if="showDropdown" class="search-results">
      <li v-for="course in matchingCourses" :key="course.id" @click="selectCourse(course)">
        {{ course.name }}
      </li>
      <li v-if="matchingCourses.length === 0" class="no-results">No results found</li>
    </ul>
  </div>
  <!-- Display selected course -->
  <div v-if="selectedCourse" class="selected-course">
    <span class="selected-course-text">{{ selectedCourse.name }}</span>
    <span class="selected-course-remove" @click="removeSelectedCourse">Remove</span>
  </div>
</template>

<script>
// Import debounce function from lodash
import debounce from 'lodash/debounce';

export default {
  data() {
    return {
      courseName: '', // Stores the current search query
      matchingCourses: [], // Stores the list of matching courses
      showDropdown: false, // Controls the visibility of the dropdown
      selectedCourse: null, // Stores the selected course
    };
  },
  methods: {
    // Debounce the handleInput method to prevent excessive API calls
    debouncedHandleInput: debounce(function () {
      this.handleInput();
    }, 300),
    // Handle input changes in the search field
    handleInput() {
      // Simulate fetching matching courses from the database (replace with actual API call)
      this.matchingCourses = this.fetchMatchingCoursesFromDatabase(this.courseName);
      this.showDropdown = this.matchingCourses.length > 0;
    },
    // Select a course from the dropdown
    selectCourse(course) {
      this.courseName = course.name;
      this.showDropdown = false;
      this.selectedCourse = course;
    },
    // Remove the selected course
    removeSelectedCourse() {
      this.selectedCourse = null;
    },
    // Simulate fetching matching courses from the database
    fetchMatchingCoursesFromDatabase(input) {
      const coursesFromDatabase = [
        { id: 1, name: 'Mathematics' },
        { id: 2, name: 'Computer Science' },
        { id: 3, name: 'Physics' },
        { id: 4, name: 'Chemistry' },
        { id: 5, name: 'Biology' },
        { id: 6, name: 'History' },
        // Add more courses here as needed
      ];
      return coursesFromDatabase.filter(course => course.name.toLowerCase().includes(input.toLowerCase()));
    },
  },
};
</script>

<style>
/* Styles for search container and input */
.search-container {
  position: relative;
  width: 300px;
}

.search-input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
}

/* Styles for search results dropdown */
.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  max-height: 200px;
  background-color: #fff;
  list-style: none;
  padding: 0;
  margin: 0;
  border: 1px solid #ccc;
  border-top: none;
  overflow-y: auto;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-results li {
  padding: 10px;
  cursor: pointer;
}

.search-results li:hover {
  background-color: #f0f0f0;
}

.no-results {
  padding: 10px;
  text-align: center;
}

/* Styles for selected course display */
.selected-course {
  margin-top: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  background-color: #f0f0f0;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.selected-course-text {
  font-weight: bold;
}

.selected-course-remove {
  cursor: pointer;
  color: red;
}
</style>
