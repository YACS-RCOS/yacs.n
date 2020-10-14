<template>
  <div id="header">
    <b-navbar toggleable="md" type="light" variant="light">
      <b-navbar-brand class="logo" href="#">YACS</b-navbar-brand>
      <b-nav-text class="semester">{{ selectedSemester }}</b-nav-text>
      <b-navbar-toggle target="header-navbar-collapse"></b-navbar-toggle>
      <b-collapse id="header-navbar-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item>
            <router-link :to="{ name: 'CourseScheduler' }">
              <font-awesome-icon :icon="faCalendar" />
              Schedule
            </router-link>
          </b-nav-item>
          <b-nav-item>
            <router-link :to="{ name: 'CourseExplorer' }">
              <font-awesome-icon :icon="faList" />
              Explore
            </router-link>
          </b-nav-item>
        </b-navbar-nav>
        <!-- If user has logged in -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown right v-if="sessionID !== null">
            <template v-slot:button-content>Hi, {{ userName }}</template>
            <b-dropdown-item @click="logOut">Sign Out</b-dropdown-item>
          </b-nav-item-dropdown>

          <!-- If user has not logged in -->
          <template v-else>
            <b-button v-b-modal.login-modal size="sm" variant="light">
              Log In
            </b-button>

            <b-button v-b-modal.signup-modal size="sm" variant="primary">
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
              <SignUpForm />
            </b-modal>
          </template>
          <b-nav-form>
            <b-form-checkbox
              class="dark-mode-switch"
              :checked="$store.state.darkMode"
              @change="toggle_style()"
              switch
            >
              <font-awesome-icon class="style-icon" :icon="faMoon" />
            </b-form-checkbox>
          </b-nav-form>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <hr />
  </div>
</template>

<script>
import { logout } from "@/services/UserService";

import {
  faMoon,
  faCog,
  faCalendar,
  faList,
} from "@fortawesome/free-solid-svg-icons";

import SignUpComponent from "@/components/SignUp";
import LoginComponent from "@/components/Login";

import { TOGGLE_DARK_MODE } from "@/store";

export default {
  name: "Header",
  props: {
    selectedSemester: String,
  },
  components: {
    SignUpForm: SignUpComponent,
    LoginForm: LoginComponent,
  },
  data() {
    return {
      faMoon,
      faCog,
      faCalendar,
      faList,
      isLoggedIn: false,
      sessionID: "",
      userName: "",
      semesterOptions: [],
    };
  },
  created() {
    this.sessionID = this.$cookies.get("sessionID");
    this.userName = this.$cookies.get("userName");

    if (this.sessionID == "") {
      console.log("not logged in");
    } else {
      console.log("sessionID", this.sessionID);
    }
  },
  methods: {
    toggle_style() {
      this.$store.commit(TOGGLE_DARK_MODE);
    },
    onLogIn() {
      this.$refs["login-modal"].hide();
    },
    logOut() {
      var sessionId = this.$cookies.get("sessionID");
      logout(sessionId).then(() => {
        this.$cookies.remove("sessionID");
        this.$cookies.remove("userID");
        location.reload();
      });
    },
  },
};
</script>

<style>
#header .navbar {
  background: white !important;
  margin-bottom: none !important;
}

#header .nav-item {
  text-align: center;
}

/* .semester {
  font-size: 18px;
  color: grey;
} */

.logo {
  font-size: 24px;
  vertical-align: middle;
}

hr {
  margin: 0em;
  border-width: 1px;
}

#signUpButton {
  margin-left: 20px;
}

.dark-mode-switch {
  margin-left: 1em;
}
</style>
