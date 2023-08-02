<template>
  <div>
    <div class="search-container">
      <input
        ref="inputBox"
        class="search-input"
        v-model="courseName"
        @input="handleInput"
        placeholder="Enter course name"
        @blur="onFocus"
        @focus="onBlur"
        @keyup.enter="selectCourse(0)"
      >
      <ul ref="resultsList" v-if="showDropdown" class="search-results">
        <li v-if="matchingCourses.length === 0" class="no-results">No results found</li>
        <li v-for="(course, index) in matchingCourses" :key="index" @click="selectCourse(index)">
          {{ course.name }}
        </li>
      </ul>
    </div>
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
    outputValue(val) {
      // Increment the value and emit an event to notify the parent
      this.$emit('result', val);
    },

    onFocus() {
      this.showDropdown = true;
      document.addEventListener('click', this.handleClickOutside);
    },
    onBlur() {
      // Allow the click event to propagate before removing the listener
      this.$nextTick(() => {
        document.removeEventListener('click', this.handleClickOutside);
      });
    },
    handleClickOutside(event) {
      // Check if the clicked element is outside both the input box and the results list
      if (
        this.$refs.inputBox &&
        !this.$refs.inputBox.contains(event.target) &&
        this.$refs.resultsList &&
        !this.$refs.resultsList.contains(event.target)
      ) {
        this.showDropdown = false;
      }
    },

    handleInput() {
      // Simulate fetching matching courses from the database (replace this with actual API call).
      this.matchingCourses = this.fetchMatchingCoursesFromDatabase(this.courseName);
      this.showDropdown = this.matchingCourses.length > 0;
    },
    selectCourse(position) {
      if (this.matchingCourses.length == 0) {
        this.outputValue(this.courseName)
      }
      if (position < this.matchingCourses.length) {
        this.outputValue(this.matchingCourses[position].name)
      }
      this.courseName = "";
      this.showDropdown = false;
    },
    fetchMatchingCoursesFromDatabase(input) {
      // Replace this with actual API call to fetch matching courses from the database.
      // For simplicity, using a static array in this example.
      const coursesFromDatabase = [
        { id: 1, name: 'CSCI 1200 Data Structures' },
        { id: 2, name: 'CSCI 2300 Introduction to Algorithms' },
        { id: 3, name: 'CSCI 4350 Data Science' },
        { id: 4, name: 'CSCI 4800 Numerical Computing' },
        { id: 5, name: 'PHYS 1200 Physics II' },
        { id: 6, name: 'ARTS 4070 3D Animation' },
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
  width: 90%;
}

.search-input {
  width: 80%;
  font-size: 10px;
  z-index: 999;
  position: relative;
}

.search-results {
  z-index: 9999;
  position: absolute;
  top: 100%;
  left: 0;
  width: 90%;
  max-height: 200px;
  background-color: #1c1d1f;
  list-style: none;
  padding: 0;
  margin: 0;
  border: 1px solid #1c1d1f;
  border-top: none;
  overflow-y: auto;
}

.search-results li {
  padding: 2px;
  cursor: pointer;
}

.search-results li:hover {
  background-color: #27292b;
}

.no-results {
  padding: 2px;
  text-align: center;
}
</style>
