import { useState } from "react";

function ImageUpload({ onImageSelect }) {
    const [preview, setPreview] = useState(null);
    const [url, setUrl] = useState("");
    const [uploadStatus, setUploadStatus] = useState("");

    // file upload
    const handleFileChange = async (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setPreview(reader.result);
                onImageSelect(reader.result);
            };
            reader.readAsDataURL(file);

            const formData = new FormData();
            formData.append("image", file);

            try {
                const response = await fetch("http://127.0.0.1:8000/api/upload-image/", {
                    method: "POST",
                    body: formData,
                });

                const data = await response.json();
                setUploadStatus(data.message || data.error || "Upload done");
            } catch (err) {
                console.error(err);
                setUploadStatus("Error uploading image");
            }
        }
    };

    // URL input
    const handleUrlSubmit = (e) => {
        e.preventDefault();
        if (url.trim()) {
            setPreview(url);
            onImageSelect(url);
        }
    };

    return (
        <div className="card p-3 shadow-sm mx-auto" style={{ maxWidth: "100%" }}>
            <h4 className="text-center mb-3">Upload or Paste Image URL</h4>

            <input
                type="file"
                className="form-control mb-3"
                accept="image/*"
                onChange={handleFileChange}
            />

            <form onSubmit={handleUrlSubmit}>
                <div className="input-group">
                    <input
                        type="text"
                        placeholder="Enter image URL"
                        className="form-control"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                    />
                    <button className="btn btn-primary" type="submit">
                        Use URL
                    </button>
                </div>
            </form>

            {preview && (
                <div className="mt-3 text-center">
                    <img
                        src={preview}
                        alt="Preview"
                        className="img-fluid rounded"
                        style={{ maxHeight: "300px", objectFit: "contain" }}
                    />
                </div>
            )}

            {uploadStatus && (
                <p className="text-center mt-3 text-success fw-bold">{uploadStatus}</p>
            )}
        </div>
    );
}

export default ImageUpload;
