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
import { login } from "@/services/UserService";

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
          console.error(error.response);
          this.$bvToast.toast(
            `Login Unsuccesful. Please double check your email and password, then try again!`,
            {
              title: "Invalid login",
              variant: "danger",
              noAutoHide: true,
            }
          );
        });
      this.$emit("submit");
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
};
</script>

<style></style>
