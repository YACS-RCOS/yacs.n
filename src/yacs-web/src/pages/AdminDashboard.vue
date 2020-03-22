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
      </template>
        <b-tab title="Dashboard">
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
          <UploadCsvPage v-if="type === 'csv'"
            @loading="childComponentLoadingResource"
            @loadfinish="childComponentFinishedLoadingResource"
          />
          <DatePage v-else-if="type === 'date'"
            @loading="childComponentLoadingResource"
            @loadfinish="childComponentFinishedLoadingResource"
          />
        </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import { faCog } from '@fortawesome/free-solid-svg-icons';
import { faGraduationCap } from '@fortawesome/free-solid-svg-icons';
import UploadCsvPage from '@/pages/UploadCsv';
import DatePage from '@/pages/MapDates';
import AdminPageLink from '@/components/AdminPageLink';

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
      activeTabIndex: 1
    };
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
      console.log(currentTabs, previousTabs);
      this.activeTabIndex = this.tabs.length;
      // Why is the <a> tag hidden away in so many layers? No idea, haha!
      currentTabs[this.tabs.length].bvTabs.$refs.buttons[this.tabs.length].$refs.link.$el.focus();
    },
    closeTab(index) {
      this.tabs.splice(index, 1);
    }
  },
  created() {}
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
  }
}
.smaller {
  background: rgba(255,255,0, 1);
  color: black;
  z-index: 0;
  display: block;
  border-radius: 10%;
  font-weight: 500;
  margin-top: 5px;
  padding: 2px;
}
</style>