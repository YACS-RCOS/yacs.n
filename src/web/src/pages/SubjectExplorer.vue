<template>
  
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    
    <b-row class="justify-content-center">
      <!-- The subject title should be depending on the input parameter from subjectList.vue -->
      <h3 class="subjectBox">{{ subject }}</h3>
    </b-row>
    <!-- left column of courses -->
    
    <b-row v-if="!isLoadingCourses && courses.length > 0">
      <b-col cols="6">
        <b-row
          v-for="course in courseColumns[0]"
          v-bind:key="course.level + course.department"
        >
          <!-- Navigates to course page by click on the course button  -->
          <b-col class="leftCol p-1">
            <b-button
              variant="light"
              class="courseBox border mb-1"
              :to="{
                name: 'CoursePage',
                params: {
                  course: course.name,
                  subject: course.department,
                },
              }"
            >
              {{ course.title }}
              <br />
              <span class="d-inline">
                {{ course.department }}
                {{ course.level }}
              </span>
              <course-sections-open-badge :course="course" />
              <!-- Add the transparent button to add/remove courses -->
              <b-button
                variant="outline-primary"  
                size="sm"  
                class="transparent-button"
                @click.prevent="toggleCourse(course)"
              >
              {{ course.selected ? '✕' : '+' }}
              </b-button>
            </b-button>
          </b-col>
        </b-row>
      </b-col>
      <!-- right column of courses -->
      <b-col cols="6">
        <b-row
          v-for="course in courseColumns[1]"
          :key="course.level + course.department"
        >
          <!-- Navigates to course page by click on the course button  -->
          <b-col class="rightCol p-1">
            <b-button
              variant="light"
              class="courseBox border mb-1"
              :to="{
                name: 'CoursePage',
                params: {
                  course: course.name,
                  subject: course.department,
                },
              }"
            >
              {{ course.title }}
              <br />
              <span class="d-inline">
                {{ course.department }}
                {{ course.level }}
              </span>
              <course-sections-open-badge :course="course" />
              <!-- Add the transparent button to add/remove courses -->
              <b-button
                variant="outline-primary"  
                size="sm"  
                class="transparent-button"
                @click.prevent="toggleCourse(course)"
              >
                {{ course.selected ? '✕' : '+' }}
              </b-button>
            </b-button>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
    <!-- </div> -->
    <CenterSpinner
      v-else
      :height="80"
      :fontSize="1.4"
      loadingMessage="Courses"
      :topSpacing="30"
    />
  </b-container>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import CenterSpinnerComponent from "../components/CenterSpinner";
import CourseSectionsOpenBadge from "../components/CourseSectionsOpenBadge.vue";

import SubSemesterScheduler from "@/controllers/SubSemesterScheduler";

import { SelectedCoursesCookie } from "../controllers/SelectedCoursesCookie";
import { SelectedIndexCookie } from "../controllers/SelectedIndexCookie";


import { TOGGLE_COLOR_BLIND_ASSIST } from "@/store";

import {
  addStudentCourse,
  getStudentCourses,
  removeStudentCourse,
} from "@/services/YacsService";

import {
  withinDuration,
} from "@/utils";

