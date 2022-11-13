<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <b-container v-if="isLoggedIn" id="user-info-box" class="border">
      <h1 class="text-center">Hi, {{ form.name }}!</h1>
      <b-row v-for="(data, label) in userData" :key="label" class="user-row">
        <b-form inline style="width: 100%" @submit.prevent="stopediting(label)">
          <b-col>
            {{ rendername(label) }}:
          </b-col>
          <template v-if="data.editing">
            <b-col>
              <b-input
                :ref="label"
                v-model="currentinput[label]"
                :type="data.type"
                :required="data.required"
              ></b-input>
            </b-col>
            <b-col>
              <b-button
                type="submit"
              >Done
              </b-button
              >
            </b-col>
          </template>
          <template v-else>
            <b-col>
              {{ rendervalue(form[label]) }}
            </b-col>
            <b-col>
              <b-button
                @click.prevent="startediting(label)"
              >Edit
              </b-button>
            </b-col>
          </template>
        </b-form>
      </b-row>
      <b-row class="user-row">
        <b-col>
          Current Degree:
        </b-col>
        <b-col>
          {{currentinput.degree}}
          <br>
          {{currentinput.major}}
        </b-col>
        <b-col>
          <b-button v-b-modal.degreepicker>Edit</b-button>
        </b-col>
      </b-row>
      <b-row style="margin-top: 1em">
        <b-button class="align-self-center m-auto">Submit Changes</b-button>
      </b-row>

    </b-container>
    <h1 v-else class="text-center">You should log in first.</h1>
    <b-modal id="degreepicker" size="xl">
    <DegreePicker
      :major="currentinput.major"
      :degree="currentinput.degree"
    ></DegreePicker>
  </b-modal>
  </b-container>
</template>

<script>
import { userTypes } from "@/store/modules/user";
import { mapGetters } from "vuex";
import DegreePicker from "@/components/DegreePicker";
import router from "@/routes";

export default {
  name: "User",
  components: { DegreePicker },
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
      userData: {
        name: { type: "text", required: true, editing: false },
        email: { type: "email", required: true, editing: false },
        phone: { type: "tel", editing: false }
      },
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
    startediting(val) {
      this.userData[val].editing = true;
    },
    stopediting(val) {
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
  padding: 1em;
  margin: 0.2em 0em;
}

#user-info-box .user-row *{
  justify-content: center !important;
  text-align: center;
  display: flex;
  align-self: baseline;
}

</style>

<!-- make changes readonly by default, add edit button, list classes taken-->