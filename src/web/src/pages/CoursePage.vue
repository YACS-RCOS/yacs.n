<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <div class="w-90 ml-4 mb-4">
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
      <b-button :to="'/explore/' + courseObj.department">Back</b-button>
    </div>
    <!-- <CenterSpinner
      v-else
      :height="80"
      :font-size="1.4"
      loading-message="Course"
      :top-spacing="30"
    /> -->
  </b-container>
</template>

<script>
import { generateRequirementsText } from "@/utils";
// import CenterSpinnerComponent from "../components/CenterSpinner.vue";
import CourseSectionsOpenBadge from "../components/CourseSectionsOpenBadge.vue";

export default {
  name: "CoursePage",
  components: {
    // CenterSpinner: CenterSpinnerComponent,
    CourseSectionsOpenBadge,
  },
  data() {
    return {
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
  computed: {
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
      // return this.$store.getters.courseById()
      return this.$store.getters.courses.find(
        (course) => course.name === this.courseName
      );
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
  methods: {
    generateRequirementsText,
  },
  metaInfo() {
    return {
      title: this.courseTitle,
      titleTemplate: "%s | YACS",
      meta: [
        {
          vmid: "description",
          name: "description",
          content: this.courseObj.description,
        },
        {
          vmid: "keywords",
          content:
            "RPI, YACS, Rensselaer Polytechnic Institute, " +
            this.courseName.substring(0, 4) +
            ", " +
            this.courseName.substring(5, 10) +
            ", " +
            this.courseName +
            ", " +
            this.courseTitle,
        },
      ],
    };
  },
};
</script>
