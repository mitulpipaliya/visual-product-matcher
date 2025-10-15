import { useState } from "react";
import ImageUpload from "./components/ImageUpload";

const BACKEND_URL = "https://visual-product-matcher-jdlz.onrender.com";

function App() {
    const [results, setResults] = useState([]);
    const [similarityFilter, setSimilarityFilter] = useState(0);

    const filteredResults = results.filter(
        (r) => r.similarity >= similarityFilter
    );

    const resetSearch = () => {
        setResults([]);
        setSimilarityFilter(0);
    };

    return (
        <div
            className="d-flex flex-column align-items-center p-3"
            style={{ minHeight: "100vh" }}
        >
            <div
                className="p-4 shadow-lg rounded-3"
                style={{
                    width: "100%",
                    maxWidth: "700px",
                    backgroundColor: "#2B7A78",
                    color: "#DEF2F1"
                }}
            >
                <h1
                    className="text-center mb-4"
                    style={{
                        color: "#DEF2F1",
                        fontWeight: 900,
                        letterSpacing: '2px'
                    }}
                >
                    VISUAL PRODUCT MATCHER
                </h1>

                <div className="mb-4">
                    <ImageUpload
                        onSearchResults={setResults}
                        backendUrl={BACKEND_URL}
                        onNewSearchStart={resetSearch}
                    />

                    {results.length > 0 && (
                        <div className="mt-4 p-3 rounded" style={{ backgroundColor: "#1f5c5b" }}>
                            <label className="form-label mb-1 fw-bold">
                                Similarity Filter: {Math.round(similarityFilter * 100)}%
                            </label>
                            <input
                                type="range"
                                min="0"
                                max="1"
                                step="0.01"
                                value={similarityFilter}
                                onChange={(e) => setSimilarityFilter(parseFloat(e.target.value))}
                                className="form-range"
                                style={{ accentColor: '#17252A' }}
                            />
                        </div>
                    )}
                </div>

                <h3 className="mb-3" style={{ color: "#DEF2F1" }}>
                    Similar Products ({filteredResults.length} Results)
                </h3>

                <div className="row">
                    {filteredResults.map((res) => {
                        const imageSrc = res.image_url.substring(6);
                        return (
                            <div className="col-12 col-sm-6 col-lg-4 mb-3" key={res.name}>
                                <div className="card h-100 text-center shadow-sm" style={{ backgroundColor: "#DEF2F1", color: "#17252A" }}>
                                    <img
                                        src={imageSrc}
                                        className="card-img-top"
                                        alt={res.name}
                                        style={{ height: "150px", objectFit: "contain", padding: '10px' }}
                                    />
                                    <div className="card-body p-2">
                                        <h6 className="card-title fw-bold m-0">{res.name}</h6>
                                        <p className="card-text text-muted mb-1" style={{ fontSize: '0.9em' }}>
                                            {res.category}
                                        </p>
                                        <p className="card-text fw-bold m-0">
                                            Match: {Math.round(res.similarity * 100)}%
                                        </p>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}

export default App;