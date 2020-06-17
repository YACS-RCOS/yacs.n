<template>
  <div>
    <Header class="mb-3" :semester="currentSemester"></Header>
    <b-container fluid class="py-3 h-100">
      <b-row class="h-100">
        <b-col md="4" class="d-flex flex-column">
          <b-card no-body class="h-100">
            <b-tabs card class="h-100 d-flex flex-column flex-grow-1">
              <b-tab title="Search" active class="flex-grow-1 w-100">
                <b-card-text class="d-flex flex-grow-1 w-100">
                  <div
                    v-if="loading"
                    class="d-flex flex-grow-1 flex-column w-100 justify-content-center align-items-center"
                  >
                    <b-spinner></b-spinner>

                    <strong>Loading courses...</strong>
                  </div>
                  <CourseList
                    v-if="!loading"
                    @addCourse="addCourse"
                    @removeCourse="removeCourse"
                    @showCourseInfo="showCourseInfo"
                    :courses="courses"
                    :subsemesters="subsemesters"
                    class="w-100"
                    :selectedSemester="currentSemester"
                  />
                </b-card-text>
              </b-tab>
              <b-tab title="Explore" class="flex-grow-1 w-100">

              </b-tab>
              <b-tab class="flex-grow-1">
                <template v-slot:title>
                  <div class="text-center">
                    Selected
                    <b-badge variant="light">{{ numSelectedCourses }}</b-badge>
                  </div>
                </template>
                <b-card-text class="w-100 d-flex flex-grow-1 flex-column">
                  <SelectedCourses
                    :courses="selectedCourses"
                    @removeCourse="removeCourse"
                    @removeCourseSection="removeCourseSection"
                    @addCourseSection="addCourseSection"
                  />
                </b-card-text>
              </b-tab>
            </b-tabs>
          </b-card>
        </b-col>
        <b-col md="8">
          <b-form-select
            v-if="
              !loading &&
              scheduler.scheduleSubsemesters &&
              scheduler.scheduleSubsemesters.length > 1
            "
            v-model="selectedScheduleSubsemester"
            :options="scheduler.scheduleSubsemesters"
            text-field="display_string"
            value-field="display_string"
          ></b-form-select>

          <template v-if="scheduler.schedules">
            <Schedule
              v-for="(schedule, index) in scheduler.schedules"
              :key="index"
              :schedule="schedule"
              v-show="selectedScheduleIndex === index"
            />
          </template>
          <Schedule v-else :schedule="scheduler"></Schedule>

          <b-row>
            <b-col>
              <h5>CRNs: {{ selectedCrns }}</h5>
            </b-col>

            <b-col md="4">
              <button
                id="export-ics-button"
                class="col-auto btn-sm btn btn-primary ml-auto mb-2 mr-5 mt-1 d-block"
                @click="exportScheduleToIcs"
              >
                <font-awesome-icon :icon="exportIcon" />
                Export to ICS
              </button>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
    <Footer
      :semester="currentSemester"
      @changeCurrentSemester="updateCurrentSemester"
    />
    <b-modal
      id="courseInfoModal"
      v-if="courseInfoModalCourse"
      v-model="showCourseInfoModal"
      :title="courseInfoModalCourse.name + ' ' + courseInfoModalCourse.title"
      hide-footer
    >
      <span v-if="courseInfoModalCourse.frequency">
        Offered: {{ courseInfoModalCourse.frequency }}
        <br />
        <br />
      </span>
      <span>
        {{
          generateRequirementsText(
            courseInfoModalCourse.prerequisites,
            courseInfoModalCourse.corequisites,
            courseInfoModalCourse.raw_precoreqs
          )
        }}
      </span>
      <span v-if="courseInfoModalCourse.description">
        <br />
        <br />
        {{ courseInfoModalCourse.description }}
      </span>
      <br />
      <br />
      <b-button
        variant="primary"
        @click="
          toggleCourse(courseInfoModalCourse);
          showCourseInfoModal = !showCourseInfoModal;
        "
      >
        {{
          courseInfoModalCourse.selected
            ? "Remove from schedule"
            : "Add to schedule"
        }}
      </b-button>
      <b-button
        class="ml-2"
        variant="danger"
        @click="showCourseInfoModal = !showCourseInfoModal"
      >
        Close
      </b-button>
    </b-modal>
  </div>
</template>

<script>
import NotificationsMixin from "@/mixins/NotificationsMixin";

