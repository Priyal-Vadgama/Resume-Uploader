import { useState, useEffect } from "react";
import axios from "axios";
import "./index.css";

function App() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    dob: "",
    state: "",
    gender: "",
    location: "",
    pimage: null,
    resume: null,
  });

  const [candidates, setCandidates] = useState([]); // Store fetched data
  const [loading, setLoading] = useState(false); // For submission
  const [fetching, setFetching] = useState(false); // For fetching data

  // Fetch candidate data on component mount
  useEffect(() => {
    fetchCandidates();
  }, []);

  const fetchCandidates = async () => {
    setFetching(true);
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/list/");
      setCandidates(response.data.candidates);
      console.log(response.data)
    } catch (error) {
      console.error("Error fetching candidates:", error);
    } finally {
      setFetching(false);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, files } = e.target;
    if (type === "file") {
      setFormData({ ...formData, [name]: files[0] });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };
  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/list/${id}/`);
  
      alert("Candidate deleted successfully!");
      fetchCandidates(); // Refresh the candidate list
    } catch (error) {
      console.error("Error deleting candidate:", error);
      alert("Failed to delete candidate.");
    }
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formDataToSend = new FormData();
    formDataToSend.append("name", formData.name);
    formDataToSend.append("email", formData.email);
    formDataToSend.append("dob", formData.dob);
    formDataToSend.append("state", formData.state);
    formDataToSend.append("gender", formData.gender);
    formDataToSend.append("location", formData.location);
    if (formData.pimage) formDataToSend.append("pimage", formData.pimage);
    if (formData.resume) formDataToSend.append("resume", formData.resume);

    try {
      await axios.post("http://127.0.0.1:8000/api/resume/", formDataToSend, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      alert("Resume submitted successfully!");
      

      setFormData({
        name: "",
        email: "",
        dob: "",
        state: "",
        gender: "",
        location: "",
        pimage: null,
        resume: null,
      });
  
      document.querySelectorAll("input[type=file]").forEach((input) => (input.value = ""));
  
      fetchCandidates(); // Refresh candidate list
    } catch (error) {
      console.error("Error submitting form:", error);
      alert("Failed to submit the form.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative">
      <h1 className="text-4xl font-extrabold text-purple-100 fixed w-full text-center tracking-wide bg-blue-500">
        Resume Uploader
      </h1>
      <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
        <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-7xl">
          {/* Form Section */}
          <h2 className="text-2xl font-semibold text-gray-800 mb-6">
            Upload Your Resume
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <input type="text" name="name" placeholder="Full Name" className="input-style" onChange={handleChange} required />
            <input type="email" name="email" placeholder="Email Address" className="input-style" onChange={handleChange} required />
            <input type="date" name="dob" className="input-style" onChange={handleChange} required />
            <input type="text" name="state" placeholder="State" className="input-style" onChange={handleChange} required />
            <div>
            <label className=" text-gray-900 font-medium pr-4">Gender:</label>
            <label  className="pr-2" >
              <input type="radio" name="gender" value="Male"  onChange={handleChange} required /> Male
            </label>
            <label  className="pr-2" >
              <input type="radio" name="gender" value="Female" onChange={handleChange} required /> Female
            </label>
            <label  className="pr-2" >
              <input type="radio" name="gender" value="Other" onChange={handleChange} required /> Other
            </label>
          </div>
            <input type="text" name="location" placeholder="Location" className="input-style" onChange={handleChange} required />
            <div>
              <label className="block text-gray-600 font-medium">Profile Image</label>
              <input type="file" name="pimage" className="input-style cursor-pointer" accept="image/*" onChange={handleChange} required />
            </div>
            <div>
              <label className="block text-gray-600 font-medium">Resume (PDF/DOCX)</label>
              <input type="file" name="resume" className="input-style cursor-pointer" accept=".pdf,.docx" onChange={handleChange} required />
            </div>
            <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md w-full transition duration-200 cursor-pointer" disabled={loading}>
              {loading ? "Submitting..." : "Submit"}
            </button>
          </form>

          {/* Candidates Table */}
          <h2 className="text-2xl font-semibold text-gray-800 mt-8">Submitted Candidates</h2>
          {fetching ? (
            <p className="text-gray-500">Loading candidates...</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full border-collapse border border-gray-300 mt-4">
                <thead>
                  <tr className="bg-gray-200 border border-gray-300">
                    <th className="p-2 font-medium text-gray-700">Name</th>
                    <th className="p-2 font-medium text-gray-700">Email</th>
                    <th className="p-2 font-medium text-gray-700">DOB</th>
                    <th className="p-2 font-medium text-gray-700">State</th>
                    <th className="p-2 font-medium text-gray-700">Gender</th>
                    <th className="p-2 font-medium text-gray-700">Location</th>
                    <th className="p-2 font-medium text-gray-700">Profile Image</th>
                    <th className="p-2 font-medium text-gray-700">Resume</th>
                    <th className="p-2 font-medium text-gray-700">Delete</th>
                  </tr>
                </thead>
                <tbody>
                  {candidates.length > 0 ? (
                    candidates.map((candidate) => (
                      <tr key={candidate.id} className="border border-gray-300">
                        <td className="p-2 text-center">{candidate.name}</td>
                        <td className="p-2 text-center">{candidate.email}</td>
                        <td className="p-2 text-center">{candidate.dob}</td>
                        <td className="p-2 text-center">{candidate.state}</td>
                        <td className="p-2 text-center">{candidate.gender}</td>
                        <td className="p-2 text-center">{candidate.location}</td>
                        <td className="p-2 flex justify-center">
                          {candidate.pimage && (
                            <img src={`http://127.0.0.1:8000/.${candidate.pimage}`}alt="Profile" className="w-16 h-16 rounded-full border border-gray-300" />
                          )}
                        </td>
                        <td className="p-2 text-center">
                          {candidate.resume && (
                            <a href={`http://127.0.0.1:8000/.${candidate.resume}`} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                              View Resume
                            </a>
                          )}
                        </td>
                        <td className="p-2 text-center">
                         <button className="cursor-pointer " onClick={()=> handleDelete(candidate.id)}>❌</button>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="8" className="text-center text-gray-500 p-4">
                        No candidates submitted yet.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
