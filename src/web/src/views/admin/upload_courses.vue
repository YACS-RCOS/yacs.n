<script setup lang="ts">
import * as api from "@/api/admin";
import UploadModal from "@/components/modals/UploadModal.vue";
import { toast } from "vue3-toastify";
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
    @upload-success="
      (f) => {
        toast.success(`Successfully uploaded ${f}!`);
      }
    "
    @upload-error="
      (error) => {
        toast.error(`Error uploading ${error[0]}: ${error[1].response?.data ?? error[1].message}`, {
          autoClose: 60000
        });
      }
    "
  />
</template>
