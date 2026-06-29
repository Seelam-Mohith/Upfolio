import { motion } from 'framer-motion'

export default function SectionTitle({
  subtitle,
  title,
  description,
  align = 'center',
}) {
  const alignClass = align === 'center' ? 'text-center' : 'text-left'

  return (
    <motion.div
      className={`max-w-3xl mx-auto mb-16 ${alignClass}`}
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-100px' }}
      transition={{ duration: 0.6 }}
    >
      {subtitle && (
        <span className="inline-block text-sm font-semibold tracking-widest uppercase text-primary mb-4">
          {subtitle}
        </span>
      )}
      <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-6 leading-tight">
        {title}
      </h2>
      {description && (
        <p className="text-lg text-gray-400 leading-relaxed max-w-2xl mx-auto">
          {description}
        </p>
      )}
    </motion.div>
  )
}
