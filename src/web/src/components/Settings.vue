<template>

  <b-nav-dropdown text="Color Mode" style="padding-right: 5px;">
    <b-dropdown-item
      :class="this.darkMode === false ? 'drop-down-item' : ''"
      @click="toggle_style(false)"
    >
      Light Mode
    </b-dropdown-item>
    <b-dropdown-item
      :class="this.darkMode === true ? 'drop-down-item' : ''"
      @click="toggle_style(true)"
    >
      Dark Mode
    </b-dropdown-item>
    <b-dropdown-item
      :class="this.darkMode === null ? 'drop-down-item' : ''"
      @click="toggle_device"
    >
      Follow Device Theme
    </b-dropdown-item>
  </b-nav-dropdown>

</template>


<script>

export default {
  name: "Settings",
  
};

</script>