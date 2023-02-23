FROM python:3.8
LABEL maintainer="RayiemasMP"

# Copy all files
COPY /techtrends/static /app/static
COPY /techtrends/templates /app/templates
COPY /techtrends/__init__.py /app/__init__.py
COPY /techtrends/app.py /app/app.py
COPY /techtrends/init_db.py /app/init_db.py
COPY /techtrends/schema.sql /app/schema.sql
COPY /techtrends/requirements.txt /app/requirements.txt
COPY /techtrends/README.md /app/README.md

# Set Working Directory
WORKDIR /app

# Run prerequisite
RUN pip install -r requirements.txt
RUN python3 init_db.py

# Expose Port to 6111
EXPOSE 3111

# command to run on container start
CMD [ "python3", "app.py" ]