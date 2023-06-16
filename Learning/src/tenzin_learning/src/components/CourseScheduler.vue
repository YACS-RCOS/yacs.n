<template>
  <div>
    <h1>{{ title }}</h1>
    <h3>{{ intro }}</h3>
    
    <form @submit.prevent="addCourse">
      <input v-model="newCourse.courseNum" placeholder="Course Number">
      <input v-model="newCourse.courseName" placeholder="Course Name">
      <button>Add Course</button>
    </form>
    
    <ul>
      <li v-for="course in courses" :key="course.id">
        {{ course.courseNum }} - {{ course.courseName }}
        <button @click="removeCourse(course)">Remove</button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      title: "Welcome!",
      intro: "Add and remove courses as you would like!",
      newCourse: {
        courseNum: "",
        courseName: "",
      },
      courses: [],
    };
  },
  methods: {
    addCourse() {
      if (this.newCourse.courseNum && this.newCourse.courseName) {
        const course = {
          id: this.courses.length,
          courseNum: this.newCourse.courseNum,
          courseName: this.newCourse.courseName,
        };
        this.courses.push(course);
        this.newCourse.courseNum = "";
        this.newCourse.courseName = "";
      }
    },
    removeCourse(course) {
      this.courses = this.courses.filter((c) => c.id !== course.id);
    },
  },
};
</script>

<style scoped>
li {
  list-style-type: circle;
}

h3 {
  font-weight: lighter;
}
</style>

"scripts": {
    "preview": "vite preview --port 8080"
  }
