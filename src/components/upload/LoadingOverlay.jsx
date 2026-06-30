import { motion, AnimatePresence } from 'framer-motion'
import LogoIcon from '../LogoIcon'
import UploadProgress from './UploadProgress'

export default function LoadingOverlay({ visible, progress, status }) {
  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="fixed inset-0 z-[100] flex items-center justify-center"
        >
          <div className="absolute inset-0 bg-bg-dark/80 backdrop-blur-xl" />

          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
            className="relative glass-card rounded-2xl p-8 sm:p-10 max-w-md w-full mx-4 text-center"
          >
            <div className="flex justify-center mb-6">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
              >
                <LogoIcon size={56} />
              </motion.div>
            </div>

            <h3 className="text-xl font-bold text-white mb-2">
              Analyzing Your Resume
            </h3>
            <p className="text-sm text-gray-400 mb-6">
              Our AI is scanning your resume across 50+ dimensions...
            </p>

            <UploadProgress progress={progress} status={status} />

            <div className="mt-6 grid grid-cols-3 gap-3 text-center">
              {['Parsing', 'Scoring', 'Optimizing'].map((step, i) => (
                <div key={step} className="space-y-1.5">
                  <div
                    className={`h-1 rounded-full transition-all duration-500 ${
                      progress >= (i + 1) * 33
                        ? 'bg-gradient-to-r from-primary to-secondary'
                        : 'bg-white/5'
                    }`}
                  />
                  <p
                    className={`text-[11px] font-medium transition-colors duration-500 ${
                      progress >= (i + 1) * 33 ? 'text-primary' : 'text-gray-500'
                    }`}
                  >
                    {step}
                  </p>
                </div>
              ))}
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
