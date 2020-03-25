<template>
  <div>
    <b-tabs
      fill
      active-nav-item-class="active-tab"
      v-model="activeTabIndex"
      @changed="activateNewTab"
    >
      <template v-slot:tabs-start>
        <div class="brand-container text-white d-flex align-items-center pr-2">
          <font-awesome-icon :icon="cap" :class="{
            'nav-branding-icon': true,
            'ml-2': true
          }"/>
          <h2 class="py-2 pl-2 mb-0">
            <span class="brand-name">YACS</span>
            <span class="smaller">Admin</span>
          </h2>
        </div>
        <b-progress max="100" class="progress-override" animated>
          <!-- Display each progress bar at 90% of its potential 1/3 until the timeout period between concurrent requests expires (that nstate.timeoutExpired) -->
          <b-progress-bar :value="100*!!currentRequestNum*(1/3)*((!!nstate.timeoutExpired+9)/10)" class="bg-primary">Request ({{ currentRequestNum }})</b-progress-bar>
          <b-progress-bar :value="100*(currentInFlightRequestNum/currentRequestNum)*(1/3)*((!!nstate.timeoutExpired+9)/10)" class="bg-warning text-dark">In-Flight ({{currentInFlightRequestNum}})</b-progress-bar>
          <b-progress-bar :value="100*(currentRequestRespondedNum/currentRequestNum)*(1/3)*((!!nstate.timeoutExpired+9)/10)" class="bg-success">Response ({{currentRequestRespondedNum}})</b-progress-bar>
        </b-progress>
      </template>
      <b-tab>
        <template v-slot:title>
          <font-awesome-icon :icon="faHome" />&nbsp; Dashboard
        </template>
        <b-container fluid class="d-flex mt-3 flex-wrap">
          <AdminPageLink
            v-for="(type, index) in defaultLinks"
            :key="index"
            :type="type"
            @click="addTab"
          />
        </b-container>
      </b-tab>
      <b-tab v-for="(type, index) in tabs" :key="index" lazy>
        <template v-slot:title>
          {{ type }} <button class="btn closeBtn" @click="closeTab(index)">X</button>
        </template>
        <b-container fluid>
          <UploadCsvPage v-if="type === 'csv'"
            @loading="childComponentLoadingResource"
            @loadfinish="childComponentFinishedLoadingResource"
          />
          <DatePage v-else-if="type === 'date'"
            @loading="childComponentLoadingResource"
            @loadfinish="childComponentFinishedLoadingResource"
          />
        </b-container>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
// TODO [ ] Fix close button on tab so height doesn't change.
//      [ ] Make close button on tab look better
//      [ ] Make progress bar overhead functional
//          [X] Display # of request in certain state numbers
//          [ ] Upon completion of a series of requests, given a timeout period of
//              2 seconds or so, assume all requests were part of a 'block' and mark the
//              job as complete (*indicate success*). It is possible that a user is actually
//              a professional QA tester and will try making requests from different tabs
//              at the same time. The load bar will accomodate for this by having this intermission period.
//      [X] Figure out scaling of progress bar at lower resolutions
//      [X] Would be nice to have the home tab be smaller than the rest... (Can set home tab to have "flex: 0 1 auto" since it's using flex grow for the fill)
//      [ ] Modal or tooltip on click of info icon for Admin card
//      [ ] General Settings Admin card. Possible options: "open tab on card click", "theme"
//      [ ] Should each card have its own possible options menu? Cog on bottom of card
import { faCog, faGraduationCap, faHome } from '@fortawesome/free-solid-svg-icons';
import UploadCsvPage from '@/pages/UploadCsv';
import DatePage from '@/pages/MapDates';
import AdminPageLink from '@/components/AdminPageLink';
import Vue from 'vue';

