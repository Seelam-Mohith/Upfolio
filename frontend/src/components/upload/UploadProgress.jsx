import { motion } from 'framer-motion'

export default function UploadProgress({ progress = 0, status = 'Uploading...' }) {
  const clamped = Math.min(Math.max(progress, 0), 100)

  return (
    <div className="w-full space-y-3">
      <div className="flex items-center justify-between text-sm">
        <span className="text-gray-300 font-medium">{status}</span>
        <span className="text-primary font-semibold tabular-nums">{clamped}%</span>
      </div>

      <div className="relative h-2.5 bg-white/5 rounded-full overflow-hidden">
        <motion.div
          className="absolute inset-y-0 left-0 rounded-full bg-gradient-to-r from-primary to-secondary"
          initial={{ width: 0 }}
          animate={{ width: `${clamped}%` }}
          transition={{ duration: 0.3, ease: 'easeOut' }}
        />
        <div
          className="absolute inset-y-0 left-0 w-full rounded-full"
          style={{
            background:
              'linear-gradient(90deg, transparent 0%, rgba(59,130,246,0.1) 50%, transparent 100%)',
            animation: 'shimmer 2s infinite',
          }}
        />
      </div>

      <style>{`
        @keyframes shimmer {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
      `}</style>
    </div>
  )
}
