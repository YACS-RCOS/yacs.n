<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <b-row class="justify-content-md-center">
      <b-col md="5">
        <b-card title="Final Exam Schedule">
          <b-form @submit.prevent="searchExams">
            <div
              v-for="(course, index) in selectedCourses"
              :key="index"
              class="mb-3"
            >
              <b-form-group :label="'Course ' + (index + 1)">
                <b-form-select
                  v-model="selectedCourses[index]"
                  :options="courseOptions"
                ></b-form-select>
              </b-form-group>
            </div>
            <b-button @click="addCourse" variant="primary">Add Course</b-button>
            <b-button type="submit" variant="success" class="ml-3">
              Search
            </b-button>
          </b-form>
          <b-card v-if="examDetails" class="mt-3">
            <h5 class="card-title">Exam Details</h5>
            <div v-for="exam in examDetails" :key="exam.id">
              <div>
                <strong>Course:</strong>
                {{ exam.course }}
              </div>
              <div>
                <strong>Section:</strong>
                {{ exam.section }}
              </div>
              <div>
                <strong>Room:</strong>
                {{ exam.room }}
              </div>
              <div>
                <strong>Time:</strong>
                {{ convertTime(exam.time) }}
              </div>
              <div>
                <strong>Date:</strong>
                {{ exam.day }}, {{ exam.dayOfWeek }}
              </div>
              <hr v-if="exam !== examDetails[examDetails.length - 1]" />
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
import { mapGetters } from "vuex";

export default {
  components: {
    Calendar,
  },
  name: "FinalExamSchedule",
  computed: {
    ...mapGetters(["militaryTimeState"]),
  },
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

    convertTime(time) {
      const array = time.split("-");
      const start = array[0].split(":");
      const end = array[1].split(":");
      
      // if military time is toggled, don't modify the time
      // if not toggled, modify time so that it's in standard time
      if (this.militaryTimeState){
        if (start[1].substring(start[1].length - 2).valueOf() == ("PM").valueOf() && parseInt(start[0]) != 12){
          start[0] = parseInt(start[0]) + 12;
        }
        else if (start[1].substring(start[1].length - 2).valueOf() == ("AM").valueOf() && parseInt(start[0]) == 12){
          start[0] = "00";
        }
        else if (start[1].substring(start[1].length - 2).valueOf()== ("AM").valueOf() && parseInt(start[0]) < 10){
          start[0] = "0" + start[0];
        }
        if (end[1].substring(end[1].length - 2).valueOf() == ("PM").valueOf() && parseInt(end[0]) != 12){
          end[0] = parseInt(end[0]) + 12;
        }
        else if (end[1].substring(end[1].length - 2).valueOf() == ("AM").valueOf() && parseInt(end[0]) == 12){
          end[0] = "00";
        }
        else if (end[1].substring(end[1].length - 2).valueOf() == ("AM").valueOf() && parseInt(end[0]) < 10){
          end[0] = "0" + end[0];
        }
      }
      
      return start[0] + ":" + start[1] + "-" + end[0] + ":" + end[1];
    },

    formatDate(date) {
      const month = date.toLocaleString("default", { month: "short" });
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
        const key =
          exam.Department + " - " + exam.CourseCode + " - " + exam.Section;
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
      const examDetailsRaw = this.selectedCourses.flatMap((course) => {
        return this.exams
          .filter(
            (exam) =>
              exam.CourseCode === course.CourseCode &&
              exam.Section === course.Section
          )
          .map((exam) => {
            const { startTime, endTime } = this.formatExamDateTime(
              exam.Day,
              exam.Hour
            );
            return {
              id:
                course.Department +
                " " +
                course.CourseCode +
                " " +
                course.Section +
                " " +
                exam.Day,
              course: course.Department + " " + course.CourseCode,
              section: course.Section,
              room: exam.Room,
              time: exam.Hour,
              day: exam.Day,
              dayOfWeek: (() => {
                const dateObj = new Date(exam.Day);
                const dayIndex = (dateObj.getDay() + 6) % 7;
                const options = { weekday: "long" };
                return new Intl.DateTimeFormat("default", options).format(
                  new Date(
                    dateObj.setDate(
                      dateObj.getDate() - dateObj.getDay() + dayIndex
                    )
                  )
                );
              })(),
              time_start: startTime.toISOString(),
              time_end: endTime.toISOString(),
            };
          });
      });

      const examDetailsGrouped = examDetailsRaw.reduce((acc, exam) => {
        if (!acc[exam.id]) {
          acc[exam.id] = exam;
        } else {
          acc[exam.id].room += ", " + exam.room;
        }
        return acc;
      }, {});

      this.examDetails = Object.values(examDetailsGrouped);

      console.log(this.examDetails);
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
