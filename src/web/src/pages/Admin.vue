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
      v-b-modal.addPathwayDatabase
      class="text-primary d-block"
      style="cursor: pointer;"
    >
      Add Pathway Database
    </a>

    <a
      v-b-modal.createPathwayCoursesMaster
      class="text-primary d-block"
      style="cursor: pointer;"
    >
      Create Pathway Course Master Database
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
    <b-modal id="addPathwayDatabase" title="Add Pathway Database" size="xl">
      <AddPathways />
    </b-modal>
    <b-modal id="createPathwayCoursesMaster" title="Create Pathway Course Master Database" size="xl">
      <PathwayCoursesMaster />
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
import AddPathways from "@/pages/AddPathways";
import PathwayCoursesMaster from "@/pages/PathwayCoursesMaster";

export default {
  name: "AdminPage",
  components: {
    AddPathways,
    UploadCsv,
    EditSemesters,
    SetDefault,
    EditProfessors,
    PathwayCoursesMaster
    // ManageAccounts,
  },
  data() {
    return {};
  },
};
</script>
