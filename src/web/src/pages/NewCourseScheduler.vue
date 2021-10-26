<template>
  <b-container fluid class="py-3 h-100 main-body">
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
                <CenterSpinner
                  v-if="loading"
                  class="d-flex flex-grow-1 flex-column w-100 justify-content-center align-items-center"
                  :height="60"
                  :fontSize="1"
                  loadingMessage="Courses"
                  :topSpacing="0"
                />

                <CourseList
                  v-if="!loading"
                  @addCourse="addCourse"
                  @removeCourse="removeCourse"
                  @showCourseInfo="showCourseInfo"
                  class="w-100"
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
      <div class="col-md-8">
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
        <div id="allScheduleData">
          <b-row>
            <b-col class="m-2">
              <b-button
                id="prev-schedule"
                @click="changeSchedule(-1)"
                size="sm"
              >
                Prev
              </b-button>
            </b-col>
            <b-col cols="8" class="m-2 text-center">
              <span v-if="noSectionsSelected">
                Add some sections to generate schedules!
              </span>
              <span v-else>
                Displaying schedule {{ this.index + 1 }} out of {{ this.possibilities.length }}
              </span>
            </b-col>
            <b-col class="m-2 text-right">
              <b-button
                id="next-schedule"
                @click="changeSchedule(1)"
                size="sm"
              >
                Next
              </b-button>
            </b-col>
          </b-row>
          <Schedule v-if="loading" />
<!--          <template v-else-if="scheduler.schedules">
            <Schedule
              v-for="(schedule, index) in scheduler.schedules"
              :key="index"
              :schedule="schedule"
              v-show="selectedScheduleIndex === index"
            />
          </template>-->
          <Schedule v-else :possibility="possibilities[index]"></Schedule>

          <b-row>
            <b-col class="m-2">
              <h5>CRNs: {{ selectedCrns }}</h5>
              <h5>Credits: {{ totalCredits }}</h5>
            </b-col>

            <b-col md="3" justify="end">
              <b-row>
                <b-form-checkbox
                  class="mt-2"
                  size="sm"
                  :checked="$store.state.colorBlindAssist"
                  @change="toggleColors()"
                  switch
                >
                  Color Blind Assistance
                </b-form-checkbox>
              </b-row>
              <b-row>
                <b-dropdown text="Export Data" class="mt-2">
                  <b-dropdown-item @click="exportScheduleToIcs">
                    <font-awesome-icon :icon="exportIcon" />
                    Export To ICS
                  </b-dropdown-item>
                  <b-dropdown-item @click="exportScheduleToImage">
                    <font-awesome-icon :icon="exportIcon" />
                    Export To Image
                  </b-dropdown-item>
                </b-dropdown>
              </b-row>
            </b-col>
          </b-row>
        </div>
      </div>
    </b-row>

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
      <span
        v-if="
          courseInfoModalCourse.min_credits == courseInfoModalCourse.max_credits
        "
      >
        Credits: {{ courseInfoModalCourse.min_credits }}
        <br />
      </span>
      <span v-else>
        Credits: {{ courseInfoModalCourse.min_credits }} -
        {{ courseInfoModalCourse.max_credits }}
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
        variant="secondary"
        @click="showCourseInfoModal = !showCourseInfoModal"
      >
        Close
      </b-button>
    </b-modal>
  </b-container>
</template>

<script>
import { mapGetters, mapState } from "vuex";

import NotificationsMixin from "@/mixins/NotificationsMixin";
import ScheduleComponent from "@/components/Schedule";
import SelectedCoursesComponent from "@/components/SelectedCourses";
import CourseListComponent from "@/components/CourseList";
import CenterSpinnerComponent from "../components/CenterSpinner";
import Schedule from "@/controllers/Schedule";
import SubSemesterScheduler from "@/controllers/SubSemesterScheduler";
import allExportVariables from "@/assets/dark.scss";

import { SelectedCoursesCookie } from "../controllers/SelectedCoursesCookie";

import { userTypes } from "../store/modules/user";

import { COURSES, TOGGLE_COLOR_BLIND_ASSIST } from "@/store";

import { addStudentCourse, getStudentCourses, removeStudentCourse } from "@/services/YacsService";

import { exportScheduleToIcs, exportScheduleToImage, generateRequirementsText, withinDuration } from "@/utils";

import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";

