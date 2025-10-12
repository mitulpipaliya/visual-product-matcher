import { useState } from "react";

const Loader = ({ message }) => (
    <div className="loading-container">
        <div className="fading-balls mb-2"></div>
        <p className="m-0 fw-bold">{message}</p>
    </div>
);

function ImageUpload({ onSearchResults, backendUrl, onNewSearchStart }) {
    const [preview, setPreview] = useState(null);
    const [url, setUrl] = useState("");
    const [loading, setLoading] = useState(false); 
    const [statusMessage, setStatusMessage] = useState("Awaiting image upload or URL."); 

    const handleFileChange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        onNewSearchStart(); 
        setUrl(""); 
    
        setPreview(<Loader message="Loading Preview.." />);
        
        const reader = new FileReader();
        reader.onloadend = () => setPreview(reader.result);
        reader.readAsDataURL(file);

        const formData = new FormData();
        formData.append("image", file);

        await searchSimilar(formData);
    };

    const handleUrlSubmit = async (e) => {
        e.preventDefault();
        if (!url.trim()) {
            setStatusMessage("Please enter a valid URL.");
            return;
        }
        
        onNewSearchStart();

        setPreview(<Loader message="Fetching Image from URL.." />);
        setStatusMessage("Fetching image..");

        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const blob = await response.blob();

            if (!blob.type.startsWith('image/')) {
                 throw new Error("URL did not return an image file.");
            }
            
            const reader = new FileReader();
            reader.onloadend = () => setPreview(reader.result);
            reader.readAsDataURL(blob);

            const formData = new FormData();
            formData.append("image", blob, "url_image.jpg");
            
            await searchSimilar(formData);

        } catch (err) {
            console.error("URL Fetch Error:", err);
            setStatusMessage(`Error fetching image: ${err.message}. Check URL or CORS policy.`);
            setPreview(null);
            setLoading(false);
        }
    };

    const searchSimilar = async (formData) => {
        setLoading(true); 
        setStatusMessage("Searching similar products..");
        onSearchResults([]);
        
        try {
            const response = await fetch(`${backendUrl}/api/search/`, {
                method: "POST",
                body: formData,
            });
            
            const data = await response.json();

            if (response.ok && data.results) {
                onSearchResults(data.results);
                setStatusMessage(`Search completed. Found ${data.results.length} results.`);
            } else if (data.error) {
                setStatusMessage(`Server Error: ${data.error}`);
                onSearchResults([]);
            } else {
                setStatusMessage("Search failed or returned no data.");
                onSearchResults([]);
            }
        } catch (err) {
            console.error("Search API Error:", err);
            setStatusMessage("Network error. Could not connect to the server.");
            onSearchResults([]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card p-3 shadow-lg mx-auto" style={{ backgroundColor: "#2B7A78", border: 'none' }}>
            <h5 className="text-center mb-3" style={{ color: "#DEF2F1" }}>
                Upload or Paste Image URL
            </h5>

            <input
                type="file"
                className="form-control mb-3"
                accept="image/*"
                onChange={handleFileChange}
                style={{ backgroundColor: "#3AAFA9", color: "#DEF2F1", border: 'none' }}
            />

            <form onSubmit={handleUrlSubmit}>
                <div className="input-group">
                    <input
                        type="text"
                        placeholder="Enter image URL"
                        className="form-control"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        style={{ backgroundColor: "#3AAFA9", color: "#DEF2F1", border: 'none' }}
                    />
                    <button 
                        className="btn" 
                        type="submit"
                        disabled={loading}
                        style={{ backgroundColor: "#17252A", color: "#DEF2F1", borderColor: "#17252A" }}
                    >
                        {loading ? 'Processing...' : 'Use URL'}
                    </button>
                </div>
            </form>

            <div className="mt-3 text-center">
                {preview === null ? (
                    <div style={{ minHeight: "200px", display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                         <p className="text-muted m-0" style={{ color: '#DEF2F1A0' }}>Image Preview</p>
                    </div>
                ) : (typeof preview === 'string' ? (
                    <img
                        src={preview}
                        alt="Preview"
                        className="img-fluid rounded shadow"
                        style={{ maxHeight: "300px", objectFit: "contain", border: '2px solid #DEF2F1' }}
                    />
                ) : (
                    preview
                ))}
            </div>

            {statusMessage && (
                <p 
                    className={`text-center mt-3 fw-bold m-0`} 
                    style={{ color: statusMessage.includes("Error") ? 'red' : '#DEF2F1' }}
                >
                    {statusMessage}
                </p>
            )}
 
            {loading && !Array.isArray(onSearchResults) && (
                 <div className="mt-3">
                     <Loader message="Searching similar products.." />
                 </div>
            )}
            
        </div>
    );
}

export default ImageUpload;