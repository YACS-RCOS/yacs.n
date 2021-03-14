<template>
  <div>
    <Header class="mb-3"></Header>
    <router-view />
    <Footer />
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { SELECT_SEMESTER } from "@/store";
import HeaderComponent from "@/components/Header";
import FooterComponent from "@/components/Footer";
import { userTypes } from "@/store/modules/user";

export default {
  name: "StudentPage",
  components: {
    Header: HeaderComponent,
    Footer: FooterComponent,
  },
  async created() {
    try {
      if (!this.isLoggedIn) {
        await this.$store.dispatch(userTypes.actions.LOAD_SESSION_COOKIE);
      }
      // eslint-disable-next-line no-empty
    } catch {}

    await this.$store.dispatch(SELECT_SEMESTER, this.$route.query.semester);
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
