<template>
  <div>
    <div>
      <input class="text-input" v-model="textInput" type="text" placeholder="course name" @keyup.enter="courselist">
    </div>
    <div class="fulfilled-list">
      <li v-for="course in courses" :key="course" draggable="true" @dragstart="dragStart(course)">
        {{ course }}
      </li>
    </div>

    <div>
      <h1>Course Template</h1>
    </div>
    <div class="table-container">
      <table>
        <tbody>
          <tr v-for="(semester, semesterIndex) in courseTable" :key="semesterIndex">
            <td v-for="(column, columnIndex) in semester" :key="columnIndex" @dragover.prevent @drop="dropCourse(semesterIndex, columnIndex)">
              <div class="course-item" :class="{ 'drag-over': isDragOver }" @dragenter="dragEnter" @dragleave="dragLeave" @click="removeCourse(semesterIndex, columnIndex)">
                <template v-for="course in column">
                  {{ course }}
                </template>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      courses: [],
      courseTable: [
        [[], []], // Semester 1
        [[], []], // Semester 2
        [[], []], // Semester 3
        [[], []], // Semester 4
      ],
      textInput: "",
      isDragOver: false,
      dragData: null,
    };
  },
  methods: {
    async courselist() {
      let course = this.textInput;
      const response1 = await fetch("/api/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ course }),
      });

      this.courses = await response1.json();
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
    dropCourse(semesterIndex, columnIndex) {
      this.courseTable[semesterIndex][columnIndex].push(this.dragData);
      this.dragData = null;
      this.isDragOver = false;
    },
    removeCourse(semesterIndex, columnIndex) {
      this.courseTable[semesterIndex][columnIndex] = [];
    },
    updateCourse(rowIndex, columnIndex) {
      // Not needed in this implementation as courses are not edited directly in the table cells
    },
  },
};
</script>

<style scoped>
.fulfilled-list {
  font-size: 1em;
}

.table-container {
  margin-top: 1em;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid black;
  padding: 0.5em;
}

.course-item {
  display: inline-block;
  margin-right: 0.5em;
  cursor: pointer;
}

.drag-over {
  border: 2px dashed red;
}
</style>
