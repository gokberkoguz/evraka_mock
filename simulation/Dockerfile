FROM python:3.8

WORKDIR /app

# Copy the Python script for simulation
COPY simulation/main.py .

# Install any dependencies required for the simulation script
RUN pip install requests

CMD ["python", "main.py"]
