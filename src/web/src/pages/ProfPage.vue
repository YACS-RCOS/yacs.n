<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <div v-if="prof" class="w-90 ml-4 mb-4">
      <b-row>
        <b-col>
          <h1 class="mt-4">{{ prof.Name }}</h1>
          <h4 class="mb-1">{{ prof.Title }}</h4>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <br />
          <h6 class="mb-1 d-inline">Department: {{prof.Department}}</h6>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <h6 class="mb-1 d-inline">School: {{prof.Portfolio}}</h6>
        </b-col>
      </b-row>
      <b-row>
        <b-col class="mb-4">
          <br />
          <h6 class="mb-1 d-inline">Contact Info</h6>
          <!-- <li>Phone: {{prof.Phone}}</li> -->
          <li> Email: 
          <a v-bind:href="'mailto:' + prof.Email">{{prof.Email}}</a>
          </li>
          <li> Faculty Page: 
          <a v-bind:href="prof['Profile Page']">{{prof['Profile Page']}}</a>
          </li>
        </b-col>
      </b-row>

      <b-button @click="$router.go(-1)">Back</b-button>
    </div>
    <CenterSpinner
      v-else
      :height="80"
      :fontSize="1.4"
      loadingMessage="Professor"
      :topSpacing="30"
    />
  </b-container>
</template>

<script>
import json from "./Professors.json";
import CenterSpinnerComponent from "../components/CenterSpinner.vue";

export default {
  components: {
    CenterSpinner: CenterSpinnerComponent,
  },
  name: "ProfPage",
  data() {
    return {
      rcs: this.$route.params.rcs,
      breadcrumbNav: [
        {
          text: "YACS",
          to: "/",
        },
        {
          text: "Professors",
          to: "/professor",
        },
        {
          text: this.$route.params.rcs,
        },
      ],
      professors: json,
    };
  },
  computed: {
    prof() {
      return this.professors.find(
        (p) => p.Email.replace("@rpi.edu", "") === this.rcs
      );
    },
  },
};
</script>
