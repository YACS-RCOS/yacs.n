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
          <Schedule v-if="loading" />
          <template v-else-if="scheduler.schedules">
            <Schedule
              v-for="(schedule, index) in scheduler.schedules"
              :key="index"
              :schedule="schedule"
              v-show="selectedScheduleIndex === index"
            />
          </template>
          <Schedule v-else :schedule="scheduler"></Schedule>

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
      data-cy="course-info-modal"
    >
      <span v-if="courseInfoModalCourse.frequency">
<!--        Offered: {{ courseInfoModalCourse.frequency }}-->
        <br />
        <br />
      </span>
      <span
        v-if="
          courseInfoModalCourse.min_credits == courseInfoModalCourse.max_credits
        "
      >
<!--        Credits: {{ courseInfoModalCourse.min_credits }}-->
        <br />
      </span>
      <span v-else>
        Credits: {{ courseInfoModalCourse.min_credits }} -
        {{ courseInfoModalCourse.max_credits }}
        <br />
      </span>
      <span>
<!--        {{
          generateRequirementsText(
            courseInfoModalCourse.prerequisites,
            courseInfoModalCourse.corequisites,
            courseInfoModalCourse.raw_precoreqs
          )
        }}-->
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
import CenterSpinnerComponent from "../components/CenterSpinner";
import CourseListComponent from "@/components/CourseList";
import SelectedCoursesComponent from "@/components/SelectedCourses";
import ScheduleComponent from "@/components/Schedule";

import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";
export default {
  name: 'MainPage',
  components: {
    CenterSpinner: CenterSpinnerComponent,
    CourseList: CourseListComponent,
    SelectedCourses: SelectedCoursesComponent,
    Schedule: ScheduleComponent,
  },
  created() {
  },
  data: () => ({
    possibilities: [{
      sections: [],
      time: [0, 0, 0, 0, 0]
    }],
    currentIndex: -1,
    courses: [{ sections: [{ isSelected: false, sessions: [0, 0, 0, 0, 0] }] }],
    selections: new Map(),
    ///////////////////////////
    selectedCourses: {},
    selectedCrns: "",
    totalCredits: 0,
    exportIcon: faPaperPlane,
    courseInfoModalCourse: null,
    showCourseInfoModal: false,
    scheduler: {
      scheduleSubsemesters: null
    }
  }),
  methods: {
    addCourse() {
    },
    addCourseSection(/*course, section*/) {
    },
    removeCourse(/*course*/) {
    },
    removeCourseSection(/*section*/) {
    },
    exportScheduleToIcs() {

    },
    exportScheduleToImage() {

    },
    showCourseInfo() {

    },
  },
  watch: {

  },
  computed: {
    loading() {
      return this.$store.state.isLoadingCourses;
    },
    numSelectedCourses() {
      return 0
    }
  }
}
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
</style>