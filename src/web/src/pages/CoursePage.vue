<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <div v-if="!isLoadingCourses && courseObj" class="w-90 ml-4 mb-4">
      <b-row>
        <b-col>
          <h1 class="mt-4">{{ courseObj.title }}</h1>
          <h4 class="mb-1 d-inline">{{ courseName }}</h4>
          &nbsp;
          <div class="d-inline">
            <course-sections-open-badge :course="courseObj" />
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <h6 class="mb-1 d-inline">{{ getCredits }} Credits</h6>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <p v-html="transformed" />
        </b-col>
      </b-row>
      <b-row>
        <b-col class="mb-4">
          <br />
          {{ courseObj.description }}
        </b-col>
      </b-row>
      <b-button
        variant="primary"
        class="mr-2"
        @click="toggleCourse(courseObj);"
      > Info
      </b-button>
      <b-button @click="$router.go(-1)">Back</b-button>
      <!--      :to="'/explore/' + courseObj.department"-->
    </div>
    <CenterSpinner
      v-else-if="isLoadingCourses"
      :height="80"
      :fontSize="1.4"
      loadingMessage="Course"
      :topSpacing="30"
    />
    <!-- If !courseObj -->
    <div v-else class="w-90 ml-4 mb-4">
      <b-row>
        <b-col>
          <h1 class="mt-4">Course not found</h1>
          <p>
            This course may not exist, not offered this semester, or offered
            under a different name.
          </p>
          <b-button @click="$router.go(-1)">Back</b-button>
        </b-col>
      </b-row>
    </div>
  </b-container>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import { COURSES } from "@/store";
import CenterSpinnerComponent from "../components/CenterSpinner.vue";
import CourseSectionsOpenBadge from "../components/CourseSectionsOpenBadge.vue";
import SubSemesterScheduler from "@/controllers/SubSemesterScheduler";

import { SelectedCoursesCookie } from "../controllers/SelectedCoursesCookie";
import { SelectedIndexCookie } from "../controllers/SelectedIndexCookie";

import {
  addStudentCourse,
  getStudentCourses,
  removeStudentCourse,
} from "@/services/YacsService";

import {
  withinDuration,
} from "@/utils";


export default {
  components: {
    CenterSpinner: CenterSpinnerComponent,
    CourseSectionsOpenBadge,
  },
  name: "CoursePage",
  data() {
    return {
      selectedCourses: {},
      courseName: this.$route.params.course,
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
        {
          text: this.$route.params.course,
        },
      ],
    };
  },
  methods: {
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
    toggleCourse(course) {
      console.log(course);
      if (course.selected) {
        this.removeCourse(course);
      } else {
        this.addCourse(course);
      }
    },
  },
  computed: {
    ...mapState(["isLoadingCourses"]),
    ...mapGetters([COURSES]),
    transformed() {
      let precoreqtext = this.courseObj.raw_precoreqs;
      if (precoreqtext === null) {
        return "No information on pre/corequisites";
      }
      const regex = /([A-Z]){4}( )([0-9]){4}/g;
      while (precoreqtext.search(regex) != -1) {
        let index = precoreqtext.search(regex);
        let beforetext = precoreqtext.slice(0, index);
        let dept = precoreqtext.slice(index, index + 4);
        let course_name = precoreqtext
          .slice(index, index + 9)
          .split(" ")
          .join("-");
        let link = '<a href="/explore/'.concat(
          dept,
          "/",
          course_name,
          '">',
          course_name,
          "</a>"
        );
        let aftertext = precoreqtext.slice(index + 9);
        precoreqtext = beforetext.concat(link, aftertext);
      }
      return precoreqtext;
    },
    courseObj() {
      return this.courses.find((course) => course.name === this.courseName);
    },
    getCredits() {
      var credits;
      if (this.courseObj.min_credits != this.courseObj.max_credits) {
        credits = [this.courseObj.min_credits, this.courseObj.max_credits].join(
          "-"
        );
      } else {
        credits = this.courseObj.min_credits;
      }
      return credits;
    },
  },
  metaInfo() {
    return {
      title: this.courseObj.name,
      titleTemplate: "%s | YACS",
      meta: !this.courseObj
        ? undefined
        : [
            {
              vmid: "description",
              name: "description",
              content: this.courseObj.description,
            },
            {
              vmid: "keywords",
              content: [
                this.courseObj.full_title,
                this.courseObj.name,
                this.courseObj.department,
                this.courseObj.level,
                this.courseObj.school,
                "RPI",
                "YACS",
                "Rensselaer Polytechnic Institute",
              ].join(", "),
            },
          ],
    };
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
  },
};
</script>
