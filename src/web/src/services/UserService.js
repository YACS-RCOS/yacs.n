import axios from "axios";

const client = axios.create({
  baseURL: "/api",
});

export const login = (userInfo) => client.post("/session", userInfo);

/**
 *
 * @param {string} sessionID
 */
export const getUserInfo = (sessionID) => client.get(`/user/${sessionID}`);

export const signup = (userInfo) => client.post("/user", userInfo);

export const logout = (sessionId) =>
  client.delete("/session", {
    data: {
      sessionID: sessionId,
    },
    headers: {
      "Content-Type": "application/json",
    },
  });
