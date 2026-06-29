import { motion } from 'framer-motion'
import { ArrowDown } from 'lucide-react'
import SectionTitle from './SectionTitle'
import { howItWorks } from '../data/navigation'

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="relative py-24 lg:py-32 overflow-hidden">
      <div className="absolute inset-0 bg-gradient-radial" />
      <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-secondary/5 rounded-full blur-[120px]" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <SectionTitle
          subtitle="How It Works"
          title="Three Simple Steps to Smarter Investing"
          description="Get started with Upfolio in minutes. No complex setup, no learning curve — just actionable AI-powered insights."
        />

        <div className="grid lg:grid-cols-3 gap-8 lg:gap-12 items-start">
          {howItWorks.map((item, index) => (
            <motion.div
              key={item.step}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-100px' }}
              transition={{ duration: 0.6, delay: index * 0.2 }}
              className="relative text-center lg:text-left"
            >
              <div className="flex flex-col items-center lg:items-start">
                <div className="relative">
                  <div className="w-16 h-16 rounded-2xl glass flex items-center justify-center mb-6">
                    <span className="text-2xl font-bold gradient-text">
                      {item.step}
                    </span>
                  </div>
                  {index < howItWorks.length - 1 && (
                    <div className="hidden lg:block absolute -right-20 top-8">
                      <ArrowDown className="text-primary/30 -rotate-90" size={24} />
                    </div>
                  )}
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  {item.title}
                </h3>
                <p className="text-gray-400 leading-relaxed">{item.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
