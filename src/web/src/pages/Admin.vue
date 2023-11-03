<template>
  <b-container>
    <br><b-button href="/">Go back home</b-button><br>
    <h2 style="text-align: center;">Admin Panel</h2>
    <br /><hr /><h2>Operations</h2><hr /><br />

    <a v-b-modal.csvModal class="text-primary d-block" style="cursor: pointer;">
      Import Courses via CSV
    </a>
    <a
      v-b-modal.editSemestersModal
      class="text-primary"
      style="cursor: pointer;"
    >
      Edit Semesters
    </a>
    <a
      v-b-modal.defaultModal
      class="text-primary d-block"
      style="cursor: pointer;"
    >
      Set Default Semester
    </a>
    <a
      v-b-modal.editProfessors
      class="text-primary d-block"
      style="cursor: pointer;"
    >
      Edit Professors
    </a>
    <a
      v-b-modal.jsonModal
      class="text-primary d-block"
      style="cursor: pointer;"
    >
      Import Professors via JSON
    </a>

    <b-modal id="csvModal" title="Import Courses via CSV" size="xl">
      <UploadCsv />
    </b-modal>
    <b-modal id="editSemestersModal" title="Edit Semesters" size="xl">
      <EditSemesters />
    </b-modal>
    <b-modal id="defaultModal" title="Set Default Semester" size="xl">
      <SetDefault />
    </b-modal>
    <b-modal id="editProfessors" title="Edit Professors" size="xl">
      <EditProfessors />
    </b-modal>
    <b-modal id="jsonModal" title="Import Professors via JSON" size="xl">
      <UploadJson />
    </b-modal>
    <br /><hr /><h2>Statistics</h2><hr /><br />
    Total Users: {{ this.total_users }}<br>
    Logged-in Users: {{ this.num_sessions }}<br>
    <br>
    Current Number of people on the site:
    Network bandwith:
    <br>
    Total Courses:<br>
    Last update:<br>
    <br />
    <hr />
    <br />
  </b-container>
</template>

<script>
import UploadCsv from "@/pages/UploadCsv";
import EditSemesters from "@/pages/EditSemesters";
import SetDefault from "@/pages/SetDefault";
import EditProfessors from "@/pages/EditProfessors";
import UploadJson from "@/pages/UploadJson.vue";

import { getUserStats } from "@/services/UserService";
import {getSessionStats} from "@/services/AdminService";

export default {
  name: "AdminPage",
  components: {
    UploadCsv,
    EditSemesters,
    SetDefault,
    EditProfessors,
    UploadJson,
    // ManageAccounts,
  },
  data() {
    return {
      total_users:"",
      num_sessions:"",
    };
  },
  mounted() {
    //setInterval(() => {
      this.getUserStats();
    //}, 1000);
  },
  methods: {
    async getUserStats() {
      console.log("here")
      let userStats=await getUserStats();
      let sessionStats=await getSessionStats();
      this.total_users = userStats.data.content.total_users;
      this.num_sessions = sessionStats.data.content.num_sessions;
    },
  },
};
</script>
