<template>
  <div v-if="ready" class="w-90 ml-4 mb-4">
    <b-row>
      <b-col>
        <h1 class="mt-4">{{ courseTitle }}</h1>
        <h4 class="mb-1">{{ courseName }}</h4>
        <h6 class="mb-1">{{getCredits}} Credits</h6>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        {{
          generateRequirementsText(
            courseObj.prerequisites,
            courseObj.corequisites,
            courseObj.raw_precoreqs
          )
        }}
      </b-col>
    </b-row>
    <b-row>
      <b-col class="mb-4">
        <br />
        {{ courseObj.description }}
      </b-col>
    </b-row>
    <b-button :to="backRoute">Back</b-button>
  </div>
  <div v-else>
    <b-spinner></b-spinner>
    <strong class="m-2">Loading Course...</strong>
  </div>
</template>

<script>
import { getCourses } from "../services/YacsService";
import { getDefaultSemester } from "@/services/AdminService";
import { generateRequirementsText } from "@/utils";

export default {
  name: "CoursePage",
  data() {
    return {
      ready: false,
      courseName: this.$route.params.course,
      courseTitle: String,
      courseObj: {},
      selectedSemester: String,
      backRoute: String,
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
    generateRequirementsText,
  },
  async created() {
    const querySemester = this.$route.query.semester;
    console.log(this.$route);
    this.selectedSemester =
      querySemester && querySemester != "null"
        ? querySemester
        : await getDefaultSemester();
    const courses = await getCourses(this.selectedSemester);
    for (const c of courses) {
      if (c.name === this.courseName) {
        this.courseTitle = c.title;
        this.courseObj = c;
      }
    }
    this.backRoute = "/explore/" + this.courseObj.department;
    this.ready = true;
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
    getCredits() {
      var credits;
      if (this.courseObj.max_credits != this.courseObj.min_credits){
        credits = [this.courseObj.min_credits,this.courseObj.max_credits].join("-");
      } else{
        credits = this.courseObj.min_credits;
      }
      return credits;
    },
  },
};
</script>
