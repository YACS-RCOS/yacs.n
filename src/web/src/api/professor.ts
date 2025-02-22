import { useMemoize } from "@vueuse/core";
import { app } from "./common";

export interface Professor {
  name: string;
  title: string;
  email: string;
  phone_number: string;
  department: string;
  portfolio_page: string;
  profile_page: string | null;
};

/** Gets professor info */
export const getProfessors = useMemoize(
  async (): Promise<Professor[]> => {
    const resp = await app.get<Professor[]>("/professor");
    return resp.data;
  }
);
