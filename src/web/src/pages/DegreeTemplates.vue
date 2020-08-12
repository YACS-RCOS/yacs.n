<template>
  <div>
    <p>hi welcome to degree templates</p>
  </div>
</template>

<script>
import { getDegreeTemplate } from "../services/YacsService";
export default {
  name: "DegreeTemplates",
  data() {
    return {
      templates: [],
    };
  },

  created() {
    getDegreeTemplate().then((list) => {
      this.templates = list;
    });
  },
};
</script>

<style></style>
