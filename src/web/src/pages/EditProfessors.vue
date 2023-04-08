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
        <button @click="getOfficeHours()">getProfOfficeHours</button>
        <button @click="getProfNumberByEmail()">getProfNumberByEmail</button>
        <button @click="getProfByRcs()">getProfByRcs</button>
        <button @click="getProfByEmail()">getProfByEmail</button>
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
      //works
      getProf(){
        console.log("getProfessors");
        this.result = getProfessors();
        console.log(this.result)
      },
      //works  
      getProfName(){
      console.log("get_professor_name");
        this.result = get_professor_name_by_email(this.email);
        console.log(this.result)
      },
      //works
      getProfDepartment(){
        console.log("get_professor_from_department");
        this.result = get_professor_from_department(this.department);
        console.log(this.result)
      },
      //works
      getOfficeHours(){
        console.log("get_office_hours");
        this.result = get_office_hours(this.email);
        console.log(this.result)
      },
      //works
      getProfNumberByEmail(){
        console.log("get_professor_phone_number_by_email");
        this.result = get_professor_phone_number_by_email(this.email);
        console.log(this.result)
      },
      //works
      getProfByRcs(){
        console.log("get_professor_info_by_rcs");
        this.result = get_professor_info_by_rcs(this.rcs);
        console.log(this.result)
      },
      //works
      getProfByEmail(){
        console.log("get_professor_info_by_email");
        this.result = get_professor_info_by_email(this.email);
        console.log(this.result)
      },
      removeProf(){ 
        console.log("remove_professor");
        this.result = remove_professor_by_email(this.email);
        console.log(this.result)
      },
      //works
      addProf(){
        console.log("addProfessors");
        this.result = addProfessors(this.addMsg);
        console.log(this.result)
      },
      addProfTest(){
        console.log("addProfessorsTest");
        this.result = addProfessorsTest();
        console.log(this.result)
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
  