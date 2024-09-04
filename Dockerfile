FROM python:3.12
WORKDIR /studythere-backend
COPY ./requirements.txt /studythere-backend/
RUN pip install --no-cache-dir --upgrade -r /studythere-backend/requirements.txt
COPY . /studythere-backend/.
EXPOSE 8000
CMD alembic upgrade head && uvicorn main:app --proxy-headers --port 8000 --host 0.0.0.0