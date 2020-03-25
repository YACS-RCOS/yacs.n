<template>
  <b-container>
    <h1>Admin Panel</h1>
    <hr />
    <UploadCsv />
  </b-container>
</template>

<script>
import UploadCsv from '@/pages/UploadCsv'

export default {
  name: 'AdminPage',
  components: {
    UploadCsv
  },
  data() {
    return {}
  }
};
</script>
