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
    <div class="buttonDiv" data-onsuccess="onSignIn"></div>
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
  mounted() {
    window.google.accounts.id.initialize({
      // FIXME: replace with relevenat client_id, this is just a test version
        client_id: "747784477249-pkqhk4sj2s6hhe1i3pa74k57d8c1mspv.apps.googleusercontent.com",
        callback: this.handleCredentialResponse
    });
    // FIXME: make the login button look better and adhere to local language and color theme. also center it.
    window.google.accounts.id.renderButton(
      document.getElementById("buttonDiv"),
      { theme: "outline", size: "large" }  // customization attributes
    );
    window.google.accounts.id.prompt(); // also display the One Tap dialog
  },
  methods: {
    // FIXME: network error with GET request on API
    onSignIn(googleUser) {
      var profile = googleUser.getBasicProfile();

      try {
        this.$bvToast.toast(`You are now logged in!`, {
          title: `Welcome ${profile.getName()}`,
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
    // FIXME: change scopes. make this act the same as a normal login. add logout functionality.
    handleCredentialResponse(response) {
      console.log("Encoded JWT ID token: " + response.credential);
      console.log(response)
    },
    async onSubmit(evt) {
      evt.preventDefault();
      
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
