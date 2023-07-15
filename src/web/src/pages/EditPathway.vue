<template>
    <b-container class="mt-3">
      <section id="edits">
        <h2>Pathway Testing</h2>
        <div class="form-group">
          <label for="Name">Name:</label>
          <input
            v-model="name"
            type="text"
            class="form-control"
            id="name"
            placeholder="Enter name"
          />
        </div>
        <div class="form-group">
          <label for="Required">Required:</label>
          <input
            v-model="Required"
            type="text"
            class="form-control"
            id="Required"
            placeholder="Enter a course"
          />
        </div>
        <div class="form-group">
          <label for="ChooseOne">Choose one of the following:</label>
          <input
            v-model="ChooseOne"
            type="text"
            class="form-control"
            id="ChooseOne"
            placeholder="Enter a course"
          />
        </div>
        <div class="form-group">
          <label for="ChooseOther">Choose other one of the following:</label>
          <input
            v-model="ChooseOther"
            type="text"
            class="form-control"
            id="ChooseOther"
            placeholder="Enter a course"
          />
        </div>
        <div class="form-group">
          <label for="ChooseRemaining">Choose remaining credits from:</label>
          <input
            v-model="ChooseRemaining"
            type="text"
            class="form-control"
            id="ChooseRemaining"
            placeholder="Enter a course"
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
  import {
    
  } from "@/services/YacsService";
  
  export default {
    name: "EditProfessors",
    props: {},
    data() {
      return {
        name: "",
        
      };
    },
    /*   functions not defined yet
    methods: {
      getPathway() {
        console.log("getPathway");
        this.result = getPathway();
        console.log(this.result);
      },
      getPathwayName() {
        console.log("get_pathway_name");
        this.result = get_pathway_name_by_email(this.email);
        console.log(this.result);
      },
      removePathway() {
        console.log("remove_pathway");
        this.result = remove_pathway(this.email);
        console.log(this.result);
      },
      addPathway() {
        console.log("addPathway");
        this.result = addPathway(this.addMsg);
        console.log(this.result);
      },
      addPathwayTest() {
        console.log("addPathwayTest");
        this.result = addPathwayTest();
        console.log(this.result);
      },
    },
    */
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
  