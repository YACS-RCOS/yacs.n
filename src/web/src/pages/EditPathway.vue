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
        <button @click="getPathName()" class="btn btn-primary">
          Get Pathway Name
        </button>
        <button @click="addPathway()" class="btn btn-success">Add Pathway</button>
        <button @click="addPathwayTest()" class="btn btn-success">
          Add Pathway Test
        </button>
        <button @click="removePathway()" class="btn btn-danger">Remove Pathway</button>
      </section>
    </b-container>
  </template>
  
  <script>
  import json from "./pathwayV2.json";

  import {
    getPathway,
    getCourses,
  } from "@/services/YacsService";

  import {
    removePathway,
    removeCourse,
    addPathway,
    addCourse,
  } from "@/services/AdminService";
  
  export default {
    name: "EditPathway",
    props: {},

    data() {
      return {
        categories: json,
        coursesShow: true,
      };
    },
    computed: {
      categoryCols() {
        let ret = [];
        let col1 = [];
        let col2 = [];
        for (var i = 0; i < this.categories.length; i++) {
          if (i < this.categories.length / 2) {
            col1.push(this.categories[i]);
          } else {
            col2.push(this.categories[i]);
          }
        }
        ret.push(col1);
        ret.push(col2);
        return ret;
      },
    },
    /*
    data() {
      return {
        course: "",
        
      };
    },
    */

    methods: {
      listCourse() {
        this.coursesShow = false;
        this.pathwaysShow = false;
      },
      getPathway() {
        console.log("getPathway");
        this.result = getPathway();
        console.log(this.result);
      },
      getCourse() {
        console.log("getCourse");
        this.result = getCourse(this.course);
        console.log(this.result);
      },
      removePathway() {
        console.log("removePathway");
        this.result = removePathway(this.course);
        console.log(this.result);
      },
      removeCourse() {
        console.log("removeCourse");
        this.result = removePathway(this.course);
        console.log(this.result);
      },
      addPathway() {
        console.log("addPathway");
        this.result = addPathway();
        console.log(this.result);
      },
      addCourse() {
        console.log("addPathway");
        this.result = addPathway();
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
  