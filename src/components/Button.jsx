import { motion } from 'framer-motion'

const variants = {
  primary:
    'bg-gradient-to-r from-primary to-secondary text-white hover:shadow-lg hover:shadow-primary/25',
  secondary:
    'glass text-gray-200 hover:bg-white/10 hover:border-primary/30',
  ghost: 'text-gray-300 hover:text-white hover:bg-white/5',
}

const sizes = {
  sm: 'px-4 py-2 text-sm',
  md: 'px-6 py-3 text-base',
  lg: 'px-8 py-4 text-lg',
}

export default function Button({
  children,
  variant = 'primary',
  size = 'md',
  className = '',
  href,
  icon: Icon,
  ...props
}) {
  const baseStyles =
    'inline-flex items-center justify-center gap-2 font-semibold rounded-xl transition-all duration-300 border border-transparent'

  const Component = href ? motion.a : motion.button

  return (
    <Component
      href={href}
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      {...props}
    >
      {Icon && <Icon size={20} />}
      {children}
    </Component>
  )
}
