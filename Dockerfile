# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install cron and required packages
RUN apt-get update && apt-get install -y vim cron bash procps && rm -rf /var/lib/apt/lists/*

# Ensure cron log file exists
RUN touch /var/log/cron.log

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the bot's code into the container
COPY . .

# Create a crontab file that runs the fetch_lift_status_from_liftie.py every 5 minutes
RUN echo "*/30 * * * * /usr/local/bin/python3 /app/data/fetch_lift_status_from_liftie.py >> /var/log/cron.log 2>&1 && echo \"[\$(date)] Fetch script executed\" >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron-job

# Set permissions for the cron job and apply it
RUN chmod 0644 /etc/cron.d/my-cron-job && crontab /etc/cron.d/my-cron-job

# Ensure cron starts properly by using a shell entry point and starting cron explicitly
CMD ["sh", "-c", "cron && tail -f /var/log/cron.log & python -m bot.liftie-bot"]
