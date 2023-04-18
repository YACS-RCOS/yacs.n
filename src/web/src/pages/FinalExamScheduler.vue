<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <b-row>
      <b-col md="4">
        <b-card title="Final Exam Schedule">
          <b-form @submit.prevent="searchExam">
            <b-form-group label="Select a Course">
              <b-form-select v-model="selectedCourse" :options="courseOptions"></b-form-select>
            </b-form-group>
            <b-button type="submit" variant="success">Search</b-button>
          </b-form>
        </b-card>
      </b-col>
      <b-col md="8">
        <b-card>
          <b-calendar v-model="selectedDate" @context="onContext" locale="en-US"></b-calendar>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import Finals from "./Finals.json";

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
      exams: Finals,
      selectedDate: new Date(),
      selectedCourse: null,
      courseOptions: [],
    };
  },
  mounted() {
    this.initCourseOptions();
    this.initCalendar();
  },
  methods: {
    initCourseOptions() {
      this.courseOptions = this.exams.map((exam) => ({
        value: exam.CourseCode,
        text: exam.Department + " - " + exam.CourseCode,
      }));
    },
    initCalendar() {
      const firstExamDate = new Date(this.exams[0].Day);
      this.selectedDate = firstExamDate;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },
    searchExam() {
      this.selectedDate = new Date(
        this.exams.find((exam) => exam.CourseCode === this.selectedCourse).Day
      );
    },
    onContext(ctx) {
      const date = new Date(ctx.date);
      const examsOnDate = this.exams.filter((exam) => {
        const examDate = new Date(exam.Day);
        return (
          examDate.getDate() === date.getDate() &&
          examDate.getMonth() === date.getMonth() &&
          examDate.getFullYear() === date.getFullYear()
        );
      });

      if (examsOnDate.length > 0) {
        let examsList = "Exams on " + ctx.label + ":\n";
        examsOnDate.forEach((exam) => {
          examsList +=
            exam.Department +
            " " +
            exam.CourseCode +
            " " +
            exam.Section +
            " " +
            exam.Room +
            " " +
            exam.Hour +
            "\n";
        });
        alert(examsList);
      }
    },
  },
};
</script>
