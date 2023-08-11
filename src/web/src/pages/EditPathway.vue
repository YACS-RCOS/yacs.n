<template>
    <b-container class="mt-3">
      <section id="edits">
        <h2>Pathway Testing</h2>
        <div class="form-group">
          <label for="PathwayName">PathwayName:</label>
          <input
            v-model="PathwayName"
            type="text"
            class="form-control"
            id="PathwayName"
            placeholder="Enter a pathway name"
          />
        </div>
        <div class="form-group">
          <label for="CourseName">CourseName:</label>
          <input
            v-model="CourseName"
            type="text"
            class="form-control"
            id="CourseName"
            placeholder="Enter a course name"
          />
        </div>
        <div class="form-group">
          <label for="result">Result:</label>
          <p id="result">{{ this.result }}</p>
        </div>
        <button @click="getPathway()" class="btn btn-primary">Get Pathway</button>
        <button @click="getCourse()" class="btn btn-primary">Get Course</button>
        <button @click="addPathway()" class="btn btn-success">Add Pathway</button>
        <button @click="addCourse()" class="btn btn-success">Add Course</button>
        <button @click="removePathway()" class="btn btn-danger">Remove Pathway</button>
        <button @click="removeCourse()" class="btn btn-danger">Remove Course</button>
      </section>
    </b-container>
  </template>
  
  <script>
  import {
    getPathway,
    getCourse,
  } from "@/services/YacsService";

  import {
    addPathway,
    addCourse,
    removePathway,
    removeCourse,
  } from "@/services/AdminService";
  
  export default {
    name: "EditPathway",
    props: {},

    data() {
      return {
        pathway: "",
        course: "",
      };
    },
    

    methods: {
      getPathway() {
        console.log("getPathway");
        this.result = getPathway(this.course);
        console.log(this.result);
      },
      getCourse() {
        console.log("getCourse");
        this.result = getCourse(this.pathway);
        console.log(this.result);
      },
      removePathway() {
        console.log("removePathway");
        this.result = removePathway(this.pathway);
        console.log(this.result);
      },
      removeCourse() {
        console.log("removeCourse");
        this.result = removeCourse(this.course);
        console.log(this.result);
      },
      addPathway() {
        console.log("addPathway");
        this.result = addPathway(this.pathway);
        console.log(this.result);
      },
      addCourse() {
        console.log("addPathway");
        this.result = addCourse(this.course);
        console.log(this.result);
      },
    },
    
  };
  </script>
  

  <style lang="scss">
  $danger: #dc3545;
  $success: #28a745;
  $primary: #007bff;
  
  .btn-primary {
    border-radius: 0;
    padding: 10px 20px;
  }
  
  .btn-danger {
    border-radius: 0;
    padding: 10px 20px;
  }
  
  .btn-success {
    border-radius: 0;
    padding: 10px 20px;
  }
  
  .success {
    animation: success ease-in-out 2s;
  }
  
  .fail {
    animation: fail ease-in-out 2s;
  }
  
  @keyframes success {
    50% {
      background-color: $success;
    }
    to {
      background-color: $primary;
    }
  }
  
  @keyframes fail {
    50% {
      background-color: $danger;
    }
    to {
      background-color: $primary;
    }
  }
  </style>
  