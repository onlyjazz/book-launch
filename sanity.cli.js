// sanity.cli.js
import { defineCliConfig } from "sanity/cli";

export default defineCliConfig({
  api: {
    projectId: "rh2kgtdt",
    dataset: "production",
  },
  server: {
    hostname: "localhost",
    port: 3333,
  }
});
