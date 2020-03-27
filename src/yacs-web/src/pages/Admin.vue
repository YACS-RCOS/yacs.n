<template>
  <b-container>
    <h1>Admin Panel</h1>
    <hr />
    <a v-b-modal.csvModal class="text-primary d-block" style="cursor: pointer;">Import courses via CSV</a>
    <a v-b-modal.dateRangeNameBindingModal class="text-primary" style="cursor: pointer;">Assign semester part name to date ranges</a>
    <b-modal id="csvModal" title="Import Course CSV" size="xl">
      <UploadCsv />
    </b-modal>
    <b-modal id="dateRangeNameBindingModal" title="Assign semester part name to date range" size="xl">
      <MapDates />
    </b-modal>
  </b-container>
</template>

<script>
import UploadCsv from '@/pages/UploadCsv'
import MapDates from '@/pages/MapDates'

export default {
  name: 'AdminPage',
  components: {
    UploadCsv,
    MapDates
  },
  data() {
    return {}
  }
};
</script>
