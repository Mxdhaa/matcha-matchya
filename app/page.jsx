import React, { useState, useRef } from 'react';
import { Upload, FileText, CheckCircle, XCircle, Sparkles, Brain, Target, TrendingUp } from 'lucide-react';

const FuturisticResumeEvaluator = () => {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState({
    similarity: 0,
    matchedSkills: [],
    missingSkills: [],
    extraSkills: [],
    improvements: []
  });
  const [showResults, setShowResults] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileUpload = (event) => {
    const uploadedFile = event.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
    }
  };

  const handleEvaluate = () => {
    setIsAnalyzing(true);
    setTimeout(() => {
      setIsAnalyzing(false);
      setShowResults(true);
    }, 3000);
  };

  const SkillBadge = ({ skill, type }) => {
    const colors = {
      matched: 'bg-gradient-to-r from-green-400 to-emerald-500 text-white',
      missing: 'bg-gradient-to-r from-red-400 to-pink-500 text-white',
      extra: 'bg-gradient-to-r from-purple-400 to-indigo-500 text-white'
    };
    
    return (
      <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium m-1 ${colors[type]} backdrop-blur-sm shadow-lg`}>
        {skill}
      </span>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-100 via-lavender-100 to-green-100 p-6" style={{background: 'linear-gradient(135deg, #fce7f3 0%, #f3e8ff 30%, #dcfce7 100%)'}}>
      {/* Animated background elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-4 -right-4 w-72 h-72 bg-pink-200 rounded-full mix-blend-multiply filter blur-xl opacity-40 animate-pulse"></div>
        <div className="absolute -bottom-8 -left-4 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-40 animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse delay-500"></div>
      </div>

      <div className="relative z-10 max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center items-center gap-3 mb-4">
            <Brain className="w-12 h-12 text-purple-500" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-purple-500 via-pink-400 to-green-500 bg-clip-text text-transparent">
              AI Resume Evaluator
            </h1>
            <Sparkles className="w-12 h-12 text-pink-400" />
          </div>
          <p className="text-xl text-gray-600 font-medium">
            Advanced AI-powered resume analysis for the future of hiring
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Panel - Upload & Job Description */}
          <div className="space-y-6">
            {/* File Upload */}
            <div className="bg-white/30 backdrop-blur-lg rounded-3xl p-8 border border-white/40 shadow-2xl">
              <h2 className="text-2xl font-bold text-gray-700 mb-6 flex items-center gap-2">
                <FileText className="w-6 h-6 text-purple-500" />
                Resume Upload
              </h2>
              
              <div
                onClick={() => fileInputRef.current?.click()}
                className="border-2 border-dashed border-purple-300 rounded-2xl p-8 text-center cursor-pointer hover:border-pink-400 transition-all duration-300 bg-white/20 hover:bg-white/30"
              >
                <Upload className="w-16 h-16 mx-auto text-purple-400 mb-4" />
                <p className="text-lg font-medium text-gray-600 mb-2">
                  {file ? file.name : 'Drop your resume here or click to upload'}
                </p>
                <p className="text-sm text-gray-500">
                  Supports PDF and image formats
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  onChange={handleFileUpload}
                  accept=".pdf,image/*"
                  className="hidden"
                />
              </div>
            </div>

            {/* Job Description */}
            <div className="bg-white/30 backdrop-blur-lg rounded-3xl p-8 border border-white/40 shadow-2xl">
              <h2 className="text-2xl font-bold text-gray-700 mb-6 flex items-center gap-2">
                <Target className="w-6 h-6 text-green-500" />
                Job Requirements
              </h2>
              
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                className="w-full h-32 p-4 rounded-xl bg-white/60 backdrop-blur-sm border border-white/40 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent resize-none text-gray-700 placeholder-gray-400"
                placeholder="Enter the job description here... Include required skills, experience level, and key responsibilities to get the most accurate analysis."
              />
              
              <button
                onClick={handleEvaluate}
                disabled={!file || isAnalyzing}
                className="w-full mt-6 py-4 px-6 bg-gradient-to-r from-purple-400 to-pink-400 text-white font-bold text-lg rounded-xl hover:from-purple-500 hover:to-pink-500 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg transform hover:scale-105"
              >
                {isAnalyzing ? (
                  <div className="flex items-center justify-center gap-2">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Analyzing Resume...
                  </div>
                ) : (
                  'Evaluate Resume'
                )}
              </button>
            </div>
          </div>

          {/* Right Panel - Results */}
          {showResults && (
            <div className="space-y-6">
              {/* Similarity Score */}
              <div className="bg-white/30 backdrop-blur-lg rounded-3xl p-8 border border-white/40 shadow-2xl">
                <h2 className="text-2xl font-bold text-gray-700 mb-6 flex items-center gap-2">
                  <TrendingUp className="w-6 h-6 text-green-500" />
                  Match Score
                </h2>
                
                <div className="text-center">
                  <div className="relative inline-block">
                    <svg className="transform -rotate-90 w-32 h-32">
                      <circle
                        cx="64"
                        cy="64"
                        r="56"
                        stroke="currentColor"
                        strokeWidth="8"
                        fill="none"
                        className="text-gray-300"
                      />
                      <circle
                        cx="64"
                        cy="64"
                        r="56"
                        stroke="currentColor"
                        strokeWidth="8"
                        fill="none"
                        strokeDasharray={`${2 * Math.PI * 56}`}
                        strokeDashoffset={`${2 * Math.PI * 56 * (1 - results.similarity / 100)}`}
                        className="text-green-500 transition-all duration-1000"
                      />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-3xl font-bold text-gray-700">{results.similarity}%</span>
                    </div>
                  </div>
                  <p className="text-lg font-medium text-gray-600 mt-4">
                    Compatibility Score
                  </p>
                </div>
              </div>

              {/* Skills Analysis */}
              <div className="bg-white/30 backdrop-blur-lg rounded-3xl p-8 border border-white/40 shadow-2xl">
                <h2 className="text-2xl font-bold text-gray-700 mb-6">Skills Analysis</h2>
                
                <div className="space-y-6">
                  {/* Matched Skills */}
                  <div>
                    <div className="flex items-center gap-2 mb-3">
                      <CheckCircle className="w-5 h-5 text-green-500" />
                      <h3 className="text-lg font-semibold text-gray-700">Matched Skills</h3>
                    </div>
                    <div className="flex flex-wrap">
                      {results.matchedSkills.map((skill, index) => (
                        <SkillBadge key={index} skill={skill} type="matched" />
                      ))}
                    </div>
                  </div>

                  {/* Missing Skills */}
                  <div>
                    <div className="flex items-center gap-2 mb-3">
                      <XCircle className="w-5 h-5 text-red-500" />
                      <h3 className="text-lg font-semibold text-gray-700">Missing Skills</h3>
                    </div>
                    <div className="flex flex-wrap">
                      {results.missingSkills.map((skill, index) => (
                        <SkillBadge key={index} skill={skill} type="missing" />
                      ))}
                    </div>
                  </div>

                  {/* Extra Skills */}
                  <div>
                    <div className="flex items-center gap-2 mb-3">
                      <Sparkles className="w-5 h-5 text-purple-500" />
                      <h3 className="text-lg font-semibold text-gray-700">Additional Skills</h3>
                    </div>
                    <div className="flex flex-wrap max-h-32 overflow-y-auto">
                      {results.extraSkills.map((skill, index) => (
                        <SkillBadge key={index} skill={skill} type="extra" />
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Improvement Suggestions */}
              <div className="bg-white/30 backdrop-blur-lg rounded-3xl p-8 border border-white/40 shadow-2xl">
                <h2 className="text-2xl font-bold text-gray-700 mb-6">AI Recommendations</h2>
                
                <div className="space-y-4">
                  {results.improvements.map((improvement, index) => (
                    <div key={index} className="bg-white/40 rounded-xl p-4 border border-white/30">
                      <p className="text-gray-700 font-medium">{improvement}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FuturisticResumeEvaluator;