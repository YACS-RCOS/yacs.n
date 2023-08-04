<template>
    <b-modal ref="my-modal">
      <div class="block text-left" v-if="getPath != null" md="10">
        <h3
          class="text-center"
          style="color: #007bff; margin-top: -5px; margin-bottom: 5px;"
        >
          {{ getPath.Name[0] }}
        </h3>
        <br />
        <div v-for="(item, itemName) in getPath" :key="itemName">
          <h4 style="color: #3395ff; margin-top: -20px;">
            {{ itemName + ": " }}
          </h4>
          <li
            v-for="course in item"
            :key="course"
            v-on:click="goPage(course)"
            class="courseInPath"
          >
            {{ course }}
          </li>
          <br />
        </div>
      </div>
    </b-modal>

    <b-row>
      <b-col
        v-for="(catCol, index) in categoryCols"
        :key="`catCol-${index}`"
        md="6"
        v-show="coursesShow"
      >
        <b-row
          v-for="categoryObj in catCol"
          :key="categoryObj['Category Name'][0]"
          class="categoryBox border m-2 mb-4"
        >
          <b-col>
            <b-row class="category-title">
              <h3 class="m-1 ml-2">
                {{ categoryObj["Category Name"][0] }}
              </h3>
            </b-row>
            <b-row>
              <div class="d-flex flex-column flex-grow-1">
                <div
                  v-for="pathway in categoryObj['Pathways']"
                  :key="pathway['Name'][0]"
                  role="tablist"
                >
                  <div class="mt-1 mb-1 w-100">
                      {{ pathway["Name"][0] }}
                  </div>
                </div>
              </div>
            </b-row>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
  
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
        console.log("remove_pathway");
        this.result = removePathway(this.course);
        console.log(this.result);
      },
      removeCourse() {
        console.log("remove_course");
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
  