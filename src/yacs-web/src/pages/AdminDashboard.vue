<template>
  <div>
    <b-tabs
      fill
      active-nav-item-class="active-tab"
    >
      <template v-slot:tabs-start>
        <div class="brand-container text-white d-flex align-items-center pr-2">
          <font-awesome-icon :icon="cog" :class="{
            'nav-branding-icon': true,
            'ml-2': true,
            'loading': loading
          }"/>
          <h2 class="py-2 pl-2 mb-0">
            <span class="brand-name">YACS</span>
            <span class="smaller">Admin</span>
          </h2>
        </div>
      </template>
      <b-tab title="Dashboard">
        <b-container class="d-flex justify-content-around mt-3">
          <b-card no-body class="bg-primary text-white text-center justify-content-center d-flex" style="height:200px; width:200px;" @click="addTab($event, 'csv')">
            <span>CSV</span>
          </b-card>
          <b-card no-body class="bg-success text-white text-center justify-content-center d-flex" style="height:200px; width:200px;" @click="addTab($event, 'date')">
            <span>Dates</span>
          </b-card>
        </b-container>
      </b-tab>
      <b-tab v-for="(type, index) in tabs" :key="index" :title="type" lazy>
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
import UploadCsvPage from '@/pages/UploadCsv';
import DatePage from '@/pages/MapDates';

export default {
  name: 'AdminPage',
  components: {
    UploadCsvPage,
    DatePage
  },
  data() {
    return {
      cog: faCog,
      loading: false,
      tabs: []
    };
  },
  methods: {
    childComponentLoadingResource () {
      this.loading = true;
    },
    childComponentFinishedLoadingResource () {
      this.loading = false;
    },
    addTab(_, type) {
      this.tabs.push(type);
    }
  },
  created() {}
};
</script>

<style lang="scss">
$tabBorderWidth: 2px;
$tabBorderColor: #ccc;
$navbarBgColor: #A62639;
$tabBgColor: rgb(185, 45, 66);
$tabActiveBgColor: #DB324D;
$tabActiveFgColor: #FAFAFA;
$tabHoverBgColor: rgb(209, 49, 73);

ul.nav-tabs {
  background-color: $navbarBgColor;
  border: none;
}
li {
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
  &.nav-branding-icon {
    will-change: transform;
  }
  & > svg.nav-branding-icon:hover {
    animation: spin forwards linear 1s;
  }
  & > svg.nav-branding-icon.loading {
    animation: spin forwards linear 2s infinite;
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
@keyframes spin {
  to {
    transform: rotate3d(0, 0, 1, 360deg);
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
  // box-shadow: -1px 1px 9px 1px white;
  padding: 2px;
}
</style>