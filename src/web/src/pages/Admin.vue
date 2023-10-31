<template>
  <b-container>
    <h1>Admin Panel</h1>
    <hr />
    <br />

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

    <!-- Footer of Admin Panel -->
    <br />
    <hr />
    <br />

    <b-button href="/">Go back home</b-button>
  </b-container>
</template>

<script>
import UploadCsv from "@/pages/UploadCsv";
import EditSemesters from "@/pages/EditSemesters";
import SetDefault from "@/pages/SetDefault";
import EditProfessors from "@/pages/EditProfessors";
import UploadJson from "@/pages/UploadJson.vue";

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
    return {};
  },
};
</script>