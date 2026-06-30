import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowRight, CheckCircle } from 'lucide-react'
import toast from 'react-hot-toast'
import UploadBox from '../components/upload/UploadBox'
import FilePreview from '../components/upload/FilePreview'
import JDInput from '../components/upload/JDInput'
import AnalyzeButton from '../components/upload/AnalyzeButton'
import LoadingOverlay from '../components/upload/LoadingOverlay'
import GlassCard from '../components/GlassCard'
import { uploadResume } from '../services/api'

export default function Upload() {
  const navigate = useNavigate()

  const [file, setFile] = useState(null)
  const [uploadError, setUploadError] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState('Uploading...')
  const [complete, setComplete] = useState(false)

  const handleFileSelect = useCallback((selectedFile, error) => {
    if (error) {
      setUploadError(error)
      setFile(null)
      return
    }
    setFile(selectedFile)
    setUploadError(null)
  }, [])

  const handleRemove = useCallback(() => {
    setFile(null)
    setUploadError(null)
  }, [])

  const handleAnalyze = useCallback(async () => {
    if (!file) return

    setUploading(true)
    setProgress(0)
    setComplete(false)

    try {
      const statuses = [
        'Uploading resume...',
        'Parsing document structure...',
        'Extracting skills & experience...',
        'Analyzing ATS compatibility...',
        'Generating insights...',
      ]

      const statusInterval = setInterval(() => {
        setStatus((prev) => {
          const idx = statuses.indexOf(prev)
          return idx < statuses.length - 1 ? statuses[idx + 1] : prev
        })
      }, 1600)

      setStatus(statuses[0])

      const result = await uploadResume(file, jobDescription, (p) => {
        setProgress(p)
      })

      clearInterval(statusInterval)
      setStatus('Analysis complete!')
      setComplete(true)

      toast.success('Resume analyzed successfully!')

      setTimeout(() => {
        navigate('/analyze', { state: { result: result.data } })
      }, 800)
    } catch (err) {
      setUploading(false)
      setProgress(0)
      toast.error(err.message || 'Analysis failed. Please try again.')
    }
  }, [file, jobDescription, navigate])

  return (
    <section className="relative min-h-screen flex items-center pt-28 pb-16 overflow-hidden">
      <div className="absolute inset-0 bg-grid" />
      <div className="absolute inset-0 bg-gradient-radial" />

      <div className="relative max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-10"
        >
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white mb-4">
            Upload Your{' '}
            <span className="gradient-text">Resume</span>
          </h1>
          <p className="text-base sm:text-lg text-gray-400 max-w-lg mx-auto">
            Get instant AI-powered insights, ATS compatibility score, and
            personalized optimization suggestions.
          </p>
        </motion.div>

        <GlassCard className="p-6 sm:p-8 md:p-10 glow" hover={false}>
          <div className="space-y-6">
            <UploadBox
              onFileSelect={handleFileSelect}
              error={uploadError}
              disabled={uploading}
            />

            <AnimatePresence mode="wait">
              {file && (
                <motion.div
                  key="file-preview"
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                >
                  <FilePreview file={file} onRemove={handleRemove} />
                </motion.div>
              )}
            </AnimatePresence>

            <JDInput
              value={jobDescription}
              onChange={setJobDescription}
              disabled={uploading}
            />

            {complete ? (
              <motion.div
                initial={{ opacity: 0, scale: 0.96 }}
                animate={{ opacity: 1, scale: 1 }}
                className="flex items-center justify-center gap-2.5 px-8 py-4 text-base font-bold rounded-xl bg-green-500/10 border border-green-500/20 text-green-400"
              >
                <CheckCircle size={22} />
                Analysis Complete — Redirecting...
              </motion.div>
            ) : (
              <AnalyzeButton
                onClick={handleAnalyze}
                loading={uploading}
                disabled={!file}
              />
            )}
          </div>
        </GlassCard>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="text-center text-xs text-gray-500 mt-6"
        >
          Your resume data is encrypted and never stored without permission.
        </motion.p>
      </div>

      <LoadingOverlay
        visible={uploading}
        progress={progress}
        status={status}
      />
    </section>
  )
}
