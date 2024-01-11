FROM node:current-alpine

RUN mkdir /project
WORKDIR /project

COPY . .

RUN apk add curl 
RUN curl -L https://unpkg.com/@pnpm/self-installer | node
RUN pnpm i

CMD ["sh", "startup.sh"]
