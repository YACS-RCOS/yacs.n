<template>
  <div>
    <Header class="mb-3" />
    <router-view />
    <Footer />
  </div>
</template>

<script>
import { mapGetters } from "vuex";

import HeaderComponent from "@/components/Header";
import FooterComponent from "@/components/Footer";

import { SELECT_SEMESTER } from "@/store";
import { userTypes } from "@/store/modules/user";

export default {
  name: "StudentPage",
  components: {
    Header: HeaderComponent,
    Footer: FooterComponent,
  },
  computed: {
    ...mapGetters({
      isLoggedIn: userTypes.getters.IS_LOGGED_IN,
    }),
  },
  async created() {
    console.log(this.$route.query.semester);
    await this.$store.dispatch(SELECT_SEMESTER, this.$route.query.semester);

    try {
      if (!this.isLoggedIn) {
        await this.$store.dispatch(userTypes.actions.LOAD_SESSION_COOKIE);
      }
      // eslint-disable-next-line no-empty
    } catch {}
  },
};
</script>

<style lang="scss">
footer {
  margin: 0px !important;
}
</style>
