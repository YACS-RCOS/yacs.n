<template>
  <b-container fluid class="py-3 h-100">
    <b-row class="h-100">
      <b-col md="4" class="d-flex flex-column">
        <b-card no-body class="h-100">
          <b-tabs card class="h-100 d-flex flex-column flex-grow-1">
            <b-tab
              title="Course Search"
              active
              class="flex-grow-1 w-100"
              data-cy="course-search-tab"
            >
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
                  :selectedSemester="selectedSemester"
                />
              </b-card-text>
            </b-tab>
            <b-tab class="flex-grow-1" data-cy="selected-courses-tab">
              <template v-slot:title>
                <div class="text-center" data-cy="selected-courses-tab-header">
                  Selected Courses
                  <b-badge variant="light" data-cy="num-selected-courses">
                    {{ numSelectedCourses }}
                  </b-badge>
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
    <!-- NOTE: Content Class Specifies The Styling For Modal In Dark Mode. -->
    <b-modal
      id="courseInfoModal"
      v-if="courseInfoModalCourse"
      v-model="showCourseInfoModal"
      :title="courseInfoModalCourse.name + ' ' + courseInfoModalCourse.title"
      content-class= "`${$store.state.darkMode}` ? onStyleDarkMode : offStyleDarkMode"
      hide-footer
      data-cy="course-info-modal"
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
  </b-container>
</template>

<script>
import NotificationsMixin from "@/mixins/NotificationsMixin";
import ScheduleComponent from "@/components/Schedule";
import SelectedCoursesComponent from "@/components/SelectedCourses";
import CourseListComponent from "@/components/CourseList";

import Schedule from "@/controllers/Schedule";
import SubSemesterScheduler from "@/controllers/SubSemesterScheduler";

import {
  getSubSemesters,
  getCourses,
  addStudentCourse,
  removeStudentCourse,
  getStudentCourses,
} from "@/services/YacsService";

import {
  withinDuration,
  generateRequirementsText,
  findCourseByCourseSessionCRN,
  exportScheduleToIcs,
} from "@/utils";

import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";

export default {
  name: "MainPage",
  mixins: [NotificationsMixin],
  components: {
    Schedule: ScheduleComponent,
    SelectedCourses: SelectedCoursesComponent,
    CourseList: CourseListComponent,
  },
  props: {
    selectedSemester: String,
  },
  data() {
    return {
      selectedCourses: {},
      selectedScheduleSubsemester: null,
      scheduler: new Schedule(),
      subsemesters: [],
      courses: [],
      loading: false,
      exportIcon: faPaperPlane,

      courseInfoModalCourse: null,
      showCourseInfoModal: false,
    };
  },
  methods: {
    generateRequirementsText,
    exportScheduleToIcs() {
      exportScheduleToIcs(Object.values(this.selectedCourses));
    },
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
            if (cid.semester == this.selectedSemester) {
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
        getCourses(this.selectedSemester),
        getSubSemesters(this.selectedSemester),
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
              !arr.every((o, oi) => oi == i || withinDuration(s, o))
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
                findCourseByCourseSessionCRN(
                  this.courses,
                  err.existingSession.crn
                ),
                err.addingSession,
                err.existingSession
              );
              return;
            } else {
              continue;
            }
          } else {
            throw err;
          }
        }
      }

      course.selected = true;
      // This must be vm.set since we're adding a property onto an object
      this.$set(this.selectedCourses, course.id, course);
      this.scheduler.addCourse(course);

      if (this.userID) {
        const info = {
          name: course.name,
          semester: this.selectedSemester,
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
          semester: this.selectedSemester,
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
            findCourseByCourseSessionCRN(this.courses, err.existingSession.crn),
            err.addingSession,
            err.existingSession
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
          semester: this.selectedSemester,
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
          semester: this.selectedSemester,
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

    /**
     * @param {Course} course
     */
    showCourseInfo(course) {
      this.courseInfoModalCourse = course;
      this.showCourseInfoModal = true;
      alert(this.state.darkMode);
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
    selectedSections() {
      return Object.values(this.selectedCourses)
        .map((c) => c.sections.filter((s) => s.selected))
        .flat();
    },
    /**
     * Returns list of CRNs for all selected sections
     * @returns {string[]}
     */
    selectedCrns() {
      return this.selectedSections.map((s) => s.crn).join(", ");
    },
    numSelectedCourses() {
      return Object.values(this.selectedCourses).length;
    },
  },
  watch: {
    selectedSemester: {
      immediate: true,
      handler(newSemester) {
        this.loading = true;
        history.pushState(null, "", encodeURI(`/?semester=${newSemester}`));

        this.updateDataOnNewSemester()
          .then(() => this.loadStudentCourses(newSemester))
          .then(() => (this.loading = false));
      },
    },
  },
};
</script>

<style scoped>

/deep/ .onStyleDarkMode {
  background: 'var(--dark-primary)';
  color: white;
}

/deep/ .offStyleDarkMode {
  background: white;
  color: black;
}

</style>

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
