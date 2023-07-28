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
                    @change="searchExams"
                    v-model="selectedCourses[index]"
                    :options="filterCourses(index)"
                ></b-form-select>

              </b-form-group>
            </div>


            <b-button @click="$bvModal.show('add-modal-id')" variant="primary">Add Course</b-button>

            <b-modal id="add-modal-id" hide-footer title="Add Course"
                     @close="$bvModal.hide('add-modal-id')"
                     @keydown.esc="$bvModal.hide('add-modal-id')">

              <b-form-group :label="''">
                <b-form-select
                    v-model="currCourse"
                    :options="filterCourses()"
                ></b-form-select>
              </b-form-group>

              <b-button class="mt-3" variant="outline-success" block
                        @click="currCourse ? ($bvModal.hide('add-modal-id'), addCourse(currCourse), searchExams()) : null">
                Confirm
              </b-button>
              <b-button class="mt-3" variant="outline-danger" block @click="$bvModal.hide('add-modal-id')">
                Cancel
              </b-button>

            </b-modal>

            <b-button :disabled="this.selectedCourses.length===0" @click="$bvModal.show('delete-modal-id')"
                      variant="danger"
                      class="ml-3">Delete
            </b-button>
            <b-modal id="delete-modal-id" hide-footer title="Delete Course"
                     @close="$bvModal.hide('delete-modal-id')"
                     @keydown.esc="$bvModal.hide('delete-modal-id')">


              <b-form-group :label="''">
                <b-form-checkbox-group v-model="selectToDelete" v-for="(course, index) in selectedCourses" :key="index">
                  <b-form-checkbox type="radio" :value="course || index">
                    {{ (course ? (course.CourseCode + " - " + course.Section) : 'No Course Selected') }}
                  </b-form-checkbox>
                </b-form-checkbox-group>
              </b-form-group>

              <b-button class="mt-3" variant="outline-success" block
                        @click="$bvModal.hide('delete-modal-id'); deleteCourses()">
                Confirm
              </b-button>
              <b-button class="mt-3" variant="outline-danger" block @click="$bvModal.hide('delete-modal-id')">
                Cancel
              </b-button>

            </b-modal>

          </b-form>
          <b-card v-if="examDetails && this.selectedCourses.length!==0" class="mt-3">
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
                {{ exam.time }}
              </div>
              <div>
                <strong>Date:</strong>
                {{ exam.day }}, {{ exam.dayOfWeek }}
              </div>
              <hr v-if="exam !== examDetails[examDetails.length - 1]"/>
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
import {SelectedCoursesCookie} from "../controllers/SelectedCoursesCookie";
import {FinalsPageCookie} from "@/controllers/FinalsPageCookie";

export default {
  components: {
    Calendar,
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
      currCourse: null,
      selectToDelete: [],
      selectedCourses: [],
      courseOptions: [],
      examDetails: [],
      calendarWeeks: [],
      coursesOnSchedule: []
    };
  },
  mounted() {
    try {
      this.initCourseOptions();
      let finalsPageCookie = FinalsPageCookie.load(this.$cookies);
      console.log(finalsPageCookie.getExams());
      //this.loadSelectedCoursesFromCookie();
    } catch (error) {
      console.error("An error occurred in the mounted() hook:", error);
    }
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

      return {startTime: startDateTime, endTime: endDateTime};
    },

    formatDate(date) {
      const month = date.toLocaleString("default", {month: "short"});
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
      console.log("exams:", this.exams);
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
    addCourse(currCourse) {
      ///const finalsPageCookie = FinalsPageCookie.load(this.$cookies);
      let finalsPageCookie = FinalsPageCookie.load(this.$cookies);

      if (currCourse !== null) {
        this.selectedCourses.push(currCourse);
        console.log("selected courses:", this.selectedCourses);
        // finalsPageCookie.addCourse();

        // let exams = finalsPageCookie.getExams();
        // console.log("exams before push:", exams);

        // exams.push(currCourse);
        // console.log("exams after push:", exams);

        finalsPageCookie.setExams(this.selectedCourses);
        finalsPageCookie.save();
      }
      console.log("cookie:", finalsPageCookie.getExams());
      this.currCourse = null;
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
              const {startTime, endTime} = this.formatExamDateTime(
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
                  const options = {weekday: "long"};
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

      //console.log(this.examDetails);
    },
    deleteCourses() {
      //console.log(this.selectedCourses);
      //console.log(this.selectToDelete);
      for (let i = 0; i < this.selectToDelete.length; i++) {
        let index = this.selectedCourses.indexOf(this.selectToDelete[i]);
        this.selectedCourses.splice(index, 1);
      }

      for (let i = 0; i < this.selectToDelete.length; i++) {
        this.selectToDelete.splice(i, 1);
      }

      this.searchExams();
    },
    filterCourses(index) {
      return this.courseOptions.filter(option => {
        if (index !== undefined) {
          return !this.selectedCourses.includes(option.value) || option.value === this.selectedCourses[index];
        } else {
          return !this.selectedCourses.includes(option.value);
        }
      });
    },
    loadSelectedCoursesFromCookie() {
      this.coursesOnSchedule = SelectedCoursesCookie.load(this.$cookies);

      // for(let i = 0; i< this.coursesOnSchedule.length; i++){
      //   const exam = this.coursesOnSchedule[i].$cookies._selectedSemesters[0];
      //   const key =
      //       exam.Department + " - " + exam.CourseCode + " - " + exam.Section;
      //   if (!groupedCourses[key]) {
      //     groupedCourses[key] = {
      //       value: exam,
      //       text: key,
      //     };
      //   } else if (exam.Section === "ALL SECTIONS") {
      //     groupedCourses[key].value.Room += ", " + exam.Room;
      //   }
      // }

      console.log("courseOptions", this.courseOptions);

      try {
        this.coursesOnSchedule
            .semester(this.selectedSemester)
            .selectedCourses.forEach((selectedCourse) => {
          const course = this.courses.find(
              (course) => course.id === selectedCourse.id
          );

          this.$set(this.selectedCourses, course.id, course);
          course.selected = true;

          selectedCourse.selectedSectionCrns.forEach(
              (selectedSectionCrn) => {
                const section = course.sections.find(
                    (section) => section.crn === selectedSectionCrn
                );

                section.selected = true;
              }
          );
        });
      } catch (err) {
        // If there is an error here, it might mean the data was changed,
        //  thus we need to reload the cookie
        console.log("HIT ERROR IN LOADING COURSES ON SCHEDULE")
      }

      console.log("COURSES ON SCHEDULE", this.coursesOnSchedule);

      console.log("cOnS", Object.values(this.coursesOnSchedule));
      console.log("[1]", Object.values(Object.values(this.coursesOnSchedule)[1]));


      const groupedCourses = Object.values(Object.values(this.coursesOnSchedule)[1]).reduce((acc, exam) => {
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

      console.log("GROUPED COURSES", groupedCourses);
      console.log(typeof groupedCourses);
      this.selectedCourses.concat(Object.values(groupedCourses.value));

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
