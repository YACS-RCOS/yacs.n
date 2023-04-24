<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <b-row class="justify-content-md-center">
      <b-col md="5">
        <b-card title="Final Exam Schedule">
          <b-form @submit.prevent="searchExams">
            <div v-for="(course, index) in selectedCourses" :key="index" class="mb-3">
              <b-form-group :label="'Course ' + (index + 1)">
                <b-form-select v-model="selectedCourses[index]" :options="courseOptions"></b-form-select>
              </b-form-group>
            </div>
            <b-button @click="addCourse" variant="primary">Add Course</b-button>
            <b-button type="submit" variant="success" class="ml-3">Search</b-button>
          </b-form>
          <b-card v-if="examDetails" class="mt-3">
            <h5 class="card-title">Exam Details</h5>
            <div v-for="exam in examDetails" :key="exam.id">
              <div><strong>Course:</strong> {{ exam.course }}</div>
              <div><strong>Section:</strong> {{ exam.section }}</div>
              <div><strong>Room:</strong> {{ exam.room }}</div>
              <div><strong>Time:</strong> {{ exam.time }}</div>
              <div><strong>Date:</strong> {{ exam.day }}, {{ exam.dayOfWeek }}</div>
              <hr v-if="exam !== examDetails[examDetails.length - 1]">
            </div>
          </b-card>
        </b-card>
      </b-col>
      <b-col md="7">
        <calendar :exam-details="examDetails"></calendar>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import Finals from "./Finals.json";
import Calendar from "./Calendar.vue";

export default {
  components: {
    Calendar,
  },
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
      selectedCourses: [null],
      courseOptions: [],
      examDetails: [],
      calendarWeeks: [],
    };
  },
  mounted() {
    this.initCourseOptions();
  },
  methods: {
    formatExamDateTime(day, time) {
      const [start, end] = time.split("-");
      const startDateTime = new Date(day);
      const endDateTime = new Date(day);
      const [startHour, startMinutes] = start.split(":");
      const [endHour, endMinutes] = end.split(":");

      startDateTime.setHours(parseInt(startHour));
      startDateTime.setMinutes(parseInt(startMinutes));
      endDateTime.setHours(parseInt(endHour));
      endDateTime.setMinutes(parseInt(endMinutes));

      return { startTime: startDateTime, endTime: endDateTime };
    },

    formatDate(date) {
      const month = date.toLocaleString('default', { month: 'short' });
      const day = date.getDate();
      return `${month} ${day}`;
    },

    getExamsForDate(date) {
      return this.examDetails.filter((exam) => {
                const examDate = new Date(exam.day);
        return examDate.toDateString() === date.toDateString();
      });
    },
    initCourseOptions() {
      const groupedCourses = this.exams.reduce((acc, exam) => {
        const key = exam.Department + " - " + exam.CourseCode + " - " + exam.Section;
        if (!acc[key]) {
          acc[key] = {
            value: exam,
            text: key,
          };
        } else if (exam.Section === "ALL SECTIONS") {
          acc[key].value.Room += ", " + exam.Room;
        }
        return acc;
      }, {});

      this.courseOptions = Object.values(groupedCourses);
    },
    addCourse() {
      this.selectedCourses.push(null);
    },
    searchExams() {
      this.examDetails = this.selectedCourses.flatMap((course) => {
        return this.exams
          .filter((exam) => exam.CourseCode === course.CourseCode && exam.Section === course.Section)
          .map((exam) => {
            const { startTime, endTime } = this.formatExamDateTime(exam.Day, exam.Hour);
            return {
              course: course.Department + " " + course.CourseCode,
              section: course.Section,
              room: exam.Room,
              time: exam.Hour,
              day: exam.Day,
              dayOfWeek: new Date(exam.Day).toLocaleString('default', { weekday: 'long' }),
              time_start: startTime.toISOString(),
              time_end: endTime.toISOString(),
            };
          });
      });


      console.log(this.examDetails); // print examDetails to the console
      
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

.text-left {
  position: absolute;
  top: 0;
  left: 0;
}
  
.calendar-table {
  width: 100%;
}
  
.calendar-table th,
.calendar-table td {
  width: 20%;
  position: relative;
}
</style>
