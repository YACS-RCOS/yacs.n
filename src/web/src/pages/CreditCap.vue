<template>
  <b-container class="mt-3">
    <h2>Enter the Credit Cap and Warning Message </h2>
    <form @submit="onUpdate" class="form-group" method="post">
      <p>Enter the credit cap</p>
      <input v-model="credit_cap" placeholder="Credit Cap">
      <p>Enter the warning message</p>
      <input v-model="warning_message" placeholder="Warning Message">
      <br />
      <br />
      <input type="Submit" class="btn btn-success btn-sm" value="Submit" />
    </form>
    <b-spinner v-show="loading" />
  </b-container>
</template>

<script>
import { uploadCreditCap } from "@/services/AdminService";

export default {
  name: "CreditCap",
  props: {},
  components: {
  },
  data() {
    return{
      loading: false,
      credit_cap: 0,
      warning_message: "",
    };
  },
  methods:{
    onUpdate(event){
      event.preventDefault();
      this.loading = true;
      uploadCreditCap(this.credit_cap, this.warning_message)
      .then((response) => {
        console.log(response);
        this.$bvToast.toast(`successfully set credit cap to ${this.credit_cap}`, {
          title: "Upload Result",
          variant: "info",
          noAutoHide: false,
        });
        this.loading = false;
      })
      .catch((error) => {
        console.log(error.response);
        this.$bvToast.toast(
          `HTTP ${error.response.status}: ${error.response.data}`,
          {
            title: "Update Result",
            variant: "danger",
            noAutoHide: true,
          }
        );
        this.loading = false;
      });
    }
  },
};
</script>