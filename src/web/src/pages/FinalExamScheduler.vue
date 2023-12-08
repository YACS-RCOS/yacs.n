<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <b-row class="justify-content-md-center">
      <b-col md="5">
        <b-card title="Final Exam Schedule">
          <b-form @submit.prevent="searchExams">
            
            <template>
              <!-- COURSES CURRENTLY SELECTED AND DISPLAYED -->
              <div v-for="(course, index) in selectedCourses" :key="index" class="mb-3">
                <div class="d-flex align-items-center">
                  <b-form-group :label="'Course ' + (index + 1)" class="flex-grow-1">
                    <b-form-select @change="searchExams" v-model="selectedCourses[index]" :options="filterCourses(index)"></b-form-select>
                  </b-form-group>
                  <b-button @click="deleteCourse(index)" variant="danger" class="delete-button ml-2 mt-3">X</b-button>
                </div>
              </div>
            </template>

            <template>
              <div class = "button-container">
                
                <!-- ADD COURSE BUTTON FOR ADDING NEW COURSE -->
                <b-button @click="$bvModal.show('add-modal-id')" variant="primary" class = "mt-3">Add Course</b-button>

                <b-modal id="add-modal-id" hide-footer title="Add Course"
                        @close="$bvModal.hide('add-modal-id')"
                        @keydown.esc="$bvModal.hide('add-modal-id')">

                  <b-form-group :label="''">
                    <b-form-select
                        v-model="currCourse"
                        :options="filterCourses()"
                    ></b-form-select>
                  </b-form-group>
                  
                  <!-- CONFIRM / CANCEL BUTTONS WITHIN ADD CLASS -->
                  <b-button class="mt-3" variant="success" block
                            @click="currCourse ? ($bvModal.hide('add-modal-id'), addCourse(currCourse), searchExams()) : null">
                    Confirm
                  </b-button>
                  <b-button class="mt-3" variant="danger" block @click="$bvModal.hide('add-modal-id')">
                    Cancel
                  </b-button>

                </b-modal>
                <!-- Remove All Classes Button -->
                <b-button v-if="this.selectedCourses.length > 1" @click="deleteAllCourses()" variant="danger" class="mt-3">
                  Remove All Courses 
                </b-button>

              </div>
            </template>
          </b-form>

          <!-- EXAM DETAILS CARD -->
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

        <b-col md="7">
          <div class="mt-3">
            <b-button variant="secondary" class = "button-color" @mouseover = "hoverButton"  @click="goToSchoolWebsite">Go to School Website</b-button>
          </div>
        </b-col>
        
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
      currCourse: null,
      selectToDelete: [],
      selectedCourses: [],
      courseOptions: [],
      examDetails: [],
      calendarWeeks: [],
      coursesOnSchedule: [],
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
      if (currCourse !== null) {
        this.selectedCourses.push(currCourse);
      }
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

    },

    deleteCourse(index) {
      // Remove the course from selectedCourses using the removeCourse method
      this.selectedCourses.splice(index, 1);
      this.searchExams();
    },

    deleteAllCourses() {
      // Remove all Courses by resetting the array of selected courses.
      this.selectedCourses = [];
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

    goToSchoolWebsite() {
      window.open('https://info.rpi.edu/registrar/grades',  '_blank');
    },
  },
};
</script>

<style>

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

.button-container {
  display: flex;
  gap: 20px;
}

.button-color {
  color:white;
}

.button-color:hover {
  color: black;

}

</style>
