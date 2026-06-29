import { motion } from 'framer-motion'
import { ArrowRight, Check } from 'lucide-react'
import Button from './Button'

const benefits = [
  '14-day free trial, no credit card required',
  'Cancel anytime with one click',
  'Full access to all premium features',
  'Dedicated onboarding specialist',
]

export default function CTA() {
  return (
    <section id="cta" className="relative py-24 lg:py-32 overflow-hidden">
      <div className="absolute inset-0">
        <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-primary/50 to-transparent" />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7 }}
          className="glass-card p-8 md:p-12 lg:p-16 text-center glow relative overflow-hidden"
        >
          <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-secondary/5" />

          <div className="relative">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2, duration: 0.6 }}
            >
              <span className="inline-block text-sm font-semibold tracking-widest uppercase text-primary mb-4">
                Get Started Today
              </span>
              <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-4 leading-tight">
                Ready to Transform Your
                <br />
                <span className="gradient-text">Investment Portfolio</span>?
              </h2>
              <p className="text-lg text-gray-400 mb-8 max-w-xl mx-auto">
                Join thousands of smart investors who use Upfolio to optimize
                their portfolios with AI-powered insights.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.4, duration: 0.6 }}
              className="flex flex-col sm:flex-row gap-4 justify-center mb-8"
            >
              <Button size="lg">
                Start Your Free Trial
                <ArrowRight size={20} />
              </Button>
              <Button variant="secondary" size="lg">
                Talk to Sales
              </Button>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.6, duration: 0.6 }}
              className="flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-8"
            >
              {benefits.map((benefit) => (
                <div key={benefit} className="flex items-center gap-2">
                  <div className="w-5 h-5 rounded-full bg-green-500/20 flex items-center justify-center">
                    <Check size={12} className="text-green-400" />
                  </div>
                  <span className="text-sm text-gray-400">{benefit}</span>
                </div>
              ))}
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
