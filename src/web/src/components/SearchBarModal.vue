<template>
  <div>
    <div v-if="showDropdown" ref="resultsList" class="results">
      <input
        ref="searchBar"
        class="search-input"
        v-model="searchInput"
        placeholder="Enter course name"
        @input="inputHandler"
        @keyup.enter="selectEnter"
      />
      <div class="subject-clear-filter">
        <button class="subject-clear-button" type="button" @click="filterCourses('')">
          CLEAR
        </button>
      </div>
      <div class="subject-filter">
        <div class="subject-group" :style="subjectGroupColors[subject_group.title]" v-for="(subject_group, subject_group_index) in subjectGroups" :key="subject_group_index">
          {{ extractTitle(subject_group.title) }}<br>
          <button class="subject-buttons" :style="subjectColors[subject]" type="button" v-for="(subject, subject_index) in subject_group.elements" :key="subject_index" @click="filterCourses(subject)">
            {{ extractTitle(subject) }}
          </button>
          <br>
        </div>
      </div>

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
</template>

<script>
import debounce from 'lodash/debounce';

export default {
  data() {
    return {
      all_courses: [],
      courses: [],
      subjectGroups: [],
      subjectColors: {},
      subjectGroupColors: {},
      filterSubject: '',

      searchInput: '',
      searchMatches: [],
      showDropdown: false,
    };
  },

  methods: {
    sumAsciiValues(word) {
      let sum = 0;
      for (let i = 0; i < word.length; i++) {
        sum += word.charCodeAt(i); // Get ASCII value of character and add to sum
      }
      return sum;
    },

    extractColorHSL(element) {
      if (element.includes("#")) {
        return element.split("#")[1].split(",")
      }
      return []
    },

    extractTitle(element) {
      return element.split('#')[0]
    },

    colorText(hue, saturation, lightness) {
      // console.log("hue: " + hue + " sat:" + saturation + " light: " + lightness);
      return {
        backgroundColor: `hsl(${hue}, ${saturation}%, ${lightness}%)`
      };
    },

    colorTextExtract(element, hue_offset = 0, saturation_offset = 0, lightness_offset = 0, index = -1) {
      let colors = this.extractColorHSL(element);
      if (colors.length == 3) {
        return this.colorText((colors[0] + hue_offset) % 360, (colors[1] + saturation_offset), (colors[2] + lightness_offset));
      }
      if (index != -1) {
        return this.colorText((index * 360 + hue_offset) % 360, saturation_offset, lightness_offset)
      }
      else {
        return this.colorText(hue_offset % 360, saturation_offset, lightness_offset)
      }
    },

    randColorText(text, offset, multiple = 1, saturation = 33, lightness = 70) {
      return {
        backgroundColor: `hsl(${((this.sumAsciiValues(text) + offset) % 360) * multiple}, ${saturation}, ${lightness})`
      };
    },

    outputValue(val) {
      // Increment the value and emit an event to notify the parent
      this.$emit('result', val);
    },

    dropdown(show) {
      this.showDropdown = show;
      this.$emit('showDropdown', show);
    },

    open() {
      console.log('open uwu')
      if (this.showDropdown == true) {
        this.dropdown(false);
        return
      }
      this.dropdown(true);
      this.$nextTick(() => {
        this.$refs.searchBar.focus();
      });
      this.searchMatches = this.courses;
      document.removeEventListener('click', this.handleClickOutside);
      document.addEventListener('click', this.handleClickOutside);
    },

    handleClickOutside(event) {
      // Check if the clicked element is outside both the input box and the results list
      if (this.$refs.resultsList && !this.$refs.resultsList.contains(event.target)) {
        this.dropdown(false);
      }
    },

    inputHandler() {
      this.dropdown(true);
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
      this.dropdown(false);
    },

    filterCourses(subject) {
      this.courses = [];
      if (subject === '') {
        this.courses = this.all_courses;
      }
      else {
        subject = subject.toLowerCase();
        this.courses = this.all_courses.filter(course => course.search_name.startsWith(subject));
      }
      this.search();
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
      this.searchMatches = await response.json();
    },

    async fetchElements() {
      const response = await fetch('/api/dp/courses/false');
      let course_list = await response.json();
      for (let i = 0; i < course_list.length; ++i) {
        this.all_courses.push({display_name: course_list[i], search_name: course_list[i].toLowerCase()})
        this.courses.push({display_name: course_list[i], search_name: course_list[i].toLowerCase()})
      }
    },

    async fetchSubjectGroups() {
      const response = await fetch('/api/dp/subjectgroups');
      this.subjectGroups = await response.json();
    },

    computeSubjectColors() {
      for (let i = 0; i < this.subjectGroups.length; ++i) {
        let group = this.subjectGroups[i];
        this.subjectGroupColors[group.title] = this.colorTextExtract(group.title, 0, 22, 70, i / this.subjectGroups.length);
        for (let j = 0; j < group.elements.length; ++j) {
          this.subjectColors[group.elements[j]] = this.colorTextExtract(group.title, j, 18 - j * 0.5, 70 - 10 + j * 0.2, i / this.subjectGroups.length)
        }
      }
    }
  },
  async created() {
    await this.fetchElements();
    await this.fetchSubjectGroups();
    this.computeSubjectColors();
  },  
};
</script>

<style scoped>
.search-open {
  border-radius: 4px;
  font-size: 16px;
  background-color:rgba(0,0,0,0);
  height: 20px;
  align-content: center;
  border: none;
  padding: 0;
  margin: 0;
  color:rgb(224, 232, 239);
  font-weight: 900;
}

.search-input {
  width: 99%;
  font-size: 11px;
  margin: 2px;
}

.results {
  position: absolute;
  z-index: 9999;
  top: 100%;
  left: 0;
  width: 325px;
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
  max-height: 200px;
  background-color: #323435;
  list-style: none;
  margin: 2px;
  padding: 2px;
  border-radius: 4px;
  border: 2px solid #2d2e31;
  overflow-y:scroll;
}

.subject-filter {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 5px;
  margin: 2px;
  position: relative;
}

.subject-clear-filter {
  width: 100%;
}

.subject-clear-button {
  width: 99%;
  margin: 2px;
  font-weight: 600;
  font-size: 13px;
  background-color: #71797e;
  border: none;
  border-radius: 4px;
}

.subject-group {
  font-weight: 700;
  font-size: 14px;
  color: #141415;
  border-radius: 4px;
  padding: 6px;
  padding-top: 4px;
  padding-bottom: 2px;
}

.subject-buttons {
  border: none;
  border-radius: 4px;
  font-size: 11px;
  width: 42px;
  padding: 1px;
  font-weight: 600;
  margin-left: 2px;
  margin-right: 2px;
  color: #141415;
  transition: background-color 0.15s ease;
  text-align: center;
}
.subject-buttons:hover {
  background-color: rgb(80, 85, 87);
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
  font-size: 11px;
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
