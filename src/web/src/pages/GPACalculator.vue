<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <b-row class="justify-content-md-center">
      <b-col md="6">
        <b-card title="Calculate GPA">
          <b-form @submit.prevent="calculateGPA">
            <div
              v-for="(course, index) in courses"
              :key="index"
              class="mb-3"
            >
              <b-form-group :label="'Course ' + (index + 1)">
                <b-form-input v-model="course.name" placeholder="Course Name"></b-form-input>
                <b-form-input v-model="course.credits" placeholder="Credits"></b-form-input>
                <b-form-input v-model="course.grade" placeholder="Grade"></b-form-input>
              </b-form-group>
            </div>
            <b-button @click="addCourse" variant="primary">Add Course</b-button>
            <b-button type="submit" variant="success" class="ml-3">
              Calculate GPA
            </b-button>
          </b-form>
          <b-card v-if="gpa" class="mt-3">
            <h5 class="card-title">GPA Result</h5>
            <div>
              <strong>Your GPA:</strong> {{ gpa }}
            </div>
          </b-card>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data() {
    return {
      breadcrumbNav: [
        { text: 'Home', href: '/' },
        { text: 'Calculate GPA', active: true }
      ],
      courses: [{ name: '', credits: 0, grade: 0 }],
      gpa: null
    };
  },
  methods: {
    addCourse() {
      this.courses.push({ name: '', credits: 0, grade: 0 });
    },
    calculateGPA() {
      let totalCredits = 0;
      let totalGradePoints = 0;

      this.courses.forEach(course => {
        const credits = parseFloat(course.credits);
        const grade = parseFloat(course.grade);

        if (!isNaN(credits) && !isNaN(grade)) {
          totalCredits += credits;
          totalGradePoints += credits * grade;
        }
      });

      if (totalCredits > 0) {
        this.gpa = (totalGradePoints / totalCredits).toFixed(2);
      } else {
        this.gpa = null;
      }
    }
  }
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>
