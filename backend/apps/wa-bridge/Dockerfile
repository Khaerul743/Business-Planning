FROM node:20-slim

# Install Chromium and required font dependencies for Puppeteer / whatsapp-web.js
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    fonts-liberation \
    ca-certificates \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Tell Puppeteer to use the installed system Chromium executable
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

WORKDIR /app

COPY package*.json ./

RUN npm ci --only=production

COPY . .

EXPOSE 3001

CMD ["npm", "start"]
