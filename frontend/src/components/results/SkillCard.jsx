import { motion } from 'framer-motion'
import { CheckCircle2, XCircle } from 'lucide-react'
import { cn } from '../../utils/cn'

export default function SkillCard({ title, skills, type = 'matched', className }) {
  const isMatched = type === 'matched'

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn('glass-card rounded-2xl p-5', className)}
    >
      <div className="flex items-center gap-2 mb-4">
        {isMatched ? (
          <CheckCircle2 size={18} className="text-green-400" />
        ) : (
          <XCircle size={18} className="text-red-400" />
        )}
        <h3 className="text-sm font-semibold text-white">{title}</h3>
        <span className="text-xs text-gray-500 ml-auto">{skills.length}</span>
      </div>
      <div className="flex flex-wrap gap-2">
        {skills.map((skill) => (
          <span
            key={skill}
            className={cn(
              'inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg transition-colors',
              isMatched
                ? 'bg-green-500/10 text-green-300 border border-green-500/20'
                : 'bg-red-500/10 text-red-300 border border-red-500/20'
            )}
          >
            {skill}
          </span>
        ))}
      </div>
    </motion.div>
  )
}
