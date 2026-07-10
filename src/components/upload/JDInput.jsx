import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { cn } from '../../utils/cn'
import { jobDescriptions } from '../../data/jobDescriptions'

export default function JDInput({ value, onChange, disabled, className }) {
  const [showModal, setShowModal] = useState(false)

  const handleSelect = (jd) => {
    onChange(jd.description)
    setShowModal(false)
  }

  return (
    <div className={cn('space-y-2', className)}>
      <div className="flex items-center justify-between">
        <label className="block text-sm font-medium text-gray-300">
          Job Description <span className="text-red-400">*</span>
        </label>
        <button
          type="button"
          onClick={() => setShowModal(true)}
          disabled={disabled}
          className={cn(
            'px-3 py-1.5 text-xs rounded-lg border transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed',
            value
              ? 'bg-primary/20 border-primary/50 text-primary-300'
              : 'border-red-400/50 bg-red-400/10 text-red-400 hover:border-red-400 hover:bg-red-400/20 animate-pulse'
          )}
        >
          {value ? 'Change JD' : 'Select JD'}
        </button>
      </div>

      <div className="relative">
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          disabled={disabled}
          rows={5}
          placeholder="Paste the job description here to get targeted keyword matching and personalized suggestions..."
          className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-sm text-white placeholder-gray-500 resize-none transition-all duration-300 focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 disabled:opacity-50 disabled:cursor-not-allowed"
        />

        <div className="absolute bottom-3 right-3 text-[11px] text-gray-500 tabular-nums">
          {value.length}
          <span className="text-gray-600"> / 2000</span>
        </div>
      </div>

      <AnimatePresence>
        {showModal && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
              onClick={() => setShowModal(false)}
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="fixed inset-4 sm:inset-8 md:inset-12 z-50 overflow-hidden rounded-2xl border border-white/10 bg-gray-900 shadow-2xl"
            >
              <div className="flex items-center justify-between px-6 py-4 border-b border-white/10">
                <h2 className="text-lg font-semibold text-white">Select Job Description</h2>
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <div className="p-4 overflow-y-auto h-[calc(100%-57px)]">
                <div className="grid gap-3 sm:grid-cols-2">
                  {jobDescriptions.map((jd) => (
                    <button
                      key={jd.id}
                      type="button"
                      onClick={() => handleSelect(jd)}
                      className={cn(
                        'text-left p-4 rounded-xl border transition-all duration-200',
                        value === jd.description
                          ? 'bg-primary/20 border-primary/50'
                          : 'bg-white/5 border-white/10 hover:bg-white/10 hover:border-white/20'
                      )}
                    >
                      <div className="text-sm font-medium text-white mb-1">{jd.title}</div>
                      <div className="text-[11px] text-gray-500 line-clamp-2">{jd.description.split('\n')[1]}</div>
                    </button>
                  ))}
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  )
}
