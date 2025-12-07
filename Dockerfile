FROM node:18-bullseye AS builder
WORKDIR /app
COPY package.json package-lock.json* .npmrc* ./
COPY server/package.json server/package-lock.json* server/tsconfig.json ./server/
COPY frontend/package.json frontend/package-lock.json* frontend/tsconfig.json frontend/tsconfig.node.json frontend/vite.config.ts frontend/postcss.config.js frontend/tailwind.config.js ./frontend/
RUN npm install
COPY . .
RUN npm run build

FROM node:18-bullseye
WORKDIR /app
COPY --from=builder /app .
ENV PORT=4000
EXPOSE 4000
CMD ["node", "server/dist/index.js"]
