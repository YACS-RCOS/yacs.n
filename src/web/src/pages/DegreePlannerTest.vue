<template>
  <div class="search-container">
    <input
      v-model="courseName"
      @input="handleInput"
      placeholder="Enter course name"
      class="search-input"
    >
    <ul v-if="showDropdown" class="search-results">
      <li v-for="course in matchingCourses" :key="course.id" @click="selectCourse(course)">
        {{ course.name }}
      </li>
      <li v-if="matchingCourses.length === 0" class="no-results">No results found</li>
    </ul>
  </div>
</template>

<script>
import debounce from 'lodash/debounce'; // Import the debounce function from lodash

export default {
  data() {
    return {
      courseName: '',
      matchingCourses: [],
      showDropdown: false,
    };
  },
  methods: {
    // Debounce the handleInput method to prevent excessive API calls
    debouncedHandleInput: debounce(function () {
      this.handleInput();
    }, 300),
    handleInput() {
      // Simulate fetching matching courses from the database (replace this with actual API call).
      this.matchingCourses = this.fetchMatchingCoursesFromDatabase(this.courseName);
      this.showDropdown = this.matchingCourses.length > 0;
    },
      selectCourse(course) {
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
        { id: 6, name: 'History' },
        // Add more courses here as needed
      ];
      return coursesFromDatabase.filter(course => course.name.toLowerCase().includes(input.toLowerCase()));
    },
  },
};
</script>

<style>
.search-container {
  position: relative;
  width: 300px;
}

.search-input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
}

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
</style>
