<template>
  <div>
    <div class="search-container">
      <input
        ref="inputBox"
        class="search-input"
        v-model="searchInput"
        @input="inputHandler"
        placeholder="Enter course name"
        @blur="onBlur"
        @focus="onFocus"
        @keyup.enter="selectEnter"
      >
      <div v-if="showDropdown" ref="resultsList" class = results>
        <ul class="search-results">
          <li v-if="searchMatches.length === 0" class="no-results">No results found</li>
          <li v-for="(course, index) in searchMatches" :key="index" @click="selectMatch(index)">
            {{ course.display_name }}
          </li>
        </ul>
        <ul class="suggestions">
          <li>Recommendations:</li>
          <li> none for now ;-; </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import debounce from 'lodash/debounce';

export default {
  data() {
    return {
      courses: [],

      searchInput: '',
      searchMatches: [],
      showDropdown: false,
    };
  },
  methods: {
    outputValue(val) {
      // Increment the value and emit an event to notify the parent
      this.$emit('result', val);
    },

    onBlur() {
      document.addEventListener('click', this.handleClickOutside);
    },

    onFocus() {
      // Allow the click event to propagate before removing the listener
      this.showDropdown = true;
      this.searchMatches = this.courses;
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

    inputHandler() {
      this.showDropdown = true;
      this.debouncedsearch();
    },

    debouncedsearch: debounce(function () {
      this.search();
    }, 400),

    search() {
      let input = this.searchInput
      input = input.toLowerCase();
      console.log('performed search')
      this.searchMatches = this.courses.filter(course => course.search_name.includes(input));
    },

    async searchAlternative() {
      this.searchMatches = await this.searchOnline(this.searchInput);
    },

    selectEnter() {
      this.search();
      this.selectMatch(0);
    },

    selectMatch(position) {
      if (/^\d+$/.test(this.searchInput.substring(5,9))) {
        console.log('input was a course ID')
        this.outputValue(this.searchInput)
      }
      else if (this.searchMatches.length == 0) {
        this.outputValue(this.searchInput)
      }
      else if (position < this.searchMatches.length) {
        this.outputValue(this.searchMatches[position].display_name)
      }
      this.searchInput = "";
      this.showDropdown = false;
    },

    async searchOnline(input) {
      // uses degree planner's own searching algorithm, requires api call so more taxing on the backend
      // uses a fast token matching algorithm rather than exact filtering
      const response = await fetch('/api/dp/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(input),
      });
      let matches = await response.json();
      return matches
    },

    async fetchElements() {
      const response = await fetch('/api/dp/courses/false');
      let course_list = await response.json();
      for (let i = 0; i < course_list.length; ++i) {
        this.courses.push({display_name: course_list[i], search_name: course_list[i].toLowerCase()})
      }
    },
  },
  async created() {
    await this.fetchElements().then(this.$emit('complete'));
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

.results {
  z-index: 9999;
  position: absolute;
  top: 100%;
  left: 0;
  width: 90%;
  background-color: #141415;
  list-style: none;
  margin: 1px;
  padding: 6px;
  border-radius: 4px;
  border: 2px solid #2d2e31;
  border-top: none;
}

.search-results {
  top: 100%;
  left: 0;
  width: 100%;
  max-height: 300px;
  background-color: #323435;
  list-style: none;
  margin: 2px;
  padding: 2px;
  border-radius: 4px;
  border: 2px solid #2d2e31;
  overflow-y:scroll;
}

.suggestions {
  top: 100%;
  left: 0;
  width: 100%;
  max-height: 250px;
  background-color: #4c5458;
  list-style: none;
  margin: 2px;
  padding: 2px;
  border-radius: 4px;
  border: 2px solid #2d2e31;
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
