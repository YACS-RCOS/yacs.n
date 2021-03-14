<template>
  <b-navbar
    id="header"
    class="bg-white"
    style="margin-bottom: 0 !important;"
    toggleable="md"
    type="primary"
    variant="light"
  >
    <b-navbar-brand
      class="align-middle text-dark"
      :to="{ name: 'CourseScheduler' }"
    >
      YACS
    </b-navbar-brand>
    <b-nav-text class="text-secondary">{{ selectedSemester }}</b-nav-text>
    <b-navbar-toggle
      id="header-navbar-collapse-toggle"
      target="header-navbar-collapse"
    >
      <font-awesome-icon icon="bars" />
    </b-navbar-toggle>
    <b-collapse id="header-navbar-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item :to="{ name: 'CourseScheduler' }">
          <font-awesome-icon icon="calendar" />
          Schedule
        </b-nav-item>
        <b-nav-item :to="{ name: 'CourseExplorer' }">
          <font-awesome-icon icon="list" />
          Explore
        </b-nav-item>
      </b-navbar-nav>
      <!-- If user has logged in -->
      <b-navbar-nav class="ml-auto">
        <b-nav-form id="darkmode-toggle-form" class="mr-md-2">
          <b-form-checkbox
            :checked="$store.state.darkMode"
            @change="toggle_style()"
            switch
          >
            <div>
              <!-- We need the outer div to keep the icon aligned with the checkbox -->
              <font-awesome-icon icon="moon" />
            </div>
          </b-form-checkbox>
        </b-nav-form>

        <b-nav-item-dropdown right v-if="isLoggedIn">
          <!-- Using 'button-content' slot -->
          <template v-slot:button-content>Hi, {{ user.name }}</template>
          <b-dropdown-item @click="logOut">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>

        <!-- If user has not logged in -->
        <template v-else>
          <b-button
            id="login-button"
            v-b-modal.login-modal
            size="sm"
            variant="secondary"
            class="mr-md-2"
          >
            Log In
          </b-button>

          <b-button
            id="signup-button"
            v-b-modal.signup-modal
            size="sm"
            variant="primary"
          >
            Sign Up
          </b-button>

          <b-modal
            id="login-modal"
            ref="login-modal"
            hide-footer
            title="Log In"
          >
            <LoginForm @submit="onLogIn()" />
          </b-modal>

          <b-modal id="signup-modal" hide-footer title="Sign Up">
            <SignUpForm @submit="onSignUp()" />
          </b-modal>
        </template>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
import { mapGetters, mapState } from "vuex";

import SignUpComponent from "@/components/SignUp";
import LoginComponent from "@/components/Login";

import { TOGGLE_DARK_MODE } from "@/store";

import { userTypes } from "../store/modules/user";

export default {
  name: "Header",
  components: {
    SignUpForm: SignUpComponent,
    LoginForm: LoginComponent,
  },

  methods: {
    toggle_style() {
      this.$store.commit(TOGGLE_DARK_MODE);
    },
    onLogIn() {
      this.$refs["login-modal"].hide();
    },
    onSignUp() {
      this.$refs["signup-modal"].hide();
    },
    async logOut() {
      try {
        await this.$store.dispatch(userTypes.actions.LOGOUT);

        this.$bvToast.toast(`You are now logged out!`, {
          variant: "success",
        });
      } catch (err) {
        this.$bvToast.toast(err, {
          title: "Failed to logout",
          variant: "danger",
        });
      }
    },
  },
  computed: {
    ...mapGetters({
      isLoggedIn: userTypes.getters.IS_LOGGED_IN,
      user: userTypes.getters.CURRENT_USER_INFO,
    }),
    ...mapState(["selectedSemester"]),
    ...mapState({ sessionId: userTypes.state.SESSION_ID }),
  },
};
</script>

<style lang="scss" scoped>
@include media-breakpoint-down(sm) {
  #login-button,
  #signup-button,
  #darkmode-toggle-form {
    // equivalent to mb-1
    margin-bottom: $spacer * 0.25;
    margin-top: $spacer * 0.25;
  }
}

#header {
  .nav-item {
    text-align: center;
  }
  // centering of the dark mode toggle
  .inline-form,
  .form-inline {
    justify-content: center;
  }
}

// no idea why but need to manually set this for it to show up
.dark #header-navbar-collapse-toggle {
  color: var(--dark-text-primary) !important;
}
</style>
