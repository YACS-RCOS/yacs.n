<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <b-container v-if="isLoggedIn" id="user-info-box" class="border align-content-center">
      <h1 class="text-center">Hi, {{ form.name }}!</h1>
      <b-row v-for="(data, label) in userData" :key="label" class="user-row">
        <b-col>
          {{ rendername(label) }}:
        </b-col>

        <b-form v-if="data.editing" inline @submit.prevent="doneedit(label)">
          <b-col>
            <b-input
              :ref="label"
              v-model="currentinput[label]"
              :type="data.type"
              required
            ></b-input>
          </b-col>
          <b-col>
            <b-button
              type="submit"
            >Done
            </b-button
            >
          </b-col>
        </b-form>

        <template v-else>
          <b-col>
            {{ rendervalue(form[label.toLowerCase()]) }}
          </b-col>
          <b-col>
            <b-button
              @click="addedit(label)"
            >Edit
            </b-button>
          </b-col>
        </template>
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
      form: {}, //this will populate itself
      currentinput: {}
    };
  },
  mounted() {
    if (!this.isLoggedIn) {
      router.push("/");
    }
    this.form = Object.assign({}, this.user);
    this.currentinput = Object.assign({}, this.user);
    console.log(this.form);

    let temp = {};
    for (const lab of [{ name: "text" }, { email: "email" }, { phone: "tel" }]) {
      const x = Object.keys(lab)[0];
      temp[x] = { editing: false, type: lab[x] };
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
      this.$nextTick(() => {
        console.log(val);
      });
    },
    rendername(value) {
      return value[0].toUpperCase() + value.substring(1);
    },
    rendervalue(value) {
      if (value === undefined || value.length == 0) {
        return "<not set>";
      } else {
        return value;
      }
    },
    addedit(val) {
      this.userData[val].editing = true;
    },
    doneedit(val) {
      this.userData[val].editing = false;
    },
    checkInput(input, type) {
      switch (type) {
        case "email":
          return document.getEle;
      }
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

#user-info-box .user-row {
  margin-bottom: 0.2em;
}

</style>

<!-- make changes readonly by default, add edit button, list classes taken-->