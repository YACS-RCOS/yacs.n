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
                <b-form-select v-model="course.grade" :options="gradeOptions" placeholder="Grade"></b-form-select>
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
      courses: [{ name: '', credits: 0, grade: '' }],
      gpa: null,
      gradeOptions: ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F']
    };
  },
  methods: {
    addCourse() {
      this.courses.push({ name: '', credits: 0, grade: '' });
    },
    calculateGPA() {
      let totalCredits = 0;
      let totalGradePoints = 0;

      this.courses.forEach(course => {
        const credits = parseFloat(course.credits);
        const grade = this.convertGradeToNumber(course.grade);

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
    },
    convertGradeToNumber(grade) {
      switch (grade) {
        case 'A': return 4.0;
        case 'A-': return 3.7;
        case 'B+': return 3.3;
        case 'B': return 3.0;
        case 'B-': return 2.7;
        case 'C+': return 2.3;
        case 'C': return 2.0;
        case 'C-': return 1.7;
        case 'D+': return 1.3;
        case 'D': return 1.0;
        case 'F': return 0.0;
        default: return NaN;
      }
    }
  }
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>
