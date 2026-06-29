import { useDropzone } from 'react-dropzone'
import { Upload, FileText, CheckCircle } from 'lucide-react'
import GlassCard from '../components/GlassCard'

export default function Analyze() {
  const { getRootProps, getInputProps, isDragActive, acceptedFiles } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
    },
    maxFiles: 1,
  })

  return (
    <section className="relative min-h-screen flex items-center pt-24 pb-16 overflow-hidden">
      <div className="absolute inset-0 bg-grid" />
      <div className="absolute inset-0 bg-gradient-radial" />

      <div className="relative max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        <div className="text-center mb-12">
          <h1 className="text-4xl sm:text-5xl font-extrabold text-white mb-4">
            Analyze Your <span className="gradient-text">Resume</span>
          </h1>
          <p className="text-lg text-gray-400">
            Upload your resume and get instant AI-powered insights, ATS
            compatibility score, and optimization suggestions.
          </p>
        </div>

        <GlassCard className="p-8 md:p-12 glow" hover={false}>
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-300 ${
              isDragActive
                ? 'border-primary bg-primary/5'
                : 'border-white/10 hover:border-primary/40 hover:bg-white/5'
            }`}
          >
            <input {...getInputProps()} />
            <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-6">
              <Upload className="text-primary" size={28} />
            </div>
            {isDragActive ? (
              <p className="text-lg text-primary font-medium">
                Drop your resume here
              </p>
            ) : (
              <>
                <p className="text-lg text-white font-medium mb-2">
                  Drag & drop your resume here
                </p>
                <p className="text-sm text-gray-400 mb-6">
                  or click to browse — PDF, DOCX, or TXT
                </p>
              </>
            )}
          </div>

          {acceptedFiles.length > 0 && (
            <div className="mt-6 space-y-3">
              {acceptedFiles.map((file) => (
                <div
                  key={file.name}
                  className="flex items-center gap-3 glass rounded-xl p-4"
                >
                  <FileText className="text-primary flex-shrink-0" size={20} />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-white truncate">
                      {file.name}
                    </p>
                    <p className="text-xs text-gray-400">
                      {(file.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                  <CheckCircle className="text-green-400 flex-shrink-0" size={20} />
                </div>
              ))}
            </div>
          )}
        </GlassCard>
      </div>
    </section>
  )
}
