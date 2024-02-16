<template>
  <b-form @submit="onSubmit" @reset="onReset" v-if="showForm">
    <b-form-group id="input-group-1" label="Email address:" label-for="input-1">
      <b-form-input
        id="input-1"
        v-model="form.email"
        type="email"
        required
        placeholder="Enter email"
      ></b-form-input>
    </b-form-group>

    <b-form-group id="input-group-2" label="Password:" label-for="input-2">
      <b-form-input
        id="input-2"
        type="password"
        v-model="form.password"
        required
        placeholder="Enter password"
      ></b-form-input>
    </b-form-group>
    <b-button type="submit" variant="primary">Submit</b-button>
    <b-button @click="initiateGoogleOneTap" variant="primary" style="margin-left: 10px;">Login with Google</b-button>
    <div>
      <b-button-group size="md">
        <button
          style="padding-left: 0; padding-right: 0; padding-top: 12px;"
          type="button"
          disabled="disabled"
          class="btn btn-link disabled"
        >
          New to YACS?
        </button>
        <b-button
          id="signup-button"
          v-b-modal.signup-modal
          variant="link"
          style="padding-top: 12px;"
        >
          Sign up now.
        </b-button>
        <b-modal id="signup-modal" hide-footer title="Sign Up">
          <SignUpForm @submit="onSignUp()" />
        </b-modal>
      </b-button-group>
    </div>
  </b-form>
</template>

<script>
import { mapGetters } from "vuex";
import SignUpComponent from "@/components/SignUp";
import { userTypes } from "../store/modules/user";

export default {
  name: "Login",
  components: {
    SignUpForm: SignUpComponent,
  },
  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      showForm: true,
    };
  },
  methods: {
    async onSubmit(evt) {
      if (evt) {
        evt.preventDefault();
      }
      try {
        await this.$store.dispatch(userTypes.actions.LOGIN, this.form);

        this.$bvToast.toast(`You are now logged in!`, {
          title: `Welcome ${this.user.name}`,
          variant: "success",
        });

        this.$emit("submit");
      } catch (err) {
        this.$bvToast.toast(err, {
          title: "Login failed!",
          variant: "danger",
        });
      }
    },
    onSignUp() {
      this.$refs["signup-modal"].hide();
    },
    initiateGoogleOneTap() {
        window.google.accounts.id.initialize({
            client_id: "833663758121-ff8hq6a8ibujhv969laf6h9edc000ad2.apps.googleusercontent.com",
            callback: this.handleGoogleResponse
        });

        window.google.accounts.id.prompt(); // This triggers the One Tap UI
    },

    async handleGoogleResponse(response) {
      // Extract user information from the ID token
      const idToken = response.credential;
      const decodedData = this.decodeIdToken(idToken);

      // Set the required form field values
      
      this.form.email = decodedData.email;
      this.form.password = decodedData.name+decodedData.email;

      // Automatically create the account
      await this.onSubmit();
    },

    decodeIdToken(token) {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonData = decodeURIComponent(atob(base64).split('').map(function(c) {
          return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }).join(''));
      return JSON.parse(jsonData);
    },
    onReset(evt) {
      evt.preventDefault();
      // Reset our form values
      this.form.email = "";
      this.form.password = "";
      // Trick to reset/clear native browser form validation state
      this.showForm = false;
      this.$nextTick(() => {
        this.showForm = true;
      });
    },
  },
  computed: {
    ...mapGetters({
      isLoggedIn: userTypes.getters.IS_LOGGED_IN,
      user: userTypes.getters.CURRENT_USER_INFO,
    }),
  },
};
</script>

<style></style>