<template>
  <b-container class="mt-3">
    <h2>Enter the Credit Cap and Warning Message </h2>
    <form @submit="onUpdate" class="form-group" method="post">
      <p>Enter the credit cap</p>
      <input v-model="credit_cap" placeholder="Credit Cap">
      <p>Enter the warning message</p>
      <input v-model="warning_message" placeholder="Warning Message">
      <input type="Submit" class="btn btn-success btn-sm" value="Submit" />
    </form>
  </b-container>
</template>

<script>

export default {
  name: "CreditCap",
  props: {},
  components: {
  },
  data() {
    return{
      credit_cap: 0,
      warning_message: "",
    };
  },
  methods:{
    onUpdate(event){
      event.preventDefault();
      console.log(this.credit_cap);
      console.log(this.warning_message);
    }
  },
};
</script>