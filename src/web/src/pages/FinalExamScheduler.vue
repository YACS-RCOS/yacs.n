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
        </b-card>
      </b-col>
      <b-col md="7">
        <b-card>
          <b-calendar
            v-model="selectedDate"
            @context="onContext"
            locale="en-US"
            :events="calendarEvents"
            event-color="success"
            event-variant="light"
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
      const currentYear = new Date().getFullYear();
      this.selectedDate.setFullYear(currentYear);
    },
    addCourse() {
      this.selectedCourses.push(null);
    },
    searchExams() {
      this.calendarEvents = this.selectedCourses.flatMap((course) => {
        return this.exams
          .filter((exam) => exam.CourseCode === course)
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
    },
    onContext(ctx) {
      const date = new Date(ctx.date);
      const examsOnDate = this.calendarEvents.filter((event) => {
        const eventDate = new Date(event.date);
        return (
          eventDate.getDate() === date.getDate() &&
          eventDate.getMonth() === date.getMonth() &&
          eventDate.getFullYear() === date.getFullYear()
        );
      });

      if (examsOnDate.length > 0) {
        this.$bvModal.msgBoxOk(
          examsOnDate
            .map(
              (exam) =>
                `<strong>Course:</strong> ${exam.title.split(" ")[0]} ${
                  exam.title.split(" ")[1]
                }<br>
                <strong>Section:</strong> ${exam.title.split(" ")[2]}<br>
                <strong>Room:</strong> ${exam.title.split(" ")[3]}<br>
                <strong>Time:</strong> ${exam.title.split(" ")[4]} ${
                  exam.title.split(" ")[5]
                }`
            )
            .join("<hr>"),
          {
            title: "Exam Details",
            size: "md",
            buttonSize: "md",
            okVariant: "success",
            headerClass: "p-2 border-bottom-0",
            footerClass: "p-2 border-top-0",
            centered: true,
            html: true,
          }
        );
      }
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
</style>