const noConflict = (p, section) => {
  for (let i = 0; i < 5; i++) {
    if ((p.time[i] & section.times[i]) > 0) return false
  }
  return true
}
const addSection = (p, section) => {
  let ret = [0, 0, 0, 0, 0]
  for (let i = 0; i < 5; i++)
    ret[i] = p.time[i] | section.times[i]
  return {
    sections: p.sections.concat(section),
    time: ret
  }
}
export default {
  name: "MainPage",
  mixins: [NotificationsMixin],
  components: {
    Schedule: ScheduleComponent,
    SelectedCourses: SelectedCoursesComponent,
    CourseList: CourseListComponent,
    CenterSpinner: CenterSpinnerComponent,
  },
  data() {
    return {
      selectedCourses: {},
      selectedScheduleSubsemester: null,
      scheduler: new Schedule(),
      exportIcon: faPaperPlane,

      courseInfoModalCourse: null,
      showCourseInfoModal: false,
      possibilities: [{
        sections: [],
        times: [0, 0, 0, 0, 0]
      }],
      index: 0
    };
  },
  methods: {
    toggleColors() {
      this.$store.commit(TOGGLE_COLOR_BLIND_ASSIST);
    },
    generateRequirementsText,
    exportScheduleToIcs() {
      exportScheduleToIcs(Object.values(this.selectedCourses));
    },
    exportScheduleToImage() {
      exportScheduleToImage(
        Object.values(this.selectedCourses),
        this.selectedSemester,
        {
          bgcolor: this.$store.state.darkMode
            ? allExportVariables.bColor
            : "white",
        }
      );
    },
    async loadStudentCourses() {
      if (!this.courses.length) {
        return;
      }

      // Less work to create a new scheduler which is meant for a single semester
      this.scheduler = new SubSemesterScheduler();
      // Filter out "full" subsemester
      this.subsemesters
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

      // Need to reset `selected` property on courses and sections,
      // two sources of truth ugh
      Object.values(this.selectedCourses).forEach((course) => {
        course.selected = false;

        course.sections
          .filter((section) => section.selected)
          .forEach((section) => (section.selected = false));
      });
      this.selectedCourses = {};

      if (this.isLoggedIn) {
        var cids = await getStudentCourses();

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
      } else {
        const selectedCoursesCookie = SelectedCoursesCookie.load(this.$cookies);

        try {
          selectedCoursesCookie
            .semester(this.selectedSemester)
            .selectedCourses.forEach((selectedCourse) => {
            const course = this.courses.find(
              (course) => course.id === selectedCourse.id
            );

            course.selected = true;
            this.$set(this.selectedCourses, course.id, course);
            this.scheduler.addCourse(course);

            selectedCourse.selectedSectionCrns.forEach(
              (selectedSectionCrn) => {
                const section = course.sections.find(
                  (section) => section.crn === selectedSectionCrn
                );

                section.selected = true;
                this.scheduler.addCourseSection(course, section);
              }
            );
          });
        } catch (err) {
          // If there is an error here, it might mean the data was changed,
          //  thus we need to reload the cookie
          selectedCoursesCookie.clear().save();
        }
      }
    },
    addCourse(course) {
      this.$set(this.selectedCourses, course.id, course);
      course.selected = true;
      if (this.isLoggedIn) {
        addStudentCourse({
          name: course.name,
          semester: this.selectedSemester,
          cid: "-1",
        });
      }
      course.sections.forEach(section => this.addCourseSection(course, section))
      /*let i = 0;
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

      if (this.isLoggedIn) {
        addStudentCourse({
          name: course.name,
          semester: this.selectedSemester,
          cid: "-1",
        });
      } else {
        SelectedCoursesCookie.load(this.$cookies)
          .semester(this.selectedSemester)
          .addCourse(course)
          .save();
      }*/
    },
    _addCourseSection(/*course, section*/) {
      /*this.scheduler.addCourseSection(course, section);
      section.selected = true;

      if (this.isLoggedIn) {
        addStudentCourse({
          name: course.name,
          semester: this.selectedSemester,
          cid: section.crn,
        });
      } else {
        SelectedCoursesCookie.load(this.$cookies)
          .semester(this.selectedSemester)
          .addCourseSection(course, section)
          .save();
      }*/
    },

    addCourseSection(course, section) {
      section.selected = true
      if (this.isLoggedIn) {
        addStudentCourse({
          name: course.name,
          semester: this.selectedSemester,
          cid: section.crn,
        });
      }
      /*try {
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
      }*/
    },
    removeCourse(course) {
      this.$delete(this.selectedCourses, course.id);
      course.selected = false;
      // this.scheduler.removeAllCourseSections(course);

      if (this.isLoggedIn) {
        removeStudentCourse({
          name: course.name,
          semester: this.selectedSemester,
          cid: null,
        });
      }

      course.sections.forEach(section => this.removeCourseSection(course, section))
      /*else {
        SelectedCoursesCookie.load(this.$cookies)
          .semester(this.selectedSemester)
          .removeCourse(course)
          .save();
      }*/
    },
    removeCourseSection(section) {
      // this.scheduler.removeCourseSection(section);

      section.selected = false

      if (this.isLoggedIn) {
        removeStudentCourse({
          name: section.department + "-" + section.level,
          semester: this.selectedSemester,
          cid: section.crn,
        });
      } /*else {
        SelectedCoursesCookie.load(this.$cookies)
          .semester(this.selectedSemester)
          .removeCourseSection(section)
          .save();
      }*/
    },

    /**
     * @param {Course} course
     */
    showCourseInfo(course) {
      this.courseInfoModalCourse = course;
      this.showCourseInfoModal = true;
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
    getSchedules() {
      try {
        this.possibilities = this.generateSchedule(Object.values(this.selectedCourses))
      } catch (e) {
        this.possibilities = [{
          sections: [],
          time: [0, 0, 0, 0, 0]
        }]
        console.log(e)
      }
    },
    generateSchedule(c) {
      let courses = JSON.parse(JSON.stringify(c))
      if (courses.length === 0) return [{
        sections: [],
        time: [0, 0, 0, 0, 0]
      }]
      const popped = courses.pop()
      let ret = this.generateSchedule(courses)

      if(!ret.length) throw new Error()
      return ret.map(schedule => {
        return popped.sections.filter(s => s.selected).map(section => {
          if (noConflict(schedule, section)) {
            return addSection(schedule, section)
          }
          return undefined
        }).filter(x => !!x)
      }).flat()
    },
    changeSchedule(step) {
      const l = this.possibilities.length
      if (l === 0) return
      const c = this.index + step
      if (c < 0) {
        this.index = l - 1
        return
      }
      if (c >= l) {
        this.index = 0
        return;
      }
      this.index = c
    },
  },
  computed: {
    ...mapState(["subsemesters", "selectedSemester"]),
    ...mapGetters([COURSES]),
    ...mapGetters({ isLoggedIn: userTypes.getters.IS_LOGGED_IN }),

    loading() {
      return this.$store.state.isLoadingCourses;
    },

    selectedScheduleIndex() {
      return this.scheduler.scheduleSubsemesters.findIndex(
        (s) => s.display_string === this.selectedScheduleSubsemester
      );
    },
    selectedSections() {
      this.getSchedules()
      return Object.values(this.selectedCourses)
        .map((c) => c.sections.filter((s) => s.selected))
        .flat();
    },
    /**
     * Returns list of CRNs for all selected sections
     * @returns {string}
     */
    selectedCrns() {
      return this.possibilities[this.index] && this.possibilities[this.index].sections.map((s) => s.crn).join(", ");
    },
    /**
     * Returns sum of credits being taken from all selected sections
     */
    totalCredits() {
      var array = Object.values(this.selectedCourses).map((c) => c.max_credits);

      // Getting sum of numbers
      var sum = array.reduce(function (a, b) {
        return a + b;
      }, 0);
      return sum;
    },
    numSelectedCourses() {
      return Object.values(this.selectedCourses).length;
    },

    noSectionsSelected() {
      if (this.possibilities.length === 1) {
        return !this.possibilities[0].sections.length;
      }
      return false;
    },
  },
  watch: {
    courses: {
      immediate: true,
      handler() {
        this.loadStudentCourses();
      },
    },
    isLoggedIn: {
      immediate: true,
      handler() {
        this.loadStudentCourses();
      },
    },
    selectedSections: {
      handler() {
        this.getSchedules()
      }
    }
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

@media (min-width: 1025px) {
  .main-body {
    min-height: 100vh;
  }
}

.tab-content {
  display: flex;
  flex-grow: 1;
  font-size: 15px;
}
// This makes it so active tabs are display:flex
// The default is display:block
.tab-content > .active {
  display: flex;
}

.card {
  border: none !important;
  font-size: 17px;

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
#allScheduleData {
  position: relative;
  .prev-schedule, .next-schedule {
    position: absolute;
    top: 0;
    height: 100%;
    z-index: 1000;
    line-height: 75%;
    &:hover {
      cursor: pointer;
    }
  }
  .prev-schedule {
    left: 0
  }
  .next-schedule {
    right: 0
  }
}
</style>
