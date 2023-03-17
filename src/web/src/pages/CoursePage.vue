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
      <h5>Instructors:</h5>
      <ul>
        <li v-for="item in instructorList" :key="item.id">
        {{ item.name }} -- {{ item.email }}
      </li> 
      </ul>
      
      <b-row>
        <b-col class="mb-4">

          <CourseListing
                :course="courseObj"
                @addCourse="addCourse"
                @removeCourse="removeCourse"
                @removeCourseSection="removeCourseSection"
                @addCourseSection="addCourseSection"
                defaultAction="toggleCourse"
                v-on="$listeners"
                lazyLoadCollapse
              >               
              </CourseListing>
          
          <br />
          Description
          <br />
          {{ courseObj.description }}
          <br />
          When offered: {{courseObj.frequency}} 
          <br />
        </b-col>
      </b-row>
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
import { SelectedCoursesCookie } from "../controllers/SelectedCoursesCookie";
import { mapGetters, mapState } from "vuex";
import { COURSES } from "@/store";
import { generateRequirementsText } from "@/utils";
import CenterSpinnerComponent from "../components/CenterSpinner.vue";
import CourseSectionsOpenBadge from "../components/CourseSectionsOpenBadge.vue";
import CourseListingComponent from "@/components/CourseListing";
import {
  addStudentCourse,
  removeStudentCourse,
} from "@/services/YacsService";
export default {
  components: {
    CourseListing: CourseListingComponent,
    CenterSpinner: CenterSpinnerComponent,
    CourseSectionsOpenBadge,
  },
  name: "CoursePage",
  data() {
    return {
      coursePlaceHolder: this.courseObj,
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
      instructorList:[]
    };
  },
  mounted() {
  // Create a set to store professor names and emails.
  const instructors = new Set();

  // Use the loop to get professor name and email of each session
  this.courseObj.sections.forEach((section) => {
    section.sessions.forEach((session) => {
      // Some sessions may have multiple professors, split them by "/"
      const instructorArr = session.instructor.split("/");
      instructorArr.forEach((instructor) => {
        // Split each professor name and email by space
        const [name, email] = instructor.trim().split(" ");
        // Remove duplicate items, and some strange names
        if (name && name !== "Staff" && name !== "B") {
          // Add the professor name and email as an object to the set
          instructors.add({ name: name, email: email });
        }
      });
    });
  });

  // Change set to array
  this.instructorList = Array.from(instructors);
},
  methods: {
    generateRequirementsText,
    addCourse() {
      const course = this.courseObj;
      course.selected = true;
      if (this.isLoggedIn) {
        addStudentCourse({
          name: course.name,
          semester: this.courseObj.semester,
          cid: "-1",
        });
      } else {
        SelectedCoursesCookie.load(this.$cookies)
          .semester(this.courseObj.semester)
          .addCourse(course)
          .save();
      }
      /*
      course.sections.forEach((section) =>
        this.addCourseSection(course, section)
      );
      */
    },
    addCourseSection(course, section) {
      section.selected = true;
      if (this.isLoggedIn) {
        addStudentCourse({
          name: course.name,
          semester: this.courseObj.semester,
          cid: section.crn,
        });
      } else {
        SelectedCoursesCookie.load(this.$cookies)
          .semester(this.courseObj.semester)
          .addCourseSection(course, section)
          .save();
      }
    },
    removeCourse() {
      const course = this.courseObj;
      course.selected = false;
      course.sections.forEach((section) => this.removeCourseSection(section));
      if (this.isLoggedIn) {
        removeStudentCourse({
          name: course.name,
          semester: this.courseObj.semester,
          cid: null,
        });
      } else {
        SelectedCoursesCookie.load(this.$cookies)
          .semester(this.courseObj.semester)
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
            semester: this.courseObj.semester,
            cid: section.crn,
          });
        } else {
          SelectedCoursesCookie.load(this.$cookies)
            .semester(this.courseObj.semester)
            .removeCourseSection(section)
            .save();
        }
      }
    },
    toggle() {
      if (!this.isActive) {
        this.addCourse();
        this.isActive = true;
      } else {
        this.removeCourse();
        this.isActive = false;
      }
    },

  },
  computed: {
    ...mapState(["isLoadingCourses"]),
    ...mapGetters([COURSES]),
    transformed() {
      let precoreqtext = this.courseObj.raw_precoreqs;
      console.log(this.courseObj);
      
      // let idx;
      // let idx2;

      if (precoreqtext === null) {
        //console.log(this.courseObj.);
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
};
</script>