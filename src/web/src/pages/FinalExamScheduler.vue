<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <b-row class="justify-content-md-center">
      <b-col md="8">
        <b-card title="Final Exam Schedule">
          <b-form @submit.prevent="generateFinalExamSchedule">
            <b-form-group label="Term">
              <b-form-select v-model="selectedTerm" :options="terms"></b-form-select>
            </b-form-group>
            <b-form-group label="Classes">
              <div v-for="(classInfo, index) in classes" :key="index" class="mb-3">
                <b-form-input-group>
                  <b-form-input
                    v-model="classInfo.dept"
                    placeholder="Department"
                    required
                  ></b-form-input>
                  <b-form-input
                    v-model="classInfo.courseNumber"
                    placeholder="Course #"
                    required
                  ></b-form-input>
                  <b-form-input
                    v-model="classInfo.section"
                    placeholder="Section"
                    required
                  ></b-form-input>
                  <b-input-group-append>
                    <b-button @click="removeClass(index)" variant="danger">Remove</b-button>
                  </b-input-group-append>
                </b-form-input-group>
              </div>
              <b-button @click="addClass" variant="primary">Add Class</b-button>
            </b-form-group>
            <b-button type="submit" variant="success">Generate Schedule</b-button>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: "FinalExamSchedule",
  data() {
    return {
      breadcrumbNav: [
        {
          text: "YACS",
          to: "/",
        },
        {
          text: "Final Exam Schedule",
        },
      ],
      selectedTerm: "",
      terms: ["Spring 2023", "Fall 2023", "Spring 2024"],
      classes: [
        {
          dept: "",
          courseNumber: "",
          section: "",
        },
      ],
    };
  },
  methods: {
    addClass() {
      this.classes.push({
        dept: "",
        courseNumber: "",
        section: "",
      });
    },
    removeClass(index) {
      this.classes.splice(index, 1);
    },
    generateFinalExamSchedule() {

    },
  },
};
</script>

<style>
.pathway-button {
  display: inline-block;
  background: white;
  border-style: none;
  text-align: justify;
  width: 95%;
}

.pathway-button:hover {
  background: rgba(108, 90, 90, 0.15) !important;
}
</style>