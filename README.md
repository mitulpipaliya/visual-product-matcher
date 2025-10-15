# Visual Product Matcher 🚀

 - A full-stack web application designed for fast, visually-aware content-based image retrieval. 
 - It allows users to search a large product catalog for visually similar items based on an uploaded image or a URL.

---


## 🌐 Live Application

| Item | Status | URL |
| :--- | :--- | :--- |
| **Live Application URL** | **LIVE** | [https://visual-product-matcher-ui.onrender.com](https://visual-product-matcher-ui.onrender.com) |

---


## 🧠 Core Technical Approach

### Scalable Image Similarity Architecture

The system is built on a high-efficiency architecture separating client-facing front-end from the computational back-end.

The visual matching process is implemented using **Deep Learning Feature Extraction** combined with **Vector Similarity Search**:

1.  **Feature Extraction:** The core model, **MobileNetV3Small**, is used as a feature extractor. To maintain **stability and performance**, the Keras model was converted to the lightweight **ONNX (Open Neural Network Exchange)** format. This allows the Django API to use the rapid `onnxruntime` for instantaneous model inference.
2.  **Vector Persistence:** Product images are pre-processed offline, and the resulting **1024-dimensional feature vectors** are stored in the MySQL database.
3.  **Search & Ranking:** When a query image is provided, its ONNX feature vector is calculated on-the-fly. This vector is compared against all database vectors using **Cosine Similarity**, and the results are ranked to retrieve the top 10 matches.

**Result:** Fast, stable, and scalable similarity search for large product datasets.

---

## ✨ Key Features

### 1. Image Input Flexibility

Users can start a search in **two ways**:
- **Upload a local image** directly from the device  
- **Paste a public image URL** — system handles fetching & preprocessing automatically  

Once the image is processed, the model generates a feature vector and performs the similarity search instantly.

📸 *Screenshot:*  
![Upload or URL Input](assets/upload_or_url.png)

---

### 2. Search Results and Filtering

A clean and dynamic result interface that:
- Displays the **query image** alongside search results  
- Shows:
  - **Product Name**
  - **Category**
  - **Similarity Score (in %)**
- Includes a **range slider** to filter results by similarity threshold (0–100%)

📸 *Screenshot:*  
![Search Results Screenshot](assets/search_results.png)
![Filter](assets/filter.png)

---

## Technology Stack  🛠️

| Category | Component | Rationale |
| :--- | :--- | :--- |
| **Frontend** | React, Vite, Bootstrap | Modern SPA framework, fast tooling, mobile responsiveness. |
| **Backend** | Django REST Framework | Robust framework for API development and data handling. |
| **Database** | MySQL | Relational database for structured metadata storage. |
| **Machine Learning** | MobileNetV3Small (ONNX) | Highly optimized lightweight model for feature extraction. |

---

## 🎯 Project Purpose

This project demonstrates:
- Integration of **Deep Learning** in a **Full-Stack Web Application**
- Implementation of **Feature Extraction** and **Vector Similarity Search**
- Production-level **Scalable Architecture** for visual retrieval systems

---
## 📈 Future Enhancements

* **ANN Indexing:** Implement an Approximate Nearest Neighbors (ANN) vector database (e.g., Qdrant or Faiss) to handle searches against millions of product embeddings, reducing the current $\mathcal{O}(N)$ linear scan to $\mathcal{O}(\log N)$ complexity.
* **Data Expansion:** Increase the product catalog size significantly and introduce fine-tuning of the feature extractor for domain-specific visual characteristics.
