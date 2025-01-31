<script setup lang="ts">
import * as api from "@/api/admin";
import UploadModal from "@/components/modals/UploadModal.vue";
</script>

<template>
  <UploadModal
    accept-file-types="text/csv"
    title="Upload Courses CSV"
    :action="
      (v) =>
        api.upload_course_csv(v).catch((e) => {
          throw [v.name, e];
        })
    "
  />
</template>
