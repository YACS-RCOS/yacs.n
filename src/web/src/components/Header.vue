<template>
  <div id="header">
    <b-navbar type="light" variant="light">
      <b-navbar-brand class="logo" href="#">YACS</b-navbar-brand>
      <div class="semester">{{ selectedSemester }}</div>
      <b-navbar-nav>
        <b-nav-item>
          <router-link :to="{ name: 'CourseScheduler' }">
            Schedule
          </router-link>
        </b-nav-item>
        <b-nav-item>
          <router-link :to="{ name: 'CourseExplorer' }">
            Explore
          </router-link>
        </b-nav-item>
      </b-navbar-nav>
      <!-- If user has logged in -->
      <b-navbar-nav class="ml-auto" v-if="sessionID !== null">
        <b-nav-item-dropdown right>
          <!-- Using 'button-content' slot -->
          <template v-slot:button-content>Hi, {{ userName }}</template>
          <!-- <b-dropdown-item href="#">Profile</b-dropdown-item> -->
          <b-dropdown-item @click="logOut">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>

      <!-- If user has not logged in -->
      <b-navbar-nav class="ml-auto" v-if="sessionID === null">
        <div>
          <b-button v-b-modal.login-modal size="sm" variant="light">
            Log In
          </b-button>

          <b-button
            v-b-modal.signup-modal
            size="sm"
            variant="primary"
            class="ml-2"
          >
            Sign Up
          </b-button>

          <b-modal
            id="login-modal"
            ref="login-modal"
            hide-footer
            title="Log In"
          >
            <b-form @submit="onSubmit" @reset="onReset" v-if="showForm">
              <b-form-group
                id="input-group-1"
                label="Email address:"
                label-for="input-1"
              >
                <b-form-input
                  id="input-1"
                  v-model="form.email"
                  type="email"
                  required
                  placeholder="Enter email"
                ></b-form-input>
              </b-form-group>

              <b-form-group
                id="input-group-2"
                label="Password:"
                label-for="input-2"
              >
                <b-form-input
                  id="input-2"
                  type="password"
                  v-model="form.password"
                  required
                  placeholder="Enter password"
                ></b-form-input>
              </b-form-group>

              <b-button type="submit" variant="primary">Submit</b-button>
            </b-form>
          </b-modal>

          <b-modal id="signup-modal" hide-footer title="Sign Up">
            <SignUpForm></SignUpForm>
          </b-modal>
        </div>
      </b-navbar-nav>
      <b-form-checkbox
        class="dark-mode-switch"
        v-model="darkModeEnabled"
        switch
      >
        <font-awesome-icon v-if="darkModeEnabled" :icon="faMoon" />
        <font-awesome-icon v-if="!darkModeEnabled" :icon="faSun" />
      </b-form-checkbox>
    </b-navbar>
    <hr />
  </div>
</template>

<script>
import { login, logout } from "@/services/UserService";

import { faMoon, faSun } from "@fortawesome/free-solid-svg-icons";

import SignUpComponent from "@/components/SignUp";

export default {
  name: "Header",
  props: {
    selectedSemester: String,
  },
  components: {
    SignUpForm: SignUpComponent,
  },
  data() {
    return {
      faMoon,
      faSun,
      form: {
        email: "",
        password: "",
      },

      isLoggedIn: false,
      sessionID: "",
      userName: "",
      showForm: true,
      semesterOptions: [],
      darkModeEnabled: this.$cookies.get("darkMode"),
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
  watch: {
    darkModeEnabled (newVal) {
      this.$store.commit("setDarkMode", newVal);
    }
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      let userInfo = this.form;
      console.log(userInfo);

      login(userInfo)
        .then((response) => {
          console.log(response);
          this.$cookies.set("sessionID", response.data.content["sessionID"]);
          this.$cookies.set("userName", response.data.content["userName"]);
          this.$cookies.set("userID", response.data.content["uid"]);
          location.reload();
        })
        .catch((error) => {
          console.log(error.response);
          this.$bvToast.toast(
            `Login Unsuccesful. Please double check your email and password, then try again!`,
            {
              title: "Invalid login",
              variant: "danger",
              noAutoHide: true,
            }
          );
        });
      this.$refs["login-modal"].hide();
    },
    onReset(evt) {
      evt.preventDefault();
      // Reset our form values
      this.form.email = "aaa1@wa.com";
      this.form.password = "123456";
      // Trick to reset/clear native browser form validation state
      this.showForm = false;
      this.$nextTick(() => {
        this.showForm = true;
      });
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
.navbar {
  background: white !important;
  margin-bottom: none !important;
}

.semester {
  font-size: 18px;
  color: grey;
}

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
