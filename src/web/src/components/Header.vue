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
    <div>
      <b-dropdown
        variant="outline-primary"
        size="sm"
        :text="selectedSemester"
        class="m-md-2"
      >
        <b-dropdown-item
          v-for="option in semesterOptions"
          :key="option.value"
          :value="option.value"
          @click="selectSemester(option.value)"
        >
          {{ option.value }}
        </b-dropdown-item>
      </b-dropdown>
    </div>
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
        <b-nav-item :to="{ name: 'Pathway' }">
          <font-awesome-icon icon="list" />
          Pathways
        </b-nav-item>
        <b-nav-item :to="{ name: 'GPACalculator' }">
          <font-awesome-icon icon="list" />
          GPACalculator
        </b-nav-item>
      </b-navbar-nav>
      <!-- If user has logged in -->
      <b-navbar-nav class="ml-auto">
        <b-nav-form id="darkmode-toggle-form" class="mr-md-2">
          <b-form-checkbox
            :checked="$store.state.darkMode"
            :indeterminate="followDevice"
            @change="toggle_style()"
          ></b-form-checkbox>
          <font-awesome-icon @dblclick="toggle_default()" icon="moon" />
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

          <b-modal
            id="login-modal"
            ref="login-modal"
            hide-footer
            title="Log In"
          >
            <LoginForm @submit="onLogIn()" />
          </b-modal>
        </template>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
import {
  SELECT_SEMESTER,
  COOKIE_DARK_MODE,
  TOGGLE_DARK_MODE,
  SAVE_DARK_MODE,
  RESET_DARK_MODE,
} from "@/store";
import { mapState, mapActions, mapGetters } from "vuex";
import LoginComponent from "@/components/Login";
import { userTypes } from "../store/modules/user";
export default {
  name: "Header",
  components: {
    LoginForm: LoginComponent,
  },
  data() {
    return {
      followDevice: this.$cookies.get(COOKIE_DARK_MODE) === null,
    };
  },
  methods: {
    ...mapActions([SELECT_SEMESTER]),

    toggle_style() {
      if (this.$cookies.get(COOKIE_DARK_MODE) === null) {
        this.notifyOnToggle();
      }
      this.$store.commit(TOGGLE_DARK_MODE);
      this.$store.commit(SAVE_DARK_MODE);
      this.followDevice = false;
    },
    toggle_default() {
      if (this.$cookies.get(COOKIE_DARK_MODE) !== null) {
        this.notifyOnDefault();
      }
      this.$store.commit(RESET_DARK_MODE);
      this.followDevice = true;
      this.$store.commit(TOGGLE_DARK_MODE);
    },
    onLogIn() {
      this.$refs["login-modal"].hide();
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
    notifyOnToggle() {
      this.$bvToast.toast(
        `Double click moon icon to follow device's color scheme.`,
        {
          title: "Color Scheme Changed",
          autoHideDelay: 2000,
          noHoverPause: true,
          variant: "info",
        }
      );
    },
    notifyOnDefault() {
      this.$bvToast.toast(`Toggled to follow device color.`, {
        title: "Color Scheme Changed",
        autoHideDelay: 1000,
        noHoverPause: true,
        variant: "success",
      });
    },
  },
  computed: {
    ...mapGetters({
      isLoggedIn: userTypes.getters.IS_LOGGED_IN,
      user: userTypes.getters.CURRENT_USER_INFO,
    }),
    ...mapState({ sessionId: userTypes.state.SESSION_ID }),
    ...mapState(["semesters", "selectedSemester"]),

    semesterOptions() {
      return this.semesters.map(({ semester }) => ({
        text: semester,
        value: semester,
      }));
    },
  },
};
</script>

<style lang="scss" scoped>
@include media-breakpoint-down(sm) {
  #login-button,
  #darkmode-toggle-form {
    // equivalent to mb-1
    margin-bottom: $spacer * 0.25;
    margin-top: $spacer * 0.25;
  }
}
#header {
  .navbar-brand {
    font-size: 25px;
    font-weight: bold;
  }
  .nav-item {
    text-align: center;
  }
  .navbar-nav {
    font-size: 17px;
    font-weight: normal;
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
