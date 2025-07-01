# Build stage
FROM amazoncorretto:21 AS builder

WORKDIR /app
COPY gradlew .
COPY gradle gradle
COPY build.gradle .
COPY settings.gradle .
COPY src src

RUN chmod +x gradlew
RUN ./gradlew build --no-daemon

# Runtime stage
FROM amazoncorretto:21

WORKDIR /app
COPY --from=builder /app/build/libs/*.jar app.jar

EXPOSE 1111
ENTRYPOINT ["java", "-jar", "app.jar"]