import ScheduleComponent from "@/components/Schedule";
import SelectedCoursesComponent from "@/components/SelectedCourses";
import CourseListComponent from "@/components/CourseList";
import Footer from "@/components/Footer";

import Schedule from "@/controllers/Schedule";
import SubSemesterScheduler from "@/controllers/SubSemesterScheduler";

import HeaderComponent from "@/components/Header";

import {
  getSubSemesters,
  getCourses,
  addStudentCourse,
  removeStudentCourse,
  getStudentCourses,
} from "@/services/YacsService";

import { getDefaultSemester } from "@/services/AdminService";

import { partition } from "@/utils";

import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";

import moment from "moment";

export default {
  name: "MainPage",
  mixins: [NotificationsMixin],
  components: {
    Schedule: ScheduleComponent,
    SelectedCourses: SelectedCoursesComponent,
    CourseList: CourseListComponent,
    Header: HeaderComponent,
    Footer: Footer,
  },
  data() {
    return {
      selectedCourses: {},
      selectedScheduleSubsemester: null,
      scheduler: new Schedule(),
      subsemesters: [],
      currentSemester: "",
      courses: [],
      loading: false,
      exportIcon: faPaperPlane,
      ICS_DAY_SHORTNAMES: ["MO", "TU", "WE", "TH", "FR", "SA", "SU"],
      courseInfoModalCourse: null,
      showCourseInfoModal: false,
    };
  },
  async created() {
    const querySemester = this.$route.query.semester;
    this.updateCurrentSemester(
      querySemester && querySemester != "null"
        ? querySemester
        : await getDefaultSemester()
    );
  },
  methods: {
    async loadStudentCourses(semester) {
      this.selectedCourses = {};
      this.userID = this.$cookies.get("userID");

      if (this.userID && semester) {
        console.log("Loading user courses...");
        try {
          const info = { uid: this.userID };
          var cids = await getStudentCourses(info);
          console.log(cids);

          cids.forEach((cid) => {
            if (cid.semester == this.currentSemester) {
              var c = this.courses.find(function (course) {
                return (
                  course.name == cid.course_name &&
                  course.semester == cid.semester
                );
              });

              if (cid.crn != "-1") {
                var sect = c.sections.find(function (section) {
                  return section.crn == cid.crn;
                });
                sect.selected = true;
                this.scheduler.addCourseSection(c, sect);
              } else {
                c.selected = true;
                this.$set(this.selectedCourses, c.id, c);
                this.scheduler.addCourse(c);
              }
            }
          });
        } catch (error) {
          console.log(error);
        }
      }
    },
    updateDataOnNewSemester() {
      return Promise.all([
        getCourses(this.currentSemester),
        getSubSemesters(this.currentSemester),
      ]).then(([courses, subsemesters]) => {
        this.courses = courses;
        this.subsemesters = subsemesters;
        // Less work to create a new scheduler which is meant for a single semester
        this.scheduler = new SubSemesterScheduler();
        // Filter out "full" subsemester
        subsemesters
          .filter(
            (s, i, arr) =>
              arr.length == 1 ||
              !arr.every((o, oi) => oi == i || this.withinDuration(s, o))
          )
          .forEach((subsemester) => {
            this.scheduler.addSubSemester(subsemester);
          });

        if (this.scheduler.scheduleSubsemesters.length > 0) {
          this.selectedScheduleSubsemester = this.scheduler.scheduleSubsemesters[0].display_string;
        }
      });
    },
    addCourse(course) {
      course.selected = true;
      // This must be vm.set since we're adding a property onto an object
      this.$set(this.selectedCourses, course.id, course);
      this.scheduler.addCourse(course);

      let i = 0;
      for (; i < course.sections.length; i++) {
        try {
          this._addCourseSection(course, course.sections[i]);
          break;
        } catch (err) {
          if (err.type == "Schedule Conflict") {
            if (i == course.sections.length - 1) {
              this.notifyScheduleConflict(
                course,
                err.existingSession,
                err.subsemester
              );
            } else {
              continue;
            }
          } else {
            throw err;
          }
        }
      }

      if (this.userID) {
        const info = {
          name: course.name,
          semester: this.currentSemester,
          uid: this.userID,
          cid: "-1",
        };

        addStudentCourse(info)
          .then((response) => {
            console.log(`Saved ${course.name}`);
            console.log(response);
          })
          .catch((error) => {
            console.log(error.response);
          });
      }
    },

    _addCourseSection(course, section) {
      this.scheduler.addCourseSection(course, section);
      section.selected = true;

      if (this.userID) {
        const info = {
          name: course.name,
          semester: this.currentSemester,
          uid: this.userID,
          cid: section.crn,
        };

        addStudentCourse(info)
          .then((response) => {
            console.log(`Saved section ${section.crn}`);
            console.log(response);
          })
          .catch((error) => {
            console.log(error.response);
          });
      }
    },

    addCourseSection(course, section) {
      try {
        this._addCourseSection(course, section);
      } catch (err) {
        if (err.type === "Schedule Conflict") {
          this.notifyScheduleConflict(
            course,
            err.existingSession,
            err.subsemester
          );
        }
      }
    },
    removeCourse(course) {
      this.$delete(this.selectedCourses, course.id);
      course.selected = false;
      this.scheduler.removeAllCourseSections(course);

      if (this.userID) {
        const info = {
          name: course.name,
          semester: this.currentSemester,
          uid: this.userID,
          cid: null,
        };

        removeStudentCourse(info)
          .then((response) => {
            console.log(`Unsaved ${course.name}`);
            console.log(response);
          })
          .catch((error) => {
            console.log(error.response);
          });
      }
    },
    removeCourseSection(section) {
      this.scheduler.removeCourseSection(section);
      if (this.userID) {
        var name = section.department + "-" + section.level;
        const info = {
          name: name,
          semester: this.currentSemester,
          uid: this.userID,
          cid: section.crn,
        };

        removeStudentCourse(info)
          .then((response) => {
            console.log(`Unsaved section ${section.crn}!`);
            console.log(response);
          })
          .catch((error) => {
            console.log(error.response);
          });
      }
    },
    async updateCurrentSemester(sem) {
      this.loading = true;
      this.currentSemester = sem;
      history.pushState(
        null,
        "",
        encodeURI(`/?semester=${this.currentSemester}`)
      );
      await this.updateDataOnNewSemester();
      await this.loadStudentCourses(this.currentSemester);
      this.loading = false;
    },
    addDays(date, days) {
      var result = new Date(date);
      result.setDate(result.getDate() + days);
      return result;
    },
    sortSessionsByDate(session1, session2) {
      let d1_s = new Date(`Sat Apr 25 2020 ${session1.time_start}`);
      let d2_s = new Date(`Sat Apr 25 2020 ${session2.time_start}`);
      let d1_e = new Date(`Sat Apr 25 2020 ${session1.time_end}`);
      let d2_e = new Date(`Sat Apr 25 2020 ${session2.time_end}`);
      if (
        d1_s.getTime() === d2_s.getTime() &&
        d1_e.getTime() === d2_e.getTime()
      ) {
        return 0;
      } else if (d1_s < d2_s) {
        return -1;
      }
      return 1;
    },
    getClosestDay(fromDay, sessions) {
      if (sessions.length) {
        sessions.sort((session1, session2) => {
          // In DB, days are numbered MON 0 - FRI 4
          // In JS, days are numbered SUN 0 - SAT 6
          // Course start date will be on a week day, JS Date, Mon 1 - Fri 5
          // Shift the JS date range back by 1
          if (
            Math.abs(fromDay - 1 - session1.day_of_week) <
            Math.abs(fromDay - 1 - session2.day_of_week)
          ) {
            return -1;
          } else if (
            Math.abs(fromDay - 1 - session1.day_of_week) >
            Math.abs(fromDay - 1 - session2.day_of_week)
          ) {
            return 1;
          }
          return 0;
        });
        return sessions[0].day_of_week;
      }
      return -1;
    },
    /**
     * Export all selected course sections to ICS
     */
    exportScheduleToIcs() {
      let calendarBuilder = window.ics();
      let semester;
      for (const course of Object.values(this.courses)) {
        for (const section of course.sections.filter((s) => s.selected)) {
          const sessionsPartitionedByStartAndEnd = partition(
            section.sessions,
            this.sortSessionsByDate
          );
          for (const sessionGroupOfSameMeetTime of sessionsPartitionedByStartAndEnd) {
            const days = sessionGroupOfSameMeetTime.map(
              (sess) => this.ICS_DAY_SHORTNAMES[sess.day_of_week]
            );
            // Gets closest day to the course start date
            const firstDay = this.getClosestDay(
              course.date_start.getDay(),
              sessionGroupOfSameMeetTime
            );
            const session = sessionGroupOfSameMeetTime[0];
            // The dates from the DB have no timezone, so when they are
            // cast to a JS date they're by default at time midnight 00:00:00.
            // This will exclude all classes if they're on that final day, so bump
            // the end date by 1 day.
            let exclusive_date_end = new Date(course.date_end);
            exclusive_date_end.setDate(course.date_end.getDate() + 1);
            // Moment numbers days from 0 SUN - 6 MON - 7 NEXT SUNDAY
            // firstDay is numbered     0 MON - 4 FRI, so need to add 1 to match moment's spec
            let dtStart = moment(course.date_start)
              .day(firstDay + 1)
              .toDate();
            if (dtStart < course.date_start) {
              // Go to NEXT week, uses the current week by default
              dtStart = moment(course.date_start)
                .day(firstDay + 1 + 7)
                .toDate();
            }
            semester = section.semester;
            // https://github.com/nwcell/ics.js/blob/master/ics.js#L50
            calendarBuilder.addEvent(
              `${course.full_title || course.title}`,
              `${course.department}-${course.level} ${session.section}, CRN: ${session.crn}  [from YACS]`, // Add professor and type of class (LEC || LAB) to this description arg when data is available
              "", // session.location,
              new Date(`${dtStart.toDateString()} ${session.time_start}`),
              new Date(`${dtStart.toDateString()} ${session.time_end}`),
              {
                freq: "WEEKLY",
                interval: 1,
                until: exclusive_date_end,
                byday: days,
              }
            );
          }
        }
      }
      calendarBuilder.download(
        `${semester.replace(/^(\w)(\w*?)\s?(\d+)/, function (
          _,
          semFirstLetter,
          semRest,
          year
        ) {
          return semFirstLetter.toUpperCase() + semRest.toLowerCase() + year;
        })}_Schedule`
      );
    },
    /**
     * Checks whether `s1` spans the entire duration of `s2`
     * @param {Subsemester} s1
     * @param {Subsemester} s2
     * @returns {boolean}
     */
    withinDuration(s1, s2) {
      return (
        s1.date_start.getTime() <= s2.date_start.getTime() &&
        s1.date_end.getTime() >= s2.date_end.getTime()
      );
    },
    /**
     * @param {Course} course
     */
    showCourseInfo(course) {
      this.courseInfoModalCourse = course;
      this.showCourseInfoModal = true;
    },
    generateRequirementsText(prereqs, coreqs, raw) {
      let text = [];
      if (prereqs || coreqs) {
        const same = JSON.stringify(prereqs) == JSON.stringify(coreqs);

        text.push("Requires");

        if (prereqs) {
          text.push("completion of");

          if (!same) text.push(prereqs.join(", "));
        }

        if (prereqs && coreqs) text.push(same ? "or" : "and");

        if (coreqs) {
          text.push("concurrent enrollment in");

          text.push(coreqs.join(", "));
        }
      } else {
        text.push("Requirements:", raw);
      }

      return text.join(" ");
    },
    /**
     * Toggle course selected state
     * Emits removeCourse and addCourse events
     */
    toggleCourse(course) {
      if (course.selected) {
        this.removeCourse(course);
      } else {
        this.addCourse(course);
      }
    },
  },
  computed: {
    selectedScheduleIndex() {
      return this.scheduler.scheduleSubsemesters.findIndex(
        (s) => s.display_string === this.selectedScheduleSubsemester
      );
    },
    /**
     * Returns list of CRNs for all selected sections
     * @returns {string[]}
     */
    selectedCrns() {
      return Object.values(this.selectedCourses)
        .map((c) => c.sections.filter((s) => s.selected))
        .flat()
        .map((s) => s.crn)
        .join(", ");
    },
    numSelectedCourses() {
      return Object.values(this.selectedCourses).length;
    },
  },
};
</script>

<style lang="scss">
// NOTE!
// for every v-tab a div.tab-content container is generated
// I can't find access to the div so the workaround is to
// apply the css attributes globally to .tab-content
// This means that all v-tabs in this app will have flexbox content
// Hopefully this doesn't screw up someone's debugging later lol
.tab-content {
  display: flex;
  flex-grow: 1;
}
// This makes it so active tabs are display:flex
// The default is display:block
.tab-content > .active {
  display: flex;
}

.card {
  border: none !important;

  a:visited {
    color: black;
  }

  .card-header {
    background: white !important;
  }
}

footer {
  margin: 0px !important;
}

#export-ics-button {
  background: #3d4959 !important;
}
</style>
