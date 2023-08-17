<template>
  <div>
      <div v-if="showDropdown" ref="resultsList" class="results">
        <h3>SEMESTER {{ selectedSemester + 1 }}</h3>
        <input
          ref="searchBar"
          class="search-input"
          v-model="searchInput"
          @input="inputHandler"
          placeholder="Enter course name"
          @keyup.enter="selectEnter"
        />

        <div class="subject-filter">
          <div class="subject-group" :style="arrayToHSLBackground(subjectGroupColors[subject_group.title.toLowerCase()])" v-for="(subject_group, subject_group_index) in subjectGroups" :key="subject_group_index">
            {{ extractTitle(subject_group.title) }}<br>
            <button class="subject-buttons" :style="getSubjectButtonColor(subject)" type="button" v-for="(subject, subject_index) in subject_group.elements" :key="subject_index" @click="filterCourses(subject)">
              {{ extractTitle(subject) }}
            </button>
            <br>
          </div>
        </div>
        <div ref="searchMatchList">
          <ul class="search-results">
            <li v-show="searchMatches.length === 0" class="no-results">No results found</li>
            <li v-show="searchContextSize < searchMatches.length && searchDisplayContext > 0" @click="decrementSearchPage">
              <span class="search-traversal-button">PREVIOUS</span>
            </li>
            <li v-for="(course, index) in searchMatches.slice(searchDisplayContext * searchContextSize, (searchDisplayContext + 1) * searchContextSize)" :key="index" @click="selectMatch(index)" draggable="true" @dragstart="courseDrag($event, course.display_name)">
              <span class="search-result" :style="getCourseFrontColor(course.search_name)"> {{ course.display_name.substring(0, 10) }} </span> 
              <span v-bind:class="{'search-result-body':!(course.display_name in courseSelected), 'search-result-body-selected':course.display_name in courseSelected}" :style="getCourseBackColor(course.display_name)"> {{ course.display_name.substring(10) }} </span>
              <span class="selected-tag" v-show="course.display_name in courseSelected"> (selected in semester {{ getSemestersPresentIn(course.display_name) }}) </span>
            </li>
            <li v-show="(searchDisplayContext + 1) * searchContextSize < searchMatches.length" @click="incrementSearchPage">
              <span class="search-traversal-button" >NEXT</span>
            </li>
          </ul>
        </div>

        <div class="suggestions">
        </div>
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
      courseRecType: {}, // course can be (1) core, (2) useful
      courseSelected: {},
      subjectGroups: [],
      subjectColors: {},
      subjectGroupColors: {},
      filterSubject: '',

      searchInput: '',
      searchMatches: [],
      searchDisplayContext: 0,
      searchContextSize: 50,
      showDropdown: false,
      selectedSemester: -1,

      closeModalOnSelection: false,
    };
  },

  methods: {
    courseDrag(event, course) {
      event.dataTransfer.effectAllowed = "move";
      this.$emit('courseDrag', course);
    },
    importCourses(courses) {
      this.courseSelected = [];
      for (let semester = 0; semester < courses.length; ++semester) {
        for (let i = 0; i < courses[semester].length; ++i) {
          const course_name = courses[semester][i];
          if (course_name in this.courseSelected) {
            this.courseSelected[course_name].push(semester + 1);
          }
          else {
            this.courseSelected[course_name] = [semester + 1];
          }
          //console.log(this.courseSelected[course_name]);
        }
      }
    },
    incrementSearchPage() {
      //this.$refs.searchMatchList.scrollTop = 0;
      if ((this.searchDisplayContext + 1) * this.searchContextSize < this.searchMatches.length) {
        this.searchDisplayContext++;
      }
    },
    decrementSearchPage() {
      if (this.searchDisplayContext > 0) {
        this.searchDisplayContext--;
      }
    },
    getSemestersPresentIn(course) {
      if (!(course in this.courseSelected)) {
        return
      }
      return this.courseSelected[course].join(', ')
    },
    sumAsciiValues(word) {
      let sum = 0;
      for (let i = 0; i < word.length; i++) {
        sum += word.charCodeAt(i); // Get ASCII value of character and add to sum
      }
      return sum;
    },
    getCourseFrontColor(course){
      const type = this.courseRecType[course];
      if (type == "core" || course.startsWith("csci 1200")) {
        return this.makeHSLColor(20, 85, 70)
      } 
      else if (type == "useful" || course.startsWith("csci 4220")) {
        return this.makeHSLColor(90, 75, 65)
      }
      return this.makeHSLColor(40, 55, 70)
    },
    getCourseBackColor(course){
      if (course in this.courseSelected) {
        return this.makeHSLColor(90, 55, 75)
      }
      return this.makeHSLColor(40, 0, 100)
    },
    getSubjectButtonColor(subject) {
      const colors = this.subjectColors[subject];
      if (this.filterSubject == subject) {
        return this.makeHSLBackground(colors[0] + 10, colors[1] + 30, colors[2] + 30)
      }
      return this.arrayToHSLBackground(colors)
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


    arrayToHSLBackground(array) {
      if (array.length == 4) {
        return {
          backgroundColor: `hsla(${array[0]}, ${array[1]}%, ${array[2]}%, ${array[3]})`
        };
      }
      return {
        backgroundColor: `hsl(${array[0]}, ${array[1]}%, ${array[2]}%)`
      };
    },

    makeHSLColor(hue, saturation, lightness, alpha=-1) {
      // console.log("hue: " + hue + " sat:" + saturation + " light: " + lightness);
      if (alpha != -1) {
        return {
          color: `hsla(${hue}, ${saturation}%, ${lightness}%, ${alpha})`
        };
      }
      return {
        color: `hsl(${hue}, ${saturation}%, ${lightness}%)`
      };
    },

    makeHSLBackground(hue, saturation, lightness, alpha = -1) {
      if (alpha != -1) {
        return {
          backgroundColor: `hsla(${hue}, ${saturation}%, ${lightness}%, ${alpha})`
        };
      }
      // console.log("hue: " + hue + " sat:" + saturation + " light: " + lightness);
      return {
        backgroundColor: `hsl(${hue}, ${saturation}%, ${lightness}%)`
      };
    },

    colorTextExtract(element, hue_offset = 0, saturation_offset = 0, lightness_offset = 0, alpha = 1, index = -1) {
      let colors = this.extractColorHSL(element);
      if (colors.length == 3) {
        return [(colors[0] + hue_offset) % 360, (colors[1] + saturation_offset), (colors[2] + lightness_offset), alpha]
      }
      if (index != -1) {
        return [(index * 360 + hue_offset) % 360, saturation_offset, lightness_offset, alpha]
      }
      else {
        return [hue_offset % 360, saturation_offset, lightness_offset, alpha]
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

    onClick(semester) {
      this.$nextTick(() => {
        this.$refs.searchBar.focus();
      });
      this.selectedSemester = semester;
    },

    onClose() {
      this.searchInput = '';
      this.searchDisplayContext = 0;
      this.searchMatches = this.courses;
    },

    inputHandler() {
      //this.showDropdown = true;
      this.debouncedsearch();
    },

    debouncedsearch: debounce(function () {
      this.searchDisplayContext = 0;
      this.search();
    }, 400),

    search(stop_count = -1) {
      let input = this.searchInput
      input = input.toLowerCase();
      console.log('performed search')
      if (stop_count == -1) {
        this.searchMatches = this.courses.filter(course => course.search_name.includes(input));
      } else {
        this.searchMatches = [];
        for (let i = 0; i < this.courses.length && this.searchMatches.length < stop_count; ++i) {
          if (this.courses[i].search_name.includes(input)) {
            this.searchMatches.push(this.courses[i]);
          }
        }
      }
    },

    async searchAlternative() {
      this.searchMatches = await this.searchOnline(this.searchInput);
    },

    selectEnter() {
      this.search(1);
      this.selectMatch(0);
      this.searchInput = '';
      this.search();
    },

    selectMatch(position) {
      position = (this.searchContextSize * this.searchDisplayContext) + position;
      if (this.searchMatches.length == 0) {
        this.outputValue(this.searchInput)
      }
      else if (position < this.searchMatches.length) {
        this.outputValue(this.searchMatches[position].display_name)
      }
      //if (this.closeModalOnSelection) {
      //  this.showDropdown = false;
      //}
    },

    filterCourses(subject) {
      this.courses = [];
      this.searchDisplayContext = 0;
      if (subject == '' || this.filterSubject == subject) {
        this.filterSubject = '';
        this.courses = this.all_courses;
      }
      else {
        this.filterSubject = subject;
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
      let matches = await response.json();
      return matches
    },

    async fetchElements() {
      const response = await fetch('/api/dp/courses/false');
      let course_list = await response.json();
      for (let i = 0; i < course_list.length; ++i) {
        this.all_courses.push({display_name: course_list[i], search_name: course_list[i].toLowerCase()})
        this.courses.push({display_name: course_list[i], search_name: course_list[i].toLowerCase()})
      }
      this.searchMatches = this.courses;
    },

    async fetchSubjectGroups() {
      const response = await fetch('/api/dp/subjectgroups');
      this.subjectGroups = await response.json();
    },

    computeSubjectColors() {
      for (let i = 0; i < this.subjectGroups.length; ++i) {
        let group = this.subjectGroups[i];
        this.subjectGroupColors[group.title.toLowerCase()] = this.colorTextExtract(group.title, 0, 15, 70, 0.7, i / this.subjectGroups.length);
        for (let j = 0; j < group.elements.length; ++j) {
          this.subjectColors[group.elements[j]] = this.colorTextExtract(group.title, j, 12 - j * 0.25, 70 - 5 + j * 0.2, 1, i / this.subjectGroups.length)
        }
      }
      this.$emit('setSubjectColors', this.subjectColors);
      this.$emit('setSubjectGroupColors', this.subjectGroupColors);
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

.search-input {
  width: 100%;
  font-size: 14px;
  padding: 2px;
  margin-top: 2px;
  border-radius: 4px;
  border: none;
}

.results {
  position: absolute;
  top: 100%;
  left: 0;
  width: 334px;
  background-color: rgba(39, 43, 44, 0.75);
  list-style: none;
  padding: 8px;
  border-radius: 4px;
  border: 2px solid #565a5c;
  backdrop-filter: blur(4px);
}
.results h3 {
  font-size: 14px;
  margin: 2px;
  color:#b3bfc3;
}

.search-results {
  top: 100%;
  left: 0;
  width: 100%;
  max-height: 255px;
  background-color: rgba(30, 32, 33, 0.7);
  list-style: none;
  margin-top: 2px;
  padding: 2px;
  border-radius: 4px;
  border: none;
  overflow-y:scroll;
}
.search-result {
  font-weight: 600;
  font-size: 11px;
}
.search-result-body {
  font-weight: 450;
  font-size: 11px;
}
.search-result-body-selected {
  font-weight: 400;
  font-style: italic;
  font-size: 11px;
}
.search-traversal-button {
  font-weight: 850;
  font-size: 13px;
  color: #b2babc;
}
.selected-tag {
  font-weight: 500;
  font-size: 11px;
  color: #9fa7b0;
}

.subject-filter {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 5px;
  margin-top: 4px;
  margin-bottom: 4px;
  position: relative;
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
  width: 43px;
  padding: 0px;
  font-weight: 600;
  margin-bottom: 0px;
  margin-top: 0px;
  margin-left: 2px;
  margin-right: 2px;
  color: #141415;
  background-color:#141415;
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
  margin-bottom: 2px;
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
