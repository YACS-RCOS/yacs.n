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
  </b-form>
</template>

<script>
import { mapGetters } from "vuex";

import { userTypes } from "../store/modules/user";

export default {
  name: "Login",
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
