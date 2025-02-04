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
      () => {
        toast.success(`Upload Success!`);
      }
    "
    @upload-error="
      (e) => {
        for (const error of e) {
          toast.error(
            `Error uploading ${error.reason[0]}: ${error.reason[1][1].response?.data ?? error.reason[1][1].message}`
          );
        }
      }
    "
  />
</template>