export default {
  name: "SubjectExplorer",
  components: {
    CenterSpinner: CenterSpinnerComponent,
    CourseSectionsOpenBadge,
  },
  data() {
    return {
      selectedCourses: {},
      subject: this.$route.params.subject, // subject object from CourseExplorer
      breadcrumbNav: [
        {
          text: "YACS",
          to: "/",
        },
        {
          text: "Explore",
          to: "/explore",
        },
        {
          text: this.$route.params.subject,
          to: "/explore/" + this.$route.params.subject,
        },
      ],
    };
  },
  methods: {
    toggleNav() {
      this.isNavOpen = !this.isNavOpen;
      if (this.isNavOpen) {
        this.main = "col-md-9";
      } else {
        this.main = "col-md-12";
      }
    },
    toggleColors() {
      this.$store.commit(TOGGLE_COLOR_BLIND_ASSIST);
    },

    async loadStudentCourses() {
      if (!this.courses.length) {
        return;
      }

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
            } else {
              c.selected = true;
              this.$set(this.selectedCourses, c.id, c);
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
          selectedCoursesCookie.clear().save();
        }
      }

      const selectedIndexCookie = SelectedIndexCookie.load(this.$cookies);

      try {
        this.index = selectedIndexCookie.semester(
          this.selectedSemester
        ).selectedIndex;
      } catch (err) {
        // If there is an error here, it might mean the data was changed,
        //  thus we need to reload the cookie
        selectedIndexCookie.clear().save();
      }
      this.loadedIndexCookie = 1;
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
      } else {
        SelectedCoursesCookie.load(this.$cookies)
          .semester(this.selectedSemester)
          .addCourse(course)
          .save();
      }
      course.sections.forEach((section) =>
        this.addCourseSection(course, section)
      );
    },
    addCourseSection(course, section) {
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
      }
    },
    removeCourse(course) {
      this.$delete(this.selectedCourses, course.id);
      course.selected = false;

      course.sections.forEach((section) => this.removeCourseSection(section));

      if (this.isLoggedIn) {
        removeStudentCourse({
          name: course.name,
          semester: this.selectedSemester,
          cid: null,
        });
      } else {
        SelectedCoursesCookie.load(this.$cookies)
          .semester(this.selectedSemester)
          .removeCourse(course)
          .save();
      }
    },
    removeCourseSection(section) {
      if (section.selected) {
        section.selected = false;

        if (this.isLoggedIn) {
          removeStudentCourse({
            name: section.department + "-" + section.level,
            semester: this.selectedSemester,
            cid: section.crn,
          });
        } else {
          SelectedCoursesCookie.load(this.$cookies)
            .semester(this.selectedSemester)
            .removeCourseSection(section)
            .save();
        }
      }
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
      console.log(course);
    },
    getSchedules() {
      const oldLength = this.possibilities.length;
      try {
        if (Object.values(this.selectedCourses).length === 0) {
          this.possibilities = [
            {
              sections: [],
              time: [0, 0, 0, 0, 0],
            },
          ];
        }
        const result = this.generateSchedule(
          Object.values(this.selectedCourses)
        );
        if (!result.length) {
          throw new Error("conflict!");
        }
        this.possibilities = result;

        //Don't set this.index to 0 if just loaded cookie
        if (this.loadedIndexCookie == 2) {
          if (oldLength != this.possibilities.length) {
            this.index = 0;
            this.updateIndexCookie();
          }
        } else if (this.loadedIndexCookie == 1) {
          this.loadedIndexCookie = 2;
        }
      } catch (e) {
        console.log(e.message);
        this.possibilities = [
          {
            sections: [],
            time: [0, 0, 0, 0, 0],
            conflict: e.message === "conflict!",
          },
        ];
      }
    },
    
    changeSchedule(step) {
      const l = this.possibilities.length;
      if (l === 0) return;
      const c = this.index + step;
      if (c < 0) {
        this.index = l - 1;
        return;
      }
      if (c >= l) {
        this.index = 0;
        return;
      }
      this.index = c;
    },
    updateIndexCookie() {
      SelectedIndexCookie.load(this.$cookies)
        .semester(this.selectedSemester)
        .updateIndex(this.index)
        .save();
    },
  },
  computed: {
    ...mapState(["isLoadingCourses"]),
    ...mapGetters(["courses"]),
    //courseColumns[0] corresponds to left column, [1] to right column
    courseColumns() {
      let leftColumn = [];
      let rightColumn = [];

      //Obtain All Courses Such That Department Matches The Subject Name.
      const allTempData = this.courses.filter(
        (c) => c.department === this.subject
      );
      for (let k = 0; k < allTempData.length; k++) {
        if (k % 2 == 0) leftColumn.push(allTempData[k]);
        else rightColumn.push(allTempData[k]);
      }
      return [leftColumn, rightColumn];
    },
  },
  metaInfo() {
    return {
      title: this.subject,
      titleTemplate: "%s | YACS",
      meta: [
        { vmid: "description", content: "RPI " + this.subject },
        {
          vmid: "keywords",
          content:
            "RPI, YACS, Rensselaer Polytechnic Institute, " + this.subject,
        },
      ],
    };
  },
};
</script>

<style scoped lang="scss">
.subjectBox {
  /* border: 3px solid black; */
  margin-bottom: 20px;
  height: 2.5rem;
  width: 15rem;
  font-size: xx-large;
  font-weight: 600;
  text-align: center;
}

@media screen and (max-width: 600px) {
  .courseBox {
    width: 100% !important;
    height: 7rem !important;
    display: block;
    overflow: scroll;
  }

  .leftCol {
    text-align: center;
  }

  .rightCol {
    text-align: center;
  }
}

.leftCol {
  text-align: right;
}

.rightCol {
  text-align: left;
}

.courseBox {
  height: 5rem;
  width: 60%;
  text-align: left;
}

.courseBox:hover {
  background: rgba(108, 90, 90, 0.15) !important;
}

.transparent-button {
  left: 100px;
  top: 5px;
  right: 5px;
  
  background-color: transparent;
  border: none;
  color: #007bff; /* Change the color to match your design */
  cursor: pointer;
}
</style>