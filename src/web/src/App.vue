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
  --dark-secondary: #000;
  --dark-text: #f2f2f2;
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
  .card {
    background: var(--dark-primary) !important;
    .card-header {
      background: var(--dark-primary) !important;
    }
  }
  .nav-link.active {
    background-color: var(--dark-primary) !important;
    border-color: var(--dark-secondary) !important;
  }
}

</style>
