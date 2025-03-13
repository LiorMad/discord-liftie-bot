# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install vim as part of the build process
RUN apt-get update && apt-get install -y vim

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the bot's code into the container
COPY . .

## Ensure the .env file is available (optional, but recommended)
#ENV BOT_TOKEN=${BOT_TOKEN}

# Run the bot when the container starts
CMD ["python", "-m", "bot/liftie-bot.py"]
