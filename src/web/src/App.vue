<script setup lang="ts">
import HelloWorld from "@/components/HelloWorld.vue";
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <header>
    <img alt="Vue logo" class="font-bold" src="@/assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="ur mom" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>
