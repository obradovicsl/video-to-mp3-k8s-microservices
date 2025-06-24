# MP4 to MP3 Converter — Microservices App with Kubernetes

## Project Overview

This project is a microservices-based application developed as a hands-on way to dive deep into Kubernetes and the practical side of building and running distributed systems. The app lets a user upload an MP4 video, which then gets converted to MP3 and sent back to them.

The real goal here wasn’t the app logic (which is simple), but to understand how to structure, deploy, and connect multiple services using Kubernetes. Each microservice in the system is fully containerized using Docker, and then orchestrated and managed inside a local Kubernetes cluster using Minikube. All core Kubernetes concepts — like Deployments, Services, Ingress, ConfigMaps, and Secrets — are used across the project.

---

## 🚀 Technologies Used
* **Flask** – Lightweight Python framework for writing simple web servers and service logic.
* **Docker** – Used to containerize each individual microservice.
* **Kubernetes (K8s)** – Core platform for deploying, scaling, and managing containerized applications.
* **MiniKube** – Used to run a local Kubernetes cluster on a single machine.
* **kubectl** – CLI tool for interacting with the Kubernetes API.
* **k9s** – Terminal-based UI to observe and manage Kubernetes resources.
* **RabbitMQ** – Message broker for asynchronous communication between services using two queues.
* **MongoDB** – NoSQL database for storing binary files (videos and MP3s) using GridFS.
* **MySQL** – Relational database used for managing user credentials and authentication data.
* **MoviePy** – Python library for video processing (used for converting videos to MP3).
* **Google SMTP** – For sending notification emails.

---

## 🎯 Motivation & Objectives

The primary goal of this project is to:

* Understand how to containerize and deploy services in Kubernetes.
* Learn the core K8s objects such as **Pods**, **Services**, **Deployments**, **Secrets**, **ConfigMaps**, and **Ingresses**.
* Experiment with service communication, environment variables, storage mechanisms, and workload scaling using **Kubernetes-native patterns**.
* Simulate asynchronous microservice communication using **RabbitMQ** and apply patterns such as **Competing Consumers**.

---
## 🧩 App Architecture

![Architecture image](architecture/Architecture%20ss.png)

---

## 🧩 Microservices Overview

### 1. **Gateway Service**

* Acts as the API gateway and entry point into the system.
* Validates requests via the **Auth Service** (JWT verification).
* Handles file uploads by storing videos in MongoDB (`videos` database).
* Publishes a message to the `video` queue in RabbitMQ after a successful upload.
* Exposed to the outside world via **Ingress** controller.

### 2. **Auth Service**

* Responsible for authentication and JWT token validation.
* Interacts with a **MySQL** database (`users`) that stores user credentials.
* Provides `/login` and `/verify` endpoints.

### 3. **Converter Service**

* Core of the application.
* Acts as a **consumer** for the `video` RabbitMQ queue.
* Retrieves the corresponding video file from the MongoDB `videos` database.
* Converts the video to an MP3 file using **MoviePy**.
* Saves the output to the MongoDB `mp3s` database.
* Publishes a message to the `mp3` RabbitMQ queue indicating that the MP3 is ready.

### 4. **Notification Service**

* Acts as a **consumer** for the `mp3` RabbitMQ queue.
* Sends an email notification to the user once the MP3 file has been successfully processed and stored.

### 5. **RabbitMQ**

* Manages two queues: `video` and `mp3`.
* Enables asynchronous processing between upload, conversion, and notification services.
* Leverages **Competing Consumers Pattern** for scalability of the converter service.

### 6. **Databases**

* **MySQL (`users`)** – Stores username/password information.
* **MongoDB (`videos`)** – Stores uploaded video files via GridFS.
* **MongoDB (`mp3s`)** – Stores converted MP3 files via GridFS.

> MongoDB is used with **GridFS** instead of BSON to avoid document size limitations when storing large binary files.

---

## 🔄 Workflow Summary

1. **Upload**: The user sends a POST request to `/upload` through the Gateway.
2. **Auth**: The Gateway checks the JWT token with the Auth Service.
3. **Video Store**: If authenticated, the video is saved to MongoDB (`videos`) via GridFS.
4. **Queue Message**: A message with video metadata is placed on the `video` queue.
5. **Convert**: A Converter instance consumes the message, processes the video into an MP3, stores it in MongoDB (`mp3s`), and publishes a message to the `mp3` queue.
6. **Notify**: Notification service consumes the `mp3` message and emails the user using Google SMTP.
7. **Download**: The user accesses `/download?fid=...` to retrieve the converted MP3 file.

---

## 📝 Conclusion

This project served as a comprehensive introduction to Kubernetes and microservices architecture. While the application logic remains simple, it showcases critical cloud-native concepts like container orchestration, horizontal scaling, environment isolation, service discovery, and asynchronous communication. The system can be expanded further with features like logging, tracing, metrics, persistent storage, CI/CD pipelines...