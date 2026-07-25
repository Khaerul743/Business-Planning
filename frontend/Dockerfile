FROM node:20-slim

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

ENV NODE_ENV=development

CMD ["npx", "next", "dev", "--no-turbo", "-H", "0.0.0.0", "-p", "3000"]
