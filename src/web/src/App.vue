<template>
  <div
    id="root"
    :class="$store.state.darkMode ? 'dark' : 'light'"
  >
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
  components: {},
  created () {
    this.$store.commit("setDarkMode", this.$cookies.get("darkMode") == 'true');
  },
};
</script>

<style lang="scss">
#root,
html,
body {
  height: 100%;
}

.custom-select {
    transition: 0s;
  }

.dark {
  --dark-primary: #22252e;
  --dark-secondary: #181a21;
  --dark-text: #e6e4e4;
  --dark-text-secondary: #777777;
  background-color: var(--dark-primary) !important;
  color: var(--dark-text) !important;
  .navbar {
    background-color: var(--dark-primary) !important;
  }
  .py-3 {
    background-color: var(--dark-primary) !important;
  }
  #main-block {
    background: var(--dark-primary) !important;
  }
  #credits {
    background: var(--dark-primary) !important;
  }
  #footer {
    background: var(--dark-primary) !important;
  }
  .bg-light {
    background-color: var(--dark-secondary) !important;
  }
  .card {
    background: var(--dark-primary) !important;
    .card-header {
      background: var(--dark-primary) !important;
    }
  }
  .nav-link.active {
    background-color: var(--dark-primary) !important;
    color: var(--dark-text) !important;
    border-color: var(--dark-secondary) !important;
  }
  .navbar-brand {
    color: var(--dark-text) !important;
  }
  .d-flex .btn {
    color: var(--dark-text) !important;
  }
  .btn.btn-light {
    background-color: var(--dark-primary) !important;
    color: var(--dark-text) !important;
    border-color: var(--dark-primary) !important;
  }
  .dropdown-menu {
    background-color: var(--dark-secondary) !important;
  }
  .dropdown-item {
    color: var(--dark-text) !important;
  }
  .link {
    color: var(--dark-text) !important;
  }
  .section-head {
    color: var(--dark-text-secondary) !important;
  }
  .no-courses {
    border-color: var(--dark-text-secondary) !important;
  }
  .form-control {
    color: var(--dark-text) !important;
    background-color: var(--dark-primary) !important;
    border: 1px solid var(--dark-secondary) !important;
  }
  .custom-select {
    transition: 0s;
    color: var(--dark-text) !important;
    background-color: var(--dark-primary) !important;
    border: 1px solid var(--dark-secondary) !important;
  }
  .course-listing {
    color: var(--dark-text) !important;
    border-bottom: 1px solid var(--dark-text-secondary) !important;
  }
  hr {
    border-top: 1px solid var(--dark-text-secondary) !important;
  }
  .course-search {
    color: var(--dark-text) !important;
  }
  .built-by {
    color: var(--dark-text-secondary) !important;
  }
  .nav-link.dropdown-toggle {
    color: var(--dark-text) !important;
  }
  .gridContainer {
    background-color: var(--dark-primary) !important;
  }
  .major-button {
    background-color: var(--dark-secondary) !important;
  }
  .badge {
    color: var(--dark-text);
    background-color: var(--dark-secondary);
  }
}

</style>
