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

export default {
  name: "SubjectExplorer",
  components: {
    CenterSpinner: CenterSpinnerComponent,
    CourseSectionsOpenBadge,
  },
  data() {
    return {
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
  methods: {},
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
</style>
