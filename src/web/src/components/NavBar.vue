<script setup lang="ts">
import { THEME, useThemeStore } from "@/stores/theme";
import {
  Bars3Icon,
  CalendarIcon,
  IdentificationIcon,
  ListBulletIcon,
  MagnifyingGlassIcon,
  NewspaperIcon
} from "@heroicons/vue/24/solid";
import { onClickOutside, useIntersectionObserver } from "@vueuse/core";
import { ref } from "vue";
import { RouterLink } from "vue-router/auto";
import NavBarItems, { type NavItems } from "./NavBar/NavBarItems.vue";
import SemesterSelector from "./SemesterSelector.vue";

const navItems: NavItems = [
  ["/", "Schedule", CalendarIcon],
  ["/explore", "Explore", MagnifyingGlassIcon],
  ["/pathways", "Pathways", ListBulletIcon],
  ["/professors", "Professors", IdentificationIcon],
  ["/finals", "Finals", NewspaperIcon]
];

const menu = ref<HTMLElement | null>(null);
const nav_toggle = ref<HTMLInputElement | null>(null);
const navbar_root = ref<HTMLElement | null>(null);
const theme = useThemeStore();

// this will hide the menu if the screen gets larger so that if the screen gets smaller again the menu won't reappear
useIntersectionObserver(menu, ([{ isIntersecting }]) => {
  const nav_toggle_el = nav_toggle.value;
  if (!isIntersecting && nav_toggle_el != null) {
    nav_toggle_el.checked = isIntersecting;
  }
});

// this will hide the menu if the user clicks out of it
onClickOutside(navbar_root, () => {
  const nav_toggle_el = nav_toggle.value;
  if (nav_toggle_el != null) {
    nav_toggle_el.checked = false;
  }
});

function changeColorMode() {
  theme.theme = theme.theme != THEME.LIGHT ? THEME.LIGHT : THEME.DARK;
}
</script>

<template>
  <nav
    ref="navbar_root"
    class="my-window-controls flex flex-col bg-on-primary-dark text-primary"
  >
    <div class="flex w-full grow items-center gap-x-5 p-4">
      <!-- items to always show -->
      <RouterLink
        class="text-3xl font-bold max-lg:flex-grow max-lg:basis-0"
        to="/"
      >
        YACS
      </RouterLink>

      <!-- centers content when screen size < lg-->
      <div class="flex justify-center">
        <SemesterSelector />
      </div>

      <!-- shows nav items on screen size >= lg -->
      <div class="hidden justify-center gap-x-1 lg:flex">
        <NavBarItems :items="navItems" />
      </div>

      <!-- shows left items on screen size >= lg -->
      <div class="hidden flex-grow flex-row-reverse gap-x-5 lg:flex">
        <div @click="changeColorMode">color mode placeholder</div>
        <button>login placeholder</button>
      </div>

      <!-- shows different left items on screen size < lg -->
      <div
        ref="menu"
        class="ml-auto flex basis-0 flex-row-reverse gap-x-5 max-lg:flex-grow lg:hidden"
      >
        <!-- the disjointed label will toggle the menu -->
        <label
          for="nav-toggle"
          class="cursor-pointer select-none"
        >
          <Bars3Icon class="text-default h-6 w-6" />
        </label>
      </div>
    </div>

    <!-- shows dropdown menu if screen size < lg and menu is active -->
    <input
      id="nav-toggle"
      ref="nav_toggle"
      type="checkbox"
      class="peer hidden"
    />
    <div
      class="flex h-0 flex-col justify-evenly gap-y-5 border-primary border-opacity-50 px-5 peer-checked:border-t-4 motion-safe:transition-all motion-safe:duration-300 max-lg:peer-checked:h-80 lg:hidden"
    >
      <NavBarItems :items="navItems" />
    </div>
  </nav>
</template>
