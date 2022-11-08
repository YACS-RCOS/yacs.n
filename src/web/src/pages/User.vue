<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <b-container v-if="isLoggedIn" id="user-info-box" class="border align-content-center">
      <h1 class="text-center">Hi, {{ user.name }}!</h1>
      <b-row v-for="(editing, label) in userData" :key="label" class="user-row">
        <b-col>
          {{ rendername(label) }}:
        </b-col>

        <b-col v-if="editing == false">
          {{ rendervalue(form[label.toLowerCase()]) }}
        </b-col>

         <b-col v-else-if="editing == true">
          Insert editing form here
        </b-col>

        <b-col v-if="editing == false">
          <b-button
            @click="addedit(label)"
          >Edit
          </b-button>
        </b-col>

        <b-col v-if="editing == true">
          <b-button
            @click="doneedit(label)"
          >Done
          </b-button>
        </b-col>
      </b-row>
    </b-container>
    <h1 v-else class="text-center">You should log in first.</h1>
  </b-container>
</template>

<script>
import { userTypes } from "@/store/modules/user";
import { mapGetters } from "vuex";
// import DegreePicker from "@/components/DegreePicker";
import router from "@/routes";

export default {
  name: "User",
  // components: { DegreePicker },
  data() {
    return {
      breadcrumbNav: [
        {
          text: "YACS",
          to: "/"
        },
        {
          text: "User"
        }
      ],
      userData: {},
      form: {} //this will populate itself
    };
  },
  mounted() {
    if (!this.isLoggedIn) {
      router.push("/");
    }
    this.form = Object.assign({}, this.user);
    console.log(this.form);

    let temp = {};
    for(const lab of ["name", "email", "phone"]){
      temp[lab] = false
    }
    this.userData = temp;
  },
  computed: {
    ...mapGetters({
      isLoggedIn: userTypes.getters.IS_LOGGED_IN,
      user: userTypes.getters.CURRENT_USER_INFO
    })
  },
  methods: {
    log(...val) {
      console.log(val);
    },
    rendername(value){
      return value[0].toUpperCase() + value.substring(1);
    },
    rendervalue(value) {
      if (value === undefined || value.length == 0) {
        return "<not set>";
      }
      else{
        return value;
      }
    },
    addedit(val){
      this.userData[val] = true;
    },
    doneedit(val){
      this.userData[val] = false;
    },
    async onSubmit() {

    }
  }
};
</script>

<style scoped>
#user-info-box {
  padding: 1em;
  margin-top: 2em;
  margin-bottom: 2em;
  width: 50%;
  min-width: max-content;

}

#user-info-box .user-row{
  margin-bottom: 0.2em;
}

</style>

<!-- make changes readonly by default, add edit button, list classes taken-->