<template>
    <b-container class="mt-3">
      <section id="edits">
        <h2>Professor Edits</h2>
        <p>email: <input v-model="email"> </p>
        <p>crn: <input v-model="rcs"> </p>
        <p>department: <input v-model="department"> </p>
        <p>addMsg: <input v-model="addMsg"> </p>
        <p>
          return value: {{this.result}}
        </p>
        <button @click="getProf()">getProf </button>
        <button @click="getProfName()">getProfName</button>
        <button @click="getProfDepartment()">getProfDepartment</button>
        <button @click="getOfficeHours()">getProfDepartment</button>
        <button @click="getProfEmail()">getProfDepartment</button>
        <button @click="getProfByRcs()">getProfDepartment</button>
        <button @click="getProfByEmail()">getProfDepartment</button>
        <button @click="removeProf()">removeProf</button>
        <button @click="addProf()">addProf</button>
        <button @click="addProfTest()">addProfTest</button>
      </section>
    </b-container>
  </template>
  
  <script>
  import { getProfessors,get_professor_name,get_professor_from_department,get_office_hours,get_professor_phone_number_by_email,get_professor_info_by_rcs, get_professor_info_by_email} from "@/services/YacsService";
  import { remove_professor,addProfessors,addProfessorsTest } from "@/services/AdminService";


  export default {
    name: "EditProfessors",
    props: {},
    data() {
      return {
        email: "",
        rcs: "",
        department: "",
        addMsg: "",
        result: "",
      };
    },
    methods:{
      getProf(){
        console.log("getProfessors");
        result = getProfessors();
        console.log(result)
      },
      getProfName(){
        console.log("get_professor_name");
        result = get_professor_name(this.email);
        console.log(result)
      },
      getProfDepartment(){
        console.log("get_professor_from_department");
        result = get_professor_from_department(this.department);
        console.log(result)
      },
      getProfName(){
        console.log("get_professor_name");
        result = get_professor_name(this.email);
        console.log(result)
      },
      getOfficeHours(){
        console.log("get_office_hours");
        result = get_office_hours(this.email);
        console.log(result)
      },
      getProfEmail(){
        console.log("get_professor_phone_number_by_email");
        result = get_professor_phone_number_by_email(this.email);
        console.log(result)
      },
      getProfByRcs(){
        console.log("get_professor_info_by_rcs");
        result = get_professor_info_by_rcs(this.rcs);
        console.log(result)
      },
      getProfByEmail(){
        console.log("get_professor_info_by_email");
        result = get_professor_info_by_email(this.email);
        console.log(result)
      },
      removeProf(){ 
        console.log("remove_professor");
        result = remove_professor(this.email);
        console.log(result)
      },
      addProf(){
        console.log("addProfessors");
        result = addProfessors(addMsg);
        console.log(result)
      },
      addProfTest(){
        console.log("get_professor_from_department");
        result = addProfessorsTest();
        console.log(result)
      }
    }
  };
  </script>
  
  <style lang="scss">
  $danger: #dc3545;
  $success: #28a745;
  $primary: #007bff;
  
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
  