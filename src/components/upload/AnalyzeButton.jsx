import { motion } from 'framer-motion'
import { Loader2, Sparkles } from 'lucide-react'
import { cn } from '../../utils/cn'

export default function AnalyzeButton({ onClick, loading, disabled, className }) {
  return (
    <motion.button
      onClick={onClick}
      disabled={disabled || loading}
      whileHover={disabled ? {} : { scale: 1.02 }}
      whileTap={disabled ? {} : { scale: 0.98 }}
      className={cn(
        'relative w-full flex items-center justify-center gap-2.5 px-8 py-4 text-base font-bold rounded-xl transition-all duration-300 overflow-hidden',
        loading
          ? 'bg-primary/50 text-white cursor-wait'
          : disabled
          ? 'bg-white/5 text-gray-500 cursor-not-allowed border border-white/5'
          : 'bg-gradient-to-r from-primary to-secondary text-white hover:shadow-lg hover:shadow-primary/25 active:shadow-md',
        className
      )}
    >
      {loading ? (
        <>
          <Loader2 className="animate-spin" size={22} />
          Analyzing Resume...
        </>
      ) : (
        <>
          <Sparkles size={22} />
          Analyze Resume
        </>
      )}
    </motion.button>
  )
}
