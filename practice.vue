<script>
let id = 0

export default {
	data() {
		return {
			title: "Welcome!",
			intro: "Add and remove courses as you would like!",
			num: '',
			text: '',
			courses: [
				{ id: id++, course_num: "CSCI 1100", course_name: "Computer Science I" },
				{ id: id++, course_num: "CSCI 1200", course_name: "Data Structures" },
				{ id: id++, course_num: "CSCI 2200", course_name: "Foundations of Computer Science" },
				{ id: id++, course_num: "CSCI 2300", course_name: "Introduction to Algorithms" }
			]
		}
	},
	methods: {
		// add courses to existing array
		addCourse() {
			this.courses.push({ id: id++, course_num: this.num, course_name: this.text })
			this.num = ''
			this.text = ''
		},
		// remove courses from existing array
		removeCourse(course) {
			this.courses = this.courses.filter((c) => c !== course)
		}
	}
}
</script>

<template>
	<h1> {{ title }} </h1>
	<h3> {{ intro }} </h3>
	<!-- form to add courses -->
	<form @submit.prevent="addCourse">
		<input v-model="num" placeholder="Course Number">
		<input v-model="text" placeholder="Course Name">
		<button>Add Course</button>
	</form>
	<!-- displaying array with courses -->
	<ul>
		<li v-for="course in courses" :key="course.id">
			{{ course.course_num }} - {{ course.course_name }}
			<button @click="removeCourse(course)">Remove</button>
		</li>
	</ul>
</template>

<style>
li {
	list-style-type: circle;
}

h3 {
	font-weight: lighter;
}
</style>
