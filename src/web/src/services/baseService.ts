import axios from "axios";

export const api = axios.create({
  baseURL: "/api",
});

console.log(`using api host ${api.defaults.baseURL}`);
// console.log(await api.get("/"));
