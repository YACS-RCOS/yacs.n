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
        <b-table-simple hover bordered class="calendar-table">
          <b-thead head-variant="dark">
            <b-tr>
              <b-th>Monday</b-th>
              <b-th>Tuesday</b-th>
              <b-th>Wednesday</b-th>
              <b-th>Thursday</b-th>
              <b-th>Friday</b-th>
            </b-tr>
          </b-thead>
          <b-tbody>
            <b-tr v-for="(week, weekIndex) in calendarWeeks" :key="'week-' + weekIndex">
              <b-td v-for="(day, dayIndex) in week.days" :key="'day-' + weekIndex + '-' + dayIndex">
                <div class="text-left">
                  <strong>{{ formatDate(day.date) }}</strong>
                </div>
                <div v-if="day.exams.length">
                  <ul>
                    <li v-for="exam in day.exams" :key="exam.id">
                      {{ exam.course }} <br> {{ exam.time }}
                    </li>
                  </ul>
                </div>
              </b-td>
            </b-tr>
          </b-tbody>
        </b-table-simple>
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
      selectedCourses: [null],
      courseOptions: [],
      examDetails: [],
    };
  },
  mounted() {
    this.initCourseOptions();
  },
  computed: {
    calendarWeeks() {
      const startDate = new Date(2023, 3, 24); // April 24, 2023
      const endDate = new Date(2023, 4, 5); // May 5, 2023
      const weeks = [];

      for (let currentDate = startDate; currentDate <= endDate;) {
        const week = { days: [] };

        for (let i = 0; i < 5; i++) {
          week.days.push({
            date: new Date(currentDate),
            exams: this.getExamsForDate(currentDate),
          });

          currentDate.setDate(currentDate.getDate() + 1);

          if (currentDate > endDate) {
            break;
          }
        }

        weeks.push(week);

        if (currentDate.getDay() === 6) {
          currentDate.setDate(currentDate.getDate() + 2);
        }
      }

      return weeks;
    },
  },

  methods: {
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
          .map((exam) => ({
            course: course.Department + " " + course.CourseCode,
            section: course.Section,
            room: exam.Room,
            time: exam.Hour,
            day: exam.Day,
            dayOfWeek: new Date(exam.Day).toLocaleString('default', { weekday: 'long' })
          }));
      });
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
