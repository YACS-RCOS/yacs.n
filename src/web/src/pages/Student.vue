<template>
  <div>
    <Header class="mb-3" :selectedSemester="selectedSemester"></Header>
    <router-view :selected-semester="selectedSemester" />
    <Footer
      :selectedSemester="selectedSemester"
      @changeSelectedSemester="updateSelectedSemester"
    />
  </div>
</template>

<script>
import HeaderComponent from "@/components/Header";
import FooterComponent from "@/components/Footer";
import { getDefaultSemester } from "@/services/AdminService";

export default {
  name: "StudentPage",
  components: {
    Header: HeaderComponent,
    Footer: FooterComponent,
  },
  data() {
    return {
      selectedSemester: "",
    };
  },
  async created() {
    const querySemester = this.$route.query.semester;

    this.selectedSemester =
      querySemester && querySemester != "null"
        ? querySemester
        : await getDefaultSemester();
  },
  methods: {
    updateSelectedSemester(newSemester) {
      this.selectedSemester = newSemester;
    },
  },
};
</script>

<style lang="scss">
footer {
  margin: 0px !important;
}
</style>
