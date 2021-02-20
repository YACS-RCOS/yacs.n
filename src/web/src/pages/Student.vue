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
import { mapGetters } from "vuex";

import HeaderComponent from "@/components/Header";
import FooterComponent from "@/components/Footer";
import { getDefaultSemester } from "@/services/AdminService";
import { userTypes } from "@/store/modules/user";

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
    
    const courses = await getCourses(this.selectedSemester);
    this.$store.commit(SET_COURSE_LIST, courses);

    try {
      if (!this.isLoggedIn) {
        await this.$store.dispatch(userTypes.actions.LOAD_SESSION_COOKIE);
      }
      // eslint-disable-next-line no-empty
    } catch {}
  },
  methods: {
    updateSelectedSemester(newSemester) {
      this.selectedSemester = newSemester;
    },
  },
  computed: {
    ...mapGetters({
      isLoggedIn: userTypes.getters.IS_LOGGED_IN,
    }),
  },
};
</script>

<style lang="scss">
footer {
  margin: 0px !important;
}
</style>
