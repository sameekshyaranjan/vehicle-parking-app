import "dotenv/config";
import { defineConfig } from "prisma/config";

export default defineConfig({
  schema: "prisma/mysql/schema.prisma",
  migrations: { path: "prisma/mysql/migrations" },
  datasource: { url: process.env.DATABASE_URL },
});
