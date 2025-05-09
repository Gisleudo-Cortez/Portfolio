# Builder stage
FROM rust:1.86.0 AS builder 
WORKDIR /app 
RUN apt update && apt install lld clang -y
COPY . . 
ENV SQLX_OFFLINE=true
RUN cargo build --release

# Runtime stage
FROM  debian:bookworm-slim AS runtime 
WORKDIR /app 
# Install OpenSSL - it is dynamically linked by some of our dependencies 
# Install ca-certificates - it is needed to verify TLS certificates 
# when establishing HTTPS connections
RUN apt-get update -y && apt-get install -y --no-install-recommends openssl ca-certificates \
	# Clean up 
	&& apt-get autoremove -y \
	&& apt-get clean -y \
	&& rm -rf /var/lib/apt/lists/*
# Copy the compiled binary from the builder environment 
COPY --from=builder /app/target/release/zero2prod zero2prod
# Config file needed at runtime 
COPY configuration configuration
ENV APP_ENVIRONMENT=production
ENTRYPOINT [ "./zero2prod" ]
