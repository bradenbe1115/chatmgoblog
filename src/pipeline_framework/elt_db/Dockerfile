# Use the official MongoDB image as a base
FROM mongo:latest

# Set environment variables for MongoDB root username and password
ENV MONGO_INITDB_ROOT_USERNAME=${MONGODB_USERNAME}
ENV MONGO_INITDB_ROOT_PASSWORD=${MONGODB_PASSWORD}

# Expose the default MongoDB port
EXPOSE 27017

# The default command to run MongoDB
CMD ["mongod"]