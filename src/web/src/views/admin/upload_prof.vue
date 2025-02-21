<script setup lang="ts">
import * as api from "@/api/admin";
import UploadModal from "@/components/modals/UploadModal.vue";
import { toast } from "vue3-toastify";
</script>

<template>
  <UploadModal
    accept-file-types="application/json"
    title="Upload Professors JSON"
    :action="
      (v) =>
        api.upload_prof_json(v).catch((error) => {
          throw [v.name, error];
        })
    "
    @upload-success="
      (f) => {
        toast.success(`Successfully uploaded ${f}!`);
      }
    "
    @upload-error="
      (error) => {
        toast.error(
          `Error uploading ${error[0]}: ${error[1].response?.data ?? error[1].message}`,
          { autoClose: 60000 }
        );
      }
    "
  />
</template>
