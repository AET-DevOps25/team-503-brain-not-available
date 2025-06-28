# Use an official OpenJDK runtime as a parent image
FROM amazoncorretto:21

# Update OS packages to latest security patches
RUN yum update -y && yum clean all

# Set the working directory inside the container
WORKDIR /app

# Copy the built jar file into the container
COPY build/libs/*.jar app.jar

# Expose the port the app runs on
EXPOSE 1111

# Run the jar file
ENTRYPOINT ["java", "-jar", "app.jar"]