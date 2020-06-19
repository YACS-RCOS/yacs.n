<template>
  <div>
    <Header class="mb-3" :currentSemester="currentSemester"></Header>
    <router-view :current-semester="currentSemester" />
    <Footer
      :semester="currentSemester"
      @changeCurrentSemester="updateCurrentSemester"
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
      currentSemester: "",
    };
  },
  async created() {
    const querySemester = this.$route.query.semester;

    this.currentSemester =
      querySemester && querySemester != "null"
        ? querySemester
        : await getDefaultSemester();
  },
  methods: {
    updateCurrentSemester(newSemester) {
      this.currentSemester = newSemester;
    },
  },
};
</script>

<style lang="scss">
footer {
  margin: 0px !important;
}
</style>
