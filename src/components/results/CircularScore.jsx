import { motion } from 'framer-motion'

function scoreColor(score) {
  if (score >= 80) return { stroke: '#22C55E', text: '#22C55E', label: 'Excellent' }
  if (score >= 60) return { stroke: '#3B82F6', text: '#3B82F6', label: 'Good' }
  if (score >= 40) return { stroke: '#F59E0B', text: '#F59E0B', label: 'Needs Work' }
  return { stroke: '#EF4444', text: '#EF4444', label: 'Poor' }
}

export default function CircularScore({ score = 0, size = 160, strokeWidth = 10 }) {
  const clamped = Math.min(Math.max(score, 0), 100)
  const radius = (size - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (clamped / 100) * circumference
  const colors = scoreColor(clamped)

  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.05)"
          strokeWidth={strokeWidth}
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={colors.stroke}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.2, ease: 'easeOut' }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <motion.span
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="font-extrabold tracking-tight"
          style={{
            color: colors.text,
            fontSize: size * 0.22,
            lineHeight: 1,
          }}
        >
          {clamped}
        </motion.span>
        <span
          className="font-medium mt-0.5"
          style={{
            color: colors.text,
            fontSize: size * 0.065,
            opacity: 0.7,
          }}
        >
          {colors.label}
        </span>
      </div>
    </div>
  )
}
