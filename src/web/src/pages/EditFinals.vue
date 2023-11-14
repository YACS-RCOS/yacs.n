<template>
  <b-container class="mt-3">
    <section id="edits">
      <h2>Finals Testing</h2>
      <!-- user can input the following fields to edit the finals -->
      <div class="form-group">
        <label for="deparmtent">Department:</label>
        <input
          v-model="deparmtent"
          type="text"
          class="form-control"
          id="department"
          placeholder="Enter Department"
        />
      </div>
      <div class="form-group">
        <label for="courseCode">Course Code:</label>
        <input
          v-model="courseCode"
          type="text"
          class="form-control"
          id="courseCode"
          placeholder="Enter Course Code"
        />
      </div>
      <div class="form-group">
        <label for="section">Section:</label>
        <input
          v-model="section"
          type="text"
          class="form-control"
          id="section"
          placeholder="Enter Section"
        />
      </div>
      <div class="form-group">
        <label for="room">Room:</label>
        <input
          v-model="room"
          type="text"
          class="form-control"
          id="room"
          placeholder="Enter Room"
        />
      </div>
      <div class="form-group">
        <label for="dayOfWeek">Day Of Week:</label>
        <input
          v-model="dayOfWeek"
          type="text"
          class="form-control"
          id="dayOfWeek"
          placeholder="Enter Day Of Week"
        />
      </div>
      <div class="form-group">
        <label for="day">Day:</label>
        <input
          v-model="day"
          type="text"
          class="form-control"
          id="day"
          placeholder="Enter Day"
        />
      </div>
      <div class="form-group">
        <label for="hour">Hour:</label>
        <input
          v-model="hour"
          type="text"
          class="form-control"
          id="hour"
          placeholder="Enter Hour"
        />
      </div>
      <form @submit.prevent="add_bulk_final">
         <input type="file" name="file" />
         <input type="submit"/>
      </form>
      <!-- <div class="form-group">
        <label for="file">File:</label>
        <input
          type="file"
          class="form-control-file"
          id="file"
          placeholder="Upload File"
        />
      </div> -->
      <div class="form-group">
        <label for="updateColumn">Update Column:</label>
        <input
          v-model="updateColumn"
          type="text"
          class="form-control"
          id="updateColumn"
          placeholder="Enter Column Name"
        />
      </div>
      <div class="form-group">
        <label for="updateVal">Update Value:</label>
        <input
          v-model="updateVal"
          type="text"
          class="form-control"
          id="updateVal"
          placeholder="Enter Update Value"
        />
      </div>
      <div class="form-group">
        <label for="result">Result:</label>
        <p id="result">{{ this.result }}</p>
      </div>
      <!-- buttons to make relevant API calls -->
      <button @click="get_all_final_info()" class="btn btn-primary">Get All Finals</button>
      <button @click="get_info_by_DOW()" class="btn btn-primary">Get Final by DayOfWeek</button>
      <button @click="get_info_by_courseCode()" class="btn btn-primary">Get Final by CourseCode</button>
      <button @click="get_info_by_courseCodeSection()" class="btn btn-primary">Get Final by CourseCodeSection</button>
      <button @click="get_info_by_day()" class="btn btn-primary">Get Final by Day</button>
      <button @click="get_info_by_department()" class="btn btn-primary">Get Final by Department</button>
      <button @click="get_info_by_hour()" class="btn btn-primary">Get Final by Hour</button>
      <button @click="get_info_by_room()" class="btn btn-primary">Get Final by Room</button>
      <button @click="add_final()" class="btn btn-success">Add Final</button>
      <button @click="add_bulk_final()" class="btn btn-success">Add Bulk Final</button>
      <button @click="remove_final()" class="btn btn-danger">Remove Final</button>
      <button @click="remove_bulk_final()" class="btn btn-danger">Remove Bulk Final</button>
      <button @click="update_final()" class="btn btn-primary">Update Final</button>
    </section>
  </b-container>
</template>

<!-- import API calls -->
<script>
import {
  get_all_final_info,
  get_info_by_courseCode,
  get_info_by_courseCodeSection,
  get_info_by_day,
  get_info_by_department,
  get_info_by_DOW,
  get_info_by_hour,
  get_info_by_room,
} from "@/services/YacsService";
import {
  add_bulk_final,
  remove_bulk_final,
  add_final,
  remove_final,
  update_final,
} from "@/services/AdminService";


export default {
  name: "EditFinals",
  props: {},
  data() {
    return {
      deparmtent: "",
      courseCode: "",
      section: "",
      room: "",
      dayOfWeek: "",
      day: "",
      hour: "",
    };
  },
  // method behavior definitions
  methods: {
    get_all_final_info() {
      console.log("get_all_final_info");
      this.result = get_all_final_info();
      console.log(this.result);
    },
    get_info_by_DOW() {
      console.log("get_info_by_DOW");
      this.result = get_info_by_DOW(this.dayOfWeek);
      console.log(this.result);
    },
    get_info_by_courseCode() {
      console.log("get_info_by_courseCode");
      this.result = get_info_by_courseCode(this.courseCode);
      console.log(this.result);
    },
    get_info_by_courseCodeSection() {
      console.log("get_info_by_courseCodeSection");
      this.result = get_info_by_courseCodeSection(this.courseCode, this.section);
      console.log(this.result);
    },
    get_info_by_day() {
      console.log("get_info_by_day");
      this.result = get_info_by_day(this.day);
      console.log(this.result);
    },
    get_info_by_department() {
      console.log("get_info_by_department");
      this.result = get_info_by_department(this.deparmtent);
      console.log(this.result);
    },
    get_info_by_hour() {
      console.log("get_info_by_hour");
      this.result = get_info_by_hour(this.hour);
      console.log(this.result);
    },
    get_info_by_room() {
      console.log("get_info_by_room");
      this.result = get_info_by_room(this.room);
      console.log(this.result);
    },
    add_final() {
      console.log("add_final");
      let str = this.deparmtent + "," + this.courseCode + "," + this.section + "," + this.room + "," + this.dayOfWeek + "," + this.day + "," + this.hour;
      this.result = add_final(str);
      //this.result = add_final(this.deparmtent, this.courseCode, this.section, this.room, this.dayOfWeek, this.day, this.hour)
      console.log(this.result);
    },
    remove_bulk_final() {
      console.log("remove_bulk_final");
      this.result = remove_bulk_final(this.file);
      console.log(this.result);
    },
    remove_final() {
      console.log("remove_final");
      this.result = remove_final(this.courseCode, this.section);
      console.log(this.result);
    },
    update_final() {
      console.log("update_final");
      this.result = update_final(this.courseCode, this.section, this.updateColumn, this.updateVal);
      console.log(this.result);
    },
    add_bulk_final() {
      console.log("add_bulk_final");
      let formData = new FormData(this.file);
      this.result = add_bulk_final(formData);
      console.log(this.result);
    }
  },
};
</script>

<!-- button click graphics -->
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
