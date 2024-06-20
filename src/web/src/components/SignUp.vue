<template>
  <div>
    <b-form @submit.prevent="onSubmit" v-if="show">
      <b-form-group id="input-group-2" label="Full Name:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.name"
          required
          placeholder="Enter name"
        ></b-form-input>
      </b-form-group>

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

      <!-- <b-form-group id="input-group-3" label="Phone Number:" label-for="input-3">
        <b-form-input id="input-3" v-model="form.phone" required placeholder="Enter your phone number"></b-form-input>
      </b-form-group> -->

      <b-form-group id="input-group-4" label="Password:" label-for="input-4">
        <b-form-input
          type="password"
          id="input-4"
          v-model="form.password"
          required
          placeholder="Enter your password"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-5" label="Degree:" label-for="input-5">
        <b-form-select
          id="input-5"
          v-model="form.degree"
          :options="degrees"
        ></b-form-select>
      </b-form-group>

      <b-form-group id="input-group-6" label="Major:" label-for="input-6">
        <b-form-input
          id="input-6"
          v-model="form.major"
          placeholder="Eg. CSCI or ITWS"
        ></b-form-input>
      </b-form-group>

      <button type="submit" class="btn-primary btn w-100">
        Finish Sign Up!
      </button>
      <button @click="initiateGoogleOneTap" class="btn-primary btn w-100 mt-2">
        Sign Up with Google
      </button>
    </b-form>
  </div>
</template>

<script>
import { signup } from "@/services/UserService";
import { userTypes } from "../store/modules/user";

export default {
  name: "SignUp",
  data() {
    return {
      form: {
        email: "",
        name: "",
        phone: "",
        password: "",
        degree: "",
        major: "",
      },
      degrees: [
        { text: "Select One", value: null },
        "Undergraduate",
        "Graduate",
      ],
      show: true,
    };
  },
  methods: {
    async onSubmit() {
      let {
        data: { success, errMsg },
      } = await signup(this.form);

      if (!success) {
        this.$bvToast.toast(errMsg || "Unknown error", {
          title: "Signup failed!",
          variant: "danger",
          noAutoHide: true,
        });
        this.$emit("submit");
        return;
      }

      try {
        await this.$store.dispatch(userTypes.actions.LOGIN, {
          email: this.form["email"],
          password: this.form["password"],
        });
      } catch (err) {
        this.$bvToast.toast(err, {
          title: "Login failed!",
          variant: "danger",
          noAutoHide: true,
        });
      }

      this.$emit("submit");
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
      this.form.name = decodedData.name;
      this.form.email = decodedData.email;
      // Note: Ideally, you shouldn't set a password for users signing in with Google.
      // For this demonstration, I'm using the ID token, but consider changing this approach.
      this.form.password = (decodedData.name+decodedData.email).replace(/\s+/g, '');
      this.form.degree = "Undergraduate";
      this.form.major = "CSCI";

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
    }
  },
};
</script>
