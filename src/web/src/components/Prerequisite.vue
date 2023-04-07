<template>
    <b-list-group id="prerequisite-list" flush data-cy="prerequisites">
      <div v-if="Object.keys(courses).length == 0" class="no-courses">
        There is no Prerequisite to display!
      </div>
      <b-list-group-item v-for="course of courses" :key="course.id">
        <CourseListing :course="course" v-on="$listeners" />
      </b-list-group-item>
      <li v-for="course in courses" :key = "course.title">
        {{ course.title }}
        <p>
            <b-col>
                <p v-html=course.value />
            </b-col>
        </p>
      </li>
    </b-list-group>
  </template>
  
  <script>
  import "@/typedef";
  import PrerequisiteListingComponents from "@/components/PrerequisiteListing";

  export default {
    name: "Prerequisites",
    components: {
        CourseListing: PrerequisiteListingComponents,
    },
    props: {
      courses: Object,
    },
  };
  </script>

  <style scoped lang="scss">
  #prerequisite-list {
    overflow-y: scroll !important;
    overflow-x: auto;
    min-height: 200px;
    flex-grow: 1;
    flex-basis: 0px; // allows flex and scroll combo
    border-bottom: 1px solid #dbdbdc;
  }
  .no-courses {
    margin-right: 20px;
    border-style: solid;
    border-width: 2px;
    border-color: rgb(0, 0, 0, 0.05);
    font-size: 16px;
    padding: 20px;
  }
  </style>
  