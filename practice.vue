<script>
let id = 0

export default {
  data() {
    return {
      title: 'titleClass',
      newCourse: '',
      courses: [
        { id: id++, text: 'Student Success Labs' },
        { id: id++, text: 'Deep Listening' },
        { id: id++, text: 'Cosmology: Our Universe' }
      ]
    }
  },
  methods: {
    addCourse() {
      this.courses.push({ id: id++, text: this.newCourse })
      this.newCourse = ''
    },
    removeCourse(course) {
      this.courses = this.courses.filter((t) => t !== course)
    }
  }
}
</script>

<template>
  <h1 :class="title">YACS</h1>
  <form @submit.prevent="addCourse">
    <input v-model="newCourse" placeholder= "Add your course here">
    <button>Add Course</button>    
  </form>
  <p> 
    Your courses:
  </p>
  <ul>
    <li v-for="course in courses" :key="course.id">
      {{ course.text }}
      <button @click="removeCourse(course)">Delete</button>
    </li>
  </ul>
  
</template>

<style>
  .titleClass {
    color: blue;
  }
</style>