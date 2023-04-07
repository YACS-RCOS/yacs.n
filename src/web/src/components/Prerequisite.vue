<template>
    <b-list-group id="prerequisite-list" flush data-cy="prerequisites">
      <div v-if="Object.keys(courses).length == 0" class="no-courses">
        There is no Prerequisite to display!  
      </div>
      <li v-for="course in courses" :key = "course">
        <row v-html=course /> 
      </li>
    </b-list-group>
  </template>
  
  <script>
  import "@/typedef";

  export default {
    name: "Prerequisites",
    components: {
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
  