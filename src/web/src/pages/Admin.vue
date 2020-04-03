<template>
  <b-container>
    <h1>Admin Panel</h1>
    <hr><br>

    <a v-b-modal.csvModal class="text-primary d-block" style="cursor: pointer;">
      Import Courses via CSV
    </a>
    <a v-b-modal.dateRangeNameBindingModal class="text-primary" style="cursor: pointer;">
      Rename Semesters Parts
    </a>
    <a v-b-modal.defaultModal class="text-primary d-block" style="cursor: pointer;">
      Set Default Semester
    </a>

    <b-modal id="csvModal" title="Import Courses via CSV" size="xl">
      <UploadCsv />
    </b-modal>
    <b-modal id="dateRangeNameBindingModal" title="Rename Semester Parts" size="xl">
      <MapDates />
    </b-modal>
    <b-modal id="defaultModal" title="Set Default Semester" size="xl">
      <SetDefault />
    </b-modal>

    <!-- Footer of Admin Panel -->
    <br><hr><br>
    <b-button href='/'>Go back home</b-button>

  </b-container>
</template>

<script>
import UploadCsv from '@/pages/UploadCsv'
import MapDates from '@/pages/MapDates'
import SetDefault from '@/pages/SetDefault'

export default {
  name: 'AdminPage',
  components: {
    UploadCsv,
    MapDates,
    SetDefault
  },
  data() {
    return {}
  }
};
</script>
