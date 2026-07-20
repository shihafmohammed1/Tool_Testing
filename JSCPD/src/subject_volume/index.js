/** Subject volume entry. */
export const modules = {"services": () => import("./services/index.js"), "handlers": () => import("./handlers/index.js"), "processors": () => import("./processors/index.js"), "validators": () => import("./validators/index.js"), "reports": () => import("./reports/index.js"), "integrations": () => import("./integrations/index.js")};
