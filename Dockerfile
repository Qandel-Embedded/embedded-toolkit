FROM python:3.11-slim
WORKDIR /app
# Create an interactive environment with the toolkit installed
COPY . .
RUN pip install --no-cache-dir -e . pyserial ipython
# Start an interactive python shell by default
CMD ["ipython", "-i", "-c", "from embedded_toolkit import *; print('Embedded Toolkit Interactive Shell loaded.')"]
