<template>
  <b-container class="mt-3">
    <section id="edits">
      <h2>Finals Testing</h2>
      <div class="form-group">
        <label for="email">Email:</label>
        <input
          v-model="email"
          type="email"
          class="form-control"
          id="email"
          placeholder="Enter email"
        />
      </div>
      <div class="form-group">
        <label for="rcs">RCS:</label>
        <input
          v-model="rcs"
          type="text"
          class="form-control"
          id="rcs"
          placeholder="Enter RCS"
        />
      </div>
      <div class="form-group">
        <label for="department">Department:</label>
        <input
          v-model="department"
          type="text"
          class="form-control"
          id="department"
          placeholder="Enter department"
        />
      </div>
      <div class="form-group">
        <label for="addMsg">Add message:</label>
        <input
          v-model="addMsg"
          type="text"
          class="form-control"
          id="addMsg"
          placeholder="Enter message"
        />
      </div>
      <div class="form-group">
        <label for="result">Result:</label>
        <p id="result">{{ this.result }}</p>
      </div>
      <button @click="getProf()" class="btn btn-primary">Get Prof</button>
      <button @click="getProfName()" class="btn btn-primary">
        Get Prof Name
      </button>
      <button @click="getProfDepartment()" class="btn btn-primary">
        Get Prof Department
      </button>
      <button @click="getOfficeHours()" class="btn btn-primary">
        Get Prof Office Hours
      </button>
      <button @click="getProfNumberByEmail()" class="btn btn-primary">
        Get Prof Number By Email
      </button>
      <button @click="get_professor_info_by_rcs()" class="btn btn-primary">
        Get Prof By Rcs
      </button>
      <button @click="getProfByEmail()" class="btn btn-primary">
        Get Prof By Email
      </button>
      <button @click="addProf()" class="btn btn-success">Add Prof</button>
      <button @click="addProfTest()" class="btn btn-success">
        Add Prof Test
      </button>
      <button @click="BulkAdd()" class="btn btn-success">Bulk Add</button>
      <button @click="removeProf()" class="btn btn-danger">Remove Prof</button>
      <button @click="BulkDelete()" class="btn btn-danger">Bulk Delete</button>
    </section>
  </b-container>
</template>

<script>
import {
  getProfessors,
  get_professor_name_by_email,
  get_professor_from_department,
  get_office_hours,
  get_professor_phone_number_by_email,
  get_professor_info_by_rcs,
  get_professor_info_by_email,
} from "@/services/YacsService";
import {
  remove_professor,
  addProfessors,
  addProfessorsTest,
} from "@/services/AdminService";

export default {
  name: "EditFinals",
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
  methods: {
    getProf() {
      console.log("getProfessors");
      this.result = getProfessors();
      console.log(this.result);
    },
    getProfName() {
      console.log("get_professor_name");
      this.result = get_professor_name_by_email(this.email);
      console.log(this.result);
    },
    getProfDepartment() {
      console.log("get_professor_from_department");
      this.result = get_professor_from_department(this.department);
      console.log(this.result);
    },
    getOfficeHours() {
      console.log("get_office_hours");
      this.result = get_office_hours(this.email);
      console.log(this.result);
    },
    getProfNumberByEmail() {
      console.log("get_professor_phone_number_by_email");
      this.result = get_professor_phone_number_by_email(this.email);
      console.log(this.result);
    },
    get_professor_info_by_rcs() {
      console.log("get_professor_info_by_rcs");
      this.result = get_professor_info_by_rcs(this.rcs);
      console.log(this.result);
    },
    getProfByEmail() {
      console.log("get_professor_info_by_email");
      this.result = get_professor_info_by_email(this.email);
      console.log(this.result);
    },
    removeProf() {
      console.log("remove_professor");
      this.result = remove_professor(this.email);
      console.log(this.result);
    },
    addProf() {
      console.log("addProfessors");
      this.result = addProfessors(this.addMsg);
      console.log(this.result);
    },
    addProfTest() {
      console.log("addProfessorsTest");
      this.result = addProfessorsTest();
      console.log(this.result);
    },
    BulkAdd() {
      console.log("BulkAdd");
    },
    BulkDelete() {
      console.log("BulkDelete");
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
