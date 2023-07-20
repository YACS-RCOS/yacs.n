<template>
  <div>
    <div>
      <input class="text-input" v-model="textInput" type="text" placeholder="course name" @keyup.enter="courseSearch(textInput)">
    </div>
    <div class="fulfilled-list">
      <div v-for="course in courseSearchResults" :key="course" draggable="true" @dragstart="dragStart(course)">
          {{ course }}
      </div>
    </div>

    <div class="scheduler">
      <div v-for="(semester, index) in schedulerB" :key="index" @dragover.prevent @drop="dropCourse(semester)">
        <div class="course-item" :class="{ 'drag-over': isDragOver }" @dragenter="dragEnter" @dragleave="dragLeave" @click="removeCourse(index)">
          <h3> Semester {{ index }} </h3>
          <div v-for="course in semester" :key="course">
            <button class="course-buttons" type="button">
              &#10148; {{ course }}
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      courseSearchResults: [],
      schedulerB: [],
      textInput: "",
      isDragOver: false,
      dragData: null,
    };
  },
  methods: {
    async courseSearch(course) {
      const response1 = await fetch("/api/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(course),
      });

      this.courseSearchResults = await response1.json();
    },

    dragStart(course) {
      this.dragData = course;
    },
    dragEnter(event) {
      event.preventDefault();
      this.isDragOver = true;
    },
    dragLeave() {
      this.isDragOver = false;
    },
    dropCourse(semester) {
      this.schedulerB[semester].push(this.dragData);
      this.$set(this.schedulerB, semester, [...this.schedulerB[semester]]);
      this.dragData = null;
      this.isDragOver = false;
    },
    removeCourse(semester) {
      this.schedulerB[semester].pop();
      this.$set(this.schedulerB, semester, [...this.schedulerB[semester]]);
    },    
  },

  async created() {
    this.schedulerB = Array(12).fill([])
  },
};
</script>

<style scoped>
.fulfilled-list {
  font-size: 1em;
}

.scheduler {
  width: 50%;
  border-collapse: collapse;
}

.course-item {
  display: inline-block;
  margin-right: 0.5em;
  cursor: pointer;
}

.course-buttons {
    border: none;
    border-radius: 4px;
    flex: 1;
    padding: 0px;
    width: 99%;
    margin: 1px;
    color:#e3e8e4;
    background-color: rgba(197, 211, 218, 0.01);
    transition: background-color 0.15s ease;
    text-align: left;
  }
  .course-buttons:hover {
    background-color: rgba(13, 23, 26, 0.78);
  }

.drag-over {
  border: 2px dashed red;
}
</style>
