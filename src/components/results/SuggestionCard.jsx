import { motion } from 'framer-motion'
import { Lightbulb, ChevronRight } from 'lucide-react'
import { cn } from '../../utils/cn'

export default function SuggestionCard({ title, items, icon: Icon = Lightbulb, className }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn('glass-card rounded-2xl p-5', className)}
    >
      <div className="flex items-center gap-2 mb-4">
        <Icon size={18} className="text-primary" />
        <h3 className="text-sm font-semibold text-white">{title}</h3>
      </div>
      <ul className="space-y-3">
        {items.map((item, i) => (
          <motion.li
            key={i}
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.08 }}
            className="flex items-start gap-2.5 text-sm text-gray-300 leading-relaxed"
          >
            <ChevronRight size={14} className="text-primary mt-0.5 flex-shrink-0" />
            <span>{item}</span>
          </motion.li>
        ))}
      </ul>
    </motion.div>
  )
}