export default {
  name: 'AdminPage',
  components: {
    UploadCsvPage,
    DatePage,
    AdminPageLink
  },
  data() {
    return {
      cog: faCog,
      loading: false,
      tabs: [],
      cap: faGraduationCap,
      defaultLinks: ['csv', 'date'],
      activeTabIndex: 1,
      tabsLoaded: false,
      faHome,
      nstate: Vue.prototype.nstate
    }
  },
  computed: {
    currentRequestNum() {
      return this.nstate.currentRequests;
    },
    currentInFlightRequestNum() {
      return this.nstate.currentRequestsInFlight;
    },
    currentRequestRespondedNum() {
      return this.nstate.currentResponses;
    }
  },
  methods: {
    childComponentLoadingResource () {
      this.loading = true;
    },
    childComponentFinishedLoadingResource () {
      this.loading = false;
    },
    addTab(type) {
      this.tabs.push(type);
    },
    activateNewTab(currentTabs, previousTabs) {
      if (currentTabs.length > 0) {
        // Make dashboard button not part of tabs to automatically fill empty space
        if(!this.tabsLoaded) currentTabs[0].bvTabs.$refs.buttons[0].$el.style.flex = "0 1 auto";
        console.log(currentTabs, previousTabs);
        this.activeTabIndex = this.tabs.length;
        // Why is the <a> tag hidden away in so many layers? No idea, haha!
        currentTabs[this.tabs.length].bvTabs.$refs.buttons[this.tabs.length].$refs.link.$el.focus();
      }
    },
    closeTab(index) {
      this.tabs.splice(index, 1);
    }
  },
  mounted() {
    console.log(Vue.nstate);
  }
};
</script>

<style lang="scss" scoped>
$tabBorderWidth: 2px;
$tabBorderColor: #ccc;
$navbarBgColor: #A62639;
$tabBgColor: rgb(185, 45, 66);
$tabActiveBgColor: #DB324D;
$tabActiveFgColor: #FAFAFA;
$tabHoverBgColor: rgb(209, 49, 73);

// https://vue-loader.vuejs.org/guide/scoped-css.html#child-component-root-elements
::v-deep ul.nav-tabs {
  background-color: $navbarBgColor;
  border: none;
  box-shadow: 0px -6px 35px 1px #0009;
}
::v-deep .tab-content {
  display: block !important;
}
::v-deep li {
  &.nav-item {
    margin-top: auto;
  }
  &.nav-item > a.nav-link {
    background-color: $tabBgColor;
    color: white !important;
    margin-bottom: 1px;
    border-radius: 0% !important;
    border-right: solid black 1px !important;
  }
  &.nav-item > a.nav-link:not(.active) {
    border-bottom: $tabBorderColor 3px solid !important;
    border-width: 0px 0px $tabBorderWidth 0px !important;
  }
  &.nav-item > a:hover {
    background-color: $tabHoverBgColor;
  }
  &.nav-item > a.nav-link:not(.active) {
    font-style: italic;
  }
  &.nav-item > a.active-tab {
    color: $tabActiveFgColor !important;
    background-color: $tabActiveBgColor !important;
    border-color: $tabBorderColor $tabBorderColor transparent $tabBorderColor !important;
    border-width: $tabBorderWidth $tabBorderWidth 0 $tabBorderWidth !important;
  }
}
::v-deep .progress-override {
  position: absolute;
  top: 22px;
  height: 24px;
  // Full height
  // border-radius: 0;
  // top: 0;
  // height: 49px;
  // border: solid black 2px;
  border-width: 0 2px 2px 2px;
  left: 142px;
  width: calc(100% - 142px);
}
div.brand-container {
  & {
    border-bottom: $tabBorderColor 3px solid !important;
    border-width: 0px 0px $tabBorderWidth 0px !important;
    font-size: 2em;
  }
  & > h2 {
    line-height: 2rem;
    text-align: center;
    display: flex;
    flex-flow: column nowrap;
    background: $navbarBgColor;
  }
  & > h2 span.brand-name {
    font-variant: all-petite-caps;
    font-weight: 400;
  }
  & > h2 span.brand-name ~ span {
    font-size: 1.7rem;
    font-weight: 300;
    background: rgba(255,255,0, 1);
    color: black;
    z-index: 0;
    display: block;
    border-radius: 10%;
    margin-top: 5px;
    padding: 2px;
  }
}
</style>