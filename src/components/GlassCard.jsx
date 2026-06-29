import { motion } from 'framer-motion'

export default function GlassCard({
  children,
  className = '',
  hover = true,
  glow = false,
  ...props
}) {
  return (
    <motion.div
      className={`glass-card p-6 ${glow ? 'glow-sm' : ''} ${className}`}
      whileHover={hover ? { y: -4, scale: 1.01 } : undefined}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      {...props}
    >
      {children}
    </motion.div>
  )
}
