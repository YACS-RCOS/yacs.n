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

.dark {
  --dark-primary: #262833;
  --dark-secondary: #181a21;
  --dark-text: #f2f2f2;
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
  .btn {
    color: var(--dark-text) !important;
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
  .text-center {
    color: var(--dark-text-secondary) !important;
  }
}

</style>
