import { motion } from 'framer-motion'
import * as Icons from 'lucide-react'
import SectionTitle from './SectionTitle'
import GlassCard from './GlassCard'
import { whyChooseUs } from '../data/navigation'

const containerVariants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.15 },
  },
}

const itemVariants = {
  hidden: { opacity: 0, x: -30 },
  visible: {
    opacity: 1,
    x: 0,
    transition: { duration: 0.6, ease: 'easeOut' },
  },
}

export default function WhyChooseUs() {
  return (
    <section id="why-upfolio" className="relative py-24 lg:py-32 overflow-hidden">
      <div className="absolute inset-0 bg-grid" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary/5 rounded-full blur-[150px]" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <SectionTitle
          subtitle="Why Upfolio"
          title="Built Different. Built Better."
          description="We combine cutting-edge AI technology with deep hiring expertise to deliver a resume optimization experience that truly works."
        />

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          className="grid md:grid-cols-2 gap-6"
        >
          {whyChooseUs.map((item) => {
            const LucideIcon = Icons[item.icon]
            return (
              <motion.div key={item.title} variants={itemVariants}>
                <GlassCard className="flex gap-5 items-start h-full" glow>
                  <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center flex-shrink-0">
                    {LucideIcon && <LucideIcon className="text-primary" size={24} />}
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-2">
                      {item.title}
                    </h3>
                    <p className="text-gray-400 leading-relaxed">
                      {item.description}
                    </p>
                  </div>
                </GlassCard>
              </motion.div>
            )
          })}
        </motion.div>
      </div>
    </section>
  )
}
