import { motion } from 'framer-motion'
import CircularScore from './CircularScore'
import { cn } from '../../utils/cn'

export default function ScoreCard({ score, label, subtitle, size = 'md', className }) {
  const circleSize = size === 'lg' ? 180 : 110
  const strokeWidth = size === 'lg' ? 12 : 8

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn(
        'glass-card rounded-2xl flex flex-col items-center justify-center text-center',
        size === 'lg' ? 'p-8' : 'p-5',
        className
      )}
    >
      <CircularScore score={score} size={circleSize} strokeWidth={strokeWidth} />
      <h3
        className={cn(
          'font-semibold text-white mt-4',
          size === 'lg' ? 'text-xl' : 'text-sm'
        )}
      >
        {label}
      </h3>
      {subtitle && (
        <p className="text-xs text-gray-400 mt-1 max-w-xs">{subtitle}</p>
      )}
    </motion.div>
  )
}
