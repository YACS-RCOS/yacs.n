<template>
  <div>
    <template v-if="schedules.length > 0">
      <b-container>
        <b-row>
          <b-col v-if="schedules.length > 1" class="px-0 d-flex" cols="auto">
            <div class="my-auto d-block">
              <div v-show="selectedScheduleIndex > 0">
                {{ selectedScheduleIndex - 1 + 1 }} / {{ schedules.length }}
              </div>
              <b-button
                :disabled="selectedScheduleIndex === 0"
                @click="selectedScheduleIndex -= 1"
              >
                <font-awesome-icon :icon="faAngleLeft" />
              </b-button>
            </div>
          </b-col>
          <b-col>
            <component
              :is="component"
              v-for="({ component, scheduleCourseSections, key },
              index) in schedules"
              v-show="selectedScheduleIndex === index"
              :key="key"
              :course-sections="scheduleCourseSections"
            ></component>
          </b-col>
          <b-col v-if="schedules.length > 1" class="px-0 d-flex" cols="auto">
            <div class="my-auto d-block">
              <div v-if="selectedScheduleIndex < schedules.length - 1">
                {{ selectedScheduleIndex + 1 + 1 }} / {{ schedules.length }}
              </div>
              <b-button
                :disabled="selectedScheduleIndex === schedules.length - 1"
                @click="selectedScheduleIndex += 1"
              >
                <font-awesome-icon :icon="faAngleRight" />
              </b-button>
            </div>
          </b-col>
        </b-row>
      </b-container>
    </template>
    <b-overlay v-else show>
      <Schedule />
      <template #overlay>
        <div class="text-center">
          <p v-if="courses.length > 0">No schedules possible</p>
          <p v-else>Choose some courses to get started!</p>
        </div>
      </template>
    </b-overlay>
  </div>
</template>

<script>
import Logic from "logic-solver";
import { hasSessionConflict, withinCourseDuration } from "@/utils";
import Schedule from "@/components/Schedule";
import SubSemesterSchedule from "@/components/SubSemesterSchedule";
import { faAngleLeft, faAngleRight } from "@fortawesome/free-solid-svg-icons";

export default {
  components: {
    Schedule,
    SubSemesterSchedule,
  },
  props: {
    /** @type {import("vue").PropType<import("@/typedef").Course[]>} */
    courses: {
      type: Array,
      default: () => [],
    },
    /** @type {import("vue").PropType<import("@/typedef").CourseSection[]>} */
    courseSections: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      selectedScheduleIndex: 0,
      faAngleLeft,
      faAngleRight,
    };
  },
  computed: {
    /** @returns {Map<import("@/typedef").Course, import("@/typedef").CourseSection[]>} */
    courseSectionsByCourse() {
      /** @type {Map<import("@/typedef").Course, import("@/typedef").CourseSection[]>} */
      const courseSectionsByCourse = new Map();

      this.courses.forEach((course) => {
        courseSectionsByCourse.set(
          course,
          this.courseSections.filter((section) => section.course === course)
        );
      });

      return courseSectionsByCourse;
    },
    activeSections() {
      if (this.schedules.length === 0) {
        return [];
      }

      return this.schedules[this.selectedScheduleIndex].scheduleCourseSections;
    },
    /** @returns {[string, string][]} */
    conflicts() {
      const conflicts = [];

      // O(n^million) should move to backend with comprehensive caching
      for (const course of this.courses) {
        for (const otherCourse of this.courses) {
          if (course === otherCourse) {
            continue;
          }

          if (!withinCourseDuration(course, otherCourse)) {
            continue;
          }

          for (const section of course.sections) {
            for (const otherSection of otherCourse.sections) {
              if (section === otherSection) {
                continue;
              }

              if (!hasSessionConflict(section, otherSection)) {
                continue;
              }

              conflicts.push([section.crn + "-", otherSection.crn + "-"]);
            }
          }
        }
      }

      return conflicts;
    },
    allCourseSections() {
      return this.courses.map((course) => course.sections).flat();
    },
    schedules() {
      if (this.courses.length === 0) {
        return [];
      }

      /** @type {Logic.Solver} */
      const solver = new Logic.Solver();

      this.conflicts.forEach((conflictingSections) => {
        solver.require(
          Logic.not(Logic.and(...conflictingSections.map(solver.toNameTerm)))
        );
      });

      this.courseSectionsByCourse.forEach((courseSections, course) => {
        if (courseSections.length === 1) {
          solver.require(solver.toNameTerm(courseSections[0].crn + "-"));
        } else {
          solver.require(
            Logic.exactlyOne(
              (courseSections.length > 0
                ? courseSections
                : course.sections
              ).map((section) => solver.toNameTerm(section.crn + "-"))
            )
          );
        }
      });

      /** @type {string[][]} */
      const solutions = [];
      let currentSolution;
      const limit = 100;
      let i = 0;
      while ((currentSolution = solver.solve()) && i < limit) {
        i++;
        solutions.push(currentSolution.getTrueVars());
        solver.forbid(currentSolution.getFormula());
      }

      const newSchedules = solutions.map((sectionCrns) => {
        return {
          component:
            this.$store.state.subsemesters.length > 1
              ? "SubSemesterSchedule"
              : "Schedule",
          scheduleCourseSections: sectionCrns.map((crn) =>
            this.allCourseSections.find((section) => section.crn + "-" === crn)
          ),
          key: sectionCrns.join("|"),
        };
      });

      return newSchedules;
    },
  },
  watch: {
    activeSections(sections) {
      this.$emit("changeActiveSections", sections);
    },
  },
};
</script>

<style>
.carousel-caption,
.carousel-control-next,
.carousel-control-prev,
.carousel-indicators {
  color: black;
}
</style>
