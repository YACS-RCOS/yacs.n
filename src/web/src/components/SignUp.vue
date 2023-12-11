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

      <degree-picker
        :degree="form.degree"
        :major="form.major"
        @update:degree="newval => form.degree = newval"
        @update:major="newval => form.major = newval"
      ></degree-picker>

      <button class="btn-primary btn w-100" type="submit">
        Finish Sign Up!
      </button>
    </b-form>
  </div>
</template>

<script>
import { signup } from "@/services/UserService";
import { userTypes } from "../store/modules/user";
import DegreePicker from "@/components/DegreePicker";

export default {
  name: "SignUp",
  components: { DegreePicker },
  data() {
    return {
      form: {
        email: "",
        name: "",
        phone: "",
        password: "",
        degree: "",
        major: [null]
      },
      show: true
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
    }
  },
};
</script>