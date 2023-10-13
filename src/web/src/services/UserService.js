import axios from "axios";
import { api } from "./baseService";

export const login = (userInfo) => api.post("/session", userInfo);

/**
 *
 * @param {string} sessionID
 */
export const getUserInfo = (sessionID) => api.get(`/user/${sessionID}`);

export const signup = (userInfo) => api.post("/user", userInfo);

export const logout = (sessionId) =>
  api.delete("/session", {
    data: {
      sessionID: sessionId,
    },
    headers: {
      "Content-Type": "application/json",
    },
  });
