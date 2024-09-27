import axios from "axios";

export const app = axios.create({
  baseURL: "/api"
});
