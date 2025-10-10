import ImageUpload from "./components/ImageUpload";
import { useState } from "react";

function App() {
  const [selectedImage, setSelectedImage] = useState(null);

  return (
    <div className="container-fluid p-3" style={{ minHeight: "100vh", backgroundColor: "#f8f9fa" }}>
      <div className="container mt-4" style={{ maxWidth: "600px" }}>
        <h1 className="text-center text-primary mb-4">Visual Product Matcher</h1>
        <ImageUpload onImageSelect={setSelectedImage} />
        {selectedImage && (
          <div className="text-center mt-4">
          </div>
        )}
      </div>
    </div>
  );
}

export default App;