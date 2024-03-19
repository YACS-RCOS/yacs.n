import { useLocalStorage } from "@vueuse/core";
import { defineStore } from "pinia";

export const useUserStore = defineStore("user", () => {
  const session_id = useLocalStorage<string | null>("user/session_id", null);

  function login() {
    // todo
  }
  function logout() {
    // todo
  }

  return {
    session_id,
    login,
    logout
  };
});
