/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Which port to serve YACS on */
  readonly VITE_PORT: number;
  /** Whether to enable the service worker */
  readonly VITE_ENABLE_SW: boolean;
  /**Where the API host is located */
  readonly VITE_API_HOST: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
