<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <div
      v-if="$store.state.courseList.length != 0"
      class="gridContainer w-100 mb-4"
    >
      <b-row>
        <!-- The subject title should be depending on the input parameter from subjectList.vue -->
        <h1 class="subjectBox">{{ subject }}</h1>
        <b-col>
          <b-row
            v-for="course in this.leftColumnCourses"
            v-bind:key="course.level + course.department"
          >
            <!-- Navigates to course page by click on the course button  -->
            <b-col class="m-1 ml-0">
              <b-button
                variant="light"
                class="courseBox border m-2"
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
                {{ course.department }}
                {{ course.level }}
                <br />
              </b-button>
            </b-col>
          </b-row>
        </b-col>
      </b-row>

      <br />

      <!-- left column of courses -->
      <b-col>
        <b-row
          v-for="course in courseColumns[0]"
          v-bind:key="course.level + course.department"
        >
          <!-- Navigates to course page by click on the course button  -->
          <b-col class="m-1 ml-0">
            <b-button
              variant="light"
              class="courseBox border m-2"
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
              {{ course.department }}
              {{ course.level }}
              <br />
            </b-button>
          </b-col>
        </b-row>
      </b-col>

      <!-- right column of courses -->
      <b-col>
        <b-row
          v-for="course in courseColumns[1]"
          :key="course.level + course.department"
        >
          <!-- Navigates to course page by click on the course button  -->
          <b-col class="m-1 ml-2">
            <b-button
              variant="light"
              class="courseBox border m-2"
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
              {{ course.department }}
              {{ course.level }}
              <br />
            </b-button>
          </b-col>
        </b-row>
      </b-col>
    </div>

    <div v-else>
      <b-spinner></b-spinner>
      <strong class="m-2">Loading courses...</strong>
    </div>
  </b-container>
</template>

<script>
export default {
  name: "SubjectExplorer",
  components: {},
  props: {
    selectedSemester: String,
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
    //courseColumns[0] corresponds to left column, [1] to right column
    courseColumns() {
      let leftColumn = [];
      let rightColumn = [];
      const courses = this.$store.state.courseList;
      //Obtain All Courses Such That Department Matches The Subject Name.
      const allTempData = courses.filter((c) => c.department === this.subject);
      for (let k = 0; k < allTempData.length; k++) {
        if (k % 2 == 0) leftColumn.push(allTempData[k]);
        else rightColumn.push(allTempData[k]);
      }
      return [leftColumn, rightColumn];
    },
  },
};
</script>

<style scope>
.gridContainer {
  display: inline-grid;
  grid-template-columns: auto auto;
  justify-content: center;
  align-content: center;
}

.subjectBox {
  /* border: 3px solid black; */
  margin-bottom: 20px;
  height: 2.5rem;
  width: 15rem;
  font-size: xx-large;
  font-weight: 600;
  text-align: center;
}

.courseBox {
  height: 5rem;
  width: 30rem;
  text-align: left;
}

.major-courseBox:hover {
  background: rgba(108, 90, 90, 0.15);
}
</style>
