# Stage 1: Build Flutter Web
FROM ubuntu:20.04 AS build

# Install dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y curl git unzip xz-utils zip libglu1-mesa

# Setup Flutter
WORKDIR /opt
RUN git clone https://github.com/flutter/flutter.git -b stable
ENV PATH="/opt/flutter/bin:${PATH}"

# Configure Flutter Web
RUN flutter config --enable-web

# Build the app
WORKDIR /app
COPY . .
RUN flutter pub get
RUN flutter build web --release

# Stage 2: Serve with Nginx
FROM nginx:alpine
COPY --from=build /app/build/web /usr/share/nginx/html
# Custom nginx config to handle SPA routing (fallback to index.html)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
