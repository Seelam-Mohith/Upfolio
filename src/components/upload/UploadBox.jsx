import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion } from 'framer-motion'
import { Upload, AlertCircle, FileWarning } from 'lucide-react'
import { cn } from '../../utils/cn'

const ACCEPTED_TYPES = {
  'application/pdf': ['.pdf'],
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
  'text/plain': ['.txt'],
}

const MAX_SIZE = 10 * 1024 * 1024

export default function UploadBox({ onFileSelect, error, disabled }) {
  const onDrop = useCallback(
    (accepted, rejected) => {
      if (rejected.length > 0) {
        const err = rejected[0].errors[0]
        if (err.code === 'file-too-large') {
          onFileSelect(null, 'File size exceeds 10MB limit.')
        } else if (err.code === 'file-invalid-type') {
          onFileSelect(null, 'Invalid file type. Please upload PDF, DOCX, or TXT.')
        } else {
          onFileSelect(null, err.message)
        }
        return
      }
      if (accepted.length > 0) {
        onFileSelect(accepted[0], null)
      }
    },
    [onFileSelect]
  )

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: ACCEPTED_TYPES,
    maxFiles: 1,
    maxSize: MAX_SIZE,
    disabled,
    multiple: false,
  })

  return (
    <div className="space-y-2">
      <motion.div
        {...getRootProps()}
        whileHover={disabled ? {} : { scale: 1.01 }}
        whileTap={disabled ? {} : { scale: 0.99 }}
        className={cn(
          'relative overflow-hidden border-2 border-dashed rounded-2xl p-10 sm:p-14 text-center cursor-pointer transition-all duration-300',
          isDragActive && !isDragReject && 'border-primary bg-primary/8',
          isDragReject && 'border-red-500 bg-red-500/5',
          !isDragActive && !error && !disabled && 'border-white/10 hover:border-primary/40 hover:bg-white/5',
          error && 'border-red-500/50 bg-red-500/5',
          disabled && 'opacity-50 cursor-not-allowed'
        )}
      >
        <input {...getInputProps()} />

        <div className="relative z-10">
          <div
            className={cn(
              'w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 transition-colors duration-300',
              isDragReject || error ? 'bg-red-500/10' : 'bg-primary/10'
            )}
          >
            {isDragReject || error ? (
              <FileWarning className="text-red-400" size={36} />
            ) : (
              <Upload className="text-primary" size={36} />
            )}
          </div>

          {isDragActive ? (
            <p
              className={cn(
                'text-xl font-semibold',
                isDragReject ? 'text-red-400' : 'text-primary'
              )}
            >
              {isDragReject ? 'Invalid file type' : 'Drop your resume here'}
            </p>
          ) : (
            <>
              <p className="text-xl text-white font-semibold mb-2">
                Drag & drop your resume
              </p>
              <p className="text-sm text-gray-400 mb-2">
                or <span className="text-primary underline underline-offset-2">browse files</span>
              </p>
              <p className="text-xs text-gray-500">
                Supports PDF, DOCX, TXT &middot; Max 10MB
              </p>
            </>
          )}
        </div>

        <div className="absolute inset-0 bg-gradient-radial opacity-30 pointer-events-none" />
      </motion.div>

      {error && (
        <motion.p
          initial={{ opacity: 0, y: -4 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-2 text-sm text-red-400 pl-1"
        >
          <AlertCircle size={14} />
          {error}
        </motion.p>
      )}
    </div>
  )
}
