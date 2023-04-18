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
              <hr v-if="exam !== examDetails[examDetails.length - 1]">
            </div>
          </b-card>
        </b-card>
      </b-col>
      <b-col md="7">
        <b-card>
          <b-calendar
            v-model="selectedDate"
            locale="en-US"
            :events="calendarEvents"
            event-color="success"
            event-variant="light"
            class="custom-calendar"
          >
            <template #day-content="{ date, events }">
              <div class="day-content">
                <div>{{ date.getDate() }}</div>
                <div class="day-events">
                  <span
                    v-for="event in events"
                    :key="event.id"
                    class="event"
                  >
                    {{ event.title.split(" ")[0] }} {{ event.title.split(" ")[1] }}
                  </span>
                </div>
              </div>
            </template>
          </b-calendar>
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
      selectedCourses: [null],
      courseOptions: [],
      calendarEvents: [],
      examDetails: null,
    };
  },
  mounted() {
    this.initCourseOptions();
    this.initCalendar();
  },
  methods: {
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
    initCalendar() {
      const currentYear = new Date().getFullYear();
      this.selectedDate.setFullYear(currentYear);
    },
    addCourse() {
      this.selectedCourses.push(null);
    },
    searchExams() {
      this.calendarEvents = this.selectedCourses.flatMap((course) => {
        return this.exams
          .filter((exam) => exam.CourseCode === course.CourseCode && exam.Section === course.Section)
          .map((exam) => ({
            date: new Date(exam.Day),
            title:
              exam.Department +
              " " +
              exam.CourseCode +
              " " +
              exam.Section +
              " " +
              exam.Room +
              " " +
              exam.Hour,
          }));
      });

      this.examDetails = this.selectedCourses.map((course) => ({
        course: course.Department + " " + course.CourseCode,
        section: course.Section,
        room: course.Room,
        time: course.Hour,
      }));
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

.day-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
}

.day-events {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 0.8rem;
}

.event {
  margin-top: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.custom-calendar .b-calendar-grid .row-cell {
  height: 120px;
}

.custom-calendar .b-calendar-grid .row-cell button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.custom-calendar .b-calendar-grid .row-cell button small {
  font-size: 0.8rem;
  margin-top: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
