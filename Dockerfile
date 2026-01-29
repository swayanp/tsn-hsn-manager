# 1️⃣ Base image (lightweight Python)
FROM python:3.13-slim

# 2️⃣ Set working directory inside container
WORKDIR /app

# 3️⃣ Copy dependency list first (for caching)
COPY requirements.txt .

# 4️⃣ Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copy application code
COPY . .

# 6️⃣ Expose port (FastAPI runs on 8000)
EXPOSE 8000

# 7️⃣ Start FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
