import { motion } from 'framer-motion'
import SectionTitle from './SectionTitle'
import GlassCard from './GlassCard'
import FeatureIcon from './FeatureIcon'
import { features } from '../data/navigation'

const containerVariants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.1 },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: 'easeOut' },
  },
}

export default function Features() {
  return (
    <section id="features" className="relative py-24 lg:py-32 overflow-hidden">
      <div className="absolute inset-0 bg-grid" />
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-primary/5 rounded-full blur-[120px]" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <SectionTitle
          subtitle="Features"
          title="Everything You Need to Invest Smarter"
          description="Upfolio combines cutting-edge AI with an intuitive interface to give you institutional-grade portfolio management tools."
        />

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          className="grid md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {features.map((feature) => (
            <motion.div key={feature.title} variants={itemVariants}>
              <GlassCard className="h-full" glow>
                <FeatureIcon icon={feature.icon} gradient={feature.gradient} />
                <h3 className="text-xl font-semibold text-white mt-5 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-400 leading-relaxed">
                  {feature.description}
                </p>
              </GlassCard>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}
