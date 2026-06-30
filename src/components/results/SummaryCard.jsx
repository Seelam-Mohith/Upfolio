import { motion } from 'framer-motion'
import { FileText } from 'lucide-react'
import { cn } from '../../utils/cn'

export default function SummaryCard({ title, summary, className }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn('glass-card rounded-2xl p-5', className)}
    >
      <div className="flex items-center gap-2 mb-3">
        <FileText size={18} className="text-primary" />
        <h3 className="text-sm font-semibold text-white">{title}</h3>
      </div>
      <p className="text-sm text-gray-300 leading-relaxed">{summary}</p>
    </motion.div>
  )
}
