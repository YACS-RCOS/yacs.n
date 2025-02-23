<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <b-row class="justify-content-md-center">
      <b-col md="6">
        <b-card title="Calculate Course Grade">
          <b-form @submit.prevent="calculateCourseGrade">
            <div
              v-for="(assessment, index) in assessments"
              :key="index"
              class="mb-3"
            >
              <b-form-group :label="'Assessment ' + (index + 1)">
                <b-form-input v-model="assessment.name" placeholder="Assessment Name"></b-form-input>
                <b-form-input v-model="assessment.grade" placeholder="Grade (%)"></b-form-input>
                <b-form-input v-model="assessment.weight" placeholder="Weight (%)"></b-form-input>
              </b-form-group>
            </div>
            <b-button @click="addAssessment" variant="primary">Add Assessment</b-button>
            <b-button type="submit" variant="success" class="ml-3">
              Calculate Course Grade
            </b-button>
          </b-form>
          <b-card v-if="errorMessage" class="mt-3" variant="danger">
            <h5 class="card-title">Error</h5>
            <div>
              {{ errorMessage }}
            </div>
          </b-card>
          <b-card v-else-if="courseGrade" class="mt-3">
            <h5 class="card-title">Course Grade Result</h5>
            <div>
              <strong>Your Course Grade:</strong> {{ courseGrade }}
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
        { text: 'Calculate Course Grade', active: true }
      ],
      assessments: [{ name: '', grade: 0, weight: 0 }],
      courseGrade: null,
      errorMessage: null,
    };
  },
  methods: {
    addAssessment() {
      this.assessments.push({ name: '', grade: 0, weight: 0 });
    },
    calculateCourseGrade() {
      let totalWeightedGrade = 0;
      let totalWeight = 0;
      this.errorMessage = null; // Reset error message
      this.assessments.forEach(assessment => {
        const grade = parseFloat(assessment.grade);
        const weight = parseFloat(assessment.weight);
        if (!isNaN(grade) && !isNaN(weight)) {
          totalWeightedGrade += (grade * weight) / 100; // Convert weight to decimal
          totalWeight += weight;
        }
      });
      if (totalWeight > 100) {
        this.errorMessage = "Total weight cannot exceed 100%";
        this.courseGrade = null;
      } else {
        this.courseGrade = ((totalWeightedGrade / totalWeight) * 100).toFixed(2); // Convert to percentage
      }
    },
  }
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>
