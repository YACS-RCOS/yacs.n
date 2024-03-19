import { StorageSerializers, useLocalStorage, usePreferredDark } from "@vueuse/core";
import { defineStore } from "pinia";

export enum THEME {
  DEVICE_DEFAULT,
  LIGHT,
  DARK
}

const prefer_dark = usePreferredDark();

function isDark(theme: THEME) {
  switch (theme) {
    case THEME.DEVICE_DEFAULT:
      return prefer_dark.value;
    case THEME.LIGHT:
      return false;
    case THEME.DARK:
      return true;
  }
}

export const useThemeStore = defineStore("theme", () => {
  const theme = useLocalStorage<THEME>("theme/current", () => THEME.DEVICE_DEFAULT, {
    serializer: {
      ...StorageSerializers.number,
      ...{
        read(raw) {
          const v = Number.parseInt(raw);
          return v in THEME ? (v as THEME) : THEME.DEVICE_DEFAULT;
        }
      }
    }
  });

  function applyTheme() {
    if (document) {
      const root = document.querySelector("html");

      if (root) {
        if (isDark(theme.value)) {
          root.classList.add("dark");
        } else {
          root.classList.remove("dark");
        }
      }
    }
  }

  return {
    theme,
    applyTheme
  };
});
